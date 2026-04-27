"""
环比箭头柱状图 - Streamlit交互式应用
功能：数据导入（支持CSV/Excel/TXT）、环比箭头堆叠柱状图可视化、图片导出（多格式/多分辨率）
开发环境：Python + Streamlit + Pandas + Matplotlib
核心逻辑：读取验证数据 → 绘制堆叠柱状图 → 添加环比增长率箭头 → 支持交互配置与导出
"""

# 导入核心模块
import streamlit as st  # 用于构建交互式Web应用
import pandas as pd      # 数据处理核心库
import numpy as np       # 数值计算库，支持数组操作
import matplotlib.pyplot as plt  # 绘图核心库
import matplotlib        # 绘图配置相关
from pathlib import Path # 路径处理，用于解析文件扩展名
import io                # 内存文件操作，用于图片导出
import os                # 系统信息获取，用于判断操作系统类型
from datetime import datetime  # 时间处理，用于生成导出文件名

# ===================== 基础配置函数 =====================
def set_chinese_font():
    """
    配置Matplotlib中文字体，解决中文显示乱码问题
    适配不同操作系统（Windows/macOS/Linux）的字体差异
    Returns:
        str: 实际生效的字体名称
    """
    # 获取操作系统类型
    system_name = os.name
    # 不同系统的常用中文字体列表（优先级从高到低）
    if system_name == 'nt':  # Windows系统
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']  # 黑体、微软雅黑、宋体
    elif system_name == 'posix':  # macOS/Linux系统
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']  # 苹方、思源黑体等
    else:  # 其他未知系统
        font_names = ['DejaVu Sans']  # 备用无衬线字体
    
    # 遍历字体列表，尝试设置可用字体
    for font_name in font_names:
        try:
            plt.rcParams['font.sans-serif'] = [font_name]  # 设置默认字体
            plt.rcParams['axes.unicode_minus'] = False     # 解决负号显示为方块的问题
            return font_name  # 返回成功设置的字体名称
        except:
            continue  # 字体不可用则尝试下一个
    
    # 所有中文字体都不可用时，使用默认字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return 'DejaVu Sans'

# 初始化中文字体（程序启动时执行）
set_chinese_font()

# ===================== 页面全局配置 =====================
# 设置Streamlit页面基础属性
st.set_page_config(
    page_title="环比箭头柱状图生成器",  # 浏览器标签页标题
    page_icon="📊",                     # 标签页图标（emoji/图片路径）
    layout="wide",                      # 页面布局：宽屏模式
    initial_sidebar_state="expanded"    # 侧边栏默认展开
)

# 页面主标题
st.title("📊 环比箭头柱状图 - 交互式数据可视化")
st.markdown("---")  # 分隔线

# ===================== 会话状态管理 =====================
# Streamlit的session_state用于跨交互保留数据（避免刷新后丢失）
if 'data' not in st.session_state:
    st.session_state.data = None  # 存储上传并验证后的DataFrame
if 'file_info' not in st.session_state:
    st.session_state.file_info = None  # 存储上传文件的元信息（名称/大小/行列数）
if 'fig' not in st.session_state:
    st.session_state.fig = None  # 存储生成的Matplotlib图表对象

# ===================== 常量定义 =====================
# 默认配色方案（可自定义扩展），按顺序分配给不同区域/类别
DEFAULT_COLORS = [
    '#3498db',  # 蓝色
    '#2ecc71',  # 绿色
    '#e74c3c',  # 红色
    '#f39c12',  # 橙色
    '#9b59b6',  # 紫色
    '#1abc9c',  # 青色
    '#e67e22',  # 琥珀色
    '#34495e'   # 深灰色
]

