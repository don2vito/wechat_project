# 导入系统模块，用于处理命令行参数和程序退出
import sys
# 导入操作系统模块，用于文件路径处理、系统类型判断
import os

# 导入PyQt5的UI组件：应用程序、主窗口、基础部件、布局管理器等
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QSplitter,
    QFrame, QSizePolicy  # QSizePolicy用于设置部件的大小策略
)
# 导入PyQt5核心模块：Qt枚举（布局方向等）、QSize（尺寸）
from PyQt5.QtCore import Qt, QSize
# 导入PyQt5图形模块：字体、图标
from PyQt5.QtGui import QFont, QIcon

# 导入matplotlib相关模块，用于在PyQt5中嵌入绘图
import matplotlib
# 设置matplotlib的后端为Qt5Agg，适配PyQt5
matplotlib.use('Qt5Agg')
# 导入matplotlib的Qt5画布组件（核心：将matplotlib图表嵌入PyQt）
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# 导入matplotlib的Qt5导航工具栏（提供缩放、保存等绘图工具）
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
# 导入matplotlib.pyplot用于绘图
import matplotlib.pyplot as plt
# 导入pandas用于数据读取和处理（CSV/Excel）
import pandas as pd
# 导入numpy用于数值计算（数组、数学运算）
import numpy as np


def set_chinese_font():
    """
    配置matplotlib的中文字体（解决中文乱码问题）
    不同操作系统（Windows/macOS/Linux）适配不同的中文字体
    """
    # 获取当前操作系统类型：nt=Windows，posix=macOS/Linux
    system_name = os.name
    
    # 按系统定义候选中文字体列表（优先级从高到低）
    if system_name == 'nt':  # Windows系统
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']  # 黑体、微软雅黑、宋体
    elif system_name == 'posix':  # macOS/Linux系统
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS', 'WenQuanYi Micro Hei']  # 华文黑体、苹果丽黑、文泉驿微米黑
    else:  # 其他系统（兜底）
        font_names = ['DejaVu Sans']  # 通用无衬线字体
    
    # 遍历字体列表，尝试设置可用字体（避免字体不存在报错）
    for font_name in font_names:
        try:
            # 设置matplotlib的默认字体为中文字体
            plt.rcParams['font.sans-serif'] = [font_name]
            # 解决负号（-）显示为方块的问题
            plt.rcParams['axes.unicode_minus'] = False
            return  # 找到可用字体后立即退出
        except:
            continue  # 字体不可用则尝试下一个
    
    # 所有候选字体都失败时，使用默认字体兜底
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


