import os
import json
import uuid
import shutil
from datetime import datetime
from typing import List, Dict, Any, Optional
from pathlib import Path

import duckdb
import pandas as pd
from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import hashlib
import secrets

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="数据查询分析系统", version="1.0.0")

app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_DIR = Path("uploads")
DATA_DIR = Path("data")
BACKUP_DIR = Path("backups")
USER_DB = Path("users.json")

for directory in [UPLOAD_DIR, DATA_DIR, BACKUP_DIR]:
    directory.mkdir(exist_ok=True)

class User(BaseModel):
    username: str
    password_hash: str
    created_at: str
    role: str = "user"

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class ColumnConfig(BaseModel):
    name: str
    data_type: str
    nullable: bool = True

class TableConfig(BaseModel):
    table_name: str
    columns: List[ColumnConfig]

class QueryRequest(BaseModel):
    sql: str
    limit: int = 1000
    offset: int = 0

class DataUpdateRequest(BaseModel):
    table_name: str
    action: str
    data: Dict[str, Any]
    condition: Optional[Dict[str, Any]] = None

def load_users() -> Dict[str, User]:
    if USER_DB.exists():
        with open(USER_DB, 'r', encoding='utf-8') as f:
            users_data = json.load(f)
            return {k: User(**v) for k, v in users_data.items()}
    return {}

def save_users(users: Dict[str, User]):
    with open(USER_DB, 'w', encoding='utf-8') as f:
        json.dump({k: v.dict() for k, v in users.items()}, f, ensure_ascii=False, indent=2)

def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_token(token: str) -> Optional[str]:
    return token

def get_duckdb_connection():
    db_path = DATA_DIR / "main.duckdb"
    conn = duckdb.connect(str(db_path))
    return conn

def detect_column_type(series: pd.Series) -> str:
    if pd.api.types.is_integer_dtype(series):
        return "INTEGER"
    elif pd.api.types.is_float_dtype(series):
        return "FLOAT"
    elif pd.api.types.is_datetime64_any_dtype(series):
        return "DATETIME"
    elif pd.api.types.is_bool_dtype(series):
        return "BOOLEAN"
    else:
        sample = series.dropna().head(100)
        if len(sample) == 0:
            return "VARCHAR"
        
        for val in sample:
            if isinstance(val, str):
                try:
                    if 'T' in val or ':' in val:
                        if '-' in val and ':' in val:
                            return "DATETIME"
                        return "TIME"
                    elif '-' in val or '/' in val:
                        return "DATE"
                except:
                    pass
        
        try:
            pd.to_numeric(sample)
            if sample.astype(str).str.contains('.').any():
                return "FLOAT"
            return "INTEGER"
        except:
            pass
        
        return "VARCHAR"