# ===================== 数据处理函数 =====================
def read_uploaded_file(uploaded_file):
    """
    读取用户上传的文件，支持CSV/Excel/TXT格式
    Args:
        uploaded_file: Streamlit上传的文件对象
    Returns:
        pd.DataFrame: 解析后的数据集（失败返回None）
    """
    try:
        # 获取文件扩展名（小写），用于判断文件类型
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        # 根据扩展名选择对应的读取方式
        if file_extension in ['.csv']:
            df = pd.read_csv(uploaded_file)  # 读取CSV文件
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file)  # 读取Excel文件
        elif file_extension in ['.txt']:
            # 自动识别分隔符读取文本文件（engine='python'支持灵活解析）
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        else:
            st.error(f"不支持的文件格式: {file_extension}")
            return None
        
        return df  # 返回解析后的DataFrame
    except Exception as e:
        # 捕获读取异常（如文件损坏、格式错误）
        st.error(f"读取文件失败: {str(e)}")
        return None

def validate_data(df):
    """
    验证数据集是否符合可视化要求
    Args:
        df: pd.DataFrame 待验证的数据集
    Returns:
        tuple: (bool, str) 验证结果（True/False）+ 提示信息
    """
    # 检查数据是否为空
    if df is None or df.empty:
        return False, "数据为空"
    
    # 检查数据行数（至少2行才能计算环比）
    if len(df) < 2:
        return False, "至少需要2年的数据才能计算环比增长率"
    
    # 检查是否有数值列（用于绘制柱状图）
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 1:
        return False, "数据中没有数值列"
    
    # 所有验证通过
    return True, "数据验证通过"

