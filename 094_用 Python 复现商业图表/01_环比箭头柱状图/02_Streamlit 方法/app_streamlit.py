"""
环比箭头柱状图 - Streamlit交互式应用
功能：数据导入、可视化、图片导出
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from pathlib import Path
import io
import os
from datetime import datetime

# 设置中文字体
def set_chinese_font():
    """配置中文字体"""
    system_name = os.name
    if system_name == 'nt':  # Windows
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']
    elif system_name == 'posix':  # macOS/Linux
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']
    else:
        font_names = ['DejaVu Sans']
    
    for font_name in font_names:
        try:
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            return font_name
        except:
            continue
    
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    return 'DejaVu Sans'

# 初始化字体
set_chinese_font()

# 页面配置
st.set_page_config(
    page_title="环比箭头柱状图生成器",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 应用标题
st.title("📊 环比箭头柱状图 - 交互式数据可视化")
st.markdown("---")

# 侧边栏
st.sidebar.title("⚙️ 设置")
st.sidebar.markdown("---")

# 状态管理
if 'data' not in st.session_state:
    st.session_state.data = None
if 'file_info' not in st.session_state:
    st.session_state.file_info = None
if 'fig' not in st.session_state:
    st.session_state.fig = None

# 默认颜色方案
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

def read_uploaded_file(uploaded_file):
    """读取上传的文件"""
    try:
        file_extension = Path(uploaded_file.name).suffix.lower()
        
        if file_extension in ['.csv']:
            df = pd.read_csv(uploaded_file)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(uploaded_file)
        elif file_extension in ['.txt']:
            df = pd.read_csv(uploaded_file, sep=None, engine='python')
        else:
            st.error(f"不支持的文件格式: {file_extension}")
            return None
        
        return df
    except Exception as e:
        st.error(f"读取文件失败: {str(e)}")
        return None

def validate_data(df):
    """验证数据格式"""
    if df is None or df.empty:
        return False, "数据为空"
    
    if len(df) < 2:
        return False, "至少需要2年的数据才能计算环比增长率"
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if len(numeric_cols) < 1:
        return False, "数据中没有数值列"
    
    return True, "数据验证通过"

def plot_stacked_bar_chart_with_arrow(df, colors=None, title="环比箭头柱状图"):
    """绘制环比箭头柱状图"""
    try:
        # 准备数据
        years = df.iloc[:, 0].astype(str).tolist()
        regions = df.columns[1:].tolist()
        data = df.iloc[:, 1:].values
        
        # 验证数据
        if data.shape[0] < 2:
            st.error("至少需要2年的数据")
            return None
        
        # 设置颜色
        if colors is None:
            colors = DEFAULT_COLORS[:len(regions)]
        elif len(colors) < len(regions):
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
        
        # 创建图形
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        
        # 计算x轴位置
        x = np.arange(len(years))
        bar_width = 0.55
        
        # 绘制堆叠柱状图
        bottom = np.zeros(len(years))
        for i in range(len(regions)):
            bars = ax.bar(x, data[:, i], bar_width, bottom=bottom, 
                          color=colors[i], label=regions[i])
            
            # 添加数据标签
            for bar, b, val in zip(bars, bottom, data[:, i]):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, 
                           b + height / 2,
                           f'{int(val):,}',
                           ha='center', va='center',
                           fontsize=11, color='white', fontweight='semibold')
            
            bottom += data[:, i]
        
        # 添加总数值标签
        totals = np.sum(data, axis=1)
        for i, total in enumerate(totals):
            ax.text(x[i], total + max(totals) * 0.02,
                   f'{int(total):,}',
                   ha='center', va='bottom',
                   fontsize=13, fontweight='bold', color='#333333')
        
        # 添加环比箭头
        if len(years) > 1:
            growth = ((totals[1:] - totals[:-1]) / totals[:-1]) * 100
            num_arrows = len(growth)
            
            max_total = np.max(totals)
            BASE_OFFSET_Y = max_total * 0.05
            VERTICAL_RISE_FACTOR = 0.15
            ARROW_HEAD_WIDTH = 0.06
            ARROW_HEAD_LENGTH = max_total * 0.02
            LINE_WIDTH = 1.5
            ENDPOINT_SPACING = 0.15
            
            base_offset = max_total * VERTICAL_RISE_FACTOR
            
            for i in range(num_arrows):
                start_x = x[i] + ENDPOINT_SPACING
                start_y = totals[i] + BASE_OFFSET_Y
                end_x = x[i + 1] - ENDPOINT_SPACING
                end_y = totals[i + 1] + BASE_OFFSET_Y
                base_peak_y = max(start_y, end_y)
                peak_y = base_peak_y + base_offset
                
                # 绘制箭头折线
                mid1_x, mid1_y = start_x, peak_y
                mid2_x, mid2_y = end_x, peak_y
                
                ax.plot([start_x, mid1_x, mid2_x, end_x],
                       [start_y, mid1_y, mid2_y, end_y],
                       color='#333333', linewidth=LINE_WIDTH,
                       zorder=3, solid_capstyle='round')
                
                # 绘制箭头
                arrow_start_x, arrow_start_y = mid2_x, mid2_y
                arrow_end_y = end_y
                arrow_length = arrow_end_y - arrow_start_y
                
                ax.arrow(arrow_start_x, arrow_start_y, 0, 
                        arrow_length - ARROW_HEAD_LENGTH,
                        head_width=ARROW_HEAD_WIDTH,
                        head_length=ARROW_HEAD_LENGTH,
                        fc='#333333', ec='#333333',
                        length_includes_head=True, zorder=3)
                
                # 绘制增长率标签
                label_x = (start_x + end_x) / 2
                label_y = peak_y
                
                growth_value = growth[i]
                if growth_value >= 0:
                    rate_text = f'+{int(round(growth_value))}%'
                else:
                    rate_text = f'{int(round(growth_value))}%'
                
                bbox = dict(boxstyle="circle,pad=0.4",
                           facecolor='#2c3e50',
                           edgecolor='none', alpha=1.0)
                
                ax.text(label_x, label_y, rate_text,
                       ha='center', va='center',
                       color='white', fontsize=12,
                       fontweight='bold', bbox=bbox, zorder=4)
        
        # 设置坐标轴和标题
        ax.set_xticks(x)
        ax.set_xticklabels(years, fontsize=13)
        ax.set_yticks([])
        ax.set_title(title, fontsize=18, pad=20, fontweight='bold')
        
        # 隐藏边框
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        # 设置图例
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12),
                 ncol=min(4, len(regions)), frameon=False, fontsize=11)
        
        # 调整布局
        plt.tight_layout()
        
        return fig
    except Exception as e:
        st.error(f"绘图失败: {str(e)}")
        import traceback
        st.error(traceback.format_exc())
        return None

# 主界面
col1, col2 = st.columns([1, 1])

with col1:
    st.header("1️⃣ 数据导入")
    
    # 文件上传
    uploaded_file = st.file_uploader(
        "上传数据表文件",
        type=['csv', 'xlsx', 'xls', 'txt'],
        help="支持CSV、Excel和文本文件格式"
    )
    
    if uploaded_file is not None:
        # 显示文件信息
        file_size = uploaded_file.size
        st.success(f"✅ 文件上传成功: {uploaded_file.name}")
        
        # 读取数据
        df = read_uploaded_file(uploaded_file)
        
        if df is not None:
            # 验证数据
            is_valid, msg = validate_data(df)
            
            if is_valid:
                st.session_state.data = df
                st.session_state.file_info = {
                    'name': uploaded_file.name,
                    'size': file_size,
                    'rows': len(df),
                    'cols': len(df.columns)
                }
                
                # 显示文件信息
                st.info(f"📊 文件信息: {len(df)} 行 × {len(df.columns)} 列, {file_size / 1024:.2f} KB")
                
                # 数据预览
                with st.expander("🔍 数据预览", expanded=True):
                    st.dataframe(df.head(10), use_container_width=True)
            else:
                st.error(f"❌ 数据验证失败: {msg}")

with col2:
    st.header("2️⃣ 图表配置")
    
    if st.session_state.data is not None:
        df = st.session_state.data
        
        # 图表标题
        chart_title = st.text_input(
            "图表标题",
            value="环比箭头柱状图",
            help="输入图表的标题"
        )
        
        # 颜色选择
        st.subheader("区域颜色设置")
        regions = df.columns[1:].tolist()
        custom_colors = []
        
        for i, region in enumerate(regions):
            default_color = DEFAULT_COLORS[i % len(DEFAULT_COLORS)]
            color = st.color_picker(
                f"{region} 的颜色",
                value=default_color,
                key=f"color_{i}"
            )
            custom_colors.append(color)
        
        # 生成图表按钮
        if st.button("🎨 生成图表", type="primary", use_container_width=True):
            with st.spinner("正在生成图表..."):
                fig = plot_stacked_bar_chart_with_arrow(
                    df, 
                    colors=custom_colors,
                    title=chart_title
                )
                
                if fig is not None:
                    st.session_state.fig = fig
                    st.success("✅ 图表生成成功!")
    else:
        st.info("请先上传数据文件")

# 图表展示和导出
st.markdown("---")
st.header("3️⃣ 图表展示与导出")

if st.session_state.fig is not None:
    # 显示图表
    st.pyplot(st.session_state.fig, use_container_width=True)
    
    # 导出功能
    st.markdown("### 📥 图片导出")
    
    col_export1, col_export2, col_export3 = st.columns([1, 1, 1])
    
    with col_export1:
        dpi_option = st.selectbox(
            "分辨率 (DPI)",
            options=[150, 300, 600],
            index=1,
            help="300 DPI适合打印，150 DPI适合屏幕显示"
        )
    
    with col_export2:
        format_option = st.selectbox(
            "导出格式",
            options=['PNG', 'JPG', 'PDF', 'SVG'],
            index=0,
            help="PNG推荐用于日常使用"
        )
    
    with col_export3:
        # 创建内存中的图片
        buf = io.BytesIO()
        st.session_state.fig.savefig(buf, format=format_option.lower(), 
                                    dpi=dpi_option, bbox_inches='tight')
        buf.seek(0)
        
        # 生成文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        default_filename = f"环比箭头柱状图_{timestamp}.{format_option.lower()}"
        
        st.download_button(
            label=f"⬇️ 下载图片 ({format_option})",
            data=buf,
            file_name=default_filename,
            mime=f"image/{format_option.lower()}",
            use_container_width=True
        )
    
    st.success(f"💡 提示: 图片已准备好下载，分辨率为 {dpi_option} DPI")
else:
    st.info("请先生成图表")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666;'>
        <p>💡 提示: 支持CSV、Excel(.xlsx, .xls)和文本文件(.txt)格式</p>
        <p>📊 数据格式要求: 第一列为年份，后续各列为区域数据</p>
    </div>
    """,
    unsafe_allow_html=True
)
