"""
环比箭头柱状图 - Gradio 交互式应用
功能：数据导入、颜色配置、数据可视化、图片导出
整体流程：
1. 读取用户上传的CSV/Excel/TXT文件
2. 验证数据格式有效性
3. 生成带环比增长率箭头的堆叠柱状图
4. 支持自定义图表颜色和标题
5. 导出不同格式和分辨率的图表图片
"""

# 导入核心库
import gradio as gr  # 用于构建交互式Web界面
import pandas as pd  # 数据处理库
import numpy as np   # 数值计算库
import matplotlib.pyplot as plt  # 绘图库
import matplotlib  # 绘图配置
import os  # 操作系统交互
from pathlib import Path  # 路径处理
import io  # 输入输出流
from datetime import datetime  # 时间戳生成
import re  # 正则表达式，用于颜色格式转换
import asyncio  # 异步编程
import concurrent.futures  # 线程池，用于异步导出
import time  # 计时
import logging  # 日志记录

# ======================== 日志配置 ========================
# 配置日志输出格式和级别，方便调试和运行状态跟踪
logging.basicConfig(
    level=logging.DEBUG,  # 日志级别：DEBUG(详细) < INFO < WARNING < ERROR < CRITICAL
    format='[%(asctime)s] [%(levelname)s] %(message)s',  # 时间 + 级别 + 消息
    handlers=[logging.StreamHandler()]  # 输出到控制台
)
logger = logging.getLogger(__name__)  # 创建日志实例


# ======================== 颜色转换工具函数 ========================
def rgba_to_hex(rgba_str):
    """
    将 rgba()/rgb() 格式的颜色字符串转换为十六进制格式（#RRGGBB）
    用于兼容Gradio ColorPicker的输出格式和Matplotlib的颜色要求
    
    Args:
        rgba_str: str - 格式为 'rgba(r, g, b, a)' 或 'rgb(r, g, b)' 的字符串，也支持直接传入十六进制字符串
    
    Returns:
        str - 十六进制格式的颜色字符串，如 '#2a2d2c'，转换失败时返回默认色 #3498db
    """
    print(f"[调试] rgba_to_hex 被调用，输入: {rgba_str}")
    
    # 空值处理
    if not rgba_str:
        print(f"[调试] 输入为空，返回默认颜色 #3498db")
        return '#3498db'
    
    # 已经是十六进制格式则直接返回
    if rgba_str.startswith('#'):
        print(f"[调试] 输入已经是十六进制格式: {rgba_str}")
        return rgba_str
    
    try:
        # 匹配rgba格式 (支持小数/整数，带空格/不带空格)
        match = re.match(r'rgba\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)\)', rgba_str)
        if match:
            r = int(float(match.group(1)))  # 红色通道 (0-255)
            g = int(float(match.group(2)))  # 绿色通道 (0-255)
            b = int(float(match.group(3)))  # 蓝色通道 (0-255)
            # 转换为十六进制 (02x表示两位十六进制，不足补0)
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            print(f"[调试] rgba({r},{g},{b}) 转换为: {hex_color}")
            return hex_color
        
        # 匹配rgb格式
        match = re.match(r'rgb\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)\)', rgba_str)
        if match:
            r = int(float(match.group(1)))
            g = int(float(match.group(2)))
            b = int(float(match.group(3)))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            print(f"[调试] rgb({r},{g},{b}) 转换为: {hex_color}")
            return hex_color
        
        # 格式不匹配
        print(f"[调试] 无法解析颜色格式: {rgba_str}，返回默认颜色 #3498db")
        return '#3498db'
    except Exception as e:
        # 异常处理 (如数值转换失败)
        print(f"[调试] 颜色转换失败: {str(e)}，返回默认颜色 #3498db")
        return '#3498db'