# ===================== 核心绘图函数 =====================
def plot_stacked_bar_chart_with_arrow(df, colors=None, title="环比箭头柱状图"):
    """
    绘制带环比增长率箭头的堆叠柱状图
    核心逻辑：绘制堆叠柱状图 → 计算总计值 → 添加环比箭头 → 标注增长率
    Args:
        df: pd.DataFrame 数据集（第一列为年份，后续列为各区域/类别数值）
        colors: list 自定义颜色列表（None则使用默认配色）
        title: str 图表标题
    Returns:
        matplotlib.figure.Figure: 生成的图表对象（失败返回None）
    """
    try:
        # 数据预处理：提取年份、区域名称、数值数据
        years = df.iloc[:, 0].astype(str).tolist()  # 第一列转为字符串作为年份标签
        regions = df.columns[1:].tolist()          # 后续列作为区域/类别名称
        data = df.iloc[:, 1:].values               # 数值数据转为numpy数组
        
        # 二次验证：至少需要2年数据才能计算环比
        if data.shape[0] < 2:
            st.error("至少需要2年的数据")
            return None
        
        # 颜色配置：补充自定义颜色（确保颜色数量匹配区域数量）
        if colors is None:
            colors = DEFAULT_COLORS[:len(regions)]  # 使用默认配色前N个
        elif len(colors) < len(regions):
            # 颜色不足时循环复用，再截取到匹配长度
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
        
        # 创建绘图对象：设置画布大小(12*10英寸)、分辨率(100DPI)
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        
        # 计算x轴位置：年份数量对应的等距坐标
        x = np.arange(len(years))
        bar_width = 0.55  # 柱状图宽度（0-1之间，值越大越宽）
        
        # 绘制堆叠柱状图：bottom参数控制堆叠基线
        bottom = np.zeros(len(years))  # 初始基线为0
        for i in range(len(regions)):
            # 绘制当前区域的柱状图（堆叠在之前的基线之上）
            bars = ax.bar(
                x, data[:, i], bar_width, 
                bottom=bottom,  # 堆叠基线
                color=colors[i],  # 区域颜色
                label=regions[i]  # 图例标签
            )
            
            # 为每个柱子添加数值标签（居中显示）
            for bar, b, val in zip(bars, bottom, data[:, i]):
                height = bar.get_height()
                if height > 0:  # 仅显示非零值标签
                    ax.text(
                        bar.get_x() + bar.get_width() / 2,  # 标签x坐标（柱子中心）
                        b + height / 2,  # 标签y坐标（柱子垂直中心）
                        f'{int(val):,}',  # 数值格式化（千分位分隔符）
                        ha='center', va='center',  # 水平/垂直居中
                        fontsize=11, color='white', fontweight='semibold'  # 样式
                    )
            
            bottom += data[:, i]  # 更新基线（堆叠下一个区域）
        
        # 计算每年的总计值（用于标注总计和计算环比）
        totals = np.sum(data, axis=1)
        # 为每年添加总计值标签（显示在柱子顶部）
        for i, total in enumerate(totals):
            ax.text(
                x[i], total + max(totals) * 0.02,  # 标签位置（柱子顶部+少量偏移）
                f'{int(total):,}',  # 总计值格式化
                ha='center', va='bottom',  # 居中、底部对齐
                fontsize=13, fontweight='bold', color='#333333'  # 样式
            )
        
        # 添加环比箭头和增长率标签（仅当年份数>1时）
        if len(years) > 1:
            # 计算环比增长率：(本年-上年)/上年 * 100
            growth = ((totals[1:] - totals[:-1]) / totals[:-1]) * 100
            num_arrows = len(growth)  # 箭头数量 = 年份数 - 1
            
            # 箭头样式参数配置（基于总计值的比例，保证适配不同数据范围）
            max_total = np.max(totals)                # 最大总计值（用于比例计算）
            BASE_OFFSET_Y = max_total * 0.05          # 箭头起始点y轴偏移（柱子顶部+5%）
            VERTICAL_RISE_FACTOR = 0.15              # 箭头峰值高度比例（15%）
            ARROW_HEAD_WIDTH = 0.06                  # 箭头头部宽度
            ARROW_HEAD_LENGTH = max_total * 0.02     # 箭头头部长度
            LINE_WIDTH = 1.5                         # 箭身线条宽度
            ENDPOINT_SPACING = 0.15                  # 箭头端点与柱子的水平间距
            
            base_offset = max_total * VERTICAL_RISE_FACTOR  # 箭头峰值偏移量
            
            # 遍历每个环比区间，绘制箭头和增长率
            for i in range(num_arrows):
                # 箭头起始点（上年总计值顶部）
                start_x = x[i] + ENDPOINT_SPACING
                start_y = totals[i] + BASE_OFFSET_Y
                # 箭头结束点（本年总计值顶部）
                end_x = x[i + 1] - ENDPOINT_SPACING
                end_y = totals[i + 1] + BASE_OFFSET_Y
                # 箭头峰值y坐标（取起始/结束点的最大值 + 偏移）
                base_peak_y = max(start_y, end_y)
                peak_y = base_peak_y + base_offset
                
                # 绘制箭头折线（三段式：起始→峰值→结束）
                mid1_x, mid1_y = start_x, peak_y  # 第一段终点（峰值左）
                mid2_x, mid2_y = end_x, peak_y    # 第二段终点（峰值右）
                ax.plot(
                    [start_x, mid1_x, mid2_x, end_x],  # x坐标序列
                    [start_y, mid1_y, mid2_y, end_y],  # y坐标序列
                    color='#333333', linewidth=LINE_WIDTH,  # 颜色、宽度
                    zorder=3, solid_capstyle='round'  # 层级（高于柱子）、线条端点圆润
                )
                
                # 绘制箭头头部（在折线结束段）
                arrow_start_x, arrow_start_y = mid2_x, mid2_y
                arrow_end_y = end_y
                arrow_length = arrow_end_y - arrow_start_y  # 箭头长度
                ax.arrow(
                    arrow_start_x, arrow_start_y,  # 箭头起始点
                    0, arrow_length - ARROW_HEAD_LENGTH,  # 箭头方向（y轴）、长度
                    head_width=ARROW_HEAD_WIDTH,    # 箭头头部宽度
                    head_length=ARROW_HEAD_LENGTH,  # 箭头头部长度
                    fc='#333333', ec='#333333',     # 填充色、边框色
                    length_includes_head=True,      # 长度包含箭头头部
                    zorder=3                        # 层级
                )
                
                # 绘制增长率标签（圆形背景）
                label_x = (start_x + end_x) / 2  # 标签x坐标（箭头中间）
                label_y = peak_y                 # 标签y坐标（箭头峰值）
                
                growth_value = growth[i]
                # 格式化增长率文本（正数加+号，负数直接显示）
                if growth_value >= 0:
                    rate_text = f'+{int(round(growth_value))}%'
                else:
                    rate_text = f'{int(round(growth_value))}%'
                
                # 标签背景样式（圆形、填充、无边框）
                bbox = dict(
                    boxstyle="circle,pad=0.4",  # 圆形+内边距
                    facecolor='#2c3e50',        # 背景色
                    edgecolor='none',           # 无边框
                    alpha=1.0                   # 不透明度
                )
                
                # 添加增长率文本标签
                ax.text(
                    label_x, label_y, rate_text,
                    ha='center', va='center',  # 居中对齐
                    color='white', fontsize=12, fontweight='bold',  # 样式
                    bbox=bbox, zorder=4  # 背景框、层级（高于箭头）
                )
        
        # 图表样式配置
        ax.set_xticks(x)  # 设置x轴刻度位置
        ax.set_xticklabels(years, fontsize=13)  # 设置x轴刻度标签（年份）
        ax.set_yticks([])  # 隐藏y轴刻度（堆叠图无需显示具体y值）
        ax.set_title(title, fontsize=18, pad=20, fontweight='bold')  # 标题样式
        
        # 隐藏图表边框（仅保留x轴）
        ax.spines['top'].set_visible(False)    # 顶部边框
        ax.spines['right'].set_visible(False)  # 右侧边框
        ax.spines['left'].set_visible(False)   # 左侧边框
        
        # 设置图例（顶部居中、多列显示、无边框）
        ax.legend(
            loc='upper center',                # 位置：上中
            bbox_to_anchor=(0.5, 1.12),        # 锚点（微调位置）
            ncol=min(4, len(regions)),         # 列数（最多4列）
            frameon=False,                     # 无边框
            fontsize=11                        # 字体大小
        )
        
        # 自动调整布局（避免标签/图例重叠）
        plt.tight_layout()
        
        return fig  # 返回生成的图表对象
    except Exception as e:
        # 捕获绘图异常，输出详细错误信息
        st.error(f"绘图失败: {str(e)}")
        import traceback
        st.error(traceback.format_exc())  # 输出堆栈信息（调试用）
        return None

