"""
环比箭头柱状图 - Gradio 交互式应用
功能：数据导入、颜色配置、数据可视化、图片导出
"""

import gradio as gr
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import os
from pathlib import Path
import io
from datetime import datetime
import re
import asyncio
import concurrent.futures
import time
import logging

logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] [%(levelname)s] %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)


def rgba_to_hex(rgba_str):
    """
    将 rgba() 格式的颜色字符串转换为十六进制格式
    
    Args:
        rgba_str: 格式为 'rgba(r, g, b, a)' 的字符串
        
    Returns:
        十六进制格式的颜色字符串，如 '#2a2d2c'
    """
    print(f"[调试] rgba_to_hex 被调用，输入: {rgba_str}")
    
    if not rgba_str:
        print(f"[调试] 输入为空，返回默认颜色 #3498db")
        return '#3498db'
    
    if rgba_str.startswith('#'):
        print(f"[调试] 输入已经是十六进制格式: {rgba_str}")
        return rgba_str
    
    try:
        match = re.match(r'rgba\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)\)', rgba_str)
        if match:
            r = int(float(match.group(1)))
            g = int(float(match.group(2)))
            b = int(float(match.group(3)))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            print(f"[调试] rgba({r},{g},{b}) 转换为: {hex_color}")
            return hex_color
        
        match = re.match(r'rgb\((\d+\.?\d*),\s*(\d+\.?\d*),\s*(\d+\.?\d*)\)', rgba_str)
        if match:
            r = int(float(match.group(1)))
            g = int(float(match.group(2)))
            b = int(float(match.group(3)))
            hex_color = f'#{r:02x}{g:02x}{b:02x}'
            print(f"[调试] rgb({r},{g},{b}) 转换为: {hex_color}")
            return hex_color
        
        print(f"[调试] 无法解析颜色格式: {rgba_str}，返回默认颜色 #3498db")
        return '#3498db'
    except Exception as e:
        print(f"[调试] 颜色转换失败: {str(e)}，返回默认颜色 #3498db")
        return '#3498db'


def set_chinese_font():
    """配置中文字体"""
    system_name = os.name
    if system_name == 'nt':
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']
    elif system_name == 'posix':
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


set_chinese_font()

DEFAULT_COLORS = [
    '#3498db',
    '#2ecc71',
    '#e74c3c',
    '#f39c12',
    '#9b59b6',
    '#1abc9c',
    '#e67e22',
    '#34495e'
]


def read_file(file):
    """读取上传的文件"""
    try:
        if file is None:
            return None, "请上传文件"
        
        file_extension = Path(file.name).suffix.lower()
        
        if file_extension in ['.csv']:
            df = pd.read_csv(file.name)
        elif file_extension in ['.xlsx', '.xls']:
            df = pd.read_excel(file.name)
        elif file_extension in ['.txt']:
            df = pd.read_csv(file.name, sep=None, engine='python')
        else:
            return None, f"不支持的文件格式: {file_extension}"
        
        return df, f"文件读取成功: {len(df)} 行 × {len(df.columns)} 列"
    except Exception as e:
        return None, f"读取文件失败: {str(e)}"


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
    print(f"[调试] plot_stacked_bar_chart_with_arrow 被调用")
    try:
        if df is None or df.empty:
            print("[调试] 数据为空或 None")
            return None
        
        years = df.iloc[:, 0].astype(str).tolist()
        regions = df.columns[1:].tolist()
        data = df.iloc[:, 1:].values
        
        if data.shape[0] < 2:
            return None
        
        if colors is None:
            colors = DEFAULT_COLORS[:len(regions)]
        elif len(colors) < len(regions):
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
        
        print(f"[调试] 转换前的颜色: {colors}")
        colors = [rgba_to_hex(color) for color in colors]
        print(f"[调试] 转换后的颜色: {colors}")
        
        fig, ax = plt.subplots(figsize=(12, 10), dpi=100)
        
        x = np.arange(len(years))
        bar_width = 0.55
        
        bottom = np.zeros(len(years))
        for i in range(len(regions)):
            bars = ax.bar(x, data[:, i], bar_width, bottom=bottom, 
                          color=colors[i], label=regions[i])
            
            for bar, b, val in zip(bars, bottom, data[:, i]):
                height = bar.get_height()
                if height > 0:
                    ax.text(bar.get_x() + bar.get_width() / 2, 
                           b + height / 2,
                           f'{int(val):,}',
                           ha='center', va='center',
                           fontsize=11, color='white', fontweight='semibold')
            
            bottom += data[:, i]
        
        totals = np.sum(data, axis=1)
        for i, total in enumerate(totals):
            ax.text(x[i], total + max(totals) * 0.02,
                   f'{int(total):,}',
                   ha='center', va='bottom',
                   fontsize=13, fontweight='bold', color='#333333')
        
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
                
                mid1_x, mid1_y = start_x, peak_y
                mid2_x, mid2_y = end_x, peak_y
                
                ax.plot([start_x, mid1_x, mid2_x, end_x],
                       [start_y, mid1_y, mid2_y, end_y],
                       color='#333333', linewidth=LINE_WIDTH,
                       zorder=3, solid_capstyle='round')
                
                arrow_start_x, arrow_start_y = mid2_x, mid2_y
                arrow_end_y = end_y
                arrow_length = arrow_end_y - arrow_start_y
                
                ax.arrow(arrow_start_x, arrow_start_y, 0, 
                        arrow_length - ARROW_HEAD_LENGTH,
                        head_width=ARROW_HEAD_WIDTH,
                        head_length=ARROW_HEAD_LENGTH,
                        fc='#333333', ec='#333333',
                        length_includes_head=True, zorder=3)
                
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
        
        ax.set_xticks(x)
        ax.set_xticklabels(years, fontsize=13)
        ax.set_yticks([])
        ax.set_title(title, fontsize=18, pad=20, fontweight='bold')
        
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1.12),
                 ncol=min(4, len(regions)), frameon=False, fontsize=11)
        
        plt.tight_layout()
        
        print(f"[调试] plot_stacked_bar_chart_with_arrow 准备返回 figure: {fig}")
        return fig
    except Exception as e:
        print(f"绘图失败: {str(e)}")
        return None


