class DataQueryApp {
    constructor() {
        this.API_BASE = 'http://localhost:8000/api';
        this.token = localStorage.getItem('token');
        this.username = localStorage.getItem('username');
        this.currentView = 'query';
        this.currentPage = 1;
        this.pageSize = 100;
        this.totalRows = 0;
        this.currentSql = '';
        this.tables = [];
        
        this.SQL_KEYWORDS = [
            { text: 'SELECT', desc: '查询数据', type: 'keyword' },
            { text: 'FROM', desc: '指定表', type: 'keyword' },
            { text: 'WHERE', desc: '条件过滤', type: 'keyword' },
            { text: 'AND', desc: '逻辑与', type: 'keyword' },
            { text: 'OR', desc: '逻辑或', type: 'keyword' },
            { text: 'NOT', desc: '逻辑非', type: 'keyword' },
            { text: 'ORDER BY', desc: '排序', type: 'keyword' },
            { text: 'GROUP BY', desc: '分组', type: 'keyword' },
            { text: 'HAVING', desc: '分组过滤', type: 'keyword' },
            { text: 'LIMIT', desc: '限制行数', type: 'keyword' },
            { text: 'OFFSET', desc: '偏移量', type: 'keyword' },
            { text: 'JOIN', desc: '连接表', type: 'keyword' },
            { text: 'LEFT JOIN', desc: '左连接', type: 'keyword' },
            { text: 'RIGHT JOIN', desc: '右连接', type: 'keyword' },
            { text: 'INNER JOIN', desc: '内连接', type: 'keyword' },
            { text: 'OUTER JOIN', desc: '外连接', type: 'keyword' },
            { text: 'CROSS JOIN', desc: '交叉连接', type: 'keyword' },
            { text: 'ON', desc: '连接条件', type: 'keyword' },
            { text: 'AS', desc: '别名', type: 'keyword' },
            { text: 'DISTINCT', desc: '去重', type: 'keyword' },
            { text: 'INSERT INTO', desc: '插入数据', type: 'keyword' },
            { text: 'VALUES', desc: '值列表', type: 'keyword' },
            { text: 'UPDATE', desc: '更新数据', type: 'keyword' },
            { text: 'SET', desc: '设置值', type: 'keyword' },
            { text: 'DELETE FROM', desc: '删除数据', type: 'keyword' },
            { text: 'CREATE TABLE', desc: '创建表', type: 'keyword' },
            { text: 'ALTER TABLE', desc: '修改表', type: 'keyword' },
            { text: 'DROP TABLE', desc: '删除表', type: 'keyword' },
            { text: 'UNION', desc: '合并结果', type: 'keyword' },
            { text: 'UNION ALL', desc: '合并所有', type: 'keyword' },
            { text: 'INTERSECT', desc: '交集', type: 'keyword' },
            { text: 'EXCEPT', desc: '差集', type: 'keyword' },
            { text: 'CASE', desc: '条件判断', type: 'keyword' },
            { text: 'WHEN', desc: '条件分支', type: 'keyword' },
            { text: 'THEN', desc: '结果', type: 'keyword' },
            { text: 'ELSE', desc: '默认值', type: 'keyword' },
            { text: 'END', desc: '结束', type: 'keyword' },
            { text: 'IN', desc: '包含', type: 'keyword' },
            { text: 'BETWEEN', desc: '范围', type: 'keyword' },
            { text: 'LIKE', desc: '模糊匹配', type: 'keyword' },
            { text: 'IS NULL', desc: '空值判断', type: 'keyword' },
            { text: 'IS NOT NULL', desc: '非空判断', type: 'keyword' },
            { text: 'EXISTS', desc: '存在判断', type: 'keyword' },
            { text: 'ASC', desc: '升序', type: 'keyword' },
            { text: 'DESC', desc: '降序', type: 'keyword' },
            { text: 'NULL', desc: '空值', type: 'keyword' },
            { text: 'TRUE', desc: '真', type: 'keyword' },
            { text: 'FALSE', desc: '假', type: 'keyword' },
            { text: 'PRIMARY KEY', desc: '主键', type: 'keyword' },
            { text: 'FOREIGN KEY', desc: '外键', type: 'keyword' },
            { text: 'REFERENCES', desc: '引用', type: 'keyword' },
            { text: 'INDEX', desc: '索引', type: 'keyword' },
            { text: 'VIEW', desc: '视图', type: 'keyword' },
            { text: 'TRIGGER', desc: '触发器', type: 'keyword' },
            { text: 'PROCEDURE', desc: '存储过程', type: 'keyword' },
            { text: 'FUNCTION', desc: '函数', type: 'keyword' }
        ];
        
        this.SQL_FUNCTIONS = [
            { text: 'COUNT(*)', desc: '计数', type: 'function' },
            { text: 'SUM()', desc: '求和', type: 'function' },
            { text: 'AVG()', desc: '平均值', type: 'function' },
            { text: 'MAX()', desc: '最大值', type: 'function' },
            { text: 'MIN()', desc: '最小值', type: 'function' },
            { text: 'COALESCE()', desc: '空值处理', type: 'function' },
            { text: 'IFNULL()', desc: '空值替换', type: 'function' },
            { text: 'CAST()', desc: '类型转换', type: 'function' },
            { text: 'CONVERT()', desc: '转换', type: 'function' },
            { text: 'CONCAT()', desc: '字符串连接', type: 'function' },
            { text: 'SUBSTR()', desc: '截取字符串', type: 'function' },
            { text: 'LENGTH()', desc: '字符串长度', type: 'function' },
            { text: 'UPPER()', desc: '转大写', type: 'function' },
            { text: 'LOWER()', desc: '转小写', type: 'function' },
            { text: 'TRIM()', desc: '去除空格', type: 'function' },
            { text: 'ROUND()', desc: '四舍五入', type: 'function' },
            { text: 'ABS()', desc: '绝对值', type: 'function' },
            { text: 'NOW()', desc: '当前时间', type: 'function' },
            { text: 'CURRENT_DATE', desc: '当前日期', type: 'function' },
            { text: 'CURRENT_TIMESTAMP', desc: '当前时间戳', type: 'function' },
            { text: 'DATE()', desc: '提取日期', type: 'function' },
            { text: 'YEAR()', desc: '提取年份', type: 'function' },
            { text: 'MONTH()', desc: '提取月份', type: 'function' },
            { text: 'DAY()', desc: '提取日', type: 'function' },
            { text: 'EXTRACT()', desc: '提取时间部分', type: 'function' }
        ];
        
        this.autocompleteIndex = -1;
        this.autocompleteItems = [];
        
        this.init();
    }
    
