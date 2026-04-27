import sys
import os
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFileDialog, QMessageBox, QSplitter,
    QFrame, QSizePolicy
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def set_chinese_font():
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
            return
        except:
            continue
    
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


class MatplotlibCanvas(FigureCanvas):
    def __init__(self, parent=None):
        self.fig, self.ax = plt.subplots(figsize=(12, 10), dpi=100)
        super().__init__(self.fig)
        self.setParent(parent)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.current_data = None
        self.current_fig = None
        
        set_chinese_font()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle('环比箭头柱状图 - PyQt5版')
        self.setMinimumSize(1200, 900)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        main_layout.addWidget(self.create_top_panel())
        main_layout.addWidget(self.create_chart_area(), stretch=1)
        main_layout.addWidget(self.create_bottom_panel())
        
        self.show_welcome_message()
        
    def create_top_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        title_label = QLabel('📊 环比箭头柱状图生成器')
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title_label.setFont(title_font)
        layout.addWidget(title_label)
        
        layout.addStretch()
        
        import_btn = QPushButton('📂 导入数据文件')
        import_btn.setMinimumSize(160, 40)
        import_btn.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                padding: 8px 20px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #21618c;
            }
        """)
        import_btn.clicked.connect(self.import_data)
        layout.addWidget(import_btn)
        
        return panel
        
    def create_chart_area(self):
        splitter = QSplitter(Qt.Horizontal)
        
        self.canvas = MatplotlibCanvas()
        self.toolbar = NavigationToolbar(self.canvas, self)
        self.toolbar.setStyleSheet("QToolBar { border: none; background-color: #f8f9fa; }")
        
        chart_container = QFrame()
        chart_layout = QVBoxLayout(chart_container)
        chart_layout.setContentsMargins(0, 0, 0, 0)
        chart_layout.addWidget(self.toolbar)
        chart_layout.addWidget(self.canvas)
        
        splitter.addWidget(chart_container)
        
        return splitter
        
    def create_bottom_panel(self):
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        
        layout = QHBoxLayout(panel)
        layout.setContentsMargins(15, 10, 15, 10)
        layout.setSpacing(10)
        
        self.status_label = QLabel('💡 请点击"导入数据文件"按钮开始')
        self.status_label.setStyleSheet("color: #666; font-size: 13px;")
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        
        export_png_btn = QPushButton('📥 导出 PNG')
        export_png_btn.setMinimumSize(120, 36)
        export_png_btn.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
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
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)
        export_png_btn.clicked.connect(lambda: self.export_chart('PNG'))
        export_png_btn.setEnabled(False)
        self.export_png_btn = export_png_btn
        layout.addWidget(export_png_btn)
        
        export_pdf_btn = QPushButton('📥 导出 PDF')
        export_pdf_btn.setMinimumSize(120, 36)
        export_pdf_btn.setStyleSheet("""
            QPushButton {
                background-color: #9b59b6;
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
        self.canvas.ax.clear()
        self.canvas.ax.text(
            0.5, 0.5,
            '欢迎使用环比箭头柱状图生成器\n\n请点击顶部的"导入数据文件"按钮\n选择CSV或Excel文件开始',
            ha='center', va='center',
            fontsize=16, color='#666'
        )
        self.canvas.ax.axis('off')
        self.canvas.draw()
        
    def import_data(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            '选择数据文件',
            '',
            '数据文件 (*.csv *.xlsx *.xls);;CSV文件 (*.csv);;Excel文件 (*.xlsx *.xls);;所有文件 (*.*)'
        )
        
        if not file_path:
            return
            
        try:
            file_ext = os.path.splitext(file_path)[1].lower()
            
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
            elif file_ext in ['.xlsx', '.xls']:
                df = pd.read_excel(file_path)
            else:
                QMessageBox.warning(self, '警告', '不支持的文件格式')
                return
                
            if len(df) < 2:
                QMessageBox.warning(self, '警告', '数据至少需要2行（2年的数据）')
                return
                
            if len(df.columns) < 2:
                QMessageBox.warning(self, '警告', '数据至少需要2列（年份列 + 1个数据列）')
                return
                
            self.current_data = df
            self.status_label.setText(f'✅ 已加载: {os.path.basename(file_path)} ({len(df)} 行 × {len(df.columns)} 列)')
            self.status_label.setStyleSheet('color: #27ae60; font-size: 13px; font-weight: bold;')
            
            self.plot_chart(df)
            self.export_png_btn.setEnabled(True)
            self.export_pdf_btn.setEnabled(True)
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'加载文件失败: {str(e)}')
            
    def plot_chart(self, df):
        try:
            self.canvas.ax.clear()
            
            years = df.iloc[:, 0].astype(str).tolist()
            regions = df.columns[1:].tolist()
            data = df.iloc[:, 1:].values
            
            colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6', '#1abc9c']
            colors = (colors * ((len(regions) // len(colors)) + 1))[:len(regions)]
            
            x = np.arange(len(years))
            bar_width = 0.55
            
            bottom = np.zeros(len(years))
            for i in range(len(regions)):
                bars = self.canvas.ax.bar(
                    x, data[:, i], bar_width, bottom=bottom,
                    color=colors[i], label=regions[i]
                )
                
                for bar, b, val in zip(bars, bottom, data[:, i]):
                    height = bar.get_height()
                    if height > 0:
                        self.canvas.ax.text(
                            bar.get_x() + bar.get_width() / 2,
                            b + height / 2,
                            f'{int(val):,}',
                            ha='center', va='center',
                            fontsize=11, color='white', fontweight='semibold'
                        )
                
                bottom += data[:, i]
            
            totals = np.sum(data, axis=1)
            for i, total in enumerate(totals):
                self.canvas.ax.text(
                    x[i], total + max(totals) * 0.02,
                    f'{int(total):,}',
                    ha='center', va='bottom',
                    fontsize=13, fontweight='bold', color='#333333'
                )
            
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
                    
                    self.canvas.ax.plot(
                        [start_x, mid1_x, mid2_x, end_x],
                        [start_y, mid1_y, mid2_y, end_y],
                        color='#333333', linewidth=LINE_WIDTH,
                        zorder=3, solid_capstyle='round'
                    )
                    
                    arrow_start_x, arrow_start_y = mid2_x, mid2_y
                    arrow_end_y = end_y
                    arrow_length = arrow_end_y - arrow_start_y
                    
                    self.canvas.ax.arrow(
                        arrow_start_x, arrow_start_y, 0,
                        arrow_length - ARROW_HEAD_LENGTH,
                        head_width=ARROW_HEAD_WIDTH,
                        head_length=ARROW_HEAD_LENGTH,
                        fc='#333333', ec='#333333',
                        length_includes_head=True, zorder=3
                    )
                    
                    label_x = (start_x + end_x) / 2
                    label_y = peak_y
                    
                    growth_value = growth[i]
                    if growth_value >= 0:
                        rate_text = f'+{int(round(growth_value))}%'
                    else:
                        rate_text = f'{int(round(growth_value))}%'
                    
                    bbox = dict(
                        boxstyle="circle,pad=0.4",
                        facecolor='#2c3e50',
                        edgecolor='none', alpha=1.0
                    )
                    
                    self.canvas.ax.text(
                        label_x, label_y, rate_text,
                        ha='center', va='center',
                        color='white', fontsize=12,
                        fontweight='bold', bbox=bbox, zorder=4
                    )
            
            self.canvas.ax.set_xticks(x)
            self.canvas.ax.set_xticklabels(years, fontsize=13)
            self.canvas.ax.set_yticks([])
            self.canvas.ax.set_title('环比箭头柱状图', fontsize=18, pad=20, fontweight='bold')
            
            self.canvas.ax.spines['top'].set_visible(False)
            self.canvas.ax.spines['right'].set_visible(False)
            self.canvas.ax.spines['left'].set_visible(False)
            
            self.canvas.ax.legend(
                loc='upper center',
                bbox_to_anchor=(0.5, 1.12),
                ncol=min(4, len(regions)),
                frameon=False,
                fontsize=11
            )
            
            self.canvas.fig.tight_layout()
            self.canvas.draw()
            self.current_fig = self.canvas.fig
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'绘图失败: {str(e)}')
            
    def export_chart(self, format_type):
        if self.current_fig is None:
            QMessageBox.warning(self, '警告', '请先生成图表')
            return
            
        try:
            timestamp = pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')
            default_name = f'环比箭头柱状图_{timestamp}.{format_type.lower()}'
            
            file_path, _ = QFileDialog.getSaveFileName(
                self,
                f'导出 {format_type} 文件',
                default_name,
                f'{format_type} 文件 (*.{format_type.lower()})'
            )
            
            if not file_path:
                return
                
            self.current_fig.savefig(
                file_path,
                dpi=300,
                bbox_inches='tight'
            )
            
            QMessageBox.information(self, '成功', f'图表已成功导出: {file_path}')
            
        except Exception as e:
            QMessageBox.critical(self, '错误', f'导出失败: {str(e)}')


def main():
    app = QApplication(sys.argv)
    
    app.setStyle('Fusion')
    
    window = MainWindow()
    window.show()
    
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