def load_file_to_df(file_path: Path, file_extension: str) -> pd.DataFrame:
    if file_extension in ['.xlsx', '.xls']:
        return pd.read_excel(file_path)
    elif file_extension == '.csv':
        return pd.read_csv(file_path, encoding='utf-8-sig')
    elif file_extension == '.txt':
        with open(file_path, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        delimiters = ['\t', '|', ';', ',']
        delimiter = ','
        for d in delimiters:
            if d in first_line:
                delimiter = d
                break
        
        return pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8-sig')
    else:
        raise ValueError(f"不支持的文件格式: {file_extension}")

@app.post("/api/auth/register")
async def register(user_data: UserCreate):
    users = load_users()
    
    if user_data.username in users:
        raise HTTPException(status_code=400, detail="用户名已存在")
    
    user = User(
        username=user_data.username,
        password_hash=hash_password(user_data.password),
        created_at=datetime.now().isoformat(),
        role="user"
    )
    
    users[user_data.username] = user
    save_users(users)
    
    return {"message": "注册成功", "username": user_data.username}

@app.post("/api/auth/login")
async def login(user_data: UserLogin):
    users = load_users()
    
    if user_data.username not in users:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    user = users[user_data.username]
    if user.password_hash != hash_password(user_data.password):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    
    token = secrets.token_hex(32)
    
    return {
        "message": "登录成功",
        "token": token,
        "username": user_data.username,
        "role": user.role
    }

@app.post("/api/upload")
async def upload_file(
    file: UploadFile = File(...),
    token: str = Form(...)
):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    file_extension = Path(file.filename).suffix.lower()
    if file_extension not in ['.xlsx', '.xls', '.csv', '.txt']:
        raise HTTPException(status_code=400, detail="不支持的文件格式")
    
    file_id = str(uuid.uuid4())
    file_path = UPLOAD_DIR / f"{file_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    try:
        df = load_file_to_df(file_path, file_extension)
        
        default_table_name = Path(file.filename).stem
        default_table_name = default_table_name.replace(" ", "_").replace("-", "_")
        
        column_configs = []
        for col in df.columns:
            col_type = detect_column_type(df[col])
            sample_values = df[col].dropna().head(3).tolist()
            sample_str = ", ".join([str(v)[:20] for v in sample_values])
            column_configs.append({
                "name": col,
                "data_type": col_type,
                "nullable": bool(df[col].isnull().any()),
                "sample": sample_str
            })
        
        return {
            "message": "文件解析成功",
            "default_table_name": default_table_name,
            "rows": len(df),
            "columns": column_configs,
            "file_id": file_id,
            "file_name": file.filename
        }
        
    except Exception as e:
        if file_path.exists():
            file_path.unlink()
        raise HTTPException(status_code=500, detail=f"文件处理失败: {str(e)}")

class ImportConfirmRequest(BaseModel):
    file_id: str
    file_name: str
    table_name: str
    columns: List[Dict[str, str]]

@app.post("/api/import/confirm")
async def confirm_import(request: ImportConfirmRequest, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    file_path = None
    for ext in ['.xlsx', '.xls', '.csv', '.txt']:
        potential_path = UPLOAD_DIR / f"{request.file_id}{ext}"
        if potential_path.exists():
            file_path = potential_path
            break
    
    if not file_path:
        raise HTTPException(status_code=404, detail="文件不存在，请重新上传")
    
    try:
        df = load_file_to_df(file_path, file_path.suffix)
        
        table_name = request.table_name.strip()
        if not table_name:
            table_name = Path(request.file_name).stem
        table_name = table_name.replace(" ", "_").replace("-", "_").replace(".", "_")
        
        conn = get_duckdb_connection()
        
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        type_mapping = {
            "VARCHAR": "VARCHAR",
            "INTEGER": "BIGINT",
            "FLOAT": "DOUBLE",
            "DATE": "DATE",
            "TIME": "TIME",
            "DATETIME": "TIMESTAMP",
            "BOOLEAN": "BOOLEAN"
        }
        
        columns_sql = []
        for col_config in request.columns:
            col_name = col_config["name"]
            col_type = col_config.get("data_type", "VARCHAR")
            duck_type = type_mapping.get(col_type, "VARCHAR")
            columns_sql.append(f'"{col_name}" {duck_type}')
        
        create_sql = f'CREATE TABLE {table_name} ({", ".join(columns_sql)})'
        conn.execute(create_sql)
        
        for col_config in request.columns:
            col_name = col_config["name"]
            col_type = col_config.get("data_type", "VARCHAR")
            
            if col_type in ["INTEGER", "FLOAT"]:
                df[col_name] = pd.to_numeric(df[col_name], errors='coerce')
            elif col_type == "DATE":
                df[col_name] = pd.to_datetime(df[col_name], errors='coerce').dt.date
            elif col_type == "DATETIME":
                df[col_name] = pd.to_datetime(df[col_name], errors='coerce')
            elif col_type == "BOOLEAN":
                df[col_name] = df[col_name].astype(bool)
        
        conn.execute(f"INSERT INTO {table_name} SELECT * FROM df")
        
        conn.close()
        
        return {
            "message": "数据导入成功",
            "table_name": table_name,
            "rows": len(df),
            "columns": request.columns
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败: {str(e)}")

@app.get("/api/tables")
async def get_tables(token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    tables = conn.execute("SHOW TABLES").fetchall()
    
    result = []
    for table in tables:
        table_name = table[0]
        columns = conn.execute(f"DESCRIBE {table_name}").fetchall()
        
        column_list = []
        for col in columns:
            column_list.append({
                "name": col[0],
                "type": col[1],
                "nullable": col[2] == "YES",
                "key": col[3] if len(col) > 3 else None
            })
        
        row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
        
        result.append({
            "table_name": table_name,
            "columns": column_list,
            "row_count": row_count
        })
    
    conn.close()
    
    return {"tables": result}

@app.delete("/api/tables/{table_name}")
async def delete_table(table_name: str, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
        table_names = [t[0] for t in tables]
        
        if table_name not in table_names:
            raise HTTPException(status_code=404, detail="表不存在")
        
        conn.execute(f"DROP TABLE IF EXISTS {table_name}")
        
        return {"message": f"表 {table_name} 已成功删除"}
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"删除失败: {str(e)}")
    
    finally:
        conn.close()

@app.post("/api/query")
async def execute_query(query: QueryRequest, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    sql = query.sql.strip()
    
    if not sql:
        raise HTTPException(status_code=400, detail="SQL语句不能为空")
    
    sql = sql.rstrip(';').strip()
    
    if not sql:
        raise HTTPException(status_code=400, detail="SQL语句不能为空")
    
    dangerous_keywords = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'CREATE', 'INSERT', 'UPDATE']
    sql_upper = sql.upper()
    
    for keyword in dangerous_keywords:
        if keyword in sql_upper and not sql_upper.startswith('SELECT'):
            raise HTTPException(status_code=400, detail="不允许执行危险的SQL操作")
    
    conn = get_duckdb_connection()
    
    try:
        if sql_upper.startswith('SELECT'):
            count_sql = f"SELECT COUNT(*) FROM ({sql})"
            total_count = conn.execute(count_sql).fetchone()[0]
            
            has_limit = 'LIMIT' in sql_upper
            has_offset = 'OFFSET' in sql_upper
            
            if has_limit:
                paginated_sql = sql
            else:
                paginated_sql = f"{sql} LIMIT {query.limit}"
                if query.offset > 0:
                    paginated_sql += f" OFFSET {query.offset}"
            
            result = conn.execute(paginated_sql).fetchall()
            
            columns = conn.execute(paginated_sql).description
            column_names = [col[0] for col in columns]
            
            rows = []
            for row in result:
                row_dict = {}
                for i, value in enumerate(row):
                    if isinstance(value, (datetime, pd.Timestamp)):
                        row_dict[column_names[i]] = value.isoformat()
                    elif isinstance(value, bytes):
                        row_dict[column_names[i]] = f"<binary {len(value)} bytes>"
                    else:
                        row_dict[column_names[i]] = value
                rows.append(row_dict)
            
            return {
                "columns": column_names,
                "rows": rows,
                "total_count": total_count,
                "limit": query.limit,
                "offset": query.offset
            }
        else:
            conn.execute(sql)
            return {"message": "SQL执行成功", "affected_rows": conn.execute("SELECT changes()").fetchone()[0]}
    
    except Exception as e:
        error_msg = str(e)
        if "syntax error" in error_msg.lower():
            error_msg = f"SQL语法错误: {error_msg}"
        raise HTTPException(status_code=400, detail=error_msg)
    
    finally:
        conn.close()

@app.post("/api/data/update")
async def update_data(request: DataUpdateRequest, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    try:
        if request.action == "insert":
            columns = ", ".join(request.data.keys())
            values = ", ".join([f"'{v}'" if isinstance(v, str) else str(v) for v in request.data.values()])
            sql = f"INSERT INTO {request.table_name} ({columns}) VALUES ({values})"
            conn.execute(sql)
            return {"message": "插入成功"}
        
        elif request.action == "update":
            set_clause = ", ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in request.data.items()])
            where_clause = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in request.condition.items()])
            sql = f"UPDATE {request.table_name} SET {set_clause} WHERE {where_clause}"
            conn.execute(sql)
            return {"message": "更新成功"}
        
        elif request.action == "delete":
            where_clause = " AND ".join([f"{k} = '{v}'" if isinstance(v, str) else f"{k} = {v}" for k, v in request.condition.items()])
            sql = f"DELETE FROM {request.table_name} WHERE {where_clause}"
            conn.execute(sql)
            return {"message": "删除成功"}
        
        else:
            raise HTTPException(status_code=400, detail="无效的操作类型")
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"操作失败: {str(e)}")
    
    finally:
        conn.close()

@app.post("/api/data/export")
async def export_data(query: QueryRequest, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    try:
        result = conn.execute(query.sql).fetchdf()
        
        export_id = str(uuid.uuid4())
        export_path = DATA_DIR / f"export_{export_id}.xlsx"
        
        result.to_excel(export_path, index=False, engine='openpyxl')
        
        return FileResponse(
            path=str(export_path),
            filename=f"查询结果_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"导出失败: {str(e)}")
    
    finally:
        conn.close()

@app.get("/api/data/preview/{table_name}")
async def preview_table(table_name: str, limit: int = 100, token: str = ""):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    try:
        result = conn.execute(f"SELECT * FROM {table_name} LIMIT {limit}").fetchdf()
        
        return {
            "columns": list(result.columns),
            "rows": result.to_dict('records'),
            "total_preview": len(result)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"预览失败: {str(e)}")
    
    finally:
        conn.close()

@app.post("/api/backup")
async def create_backup(token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = BACKUP_DIR / f"backup_{timestamp}"
    backup_path.mkdir(exist_ok=True)
    
    db_source = DATA_DIR / "main.duckdb"
    if db_source.exists():
        shutil.copy2(db_source, backup_path / "main.duckdb")
    
    for file in UPLOAD_DIR.glob("*"):
        if file.is_file():
            shutil.copy2(file, backup_path / file.name)
    
    return {"message": "备份成功", "backup_path": str(backup_path)}

@app.get("/api/backups")
async def list_backups(token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    backups = []
    for backup_dir in BACKUP_DIR.iterdir():
        if backup_dir.is_dir():
            backups.append({
                "name": backup_dir.name,
                "created_at": datetime.fromtimestamp(backup_dir.stat().st_mtime).isoformat(),
                "size": sum(f.stat().st_size for f in backup_dir.rglob('*') if f.is_file())
            })
    
    return {"backups": sorted(backups, key=lambda x: x['created_at'], reverse=True)}

@app.post("/api/backup/restore/{backup_name}")
async def restore_backup(backup_name: str, token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    backup_path = BACKUP_DIR / backup_name
    if not backup_path.exists():
        raise HTTPException(status_code=404, detail="备份不存在")
    
    db_backup = backup_path / "main.duckdb"
    if db_backup.exists():
        shutil.copy2(db_backup, DATA_DIR / "main.duckdb")
    
    return {"message": "恢复成功"}

@app.get("/api/stats")
async def get_stats(token: str):
    if not verify_token(token):
        raise HTTPException(status_code=401, detail="未授权")
    
    conn = get_duckdb_connection()
    
    try:
        tables = conn.execute("SHOW TABLES").fetchall()
        
        stats = {
            "total_tables": len(tables),
            "total_rows": 0,
            "database_size": 0,
            "tables": []
        }
        
        for table in tables:
            table_name = table[0]
            row_count = conn.execute(f"SELECT COUNT(*) FROM {table_name}").fetchone()[0]
            stats["total_rows"] += row_count
            stats["tables"].append({
                "name": table_name,
                "rows": row_count
            })
        
        db_path = DATA_DIR / "main.duckdb"
        if db_path.exists():
            stats["database_size"] = db_path.stat().st_size
        
        return stats
    
    finally:
        conn.close()

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    index_path = FRONTEND_DIR / "index.html"
    if index_path.exists():
        return FileResponse(str(index_path))
    return HTMLResponse("<h1>Frontend not found</h1>", status_code=404)

@app.get("/styles.css")
async def serve_css():
    css_path = FRONTEND_DIR / "styles.css"
    if css_path.exists():
        return FileResponse(str(css_path), media_type="text/css")
    return HTMLResponse("Not found", status_code=404)

@app.get("/app.js")
async def serve_js():
    js_path = FRONTEND_DIR / "app.js"
    if js_path.exists():
        return FileResponse(str(js_path), media_type="application/javascript")
    return HTMLResponse("Not found", status_code=404)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)