    init() {
        this.bindEvents();
        this.checkAuth();
        this.initEditor();
    }
    
    bindEvents() {
        document.querySelectorAll('.auth-tab').forEach(tab => {
            tab.addEventListener('click', (e) => this.switchAuthTab(e.target.dataset.tab));
        });
        
        document.getElementById('login-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.login();
        });
        
        document.getElementById('register-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.register();
        });
        
        document.getElementById('logout-btn').addEventListener('click', () => this.logout());
        
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.addEventListener('click', (e) => this.switchView(e.currentTarget.dataset.view));
        });
        
        document.getElementById('execute-query').addEventListener('click', () => this.executeQuery());
        document.getElementById('clear-editor').addEventListener('click', () => this.clearEditor());
        document.getElementById('format-sql').addEventListener('click', () => this.formatSql());
        document.getElementById('export-excel').addEventListener('click', () => this.exportExcel());
        
        document.getElementById('refresh-tables').addEventListener('click', () => this.loadTables());
        document.getElementById('table-search').addEventListener('input', (e) => this.filterTables(e.target.value));
        
        const uploadZone = document.getElementById('upload-zone');
        const fileInput = document.getElementById('file-input');
        
        uploadZone.addEventListener('click', () => fileInput.click());
        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.classList.add('dragover');
        });
        uploadZone.addEventListener('dragleave', () => {
            uploadZone.classList.remove('dragover');
        });
        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            uploadZone.classList.remove('dragover');
            if (e.dataTransfer.files.length) {
                this.handleFileUpload(e.dataTransfer.files[0]);
            }
        });
        
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length) {
                this.handleFileUpload(e.target.files[0]);
            }
        });
        
        document.getElementById('confirm-import').addEventListener('click', () => this.confirmImport());
        document.getElementById('cancel-import').addEventListener('click', () => this.cancelImport());
        
        document.getElementById('prev-page').addEventListener('click', () => this.prevPage());
        document.getElementById('next-page').addEventListener('click', () => this.nextPage());
        
        document.addEventListener('keydown', (e) => {
            if (e.ctrlKey && e.key === 'Enter') {
                this.executeQuery();
            }
            if (e.ctrlKey && e.shiftKey && e.key === 'F') {
                e.preventDefault();
                this.formatSql();
            }
        });
    }
    
    checkAuth() {
        if (this.token && this.username) {
            this.showMainApp();
            this.loadTables();
        } else {
            this.showAuthScreen();
        }
    }
    
    showAuthScreen() {
        document.getElementById('auth-screen').classList.remove('hidden');
        document.getElementById('main-app').classList.add('hidden');
    }
    
    showMainApp() {
        document.getElementById('auth-screen').classList.add('hidden');
        document.getElementById('main-app').classList.remove('hidden');
        document.getElementById('user-display').textContent = this.username;
    }
    
    switchAuthTab(tab) {
        document.querySelectorAll('.auth-tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.auth-tab[data-tab="${tab}"]`).classList.add('active');
        
        document.querySelectorAll('.auth-form').forEach(f => f.classList.remove('active'));
        document.getElementById(`${tab}-form`).classList.add('active');
    }
    
    async login() {
        const username = document.getElementById('login-username').value;
        const password = document.getElementById('login-password').value;
        
        try {
            const response = await fetch(`${this.API_BASE}/auth/login`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.token = data.token;
                this.username = data.username;
                localStorage.setItem('token', this.token);
                localStorage.setItem('username', this.username);
                this.showMainApp();
                this.loadTables();
                this.showToast('success', '登录成功', `欢迎回来，${this.username}！`);
            } else {
                this.showToast('error', '登录失败', data.detail || '用户名或密码错误');
            }
        } catch (error) {
            this.showToast('error', '连接错误', '无法连接到服务器');
        }
    }
    
    async register() {
        const username = document.getElementById('reg-username').value;
        const password = document.getElementById('reg-password').value;
        const confirm = document.getElementById('reg-confirm').value;
        
        if (password !== confirm) {
            this.showToast('error', '注册失败', '两次输入的密码不一致');
            return;
        }
        
        try {
            const response = await fetch(`${this.API_BASE}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, password })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('success', '注册成功', '请登录');
                this.switchAuthTab('login');
                document.getElementById('login-username').value = username;
            } else {
                this.showToast('error', '注册失败', data.detail || '用户名已存在');
            }
        } catch (error) {
            this.showToast('error', '连接错误', '无法连接到服务器');
        }
    }
    
    logout() {
        this.token = null;
        this.username = null;
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        this.showAuthScreen();
    }
    
    initEditor() {
        const editor = document.getElementById('sql-editor');
        const lineNumbers = document.getElementById('line-numbers');
        
        editor.addEventListener('input', () => {
            this.updateLineNumbers();
            this.handleAutocomplete();
        });
        
        editor.addEventListener('scroll', () => {
            lineNumbers.scrollTop = editor.scrollTop;
        });
        
        editor.addEventListener('keydown', (e) => {
            if (e.key === 'Tab') {
                e.preventDefault();
                const start = editor.selectionStart;
                const end = editor.selectionEnd;
                editor.value = editor.value.substring(0, start) + '  ' + editor.value.substring(end);
                editor.selectionStart = editor.selectionEnd = start + 2;
                this.updateLineNumbers();
            }
            
            if (this.autocompleteItems.length > 0) {
                const dropdown = document.getElementById('autocomplete-dropdown');
                if (dropdown.classList.contains('visible')) {
                    if (e.key === 'ArrowDown') {
                        e.preventDefault();
                        this.autocompleteIndex = Math.min(this.autocompleteIndex + 1, this.autocompleteItems.length - 1);
                        this.updateAutocompleteSelection();
                        return;
                    }
                    if (e.key === 'ArrowUp') {
                        e.preventDefault();
                        this.autocompleteIndex = Math.max(this.autocompleteIndex - 1, 0);
                        this.updateAutocompleteSelection();
                        return;
                    }
                    if (e.key === 'Enter' || e.key === 'Tab') {
                        if (this.autocompleteIndex >= 0 && this.autocompleteIndex < this.autocompleteItems.length) {
                            e.preventDefault();
                            this.insertCompletion(this.autocompleteItems[this.autocompleteIndex]);
                            return;
                        }
                    }
                    if (e.key === 'Escape') {
                        e.preventDefault();
                        this.hideAutocomplete();
                        return;
                    }
                }
            }
        });
        
        editor.addEventListener('blur', () => {
            setTimeout(() => this.hideAutocomplete(), 200);
        });
        
        this.updateLineNumbers();
    }
    
    handleAutocomplete() {
        const editor = document.getElementById('sql-editor');
        const cursorPos = editor.selectionStart;
        const text = editor.value.substring(0, cursorPos);
        
        const words = text.split(/[\s,()=<>!;]+/);
        const currentWord = words[words.length - 1] || '';
        
        if (currentWord.length < 1) {
            this.hideAutocomplete();
            return;
        }
        
        const upperWord = currentWord.toUpperCase();
        
        const allSuggestions = [
            ...this.SQL_KEYWORDS,
            ...this.SQL_FUNCTIONS,
            ...this.getTableSuggestions()
        ];
        
        const matches = allSuggestions.filter(item => 
            item.text.toUpperCase().startsWith(upperWord) ||
            item.text.toUpperCase().includes(upperWord)
        ).slice(0, 15);
        
        if (matches.length > 0 && currentWord.length >= 1) {
            this.autocompleteItems = matches;
            this.autocompleteIndex = 0;
            this.showAutocomplete(matches, cursorPos);
        } else {
            this.hideAutocomplete();
        }
    }
    
    getTableSuggestions() {
        const suggestions = [];
        
        this.tables.forEach(table => {
            suggestions.push({
                text: table.table_name,
                desc: `表 (${table.row_count}行)`,
                type: 'table'
            });
            
            if (table.columns) {
                table.columns.forEach(col => {
                    suggestions.push({
                        text: col.name,
                        desc: `${col.type}`,
                        type: 'column'
                    });
                });
            }
        });
        
        return suggestions;
    }
    
    showAutocomplete(matches, cursorPos) {
        const editor = document.getElementById('sql-editor');
        const dropdown = document.getElementById('autocomplete-dropdown');
        const list = document.getElementById('autocomplete-list');
        
        const textBeforeCursor = editor.value.substring(0, cursorPos);
        const lines = textBeforeCursor.split('\n');
        const currentLine = lines.length - 1;
        const currentCol = lines[lines.length - 1].length;
        
        const lineHeight = 20;
        const charWidth = 7.8;
        const editorRect = editor.getBoundingClientRect();
        
        let top = (currentLine + 1) * lineHeight + 12;
        let left = currentCol * charWidth + 50;
        
        if (top + 200 > editorRect.height) {
            top = (currentLine) * lineHeight - 200;
        }
        
        if (left + 250 > editorRect.width) {
            left = editorRect.width - 260;
        }
        
        dropdown.style.top = `${top}px`;
        dropdown.style.left = `${left}px`;
        
        list.innerHTML = matches.map((item, index) => {
            const iconClass = item.type;
            const iconText = item.type === 'keyword' ? 'K' : 
                            item.type === 'table' ? 'T' : 
                            item.type === 'column' ? 'C' : 'F';
            
            return `
                <div class="autocomplete-item ${index === this.autocompleteIndex ? 'selected' : ''}" 
                     data-index="${index}"
                     onmousedown="app.selectAutocompleteItem(${index})">
                    <span class="item-icon ${iconClass}">${iconText}</span>
                    <span class="item-text">${item.text}</span>
                    <span class="item-desc">${item.desc}</span>
                </div>
            `;
        }).join('');
        
        dropdown.classList.add('visible');
    }
    
    hideAutocomplete() {
        const dropdown = document.getElementById('autocomplete-dropdown');
        dropdown.classList.remove('visible');
        this.autocompleteItems = [];
        this.autocompleteIndex = -1;
    }
    
    updateAutocompleteSelection() {
        const items = document.querySelectorAll('.autocomplete-item');
        items.forEach((item, index) => {
            item.classList.toggle('selected', index === this.autocompleteIndex);
        });
        
        const selectedItem = items[this.autocompleteIndex];
        if (selectedItem) {
            selectedItem.scrollIntoView({ block: 'nearest' });
        }
    }
    
    selectAutocompleteItem(index) {
        if (index >= 0 && index < this.autocompleteItems.length) {
            this.insertCompletion(this.autocompleteItems[index]);
        }
    }
    
    insertCompletion(item) {
        const editor = document.getElementById('sql-editor');
        const cursorPos = editor.selectionStart;
        const text = editor.value;
        
        const textBeforeCursor = text.substring(0, cursorPos);
        const words = textBeforeCursor.split(/[\s,()=<>!;]+/);
        const currentWord = words[words.length - 1] || '';
        
        const wordStart = cursorPos - currentWord.length;
        
        let insertText = item.text;
        
        if (item.type === 'function' && insertText.endsWith('()')) {
            insertText = insertText.slice(0, -1);
        }
        
        editor.value = text.substring(0, wordStart) + insertText + text.substring(cursorPos);
        
        const newCursorPos = wordStart + insertText.length;
        editor.selectionStart = editor.selectionEnd = newCursorPos;
        
        this.hideAutocomplete();
        this.updateLineNumbers();
        editor.focus();
    }
    
    updateLineNumbers() {
        const editor = document.getElementById('sql-editor');
        const lineNumbers = document.getElementById('line-numbers');
        const lines = editor.value.split('\n');
        
        lineNumbers.innerHTML = lines.map((_, i) => 
            `<div>${i + 1}</div>`
        ).join('');
    }
    
    switchView(view) {
        this.currentView = view;
        
        document.querySelectorAll('.nav-btn').forEach(btn => {
            btn.classList.toggle('active', btn.dataset.view === view);
        });
        
        document.querySelectorAll('.view').forEach(v => {
            v.classList.toggle('active', v.id === `${view}-view`);
        });
    }
    
    async loadTables() {
        try {
            const response = await fetch(`${this.API_BASE}/tables?token=${this.token}`);
            const data = await response.json();
            
            if (response.ok) {
                this.tables = data.tables;
                this.renderTableTree();
            }
        } catch (error) {
            console.error('加载表失败:', error);
        }
    }
    
    renderTableTree(filter = '') {
        const tree = document.getElementById('table-tree');
        
        if (!this.tables.length) {
            tree.innerHTML = `
                <div class="empty-state">
                    <i class="fas fa-inbox"></i>
                    <p>暂无数据表</p>
                    <small>请先导入数据文件</small>
                </div>
            `;
            return;
        }
        
        const filteredTables = this.tables.filter(table => {
            if (filter && !table.table_name.toLowerCase().includes(filter.toLowerCase())) {
                const hasColumn = table.columns.some(col => 
                    col.name.toLowerCase().includes(filter.toLowerCase())
                );
                return hasColumn;
            }
            return true;
        });
        
        tree.innerHTML = filteredTables.map(table => `
            <div class="tree-item" data-table="${table.table_name}">
                <div class="tree-item-header">
                    <span class="toggle" onclick="app.toggleTable('${table.table_name}')"><i class="fas fa-chevron-right"></i></span>
                    <span class="table-icon" onclick="app.toggleTable('${table.table_name}')"><i class="fas fa-table"></i></span>
                    <span class="table-name" onclick="app.toggleTable('${table.table_name}')">${table.table_name}</span>
                    <span class="row-count">${table.row_count}</span>
                    <span class="delete-btn" onclick="event.stopPropagation(); app.deleteTable('${table.table_name}')" title="删除表">
                        <i class="fas fa-trash-alt"></i>
                    </span>
                </div>
                <div class="tree-item-children" id="columns-${table.table_name}">
                    ${table.columns.map(col => `
                        <div class="tree-column" onclick="app.insertColumn('${table.table_name}', '${col.name}')">
                            <span class="column-icon"><i class="fas fa-columns"></i></span>
                            <span class="column-name">${col.name}</span>
                            <span class="column-type">${col.type}</span>
                        </div>
                    `).join('')}
                </div>
            </div>
        `).join('');
    }
    
    toggleTable(tableName) {
        const header = document.querySelector(`.tree-item[data-table="${tableName}"] .tree-item-header`);
        const children = document.getElementById(`columns-${tableName}`);
        
        header.classList.toggle('expanded');
        children.classList.toggle('expanded');
    }
    
    insertColumn(tableName, columnName) {
        const editor = document.getElementById('sql-editor');
        const insertText = `${tableName}.${columnName}`;
        
        const start = editor.selectionStart;
        const end = editor.selectionEnd;
        
        editor.value = editor.value.substring(0, start) + insertText + editor.value.substring(end);
        editor.selectionStart = editor.selectionEnd = start + insertText.length;
        editor.focus();
        
        this.updateLineNumbers();
    }
    
    async deleteTable(tableName) {
        if (!confirm(`确定要删除表 "${tableName}" 吗？此操作不可恢复。`)) {
            return;
        }
        
        try {
            const response = await fetch(`${this.API_BASE}/tables/${tableName}?token=${this.token}`, {
                method: 'DELETE'
            });
            
            const data = await response.json();
            
            if (response.ok) {
                this.showToast('success', '删除成功', `表 "${tableName}" 已删除`);
                this.loadTables();
            } else {
                throw new Error(data.detail || '删除失败');
            }
        } catch (error) {
            this.showToast('error', '删除失败', error.message);
        }
    }
    
    filterTables(query) {
        this.renderTableTree(query);
    }
    
    async executeQuery() {
        const editor = document.getElementById('sql-editor');
        const sql = editor.value.trim();
        
        if (!sql) {
            this.showToast('warning', '提示', '请输入SQL查询语句');
            return;
        }
        
        this.currentSql = sql;
        this.currentPage = 1;
        
        document.getElementById('results-placeholder').classList.add('hidden');
        document.getElementById('results-loading').classList.remove('hidden');
        document.getElementById('results-table-wrapper').classList.add('hidden');
        document.getElementById('pagination').classList.add('hidden');
        
        const startTime = Date.now();
        
        try {
            const response = await fetch(`${this.API_BASE}/query?token=${this.token}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    sql: sql,
                    limit: this.pageSize,
                    offset: (this.currentPage - 1) * this.pageSize
                })
            });
            
            const data = await response.json();
            const elapsed = Date.now() - startTime;
            
            if (response.ok) {
                this.totalRows = data.total_count;
                this.renderResults(data.columns, data.rows);
                
                document.getElementById('query-status').textContent = 
                    `查询完成，耗时 ${elapsed}ms，共 ${data.total_count} 条记录`;
                document.getElementById('result-count').textContent = 
                    `${data.total_count} 条记录`;
                document.getElementById('export-excel').disabled = false;
            } else {
                throw new Error(data.detail || '查询失败');
            }
        } catch (error) {
            document.getElementById('results-placeholder').classList.remove('hidden');
            document.getElementById('results-loading').classList.add('hidden');
            
            this.showToast('error', '查询错误', error.message);
            document.getElementById('query-status').textContent = '查询失败';
        }
    }
    
    renderResults(columns, rows) {
        const thead = document.getElementById('results-thead');
        const tbody = document.getElementById('results-tbody');
        
        thead.innerHTML = `
            <tr>
                ${columns.map(col => `
                    <th onclick="app.sortColumn('${col}')">
                        ${col}
                        <span class="sort-icon"></span>
                    </th>
                `).join('')}
            </tr>
        `;
        
        tbody.innerHTML = rows.map(row => `
            <tr>
                ${columns.map(col => {
                    const value = row[col];
                    const isNull = value === null || value === undefined;
                    const isNumeric = typeof value === 'number';
                    
                    return `
                        <td class="${isNull ? 'null-value' : ''} ${isNumeric ? 'numeric' : ''}">
                            ${isNull ? 'NULL' : value}
                        </td>
                    `;
                }).join('')}
            </tr>
        `).join('');
        
        document.getElementById('results-loading').classList.add('hidden');
        document.getElementById('results-table-wrapper').classList.remove('hidden');
        
        if (this.totalRows > this.pageSize) {
            document.getElementById('pagination').classList.remove('hidden');
            this.updatePagination();
        } else {
            document.getElementById('pagination').classList.add('hidden');
        }
    }
    
    updatePagination() {
        const totalPages = Math.ceil(this.totalRows / this.pageSize);
        document.getElementById('page-info').textContent = 
            `第 ${this.currentPage} 页，共 ${totalPages} 页`;
        
        document.getElementById('prev-page').disabled = this.currentPage <= 1;
        document.getElementById('next-page').disabled = this.currentPage >= totalPages;
    }
    
    async prevPage() {
        if (this.currentPage > 1) {
            this.currentPage--;
            await this.executeQuery();
        }
    }
    
    async nextPage() {
        const totalPages = Math.ceil(this.totalRows / this.pageSize);
        if (this.currentPage < totalPages) {
            this.currentPage++;
            await this.executeQuery();
        }
    }
    
    sortColumn(column) {
        const ths = document.querySelectorAll('.results-table th');
        ths.forEach(th => th.classList.remove('sorted-asc', 'sorted-desc'));
        
        const th = Array.from(ths).find(th => th.textContent.trim().startsWith(column));
        
        if (th.classList.contains('sorted-asc')) {
            th.classList.remove('sorted-asc');
            th.classList.add('sorted-desc');
            this.currentSql = this.currentSql.replace(/ORDER BY.*$/i, '') + 
                ` ORDER BY ${column} DESC`;
        } else {
            th.classList.remove('sorted-desc');
            th.classList.add('sorted-asc');
            this.currentSql = this.currentSql.replace(/ORDER BY.*$/i, '') + 
                ` ORDER BY ${column} ASC`;
        }
        
        this.executeQuery();
    }
    
    clearEditor() {
        document.getElementById('sql-editor').value = '';
        this.updateLineNumbers();
    }
    
    formatSql() {
        const editor = document.getElementById('sql-editor');
        let sql = editor.value.trim();
        
        if (!sql) return;
        
        sql = this.formatSqlAdvanced(sql);
        
        editor.value = sql;
        this.updateLineNumbers();
    }
    
    formatSqlAdvanced(sql) {
        sql = sql.replace(/\s+/g, ' ').trim();
        
        sql = sql.replace(/;+$/, '').trim();
        
        const mainKeywords = [
            'SELECT', 'FROM', 'WHERE', 'GROUP BY', 'HAVING', 'ORDER BY',
            'LIMIT', 'OFFSET', 'UNION', 'UNION ALL', 'INTERSECT', 'EXCEPT'
        ];
        
        const joinKeywords = [
            'JOIN', 'LEFT JOIN', 'RIGHT JOIN', 'INNER JOIN', 'OUTER JOIN',
            'CROSS JOIN', 'FULL JOIN', 'FULL OUTER JOIN', 'LEFT OUTER JOIN',
            'RIGHT OUTER JOIN', 'NATURAL JOIN'
        ];
        
        const subKeywords = ['AND', 'OR', 'ON', 'IN', 'BETWEEN', 'CASE', 'WHEN', 'THEN', 'ELSE', 'END'];
        
        mainKeywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            sql = sql.replace(regex, `\n${keyword}`);
        });
        
        joinKeywords.forEach(keyword => {
            const regex = new RegExp(`\\b${keyword}\\b`, 'gi');
            sql = sql.replace(regex, `\n${keyword}`);
        });
        
        const lines = sql.split('\n');
        let formattedLines = [];
        let indentLevel = 0;
        
        for (let line of lines) {
            line = line.trim();
            if (!line) continue;
            
            const upperLine = line.toUpperCase();
            
            if (upperLine.startsWith('END')) {
                indentLevel = Math.max(0, indentLevel - 1);
            }
            
            if (upperLine.startsWith('CASE')) {
                indentLevel++;
            }
            
            const indent = '  '.repeat(indentLevel);
            
            if (upperLine.startsWith('SELECT')) {
                const selectPart = line.substring(6).trim();
                if (selectPart.includes(',')) {
                    const fields = selectPart.split(',').map(f => f.trim());
                    formattedLines.push('SELECT');
                    fields.forEach((field, index) => {
                        const comma = index < fields.length - 1 ? ',' : '';
                        formattedLines.push(`    ${field}${comma}`);
                    });
                } else {
                    formattedLines.push(line);
                }
            } else if (upperLine.startsWith('AND') || upperLine.startsWith('OR')) {
                formattedLines.push(`${indent}${line}`);
            } else if (upperLine.startsWith('ON')) {
                formattedLines.push(`  ${line}`);
            } else {
                formattedLines.push(`${indent}${line}`);
            }
            
            if (upperLine.startsWith('WHEN') || upperLine.startsWith('THEN') || 
                upperLine.startsWith('ELSE')) {
                // Keep current indent
            }
        }
        
        let result = formattedLines.join('\n');
        
        const stringRegex = /'[^']*'/g;
        const strings = [];
        let tempResult = result.replace(stringRegex, (match) => {
            strings.push(match);
            return `__STRING_${strings.length - 1}__`;
        });
        
        tempResult = tempResult.replace(/\bselect\b/gi, 'SELECT')
                      .replace(/\bfrom\b/gi, 'FROM')
                      .replace(/\bwhere\b/gi, 'WHERE')
                      .replace(/\band\b/gi, 'AND')
                      .replace(/\bor\b/gi, 'OR')
                      .replace(/\border by\b/gi, 'ORDER BY')
                      .replace(/\bgroup by\b/gi, 'GROUP BY')
                      .replace(/\bhaving\b/gi, 'HAVING')
                      .replace(/\blimit\b/gi, 'LIMIT')
                      .replace(/\boffset\b/gi, 'OFFSET')
                      .replace(/\bjoin\b/gi, 'JOIN')
                      .replace(/\bleft join\b/gi, 'LEFT JOIN')
                      .replace(/\bright join\b/gi, 'RIGHT JOIN')
                      .replace(/\binner join\b/gi, 'INNER JOIN')
                      .replace(/\bon\b/gi, 'ON')
                      .replace(/\binsert into\b/gi, 'INSERT INTO')
                      .replace(/\bvalues\b/gi, 'VALUES')
                      .replace(/\bupdate\b/gi, 'UPDATE')
                      .replace(/\bset\b/gi, 'SET')
                      .replace(/\bdelete from\b/gi, 'DELETE FROM')
                      .replace(/\bcreate table\b/gi, 'CREATE TABLE')
                      .replace(/\balter table\b/gi, 'ALTER TABLE')
                      .replace(/\bdrop table\b/gi, 'DROP TABLE')
                      .replace(/\bas\b/gi, 'AS')
                      .replace(/\bdistinct\b/gi, 'DISTINCT')
                      .replace(/\bcount\b/gi, 'COUNT')
                      .replace(/\bsum\b/gi, 'SUM')
                      .replace(/\bavg\b/gi, 'AVG')
                      .replace(/\bmax\b/gi, 'MAX')
                      .replace(/\bmin\b/gi, 'MIN')
                      .replace(/\bbetween\b/gi, 'BETWEEN')
                      .replace(/\bin\b/gi, 'IN')
                      .replace(/\blike\b/gi, 'LIKE')
                      .replace(/\bis null\b/gi, 'IS NULL')
                      .replace(/\bis not null\b/gi, 'IS NOT NULL')
                      .replace(/\bexists\b/gi, 'EXISTS')
                      .replace(/\bcase\b/gi, 'CASE')
                      .replace(/\bwhen\b/gi, 'WHEN')
                      .replace(/\bthen\b/gi, 'THEN')
                      .replace(/\belse\b/gi, 'ELSE')
                      .replace(/\bend\b/gi, 'END')
                      .replace(/\bunion\b/gi, 'UNION')
                      .replace(/\ball\b/gi, 'ALL')
                      .replace(/\basc\b/gi, 'ASC')
                      .replace(/\bdesc\b/gi, 'DESC');
        
        strings.forEach((str, index) => {
            tempResult = tempResult.replace(`__STRING_${index}__`, str);
        });
        
        result = tempResult;
        
        result = result.trim() + ';';
        
        return result;
    }
    
    async exportExcel() {
        if (!this.currentSql) {
            this.showToast('warning', '提示', '请先执行查询');
            return;
        }
        
        try {
            const response = await fetch(`${this.API_BASE}/data/export?token=${this.token}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ sql: this.currentSql })
            });
            
            if (response.ok) {
                const blob = await response.blob();
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `查询结果_${new Date().toISOString().slice(0, 10)}.xlsx`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
                
                this.showToast('success', '导出成功', '文件已开始下载');
            } else {
                const data = await response.json();
                throw new Error(data.detail || '导出失败');
            }
        } catch (error) {
            this.showToast('error', '导出失败', error.message);
        }
    }
    
    async handleFileUpload(file) {
        const validExtensions = ['.xlsx', '.xls', '.csv', '.txt'];
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        
        if (!validExtensions.includes(ext)) {
            this.showToast('error', '格式错误', '不支持的文件格式');
            return;
        }
        
        document.getElementById('upload-filename').textContent = file.name;
        document.getElementById('upload-progress').classList.remove('hidden');
        document.getElementById('progress-fill').style.width = '0%';
        
        const formData = new FormData();
        formData.append('file', file);
        formData.append('token', this.token);
        
        const tableName = file.name.replace(/\.[^/.]+$/, '').replace(/[^a-zA-Z0-9\u4e00-\u9fa5]/g, '_');
        formData.append('table_name', tableName);
        
        try {
            const xhr = new XMLHttpRequest();
            
            xhr.upload.addEventListener('progress', (e) => {
                if (e.lengthComputable) {
                    const percent = Math.round((e.loaded / e.total) * 100);
                    document.getElementById('progress-fill').style.width = `${percent}%`;
                    document.getElementById('upload-percent').textContent = `${percent}%`;
                }
            });
            
            xhr.addEventListener('load', () => {
                if (xhr.status === 200) {
                    const data = JSON.parse(xhr.responseText);
                    this.showColumnConfig(data);
                    this.showToast('success', '上传成功', `文件已解析，共 ${data.rows} 行`);
                } else {
                    const data = JSON.parse(xhr.responseText);
                    this.showToast('error', '上传失败', data.detail || '文件处理失败');
                    document.getElementById('upload-progress').classList.add('hidden');
                }
            });
            
            xhr.addEventListener('error', () => {
                this.showToast('error', '上传失败', '网络错误');
                document.getElementById('upload-progress').classList.add('hidden');
            });
            
            xhr.open('POST', `${this.API_BASE}/upload`);
            xhr.send(formData);
            
        } catch (error) {
            this.showToast('error', '上传失败', error.message);
            document.getElementById('upload-progress').classList.add('hidden');
        }
    }
    
    showColumnConfig(data) {
        this.importData = data;
        this.uploadedFileId = data.file_id;
        this.uploadedFileName = data.file_name;
        
        document.getElementById('import-table-name').value = data.default_table_name;
        
        const columnsList = document.getElementById('columns-list');
        columnsList.innerHTML = data.columns.map((col, index) => `
            <div class="column-item">
                <span class="column-index">${index + 1}</span>
                <div class="column-preview">
                    <div class="name">${col.name}</div>
                    <div class="sample">类型建议: ${col.data_type}</div>
                </div>
                <select class="column-type-select" data-column="${col.name}">
                    <option value="VARCHAR" ${col.data_type === 'VARCHAR' ? 'selected' : ''}>文本</option>
                    <option value="INTEGER" ${col.data_type === 'INTEGER' ? 'selected' : ''}>整数</option>
                    <option value="FLOAT" ${col.data_type === 'FLOAT' ? 'selected' : ''}>小数</option>
                    <option value="DATE" ${col.data_type === 'DATE' ? 'selected' : ''}>日期</option>
                    <option value="TIME" ${col.data_type === 'TIME' ? 'selected' : ''}>时间</option>
                    <option value="DATETIME" ${col.data_type === 'DATETIME' ? 'selected' : ''}>日期时间</option>
                    <option value="BOOLEAN" ${col.data_type === 'BOOLEAN' ? 'selected' : ''}>布尔值</option>
                </select>
            </div>
        `).join('');
        
        document.getElementById('column-config').classList.remove('hidden');
    }
    
    async confirmImport() {
        const tableName = document.getElementById('import-table-name').value.trim();
        if (!tableName) {
            this.showToast('warning', '提示', '请输入数据表名称');
            return;
        }

        const columnSelects = document.querySelectorAll('.column-type-select');
        const columns = Array.from(columnSelects).map(select => ({
            name: select.dataset.column,
            data_type: select.value
        }));

        const confirmBtn = document.getElementById('confirm-import');
        confirmBtn.disabled = true;
        confirmBtn.textContent = '导入中...';

        try {
            const response = await fetch(`${this.API_BASE}/import/confirm?token=${this.token}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    file_id: this.uploadedFileId,
                    file_name: this.uploadedFileName,
                    table_name: tableName,
                    columns: columns
                })
            });

            const data = await response.json();

            if (response.ok) {
                this.showToast('success', '导入成功', `表 "${data.table_name}" 已导入 ${data.rows} 行数据`);
                document.getElementById('column-config').classList.add('hidden');
                document.getElementById('upload-progress').classList.add('hidden');
                this.loadTables();
            } else {
                throw new Error(data.detail || '导入失败');
            }
        } catch (error) {
            this.showToast('error', '导入失败', error.message);
        } finally {
            confirmBtn.disabled = false;
            confirmBtn.textContent = '确认导入';
        }
    }
    
    cancelImport() {
        document.getElementById('column-config').classList.add('hidden');
        document.getElementById('upload-progress').classList.add('hidden');
    }
    
    showToast(type, title, message) {
        const container = document.getElementById('toast-container');
        
        const icons = {
            success: 'fas fa-check-circle',
            error: 'fas fa-times-circle',
            warning: 'fas fa-exclamation-circle',
            info: 'fas fa-info-circle'
        };
        
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <i class="${icons[type]}"></i>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()">
                <i class="fas fa-times"></i>
            </button>
        `;
        
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.style.animation = 'slideOut 0.3s ease forwards';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }
}

const app = new DataQueryApp();