# ======================== 中文字体配置 ========================
def set_chinese_font():
    """
    配置Matplotlib的中文字体，解决中文显示乱码问题
    不同操作系统(Windows/macOS/Linux)适配不同的中文字体
    
    Returns:
        str - 实际生效的字体名称
    """
    system_name = os.name  # 获取操作系统类型: nt=Windows, posix=macOS/Linux
    # 按优先级定义各系统的中文字体列表
    if system_name == 'nt':  # Windows系统
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']  # 黑体、微软雅黑、宋体
    elif system_name == 'posix':  # macOS/Linux系统
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']  # 华文黑体、苹果丽黑、文泉驿微米黑
    else:  # 其他系统
        font_names = ['DejaVu Sans']  # 备用字体
    
    # 尝试加载字体，成功则返回
    for font_name in font_names:
        try:
            plt.rcParams['font.sans-serif'] = [font_name]  # 设置默认字体
            plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示为方块的问题
            return font_name
        except:
            continue  # 字体加载失败则尝试下一个
    
    # 所有中文字体都失败时使用默认字体
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return 'DejaVu Sans'


# 初始化中文字体 (程序启动时执行)
set_chinese_font()

# ======================== 常量定义 ========================
# 默认配色方案 (8种常用颜色，覆盖大部分场景)
DEFAULT_COLORS = [
    '#3498db',  # 蓝色
    '#2ecc71',  # 绿色
    '#e74c3c',  # 红色
    '#f39c12',  # 橙色
    '#9b59b6',  # 紫色
    '#1abc9c',  # 青绿色
    '#e67e22',  # 深橙色
    '#34495e'   # 深灰色
]


# ======================== 数据读取函数 ========================
def read_file(file):
    """
    读取用户上传的文件，支持CSV/Excel/TXT格式
    
    Args:
        file: gradio.File对象 - 用户上传的文件
    
    Returns:
        tuple: (pd.DataFrame/None, str)
            - DataFrame: 读取成功返回数据框，失败返回None
            - str: 状态消息 (成功/失败信息)
    """
    try:
        if file is None:
            return None, "请上传文件"
        
        # 获取文件扩展名 (转小写，统一判断)
        file_extension = Path(file.name).suffix.lower()
        
        # 根据扩展名选择读取方式
        if file_extension in ['.csv']:
            df = pd.read_csv(file.name)  # 读取CSV文件
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file.name)  # 读取Excel文件
        elif file_extension in ['.txt']:
            # 读取文本文件 (sep=None自动识别分隔符，engine='python'兼容更多格式)
            df = pd.read_csv(file.name, sep=None, engine='python')
        else:
            return None, f"不支持的文件格式: {file_extension}"
        
        # 读取成功，返回数据和状态
        return df, f"文件读取成功: {len(df)} 行 × {len(df.columns)} 列"
    except Exception as e:
        # 捕获所有异常 (如文件损坏、路径错误等)
        return None, f"读取文件失败: {str(e)}"


# ======================== 数据验证函数 ========================
def validate_data(df):
    """
    验证数据格式是否符合绘图要求
    
    Args:
        df: pd.DataFrame - 待验证的数据框
    
    Returns:
        tuple: (bool, str)
            - bool: 验证通过返回True，失败返回False
            - str: 验证结果消息
    """
    # 空数据检查
    if df is None or df.empty:
        return False, "数据为空"
    
    # 数据行数检查 (至少2行才能计算环比)
    if len(df) < 2:
        return False, "至少需要2年的数据才能计算环比增长率"
    
    # 数值列检查 (至少1列数值数据才能绘图)
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 1:
        return False, "数据中没有数值列"
    
    # 验证通过
    return True, "数据验证通过"