class MatplotlibCanvas(FigureCanvas):
    """
    自定义Matplotlib画布类（继承FigureCanvas）
    作用：将matplotlib的Figure封装为PyQt5可识别的部件，嵌入UI中
    """
    def __init__(self, parent=None):
        # 创建matplotlib的Figure和Axes（绘图核心对象）
        # figsize：画布尺寸（宽12，高10），dpi：分辨率（100）
        self.fig, self.ax = plt.subplots(figsize=(12, 10), dpi=100)
        # 调用父类构造函数，传入Figure对象
        super().__init__(self.fig)
        # 设置画布的父部件（关联PyQt的UI层级）
        self.setParent(parent)
        # 设置画布的大小策略：水平/垂直方向都自动扩展（适配窗口缩放）
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class MainWindow(QMainWindow):
    """
    主窗口类（继承QMainWindow）
    整个应用的核心UI和业务逻辑都封装在此类中
    """
    def __init__(self):
        # 调用父类构造函数
        super().__init__()
        # 初始化属性：存储当前加载的数据（DataFrame）
        self.current_data = None
        # 初始化属性：存储当前生成的matplotlib图表对象
        self.current_fig = None
        
        # 设置中文字体（解决绘图中文乱码）
        set_chinese_font()
        # 初始化UI界面
        self.init_ui()
        
    def init_ui(self):
        """初始化主窗口的UI布局和部件"""
        # 设置窗口标题
        self.setWindowTitle('环比箭头柱状图 - PyQt5版')
        # 设置窗口最小尺寸（避免窗口过小导致UI错乱）
        self.setMinimumSize(1200, 900)
        
        # 创建中心部件（QMainWindow必须设置centralWidget）
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # 创建垂直布局（主布局），用于承载顶部面板、图表区域、底部面板
        main_layout = QVBoxLayout(central_widget)
        # 设置布局的内边距（上、右、下、左）
        main_layout.setContentsMargins(20, 20, 20, 20)
        # 设置布局内部件的间距
        main_layout.setSpacing(15)
        
        # 添加顶部面板（标题+导入按钮）
        main_layout.addWidget(self.create_top_panel())
        # 添加图表区域（占主要空间，stretch=1表示自动填充剩余空间）
        main_layout.addWidget(self.create_chart_area(), stretch=1)
        # 添加底部面板（状态提示+导出按钮）
        main_layout.addWidget(self.create_bottom_panel())
        
        # 显示欢迎界面
        self.show_welcome_message()
        
    def create_top_panel(self):
        """创建顶部面板：包含标题和导入数据按钮"""
        # 创建QFrame作为面板容器（方便设置样式）
        panel = QFrame()
        # 设置面板样式：背景色、圆角、内边距
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;  /* 浅灰色背景 */
                border-radius: 8px;         /* 圆角8px */
                padding: 10px;              /* 内边距 */
            }
        """)
        
        # 创建水平布局（标题居左，按钮居右）
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)  # 布局内边距
        layout.setSpacing(10)  # 布局内部件间距
        
        # 创建标题标签
        title_label = QLabel('📊 环比箭头柱状图生成器')
        # 设置标题字体
        title_font = QFont()
        title_font.setPointSize(16)  # 字体大小16
        title_font.setBold(True)     # 加粗
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        # 添加伸缩项（将按钮推到右侧）
        layout.addStretch()
        
        # 创建导入数据按钮
        import_btn = QPushButton('📂 导入数据文件')
        import_btn.setMinimumSize(160, 40)  # 按钮最小尺寸
        # 设置按钮样式（正常/悬浮/按下状态）
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;  /* 蓝色背景 */
                color: white;               /* 白色文字 */
                border: none;               /* 无边框 */
                border-radius: 6px;         /* 圆角6px */
                font-size: 14px;            /* 字体大小14 */
                font-weight: bold;          /* 加粗 */
                padding: 8px 20px;          /* 内边距 */
            }
            QPushButton:hover {            /* 鼠标悬浮状态 */
                background-color: #2980b9;  /* 深一点的蓝色 */
            }
            QPushButton:pressed {          /* 鼠标按下状态 */
                background-color: #21618c;  /* 更深的蓝色 */
            }
        """)
        # 绑定按钮点击事件：点击后调用import_data方法
        import_btn.clicked.connect(self.import_data)
        layout.addWidget(import_btn)
        
        return panel
        
    def create_chart_area(self):
        """创建图表显示区域：包含matplotlib画布和导航工具栏"""
        # 创建水平分割器（可扩展：后续可添加侧边栏）
        splitter = QSplitter(Qt.Horizontal)
        
        # 创建自定义matplotlib画布
        self.canvas = MatplotlibCanvas()
        # 创建matplotlib导航工具栏（绑定到画布和主窗口）
        self.toolbar = NavigationToolbar(self.canvas, self)
        # 设置工具栏样式（无边框、浅灰色背景）
        self.toolbar.setStyleSheet("QToolBar { border: none; background-color: #f8f9fa; }")
        
        # 创建图表容器（Frame）
        chart_container = QFrame()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)  # 去除容器内边距
        chart_layout.addWidget(self.toolbar)  # 添加工具栏
        chart_layout.addWidget(self.canvas)   # 添加画布
        
        # 将图表容器添加到分割器
        splitter.addWidget(chart_container)
        
        return splitter
        
    def create_bottom_panel(self):
        """创建底部面板：包含状态提示和导出按钮"""
        # 创建面板容器
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        # 创建水平布局
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        # 创建状态提示标签（显示加载状态/提示信息）
        self.status_label = QLabel('💡 请点击"导入数据文件"按钮开始')
        self.status_label.setStyleSheet("color: #666; font-size: 13px;")
        layout.addWidget(self.status_label)
        
        # 伸缩项（将导出按钮推到右侧）
        layout.addStretch()
        
        # 创建导出PNG按钮
        export_png_btn = QPushButton('📥 导出 PNG')
        export_png_btn.setMinimumSize(120, 36)
        export_png_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;  /* 绿色背景 */
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
            QPushButton:pressed {
                background-color: #1e8449;
            }
            QPushButton:disabled {         /* 禁用状态 */
                background-color: #bdc3c7;  /* 灰色 */
            }
        """)
        # 绑定点击事件：调用export_chart方法，参数为'PNG'
        export_png_btn.clicked.connect(lambda: self.export_chart('PNG'))
        # 初始状态禁用（未生成图表时不可点击）
        export_png_btn.setEnabled(False)
        # 保存按钮引用（后续启用/禁用）
        self.export_png_btn = export_png_btn
        layout.addWidget(export_png_btn)
        
        # 创建导出PDF按钮（逻辑同PNG按钮）
        export_pdf_btn = QPushButton('📥 导出 PDF')
        export_pdf_btn.setMinimumSize(120, 36)
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;  /* 紫色背景 */
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #8e44ad;
            }
            QPushButton:pressed {
                background-color: #6c3483;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        export_pdf_btn.clicked.connect(lambda: self.export_chart('PDF'))
        export_pdf_btn.setEnabled(False)
        self.export_pdf_btn = export_pdf_btn
        layout.addWidget(export_pdf_btn)
        
        return panel
        
    def show_welcome_message(self):
        """显示欢迎界面（未导入数据时的提示）"""
        # 清空画布的轴（避免残留之前的绘图）
        self.canvas.ax.clear()
        # 在画布中心添加提示文本
        self.canvas.ax.text(
            0.5, 0.5,  # 文本位置（相对坐标：0-1）
            '欢迎使用环比箭头柱状图生成器\n\n请点击顶部的"导入数据文件"按钮\n选择CSV或Excel文件开始',
            ha='center', va='center',  # 水平/垂直居中
            fontsize=16, color='#666'  # 字体大小、颜色
        )
        # 隐藏坐标轴（仅显示文本）
        self.canvas.ax.axis('off')
        # 刷新画布（显示文本）
        self.canvas.draw()
        
    def import_data(self):
        """导入数据文件：CSV/Excel，校验数据格式，调用绘图方法"""
        # 打开文件选择对话框，选择数据文件
        file_path, _ = QFileDialog.getOpenFileName(
            self,                          # 父窗口
            '选择数据文件',                # 对话框标题
            '',                            # 默认路径（当前目录）
            # 文件类型过滤：支持CSV/Excel
            '数据文件 (*.csv *.xlsx *.xls);;CSV文件 (*.csv);;Excel文件 (*.xlsx *.xls);;所有文件 (*.*)'
        )
        
        # 如果用户取消选择，直接返回
        if not file_path:
            return
            
        try:
            # 获取文件扩展名（小写）
            file_ext = os.path.splitext(file_path)[1].lower()
            
            # 根据扩展名读取文件
            if file_ext == '.csv':
                df = pd.read_csv(file_path)  # 读取CSV
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)  # 读取Excel
            else:
                # 不支持的格式，弹出警告
                QMessageBox.warning(self, '警告', '不支持的文件格式')
                return
                
            # 数据校验1：至少2行（需要2年数据才能计算环比）
            if len(df) < 2:
                QMessageBox.warning(self, '警告', '数据至少需要2行（2年的数据）')
                return
                
            # 数据校验2：至少2列（年份列 + 1个数据列）
            if len(df.columns) < 2:
                QMessageBox.warning(self, '警告', '数据至少需要2列（年份列 + 1个数据列）')
                return
                
            # 保存当前数据（DataFrame）
            self.current_data = df
            # 更新状态提示（显示文件名和数据维度）
            self.status_label.setText(f'✅ 已加载: {os.path.basename(file_path)} ({len(df)} 行 × {len(df.columns)} 列)')
            self.status_label.setStyleSheet('color: #27ae60; font-size: 13px; font-weight: bold;')
            
            # 调用绘图方法生成图表
            self.plot_chart(df)
            # 启用导出按钮（图表生成后可导出）
            self.export_png_btn.setEnabled(True)
            self.export_pdf_btn.setEnabled(True)
            
        except Exception as e:
            # 捕获所有异常，弹出错误提示
            QMessageBox.critical(self, '错误', f'加载文件失败: {str(e)}')
            
    def plot_chart(self, df):
        """
        核心绘图方法：根据导入的数据生成环比箭头柱状图
        步骤：解析数据 → 绘制堆叠柱状图 → 添加数值标签 → 计算环比增长率 → 绘制箭头和增长率标签 → 样式美化
        """
        try:
            # 清空画布（避免残留）
            self.canvas.ax.clear()
            
            # 解析数据：
            # 第1列作为年份（转为字符串）
            years = df.iloc[:, 0].astype(str).tolist()
            # 第2列及以后作为区域/类别名称
            regions = df.columns[1:].tolist()
            # 第2列及以后的数值数据（二维数组）
            data = df.iloc[:, 1:].values
            
            # 定义柱状图颜色列表（循环使用以适配多类别）
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
            # 扩展颜色列表以匹配类别数量（避免颜色不足）
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
            
            # 生成x轴坐标（年份的位置）
            x = np.arange(len(years))
            # 柱状图宽度
            bar_width = 0.55
            
            # 绘制堆叠柱状图：
            # bottom用于控制每一层的起始高度（初始为0）
            bottom = np.zeros(len(years))
            for i in range(len(regions)):
                # 绘制当前类别的堆叠柱
                bars = self.canvas.ax.bar(
                    x, data[:, i], bar_width, bottom=bottom,
                    color=colors[i], label=regions[i]  # 颜色和图例标签
                )
                
                # 为每个柱子添加数值标签（居中显示）
                for bar, b, val in zip(bars, bottom, data[:, i]):
                    height = bar.get_height()
                    if height > 0:  # 仅显示非零值
                        self.canvas.ax.text(
                            bar.get_x() + bar.get_width() / 2,  # x坐标：柱子中心
                            b + height / 2,                     # y坐标：柱子垂直中心
                            f'{int(val):,}',                    # 数值（千分位分隔）
                            ha='center', va='center',            # 居中对齐
                            fontsize=11, color='white', fontweight='semibold'  # 样式
                        )
                
                # 更新下一层的起始高度
                bottom += data[:, i]
            
            # 计算每年的总计值（所有类别求和）
            totals = np.sum(data, axis=1)
            # 为每年的总计添加数值标签（显示在柱子顶部）
            for i, total in enumerate(totals):
                self.canvas.ax.text(
                    x[i], total + max(totals) * 0.02,  # 略高于柱子顶部
                    f'{int(total):,}',
                    ha='center', va='bottom',
                    fontsize=13, fontweight='bold', color='#333333'
                )
            
            # 绘制环比箭头和增长率（至少2年数据才绘制）
            if len(years) > 1:
                # 计算环比增长率：(本年-上年)/上年 * 100
                growth = ((totals[1:] - totals[:-1]) / totals[:-1]) * 100
                num_arrows = len(growth)  # 箭头数量（年份数-1）
                
                # 计算箭头样式参数（基于数据最大值适配）
                max_total = np.max(totals)
                BASE_OFFSET_Y = max_total * 0.05       # 箭头起始点y偏移
                VERTICAL_RISE_FACTOR = 0.15            # 箭头峰值高度系数
                ARROW_HEAD_WIDTH = 0.06                # 箭头头部宽度
                ARROW_HEAD_LENGTH = max_total * 0.02   # 箭头头部长度
                LINE_WIDTH = 1.5                       # 箭头线宽
                ENDPOINT_SPACING = 0.15                # 箭头端点与柱子的间距
                
                base_offset = max_total * VERTICAL_RISE_FACTOR  # 箭头峰值偏移
                
                # 遍历每个环比周期，绘制箭头和增长率标签
                for i in range(num_arrows):
                    # 箭头起始点（上年柱子右侧）
                    start_x = x[i] + ENDPOINT_SPACING
                    start_y = totals[i] + BASE_OFFSET_Y
                    # 箭头结束点（本年柱子左侧）
                    end_x = x[i + 1] - ENDPOINT_SPACING
                    end_y = totals[i + 1] + BASE_OFFSET_Y
                    # 箭头峰值y坐标（取起始/结束点的最大值 + 偏移）
                    base_peak_y = max(start_y, end_y)
                    peak_y = base_peak_y + base_offset
                    
                    # 箭头的两个中间点（形成弧形顶部）
                    mid1_x, mid1_y = start_x, peak_y
                    mid2_x, mid2_y = end_x, peak_y
                    
                    # 绘制箭头的线条（折线）
                    self.canvas.ax.plot(
                        [start_x, mid1_x, mid2_x, end_x],  # x坐标序列
                        [start_y, mid1_y, mid2_y, end_y],  # y坐标序列
                        color='#333333', linewidth=LINE_WIDTH,
                        zorder=3, solid_capstyle='round'  # zorder控制层级（在柱子上方）
                    )
                    
                    # 绘制箭头头部
                    arrow_start_x, arrow_start_y = mid2_x, mid2_y
                    arrow_end_y = end_y
                    arrow_length = arrow_end_y - arrow_start_y
                    
                    self.canvas.ax.arrow(
                        arrow_start_x, arrow_start_y, 0,  # 箭头起始点，x方向无偏移
                        arrow_length - ARROW_HEAD_LENGTH,  # 箭头长度（扣除头部）
                        head_width=ARROW_HEAD_WIDTH,       # 箭头头部宽度
                        head_length=ARROW_HEAD_LENGTH,     # 箭头头部长度
                        fc='#333333', ec='#333333',        # 填充色/边框色
                        length_includes_head=True, zorder=3  # 长度包含头部，层级置顶
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
                    
                    # 标签背景样式（圆形）
                    bbox = dict(
                        boxstyle="circle,pad=0.4",  # 圆形，内边距0.4
                        facecolor='#2c3e50',        # 深色背景
                        edgecolor='none', alpha=1.0  # 无边框，不透明
                    )
                    
                    # 添加增长率文本
                    self.canvas.ax.text(
                        label_x, label_y, rate_text,
                        ha='center', va='center',
                        color='white', fontsize=12,
                        fontweight='bold', bbox=bbox, zorder=4  # 层级高于箭头
                    )
            
            # 设置x轴刻度和标签（年份）
            self.canvas.ax.set_xticks(x)
            self.canvas.ax.set_xticklabels(years, fontsize=13)
            # 隐藏y轴刻度（仅显示数值标签，不显示刻度线）
            self.canvas.ax.set_yticks([])
            # 设置图表标题
            self.canvas.ax.set_title('环比箭头柱状图', fontsize=18, pad=20, fontweight='bold')
            
            # 美化图表：隐藏顶部、右侧、左侧边框
            self.canvas.ax.spines['top'].set_visible(False)
            self.canvas.ax.spines['right'].set_visible(False)
            self.canvas.ax.spines['left'].set_visible(False)
            
            # 设置图例（类别说明）
            self.canvas.ax.legend(
                loc='upper center',                # 位置：上中
                bbox_to_anchor=(0.5, 1.12),        # 锚点（微调位置）
                ncol=min(4, len(regions)),         # 列数（最多4列）
                frameon=False,                     # 无边框
                fontsize=11                        # 字体大小
            )
            
            # 自动调整布局（避免标签重叠）
            self.canvas.fig.tight_layout()
            # 刷新画布（显示图表）
            self.canvas.draw()
            # 保存当前图表对象（用于导出）
            self.current_fig = self.canvas.fig
            
        except Exception as e:
            # 绘图异常提示
            QMessageBox.critical(self, '错误', f'绘图失败: {str(e)}')
            
    def export_chart(self, format_type):
        """
        导出图表为指定格式（PNG/PDF）
        :param format_type: 导出格式（'PNG' 或 'PDF'）
        """
        # 校验：未生成图表则提示
        if self.current_fig is None:
            QMessageBox.warning(self, '警告', '请先生成图表')
            return
            
        try:
            # 生成带时间戳的默认文件名（避免重复）
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            default_name = f'环比箭头柱状图_{timestamp}.{format_type.lower()}'
            
            # 打开保存文件对话框
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f'导出 {format_type} 文件',  # 对话框标题
                default_name,                # 默认文件名
                f'{format_type} 文件 (*.{format_type.lower()})'  # 文件类型过滤
            )
            
            # 用户取消保存则返回
            if not file_path:
                return
                
            # 保存图表
            self.current_fig.savefig(
                file_path,
                dpi=300,               # 分辨率300（高清）
                bbox_inches='tight'    # 紧凑布局（去除多余空白）
            )
            
            # 导出成功提示
            QMessageBox.information(self, '成功', f'图表已成功导出: {file_path}')
            
        except Exception as e:
            # 导出异常提示
            QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')


def main():
    """程序入口函数"""
    # 创建QApplication实例（PyQt5必须）
    app = QApplication(sys.argv)
    
    # 设置应用样式为Fusion（跨平台统一样式）
    app.setStyle('Fusion')
    
    # 创建主窗口实例
    window = MainWindow()
    # 显示主窗口
    window.show()
    
    # 运行应用事件循环，程序退出时返回状态码
    sys.exit(app.exec_())


# 程序入口（仅当直接运行该脚本时执行）
if __name__ == '__main__':
    main()