# ===================== 主界面交互逻辑 =====================
# 分栏布局：左栏（数据导入）、右栏（图表配置）
col1, col2 = st.columns([1, 1])

# 左栏：数据导入模块
with col1:
    st.header("1️⃣ 数据导入")  # 子标题
    
    # 文件上传组件：支持CSV/Excel/TXT格式
    uploaded_file = st.file_uploader(
        "上传数据表文件",
        type=['csv', 'xlsx', 'xls', 'txt'],
        help="支持CSV、Excel和文本文件格式 | 数据格式要求：第一列为年份，后续列为区域/类别数值"
    )
    
    # 当用户上传文件后执行
    if uploaded_file is not None:
        # 获取文件大小（字节）
        file_size = uploaded_file.size
        st.success(f"✅ 文件上传成功: {uploaded_file.name}")
        
        # 读取上传的文件
        df = read_uploaded_file(uploaded_file)
        
        # 读取成功则验证数据
        if df is not None:
            is_valid, msg = validate_data(df)
            
            # 数据验证通过
            if is_valid:
                # 将数据存入会话状态（跨交互保留）
                st.session_state.data = df
                # 存储文件元信息
                st.session_state.file_info = {
                    'name': uploaded_file.name,
                    'size': file_size,
                    'rows': len(df),
                    'cols': len(df.columns)
                }
                
                # 显示文件信息提示框
                st.info(f"📊 文件信息: {len(df)} 行 × {len(df.columns)} 列, {file_size / 1024:.2f} KB")
                
                # 数据预览：可展开/折叠的表格
                with st.expander("🔍 数据预览", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)  # 显示前10行
            else:
                # 数据验证失败提示
                st.error(f"❌ 数据验证失败: {msg}")