# ======================== 核心绘图函数 ========================
def plot_stacked_bar_chart_with_arrow(df, colors=None, title="环比箭头柱状图"):
    """
    绘制带环比增长率箭头的堆叠柱状图
    核心逻辑：
    1. 提取年份和区域数据
    2. 绘制堆叠柱状图 (每个区域一层)
    3. 计算环比增长率，绘制箭头和增长率标签
    4. 美化图表样式 (隐藏边框、配置图例、调整文字等)
    
    Args:
        df: pd.DataFrame - 数据框 (第一列为年份，后续列为区域数据)
        colors: list[str] - 各区域的颜色列表 (可选，默认使用DEFAULT_COLORS)
        title: str - 图表标题
    
    Returns:
        matplotlib.figure.Figure/None: 绘制成功返回图表对象，失败返回None
    """
    print(f"[调试] plot_stacked_bar_chart_with_arrow 被调用")
    try:
        # 空数据保护
        if df is None or df.empty:
            print("[调试] 数据为空或 None")
            return None
        
        # 数据提取
        years = df.iloc[:, 0].astype(str).tolist()  # 第一列转为字符串作为年份标签
        regions = df.columns[1:].tolist()  # 后续列名为区域名称
        data = df.iloc[:, 1:].values  # 数值数据 (二维数组)
        
        # 数据行数检查 (至少2行才能计算环比)
        if data.shape[0] < 2:
            return None
        
        # 颜色配置处理
        if colors is None:
            colors = DEFAULT_COLORS[:len(regions)]  # 使用默认颜色，匹配区域数量
        elif len(colors) < len(regions):
            # 颜色数量不足时，循环重复颜色列表
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
        
        print(f"[调试] 转换前的颜色: {colors}")
        # 统一转换为十六进制颜色 (兼容rgba/rgb格式)
        colors = [rgba_to_hex(color) for color in colors]
        print(f"[调试] 转换后的颜色: {colors}")
        
        # 创建图表对象 (figsize: 宽12英寸×高10英寸, dpi: 分辨率100)
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        
        # 柱状图X轴位置 (年份数量个刻度)
        x = np.arange(len(years))
        bar_width = 0.55  # 柱状图宽度 (0-1之间，越小越窄)
        
        # 绘制堆叠柱状图
        bottom = np.zeros(len(years))  # 每一层的底部位置 (初始为0)
        for i in range(len(regions)):
            # 绘制当前区域的柱状图 (bottom指定堆叠底部)
            bars = ax.bar(x, data[:, i], bar_width, bottom=bottom, 
                          color=colors[i], label=regions[i])
            
            # 在每个柱子中间添加数值标签 (白色粗体)
            for bar, b, val in zip(bars, bottom, data[:, i]):
                height = bar.get_height()
                if height > 0:  # 数值大于0时才显示
                    ax.text(bar.get_x() + bar.get_width() / 2,  # X坐标：柱子中心
                           b + height / 2,                     # Y坐标：柱子垂直中心
                           f'{int(val):,}',                    # 数值 (千分位分隔符)
                           ha='center', va='center',           # 水平/垂直居中
                           fontsize=11, color='white', fontweight='semibold')
            
            # 更新下一层的底部位置 (当前层的顶部 = 底部 + 高度)
            bottom += data[:, i]
        
        # 计算每年的总计值 (用于计算环比增长率)
        totals = np.sum(data, axis=1)
        
        # 在每个年份顶部添加总计数值标签
        for i, total in enumerate(totals):
            ax.text(x[i], total + max(totals) * 0.02,  # 略高于柱子顶部
                   f'{int(total):,}',                  # 千分位格式
                   ha='center', va='bottom',           # 居中，底部对齐
                   fontsize=13, fontweight='bold', color='#333333')
        
        # 绘制环比增长率箭头和标签 (至少2年才绘制)
        if len(years) > 1:
            # 计算环比增长率: (本年-上年)/上年 × 100
            growth = ((totals[1:] - totals[:-1]) / totals[:-1]) * 100
            num_arrows = len(growth)  # 箭头数量 = 年份数 - 1
            
            # 箭头样式参数配置 (基于数据最大值动态计算，适配不同数据范围)
            max_total = np.max(totals)
            BASE_OFFSET_Y = max_total * 0.05       # 箭头起始点Y轴偏移
            VERTICAL_RISE_FACTOR = 0.15            # 箭头峰值高度系数
            ARROW_HEAD_WIDTH = 0.06                # 箭头头部宽度
            ARROW_HEAD_LENGTH = max_total * 0.02   # 箭头头部长度
            LINE_WIDTH = 1.5                       # 箭头线条宽度
            ENDPOINT_SPACING = 0.15                # 箭头端点与柱子的间距
            
            base_offset = max_total * VERTICAL_RISE_FACTOR  # 箭头峰值偏移
            
            # 绘制每个箭头
            for i in range(num_arrows):
                # 箭头起始/结束位置 (X轴：年份位置 ± 间距，Y轴：总计值 + 偏移)
                start_x = x[i] + ENDPOINT_SPACING
                start_y = totals[i] + BASE_OFFSET_Y
                end_x = x[i + 1] - ENDPOINT_SPACING
                end_y = totals[i + 1] + BASE_OFFSET_Y
                
                # 箭头峰值位置 (取起始/结束Y的最大值 + 偏移)
                base_peak_y = max(start_y, end_y)
                peak_y = base_peak_y + base_offset
                
                # 箭头拐点坐标 (形成"山峰"形状)
                mid1_x, mid1_y = start_x, peak_y
                mid2_x, mid2_y = end_x, peak_y
                
                # 绘制箭头线条 (四段线：起点→左拐点→右拐点→终点)
                ax.plot([start_x, mid1_x, mid2_x, end_x],
                       [start_y, mid1_y, mid2_y, end_y],
                       color='#333333', linewidth=LINE_WIDTH,
                       zorder=3, solid_capstyle='round')  # zorder确保箭头在柱子上方
                
                # 绘制箭头头部 (在终点位置)
                arrow_start_x, arrow_start_y = mid2_x, mid2_y
                arrow_end_y = end_y
                arrow_length = arrow_end_y - arrow_start_y
                
                ax.arrow(arrow_start_x, arrow_start_y, 0, 
                        arrow_length - ARROW_HEAD_LENGTH,  # 箭头长度 (减去头部长度)
                        head_width=ARROW_HEAD_WIDTH,
                        head_length=ARROW_HEAD_LENGTH,
                        fc='#333333', ec='#333333',  # 填充色/边框色
                        length_includes_head=True, zorder=3)  # 长度包含箭头头部
                
                # 增长率标签位置 (箭头峰值中间)
                label_x = (start_x + end_x) / 2
                label_y = peak_y
                
                # 格式化增长率文本 (正数带+号，负数带-号)
                growth_value = growth[i]
                if growth_value >= 0:
                    rate_text = f'+{int(round(growth_value))}%'
                else:
                    rate_text = f'{int(round(growth_value))}%'
                
                # 标签背景样式 (圆形背景，增强可读性)
                bbox = dict(boxstyle="circle,pad=0.4",
                           facecolor='#2c3e50',  # 深蓝色背景
                           edgecolor='none', alpha=1.0)  # 无边框，不透明
                
                # 添加增长率标签
                ax.text(label_x, label_y, rate_text,
                       ha='center', va='center',
                       color='white', fontsize=12,
                       fontweight='bold', bbox=bbox, zorder=4)  # zorder确保标签在最上层
        
        # 图表样式配置
        ax.set_xticks(x)  # 设置X轴刻度位置
        ax.set_xticklabels(years, fontsize=13)  # 设置X轴标签 (年份)
        ax.set_yticks([])  # 隐藏Y轴刻度 (堆叠图不需要Y轴)
        ax.set_title(title, fontsize=18, pad=20, fontweight='bold')  # 图表标题
        
        # 隐藏边框 (只保留底部X轴)
        ax.spines['top'].set_visible(False)    # 顶部边框
        ax.spines['right'].set_visible(False)  # 右侧边框
        ax.spines['left'].set_visible(False)   # 左侧边框
        
        # 配置图例 (顶部居中，最多4列，无边框)
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12),
                 ncol=min(4, len(regions)), frameon=False, fontsize=11)
        
        # 自动调整布局 (防止文字重叠)
        plt.tight_layout()
        
        print(f"[调试] plot_stacked_bar_chart_with_arrow 准备返回 figure: {fig}")
        return fig
    except Exception as e:
        # 捕获绘图过程中的所有异常
        print(f"绘图失败: {str(e)}")
        return None