with gr.Blocks(title="环比箭头柱状图生成器") as demo:
    gr.Markdown("# 📊 环比箭头柱状图 - 交互式数据可视化")
    gr.Markdown("---")
    
    current_data = gr.State(value=None)
    current_fig = gr.State(value=None)
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 1️⃣ 数据导入")
            
            file_input = gr.File(
                label="上传数据表文件",
                file_types=['text/csv', '.csv', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', '.xlsx', 'application/vnd.ms-excel', '.xls', 'text/plain', '.txt'],
                type="filepath"
            )
            
            chart_title = gr.Textbox(
                label="图表标题",
                value="环比箭头柱状图"
            )
            
            generate_btn = gr.Button(
                "🎨 生成图表",
                variant="primary",
                size="lg"
            )
            
            status_output = gr.Textbox(
                label="状态信息",
                lines=3,
                interactive=False
            )
        
        with gr.Column(scale=1):
            gr.Markdown("## 2️⃣ 颜色配置")
            
            color_container = gr.Column(visible=False)
            
            with color_container:
                color1 = gr.ColorPicker(label="区域1 颜色", value=DEFAULT_COLORS[0], visible=False)
                color2 = gr.ColorPicker(label="区域2 颜色", value=DEFAULT_COLORS[1], visible=False)
                color3 = gr.ColorPicker(label="区域3 颜色", value=DEFAULT_COLORS[2], visible=False)
                color4 = gr.ColorPicker(label="区域4 颜色", value=DEFAULT_COLORS[3], visible=False)
                color5 = gr.ColorPicker(label="区域5 颜色", value=DEFAULT_COLORS[4], visible=False)
                color6 = gr.ColorPicker(label="区域6 颜色", value=DEFAULT_COLORS[5], visible=False)
                color7 = gr.ColorPicker(label="区域7 颜色", value=DEFAULT_COLORS[6], visible=False)
                color8 = gr.ColorPicker(label="区域8 颜色", value=DEFAULT_COLORS[7], visible=False)
                
                update_colors_btn = gr.Button(
                    "🔄 应用颜色更新",
                    variant="secondary"
                )
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("## 3️⃣ 图表预览")
            
            plot_output = gr.Plot(label="图表")
            
            data_preview = gr.DataFrame(
                label="数据预览",
                interactive=False
            )
        
        with gr.Column(scale=1):
            gr.Markdown("## 4️⃣ 图片导出")
            
            dpi_option = gr.Dropdown(
                label="分辨率 (DPI)",
                choices=[150, 300, 600],
                value=300
            )
            
            format_option = gr.Dropdown(
                label="导出格式",
                choices=['PNG', 'JPG', 'PDF', 'SVG'],
                value='PNG'
            )
            
            export_btn = gr.Button(
                "⬇️ 开始导出",
                variant="primary"
            )
            
            export_progress = gr.Progress()
            
            export_status = gr.Textbox(
                label="导出状态",
                lines=2,
                interactive=False,
                value=""
            )
            
            download_output = gr.File(
                label="下载图片",
                visible=False
            )
    
    def handle_generate(file, title):
        """处理图表生成"""
        print("[调试] handle_generate 函数被调用")
        if file is None:
            print("[调试] 文件为 None")
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False),
                    "请先上传文件", None)
        
        df, message = read_file(file)
        
        if df is None:
            print(f"[调试] 读取文件失败: {message}")
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False),
                    message, None)
        
        is_valid, validate_msg = validate_data(df)
        
        if not is_valid:
            print(f"[调试] 数据验证失败: {validate_msg}")
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False),
                    f"{message}\n{validate_msg}", None)
        
        regions = df.columns[1:].tolist()
        colors = DEFAULT_COLORS[:len(regions)]
        print(f"[调试] 准备绘图: 区域数量={len(regions)}, 颜色数量={len(colors)}")
        
        try:
            fig = plot_stacked_bar_chart_with_arrow(df, colors, title)
            
            if fig is None:
                print("[调试] plot_stacked_bar_chart_with_arrow 返回 None")
                return (None, None, None, 
                        gr.update(visible=False), 
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                        gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                        gr.update(visible=False), gr.update(visible=False),
                        "绘图失败", None)
            
            print(f"[调试] 成功创建 figure 对象: {fig}")
            color_visibilities = [gr.update(visible=i < len(regions), label=f"{regions[i]} 颜色" if i < len(regions) else "") for i in range(8)]
            
            return (fig, fig, df, gr.update(visible=True),) + tuple(color_visibilities) + (f"{message}\n{validate_msg}", df,)
        except Exception as e:
            print(f"[调试] 生成图表失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return (None, None, None, 
                    gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False), gr.update(visible=False), 
                    gr.update(visible=False), gr.update(visible=False),
                    f"生成图表失败: {str(e)}", None)
    
    generate_btn.click(
        fn=handle_generate,
        inputs=[file_input, chart_title],
        outputs=[
            plot_output, current_fig, data_preview, color_container,
            color1, color2, color3, color4, color5, color6, color7, color8,
            status_output, current_data
        ]
    )
    
    def update_colors(df, title, c1, c2, c3, c4, c5, c6, c7, c8):
        """更新图表颜色"""
        print("[调试] update_colors 函数被调用")
        if df is None:
            print("[调试] df 为 None，返回错误")
            return None, None, "请先生成图表"
        
        regions = df.columns[1:].tolist()
        raw_colors = [c1, c2, c3, c4, c5, c6, c7, c8][:len(regions)]
        print(f"[调试] 原始颜色列表: {raw_colors}")
        
        colors = [rgba_to_hex(color) for color in raw_colors]
        print(f"[调试] 转换后的颜色列表: {colors}")
        print(f"[调试] 更新颜色: 区域数量={len(regions)}, 颜色数量={len(colors)}")
        
        try:
            fig = plot_stacked_bar_chart_with_arrow(df, colors, title)
            
            if fig is None:
                print("[调试] plot_stacked_bar_chart_with_arrow 返回 None")
                return None, None, "绘图失败"
            
            print(f"[调试] 成功创建新 figure 对象: {fig}")
            print("[调试] 颜色更新成功")
            return fig, fig, "颜色已更新"
        except Exception as e:
            print(f"[调试] 颜色更新失败: {str(e)}")
            import traceback
            traceback.print_exc()
            return None, None, f"颜色更新失败: {str(e)}"
    
    update_colors_btn.click(
        fn=update_colors,
        inputs=[current_data, chart_title, color1, color2, color3, color4, color5, color6, color7, color8],
        outputs=[plot_output, current_fig, status_output]
    )
    

    
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)
    
    def export_chart_sync(fig, dpi, fmt, progress_callback):
        """同步导出图表，由线程池调用"""
        total_start_time = time.perf_counter()
        logger.debug("[导出] 开始导出流程")
        
        try:
            # 阶段1: 准备参数 (15%)
            phase1_start = time.perf_counter()
            progress_callback(0.15, "准备导出参数...")
            logger.debug("[导出] 阶段1: 准备导出参数")
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"环比箭头柱状图_{timestamp}.{fmt.lower()}"
            
            temp_dir = os.path.join(os.getcwd(), "temp")
            os.makedirs(temp_dir, exist_ok=True)
            file_path = os.path.join(temp_dir, filename)
            fmt_lower = fmt.lower()
            
            save_kwargs = {
                'format': fmt_lower,
                'dpi': dpi
            }
            
            use_bbox = True
            if fmt_lower in ['svg', 'pdf']:
                use_bbox = False
            elif fmt_lower in ['jpg', 'jpeg']:
                save_kwargs['pil_kwargs'] = {'quality': 95}
            
            if use_bbox:
                save_kwargs['bbox_inches'] = 'tight'
                save_kwargs['pad_inches'] = 0.1
            
            phase1_time = (time.perf_counter() - phase1_start) * 1000
            logger.debug(f"[导出] 阶段1完成，耗时: {phase1_time:.2f} ms")
            
            # 阶段2: 保存图表 (70%)
            phase2_start = time.perf_counter()
            progress_callback(0.35, "保存图表到文件...")
            logger.debug("[导出] 阶段2: 保存图表到文件")
            
            fig.savefig(file_path, **save_kwargs)
            
            phase2_time = (time.perf_counter() - phase2_start) * 1000
            progress_callback(0.80, "图表保存完成，验证文件...")
            logger.debug(f"[导出] 阶段2完成，耗时: {phase2_time:.2f} ms")
            
            # 阶段3: 验证文件 (10%)
            phase3_start = time.perf_counter()
            progress_callback(0.85, "验证导出文件...")
            logger.debug("[导出] 阶段3: 验证文件")
            
            if not os.path.exists(file_path):
                raise FileNotFoundError("导出文件未创建成功")
            
            file_size = os.path.getsize(file_path)
            if file_size == 0:
                raise ValueError("导出文件为空")
            
            phase3_time = (time.perf_counter() - phase3_start) * 1000
            logger.debug(f"[导出] 阶段3完成，耗时: {phase3_time:.2f} ms")
            
            # 阶段4: 完成 (5%)
            progress_callback(1.0, "导出完成！")
            total_time = (time.perf_counter() - total_start_time) * 1000
            
            logger.info(f"[导出] 成功！文件: {filename}, 大小: {file_size/1024:.2f} KB, 总耗时: {total_time:.2f} ms")
            logger.debug(f"[导出] 性能明细 - 准备参数: {phase1_time:.2f} ms, 保存: {phase2_time:.2f} ms, 验证: {phase3_time:.2f} ms")
            
            return file_path, None
            
        except Exception as e:
            logger.error(f"[导出] 失败: {str(e)}", exc_info=True)
            return None, str(e)
    
    async def export_chart_async(fig, dpi, fmt, progress=gr.Progress()):
        """异步导出图表函数"""
        if fig is None:
            logger.warning("[导出] fig为None，无法导出")
            return "请先生成图表", gr.update(visible=False)
        
        logger.info(f"[导出] 收到导出请求 - DPI={dpi}, 格式={fmt}")
        
        # 定义进度回调
        def progress_fn(p, desc):
            progress(p, desc=desc)
        
        # 在线程池中执行同步导出任务
        loop = asyncio.get_event_loop()
        file_path, error_msg = await loop.run_in_executor(
            executor,
            export_chart_sync,
            fig,
            dpi,
            fmt,
            progress_fn
        )
        
        if error_msg:
            logger.error(f"[导出] 最终失败: {error_msg}")
            return f"导出失败: {error_msg}", gr.update(visible=False)
        
        logger.info(f"[导出] 最终完成 - 文件路径: {file_path}")
        return "导出成功！", gr.update(value=file_path, visible=True)
    
    export_btn.click(
        fn=export_chart_async,
        inputs=[current_fig, dpi_option, format_option],
        outputs=[export_status, download_output]
    )
    
    gr.Markdown("---")
    gr.Markdown("""
    <div style='text-align: center; color: #666;'>
        <p>💡 提示: 支持CSV、Excel(.xlsx, .xls)和文本文件(.txt)格式</p>
        <p>📊 数据格式要求: 第一列为年份，后续各列为区域数据</p>
    </div>
    """)


if __name__ == "__main__":
    import os
    os.environ["GRADIO_ANALYTICS_ENABLED"] = "False"
    os.environ["HF_HUB_DISABLE_SYMLINKS_WARNING"] = "1"
    os.environ["HF_TOKEN"] = ""
    logger.info("[启动] 初始化 Gradio 应用，禁用网络请求")
    demo.queue(max_size=10)
    logger.info("[启动] 队列系统已就绪，准备启动服务器")
    demo.launch(share=False, server_name="127.0.0.1", server_port=7862, quiet=True)