# 右栏：图表配置模块
with col2:
    st.header("2️⃣ 图表配置")  # 子标题
    
    # 仅当数据导入并验证通过后显示配置项
    if st.session_state.data is not None:
        df = st.session_state.data
        
        # 图表标题输入框（默认值：环比箭头柱状图）
        chart_title = st.text_input(
            "图表标题",
            value="环比箭头柱状图",
            help="输入图表的主标题（显示在图表顶部）"
        )
        
        # 区域颜色自定义配置
        st.subheader("区域颜色设置")
        regions = df.columns[1:].tolist()  # 获取区域/类别名称
        custom_colors = []  # 存储用户自定义的颜色
        
        # 为每个区域生成颜色选择器
        for i, region in enumerate(regions):
            # 默认颜色：循环使用DEFAULT_COLORS
            default_color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            # 颜色选择器组件
            color = st.color_picker(
                f"{region} 的颜色",
                value=default_color,
                key=f"color_{i}"  # 唯一key（避免组件冲突）
            )
            custom_colors.append(color)  # 收集用户选择的颜色
        
        # 生成图表按钮（主按钮，强调样式）
        if st.button("🎨 生成图表", type="primary", use_container_width=True):
            # 加载状态提示
            with st.spinner("正在生成图表..."):
                # 调用绘图函数生成图表
                fig = plot_stacked_bar_chart_with_arrow(
                    df, 
                    colors=custom_colors,
                    title=chart_title
                )
                
                # 绘图成功则存入会话状态
                if fig is not None:
                    st.session_state.fig = fig
                    st.success("✅ 图表生成成功!")
    else:
        # 未导入数据时的提示
        st.info("请先上传数据文件并完成验证")

# ===================== 图表展示与导出模块 =====================
st.markdown("---")  # 分隔线
st.header("3️⃣ 图表展示与导出")

# 仅当图表生成成功后显示
if st.session_state.fig is not None:
    # 显示生成的图表（自适应容器宽度）
    st.pyplot(st.session_state.fig, use_container_width=True)
    
    # 图片导出配置
    st.markdown("### 📥 图片导出")
    
    # 导出配置分栏：分辨率、格式、下载按钮
    col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
    
    with col_export1:
        # 分辨率选择（DPI）：150（屏幕）、300（打印）、600（高清）
        dpi_option = st.selectbox(
            "分辨率 (DPI)",
            options=[150, 300, 600],
            index=1,  # 默认300DPI
            help="300 DPI适合打印，150 DPI适合屏幕显示，600 DPI为高清打印"
        )
    
    with col_export2:
        # 导出格式选择
        format_option = st.selectbox(
            "导出格式",
            options=['PNG', 'JPG', 'PDF', 'SVG'],
            index=0,  # 默认PNG
            help="PNG/JPG为位图（适合屏幕），PDF/SVG为矢量图（适合打印/缩放）"
        )
    
    with col_export3:
        # 内存中生成图片文件（避免写入本地磁盘）
        buf = io.BytesIO()
        # 保存图表到内存缓冲区
        st.session_state.fig.savefig(
            buf, 
            format=format_option.lower(),  # 格式转为小写（Matplotlib要求）
            dpi=dpi_option,                # 分辨率
            bbox_inches='tight'            # 紧凑布局（避免留白）
        )
        buf.seek(0)  # 重置缓冲区指针到起始位置
        
        # 生成带时间戳的文件名（避免重复）
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"环比箭头柱状图_{timestamp}.{format_option.lower()}"
        
        # 下载按钮：触发文件下载
        st.download_button(
            label=f"⬇️ 下载图片 ({format_option})",
            data=buf,  # 下载数据（内存缓冲区）
            file_name=default_filename,  # 默认文件名
            mime=f"image/{format_option.lower()}",  # MIME类型（浏览器识别文件类型）
            use_container_width=True
        )
    
    # 导出成功提示
    st.success(f"💡 提示: 图片已准备好下载，分辨率为 {dpi_option} DPI")
else:
    # 未生成图表时的提示
    st.info("请先完成数据导入和图表配置，点击「生成图表」按钮")

# ===================== 页脚提示 =====================
st.markdown("---")  # 分隔线
# 自定义HTML页脚（居中、浅灰色文字）
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>💡 提示: 支持CSV、Excel(.xlsx, .xls)和文本文件(.txt)格式</p>
        <p>📊 数据格式要求: 第一列为年份，后续各列为区域/类别数值（至少2年数据）</p>
        <p>🔧 技术支持: Matplotlib + Streamlit | 如有问题请检查数据格式是否符合要求</p>
    </div>
    """,
    unsafe_allow_html=True  # 允许渲染HTML
)