# ======================== Gradio界面构建 ========================
# 创建Gradio Blocks应用 (比Interface更灵活的布局方式)
with gr.Blocks(title="环比箭头柱状图生成器") as demo:
    # 页面标题和分隔线
    gr.Markdown("# 📊 环比箭头柱状图 - 交互式数据可视化")
    gr.Markdown("---")
    
    # 状态变量 (存储当前数据和图表对象，不显示在界面)
    current_data = gr.State(value=None)  # 存储当前读取的数据框
    current_fig = gr.State(value=None)   # 存储当前生成的图表对象
    
    # 第一行布局 (数据导入 + 颜色配置)
    with gr.Row():
        # 左侧列：数据导入
        with gr.Column(scale=1):
            gr.Markdown("## 1️⃣ 数据导入")
            
            # 文件上传组件
            file_input = gr.File(
                label="上传数据表文件",
                # 支持的文件类型 (MIME类型 + 扩展名)
                file_types=['text/csv', '.csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx', 'application/vnd.ms-excel', '.xls', 'text/plain', '.txt'],
                type="filepath"  # 返回文件路径而非二进制数据
            )
            
            # 图表标题输入框
            chart_title = gr.Textbox(
                label="图表标题",
                value="环比箭头柱状图"  # 默认值
            )
            
            # 生成图表按钮
            generate_btn = gr.Button(
                "🎨 生成图表",
                variant="primary",  # 主按钮样式 (蓝色)
                size="lg"           # 大尺寸
            )
            
            # 状态信息输出框
            status_output = gr.Textbox(
                label="状态信息",
                lines=3,           # 显示3行
                interactive=False  # 不可编辑
            )
        
        # 右侧列：颜色配置
        with gr.Column(scale=1):
            gr.Markdown("## 2️⃣ 颜色配置")
            
            # 颜色选择器容器 (初始隐藏，生成图表后显示)
            color_container = gr.Column(visible=False)
            
            with color_container:
                # 8个颜色选择器 (对应8个默认颜色，初始隐藏，根据区域数量显示)
                color1 = gr.ColorPicker(label="区域1 颜色", value=DEFAULT_COLORS[0], visible=False)
                color2 = gr.ColorPicker(label="区域2 颜色", value=DEFAULT_COLORS[1], visible=False)
                color3 = gr.ColorPicker(label="区域3 颜色", value=DEFAULT_COLORS[2], visible=False)
                color4 = gr.ColorPicker(label="区域4 颜色", value=DEFAULT_COLORS[3], visible=False)
                color5 = gr.ColorPicker(label="区域5 颜色", value=DEFAULT_COLORS[4], visible=False)
                color6 = gr.ColorPicker(label="区域6 颜色", value=DEFAULT_COLORS[5], visible=False)
                color7 = gr.ColorPicker(label="区域7 颜色", value=DEFAULT_COLORS[6], visible=False)
                color8 = gr.ColorPicker(label="区域8 颜色", value=DEFAULT_COLORS[7], visible=False)
                
                # 应用颜色更新按钮
                update_colors_btn = gr.Button(
                    "🔄 应用颜色更新",
                    variant="secondary"  # 次要按钮样式 (灰色)
                )
    
    # 第二行布局 (图表预览 + 图片导出)
    with gr.Row():
        # 左侧列：图表预览
        with gr.Column(scale=1):
            gr.Markdown("## 3️⃣ 图表预览")
            
            # 图表显示组件
            plot_output = gr.Plot(label="图表")
            
            # 数据预览表格
            data_preview = gr.DataFrame(
                label="数据预览",
                interactive=False  # 不可编辑
            )
        
        # 右侧列：图片导出
        with gr.Column(scale=1):
            gr.Markdown("## 4️⃣ 图片导出")
            
            # 分辨率选择下拉框
            dpi_option = gr.Dropdown(
                label="分辨率 (DPI)",
                choices=[150, 300, 600],  # 可选分辨率
                value=300                 # 默认300DPI
            )
            
            # 导出格式选择下拉框
            format_option = gr.Dropdown(
                label="导出格式",
                choices=['PNG', 'JPG', 'PDF', 'SVG'],  # 支持的格式
                value='PNG'                             # 默认PNG
            )
            
            # 导出按钮
            export_btn = gr.Button(
                "⬇️ 开始导出",
                variant="primary"
            )
            
            # 导出进度条 (自动显示，无需手动控制)
            export_progress = gr.Progress()
            
            # 导出状态信息
            export_status = gr.Textbox(
                label="导出状态",
                lines=2,
                interactive=False,
                value=""
            )
            
            # 下载文件组件 (初始隐藏，导出成功后显示)
            download_output = gr.File(
                label="下载图片",
                visible=False
            )
    
    # ======================== 事件处理函数：生成图表 ========================
    def handle_generate(file, title):
        """
        处理"生成图表"按钮点击事件
        流程：读取文件 → 验证数据 → 生成图表 → 更新界面
        
        Args:
            file: str - 文件路径
            title: str - 图表标题
        
        Returns:
            tuple: 按顺序更新的组件值
        """
        print("[调试] handle_generate 函数被调用")
        # 文件未上传
        if file is None:
            print("[调试] 文件为 None")
            return (None, None, None, 
                    gr.update(visible=False),  # 颜色容器隐藏
                    # 所有颜色选择器隐藏
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    "请先上传文件", None)
        
        # 读取文件
        df, message = read_file(file)
        
        # 读取失败
        if df is None:
            print(f"[调试] 读取文件失败: {message}")
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    message, None)
        
        # 验证数据
        is_valid, validate_msg = validate_data(df)
        
        # 验证失败
        if not is_valid:
            print(f"[调试] 数据验证失败: {validate_msg}")
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    f"{message}\n{validate_msg}", None)
        
        # 数据验证通过，准备绘图
        regions = df.columns[1:].tolist()  # 获取区域列表
        colors = DEFAULT_COLORS[:len(regions)]  # 匹配区域数量的颜色
        print(f"[调试] 准备绘图: 区域数量={len(regions)}, 颜色数量={len(colors)}")
        
        try:
            # 生成图表
            fig = plot_stacked_bar_chart_with_arrow(df, colors, title)
            
            # 绘图失败
            if fig is None:
                print("[调试] plot_stacked_bar_chart_with_arrow 返回 None")
                return (None, None, None, 
                        gr.update(visible=False), 
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                        "绘图失败", None)
            
            print(f"[调试] 成功创建 figure 对象: {fig}")
            # 根据区域数量设置颜色选择器的可见性
            color_visibilities = [
                gr.update(visible=i < len(regions), label=f"{regions[i]} 颜色" if i < len(regions) else "") 
                for i in range(8)
            ]
            
            # 返回结果：更新所有相关组件
            return (
                fig,  # 图表预览
                fig,  # 存储到current_fig状态
                df,   # 数据预览
                gr.update(visible=True),  # 颜色容器显示
            ) + tuple(color_visibilities) + (  # 颜色选择器可见性
                f"{message}\n{validate_msg}",  # 状态信息
                df  # 存储到current_data状态
            )
        except Exception as e:
            # 捕获生成图表过程中的异常
            print(f"[调试] 生成图表失败: {str(e)}")
            import traceback
            traceback.print_exc()  # 打印详细异常栈
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), gr.update(visible=False),
                    f"生成图表失败: {str(e)}", None)
    
    # 绑定"生成图表"按钮的点击事件
    generate_btn.click(
        fn=handle_generate,  # 处理函数
        inputs=[file_input, chart_title],  # 输入组件
        outputs=[
            plot_output, current_fig, data_preview, color_container,
            color1, color2, color3, color4, color5, color6, color7, color8,
            status_output, current_data
        ]  # 输出组件
    )
    
    # ======================== 事件处理函数：更新颜色 ========================
    def update_colors(df, title, c1, c2, c3, c4, c5, c6, c7, c8):
        """
        处理"应用颜色更新"按钮点击事件
        流程：收集颜色 → 转换格式 → 重新生成图表
        
        Args:
            df: pd.DataFrame - 当前数据
            title: str - 图表标题
            c1-c8: str - 各颜色选择器的值
        
        Returns:
            tuple: (fig, fig, str) - 新图表、更新状态、状态信息
        """
        print("[调试] update_colors 函数被调用")
        # 未生成图表时的保护
        if df is None:
            print("[调试] df 为 None，返回错误")
            return None, None, "请先生成图表"
        
        # 获取区域列表
        regions = df.columns[1:].tolist()
        # 收集颜色值 (只取区域数量对应的颜色)
        raw_colors = [c1, c2, c3, c4, c5, c6, c7, c8][:len(regions)]
        print(f"[调试] 原始颜色列表: {raw_colors}")
        
        # 转换颜色格式 (统一为十六进制)
        colors = [rgba_to_hex(color) for color in raw_colors]
        print(f"[调试] 转换后的颜色列表: {colors}")
        print(f"[调试] 更新颜色: 区域数量={len(regions)}, 颜色数量={len(colors)}")
        
        try:
            # 重新生成图表 (使用新颜色)
            fig = plot_stacked_bar_chart_with_arrow(df, colors, title)
            
            # 绘图失败
            if fig is None:
                print("[调试] plot_stacked_bar_chart_with_arrow 返回 None")
                return None, None, "绘图失败"
            
            print(f"[调试] 成功创建新 figure 对象: {fig}")
            print("[调试] 颜色更新成功")
            return fig, fig, "颜色已更新"
        except Exception as e:
            # 捕获异常
            print(f"[调试] 颜色更新失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None, f"颜色更新失败: {str(e)}"
    
    # 绑定"应用颜色更新"按钮的点击事件
    update_colors_btn.click(
        fn=update_colors,  # 处理函数
        inputs=[current_data, chart_title, color1, color2, color3, color4, color5, color6, color7, color8],  # 输入
        outputs=[plot_output, current_fig, status_output]  # 输出
    )
    
    # ======================== 图表导出相关函数 ========================
    # 创建线程池 (最多1个线程，避免并发导出冲突)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    
    def export_chart_sync(fig, dpi, fmt, progress_callback):
        """
        同步导出图表函数 (在线程池中执行，避免阻塞UI)
        流程：准备参数 → 保存文件 → 验证文件 → 返回结果
        
        Args:
            fig: matplotlib.figure.Figure - 图表对象
            dpi: int - 分辨率
            fmt: str - 导出格式 (PNG/JPG/PDF/SVG)
            progress_callback: function - 进度更新回调函数
        
        Returns:
            tuple: (str/None, str/None)
                - str: 文件路径 (成功) / None (失败)
                - str: 错误信息 (失败) / None (成功)
        """
        total_start_time = time.perf_counter()  # 总耗时计时
        logger.debug("[导出] 开始导出流程")
        
        try:
            # 阶段1: 准备参数 (进度15%)
            phase1_start = time.perf_counter()
            progress_callback(0.15, "准备导出参数...")
            logger.debug("[导出] 阶段1: 准备导出参数")
            
            # 生成带时间戳的文件名 (避免重复)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"环比箭头柱状图_{timestamp}.{fmt.lower()}"
            
            # 创建临时目录 (如果不存在)
            temp_dir = os.path.join(os.getcwd(), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, filename)
            fmt_lower = fmt.lower()
            
            # 保存参数配置
            save_kwargs = {
                'format': fmt_lower,  # 导出格式
                'dpi': dpi            # 分辨率
            }
            
            # 不同格式的特殊配置
            use_bbox = True
            if fmt_lower in ['svg', 'pdf']:
                use_bbox = False  # SVG/PDF不需要bbox_inches，避免裁剪
            elif fmt_lower in ['jpg', 'jpeg']:
                save_kwargs['pil_kwargs'] = {'quality': 95}  # JPG质量95%
            
            # 位图格式添加bbox配置 (裁剪空白区域)
            if use_bbox:
                save_kwargs['bbox_inches'] = 'tight'  # 紧凑布局
                save_kwargs['pad_inches'] = 0.1       # 少量内边距
            
            phase1_time = (time.perf_counter() - phase1_start) * 1000
            logger.debug(f"[导出] 阶段1完成，耗时: {phase1_time:.2f} ms")
            
            # 阶段2: 保存图表 (进度35% → 80%)
            phase2_start = time.perf_counter()
            progress_callback(0.35, "保存图表到文件...")
            logger.debug("[导出] 阶段2: 保存图表到文件")
            
            # 保存图表到文件
            fig.savefig(file_path, **save_kwargs)
            
            phase2_time = (time.perf_counter() - phase2_start) * 1000
            progress_callback(0.80, "图表保存完成，验证文件...")
            logger.debug(f"[导出] 阶段2完成，耗时: {phase2_time:.2f} ms")
            
            # 阶段3: 验证文件 (进度85%)
            phase3_start = time.perf_counter()
            progress_callback(0.85, "验证导出文件...")
            logger.debug("[导出] 阶段3: 验证文件")
            
            # 检查文件是否存在
            if not os.path.exists(file_path):
                raise FileNotFoundError("导出文件未创建成功")
            
            # 检查文件大小 (避免空文件)
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise ValueError("导出文件为空")
            
            phase3_time = (time.perf_counter() - phase3_start) * 1000
            logger.debug(f"[导出] 阶段3完成，耗时: {phase3_time:.2f} ms")
            
            # 阶段4: 完成 (进度100%)
            progress_callback(1.0, "导出完成！")
            total_time = (time.perf_counter() - total_start_time) * 1000
            
            # 记录成功日志
            logger.info(f"[导出] 成功！文件: {filename}, 大小: {file_size/1024:.2f} KB, 总耗时: {total_time:.2f} ms")
            logger.debug(f"[导出] 性能明细 - 准备参数: {phase1_time:.2f} ms, 保存: {phase2_time:.2f} ms, 验证: {phase3_time:.2f} ms")
            
            return file_path, None  # 成功返回文件路径
            
        except Exception as e:
            # 捕获所有异常并记录
            logger.error(f"[导出] 失败: {str(e)}", exc_info=True)
            return None, str(e)
    
    async def export_chart_async(fig, dpi, fmt, progress=gr.Progress()):
        """
        异步导出图表函数 (Gradio前端调用)
        作用：将同步导出任务放入线程池，避免阻塞UI
        
        Args:
            fig: matplotlib.figure.Figure - 图表对象
            dpi: int - 分辨率
            fmt: str - 导出格式
            progress: gr.Progress - Gradio进度对象
        
        Returns:
            tuple: (str, gr.update)
                - str: 导出状态信息
                - gr.update: 下载组件的更新配置
        """
        # 未生成图表时的保护
        if fig is None:
            logger.warning("[导出] fig为None，无法导出")
            return "请先生成图表", gr.update(visible=False)
        
        logger.info(f"[导出] 收到导出请求 - DPI={dpi}, 格式={fmt}")
        
        # 定义进度回调函数 (更新Gradio进度条)
        def progress_fn(p, desc):
            progress(p, desc=desc)
        
        # 获取事件循环，在线程池中执行同步任务
        loop = asyncio.get_event_loop()
        file_path, error_msg = await loop.run_in_executor(
            executor,
            export_chart_sync,
            fig,
            dpi,
            fmt,
            progress_fn
        )
        
        # 导出失败
        if error_msg:
            logger.error(f"[导出] 最终失败: {error_msg}")
            return f"导出失败: {error_msg}", gr.update(visible=False)
        
        # 导出成功
        logger.info(f"[导出] 最终完成 - 文件路径: {file_path}")
        return "导出成功！", gr.update(value=file_path, visible=True)
    
    # 绑定"开始导出"按钮的点击事件
    export_btn.click(
        fn=export_chart_async,  # 异步处理函数
        inputs=[current_fig, dpi_option, format_option],  # 输入组件
        outputs=[export_status, download_output]  # 输出组件
    )
    
    # 页面底部提示信息
    gr.Markdown("---")
    gr.Markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💡 提示: 支持CSV、Excel(.xlsx, .xls)和文本文件(.txt)格式</p>
        <p>📊 数据格式要求: 第一列为年份，后续各列为区域数据</p>
    </div>
    """)


# ======================== 程序入口 ========================
if __name__ == "__main__":
    logger.info("[启动] 初始化 Gradio 应用，启用队列系统")
    demo.queue(max_size=10)  # 启用请求队列，最大队列长度10
    logger.info("[启动] 队列系统已就绪，准备启动服务器")
    # 启动Gradio应用
    demo.launch(
        share=False,        # 不生成公共链接 (仅本地访问)
        server_name="127.0.0.1",  # 绑定本地地址
        server_port=7861    # 端口号7861
    )
