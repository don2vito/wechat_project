#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
环比箭头柱状图生成器（带详细学习注释版）

模块功能说明:
    本模块是一个专业的商业数据可视化工具，使用 Python 和 Matplotlib 生成高质量的带环比箭头的堆叠柱状图。
    主要功能包括：
    1. 生成堆叠柱状图展示不同年份各区域的数据
    2. 在柱状图上标注各区域的具体数值
    3. 在柱状图顶部标注每年的总数值
    4. 在年份之间绘制直角样式的环比增长率箭头
    5. 在箭头上方标注环比增长率百分比
    6. 支持自定义配置（图表尺寸、颜色、字体大小等）
    7. 新增完善的 DataProcessor 类，提供 CSV/Excel 读取、缺失值处理、异常值检测等高级功能

算法实现原理:
    1. 堆叠柱状图绘制：
       - 使用 matplotlib 的 bar() 函数，通过 bottom 参数实现堆叠效果
       - 从底部开始逐层绘制各区域的柱状图
       - 每个区域的底部位置 = 之前所有区域高度之和

    2. 数据标签添加：
       - 在每个柱状图分段中心位置添加数值标签
       - 使用 text() 函数定位到分段高度的中点
       - 确保标签在柱状图分段内部

    3. 环比增长率计算：
       - 环比增长率 = (本期值 - 上期值) / 上期值 × 100%
       - 使用 numpy 数组运算高效计算增长率
       - 支持多个年份连续计算

    4. 直角箭头绘制：
       - 采用三段折线绘制直角箭头
       - 从第一年柱状图顶部向上垂直上升到峰值
       - 水平移动到第二年柱状图上方
       - 垂直下降到第二年柱状图顶部
       - 在终点位置添加箭头指示方向

    5. 增长率标签放置：
       - 在箭头水平段的中点位置添加圆形背景的增长率标签
       - 使用 bbox 参数创建圆形背景
       - 根据增长率正负自动调整显示符号

使用方法:
    1. 直接运行脚本，将使用示例数据生成图表
    2. 修改 main() 函数中的数据，生成自定义图表
    3. 使用 DataProcessor 类进行高级数据处理

如何更新数据:
    在 main() 函数中找到以下部分并修改：
    
    1. years: 修改年份标签列表，例如: years = ['2023', '2024', '2025', '2026']
    2. regions: 修改区域名称列表，例如: regions = ['区域A', '区域B', '区域C']
    3. colors: 修改对应区域的颜色列表，数量需与 regions 一致
    4. data: 修改数据二维列表，格式为 [年份数, 区域数]
       例如: data = [
                   [区域1数据, 区域2数据, 区域3数据],  # 第1年
                   [区域1数据, 区域2数据, 区域3数据],  # 第2年
                   ...
               ]
    
参数说明:
    data: 二维列表或数组，形状为 [年份数, 区域数]
    years: 年份标签列表
    regions: 区域名称列表
    colors: 每个区域的颜色列表
    config: 可选的配置字典，用于覆盖默认配置项:
        - figsize: 图表尺寸，默认为 (10, 8)
        - bar_width: 柱状图宽度，默认为 0.55
        - dpi: 输出图片分辨率，默认为 150
        - output_path: 输出图片路径
        - title_fontsize: 标题字体大小
        - data_label_fontsize: 数据标签字体大小
        - percentage_fontsize: 增长率标签字体大小
        - arrow_color: 箭头颜色，默认为 '#333333'
        - percentage_background: 增长率标签背景色，默认为 '#2c3e50'

使用注意事项:
    1. 数据格式要求：
       - 数据必须是二维结构，第一维是年份，第二维是区域
       - 至少需要2年的数据才能计算环比增长率
       - 数据值应为非负数

    2. 颜色配置要求：
       - 颜色数量必须与区域数量一致
       - 建议使用对比度较高的颜色组合以提高可读性

    3. 字体要求：
       - Windows系统默认使用微软雅黑或黑体
       - macOS系统默认使用黑体
       - Linux系统默认使用文泉驿微米黑
       - 如需其他字体请修改 set_chinese_font() 函数

    4. 输出文件：
       - 输出路径会自动创建父目录
       - 支持多种图片格式（PNG、JPG等）
       - 建议使用 PNG 格式以保证最佳显示效果

    5. 性能建议：
       - 对于大量数据建议适当调整 figsize 和 dpi
       - 调整 bar_width 以适应年份数量
       - 垂直偏移量会根据数据最大值自动调整

运行要求:
    - Python 3.7+
    - matplotlib
    - numpy
    - pandas

示例:
    运行脚本后，图表将保存在指定的 output_path 路径。
"""

# ==================== 导入必要的库 ====================
# matplotlib.pyplot: Matplotlib的核心绘图模块，提供类似MATLAB的绘图接口
# 学习点：plt是matplotlib最常用的别名，所有绘图操作都基于这个模块
import matplotlib.pyplot as plt

# numpy: 高效的数值计算库，提供数组操作和数学函数
# 学习点：np是numpy的标准别名，相比Python原生列表，numpy数组运算速度快10-100倍
import numpy as np

# pandas: 强大的数据处理库，提供DataFrame数据结构和文件读写功能
# 学习点：pd是pandas的标准别名，DataFrame是处理结构化数据的核心数据结构
import pandas as pd

# 从matplotlib.patches导入图形补丁类，用于创建特殊形状（本代码中未直接使用，但保留以便扩展）
# 学习点：FancyArrowPatch可以创建自定义样式的箭头，ConnectionPatch用于连接两个坐标点
from matplotlib.patches import FancyArrowPatch, ConnectionPatch

# 从pathlib导入Path类，提供面向对象的路径操作，比os.path更现代、更安全
# 学习点：Path类支持链式调用（如Path('a/b').parent），自动处理跨平台路径分隔符
from pathlib import Path

# platform: 用于获取操作系统信息，便于跨平台兼容
# 学习点：可区分Windows/macOS/Linux，解决不同系统的字体、路径等兼容性问题
import platform

# 从typing导入类型提示工具，提高代码可读性和IDE支持
# 学习点：类型提示不是强制的，但能让代码更易维护，IDE能提供更精准的自动补全
from typing import Union, List, Dict, Tuple, Optional

# warnings: 用于发出警告信息，而不是直接抛出异常
# 学习点：警告不会终止程序运行，适合提示非致命性问题（如数据转换失败）
import warnings


# =============================================================================
# DataProcessor类：专业的数据处理工具（核心学习类）
# 设计模式：单一职责模式 + 链式调用模式
# 核心思想：将数据处理逻辑与绘图逻辑解耦，提高代码复用性和可维护性
# =============================================================================
class DataProcessor:
    """
    DataProcessor类 - 专业的数据处理工具（带详细学习注释）
    
    设计思路:
    将数据处理逻辑从绘图代码中独立出来，实现关注点分离原则。
    这样可以让绘图类专注于可视化展示，数据处理类专注于数据清洗、转换和验证。
    
    主要功能:
    1. CSV/Excel文件读取：支持多种数据格式导入
    2. 缺失值处理：提供5种不同的填充策略
    3. 异常值检测与清洗：使用IQR和Z-score两种统计学方法
    4. 数据格式转换：自动类型转换和数值化
    5. 数据验证机制：确保数据质量符合绘图要求
    6. 统计计算功能：提供描述性统计信息
    
    关键设计模式:
    - 链式调用设计：支持processor.read_file().handle_missing_values()的调用方式
    - 元数据追踪：记录所有数据处理步骤，便于审计和调试
    - 原地修改与复制选项：提供inplace参数，允许用户选择是否修改原始数据
    """
    
    def __init__(self):
        """
        初始化数据处理器（构造函数）
        
        设计思路:
        初始化时仅创建空容器，不进行任何计算，遵循惰性加载原则。
        这样可以避免不必要的资源消耗，只有在真正需要时才进行处理。
        
        关键变量说明（学习重点）:
        - self.original_data: 存储原始数据，保留原始状态便于回溯（数据溯源）
        - self.processed_data: 存储处理后的数据，用于实际使用（避免污染原始数据）
        - self.metadata: 存储处理元数据，记录数据变化过程（审计追踪）
        """
        # 初始化原始数据为None，等待后续赋值（惰性初始化）
        self.original_data = None
        # 初始化处理后的数据为None，等待后续处理
        self.processed_data = None
        # 初始化元数据字典，用于记录数据处理的各个步骤和结果（数据溯源）
        self.metadata = {}
    
    def read_file(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        读取CSV或Excel文件（文件IO核心方法）
        
        设计思路:
        提供统一的文件读取接口，自动识别文件格式并选择合适的读取方法。
        使用多态思想，让用户无需关心具体的文件格式细节。
        
        算法步骤（学习重点）:
        1. 将输入的文件路径转换为Path对象，确保跨平台兼容性
        2. 检查文件是否存在，不存在则抛出FileNotFoundError
        3. 根据文件后缀名判断文件格式（.csv或.xlsx/.xls）
        4. 使用对应的pandas函数读取文件内容
        5. 记录元数据，便于后续追踪
        6. 返回读取的DataFrame
        
        参数说明（类型提示学习）:
        - file_path: 文件路径，可以是字符串或Path对象（Union表示多类型支持）
        - **kwargs: 额外参数，传递给pandas的读取函数（可变关键字参数，灵活扩展）
        
        返回值:
        - pandas.DataFrame: 读取的数据框
        
        异常处理（编程规范学习）:
        - FileNotFoundError: 文件不存在时抛出（明确的错误类型）
        - ValueError: 不支持的文件格式时抛出（参数验证）
        - RuntimeError: 读取失败时抛出，并包含原始异常信息（异常链）
        
        编程技巧:
        - 使用from e语法保留原始异常的堆栈信息，便于调试
        - 采用守卫子句模式，提前处理异常情况
        """
        # 步骤1：将输入的文件路径转换为Path对象
        # 学习点：Path对象提供了更现代、更安全的路径操作方式，相比os.path有很多优势
        # 例如：自动处理Windows的\和Linux的/，支持链式调用（.parent/.exists()）
        file_path = Path(file_path)
        
        # 步骤2：检查文件是否存在（守卫子句模式）
        # 学习点：防御性编程的体现，在操作前先验证前置条件，提前失败
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 步骤3：获取文件后缀名并转为小写（大小写不敏感处理）
        # 学习点：suffix属性返回文件的扩展名（包括点号），lower()确保兼容大写后缀（如.CSV）
        suffix = file_path.suffix.lower()
        
        # 步骤4：根据文件格式选择读取方法（多态思想）
        try:
            # 如果是CSV文件，使用pd.read_csv()读取
            if suffix == '.csv':
                self.original_data = pd.read_csv(file_path,** kwargs)
            # 如果是Excel文件，使用pd.read_excel()读取
            elif suffix in ['.xlsx', '.xls']:
                self.original_data = pd.read_excel(file_path, **kwargs)
            # 如果是其他格式，抛出不支持的异常
            else:
                raise ValueError(f"不支持的文件格式: {suffix}")
            
            # 步骤5：记录元数据（数据溯源/审计追踪）
            # 学习点：记录关键信息便于调试和审计，是企业级代码的重要实践
            self.metadata['file_path'] = str(file_path)
            self.metadata['file_format'] = suffix
            self.metadata['original_shape'] = self.original_data.shape  # 记录原始数据维度
            
            # 步骤6：返回读取的数据
            return self.original_data
            
        # 步骤7：异常处理（异常链保留）
        # 学习点：使用from e语法保留原始异常，方便定位问题根源（Python 3+特性）
        except Exception as e:
            raise RuntimeError(f"读取文件失败: {str(e)}") from e
    
    def handle_missing_values(self, 
                               strategy: str = 'fill_zero',
                               fill_value: Union[int, float, str] = 0,
                               axis: int = 0,
                               inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        处理缺失值（数据清洗核心方法）
        
        设计思路:
        提供多种缺失值处理策略，让用户根据数据特点选择最适合的方法。
        这是策略模式的一个典型应用，将算法族封装起来，使它们可以互换。
        
        支持的处理策略（算法学习重点）:
        1. 'fill_zero': 用0填充（适用于大多数情况，特别是缺失值表示"无"的时候）
        2. 'fill_mean': 用平均值填充（适用于正态分布的数值型数据）
        3. 'fill_median': 用中位数填充（适用于有异常值的数据，中位数更稳健）
        4. 'fill_value': 用用户指定的值填充（最灵活的方式）
        5. 'drop': 删除包含缺失值的行/列（适用于缺失值较少且可以接受数据减少的情况）
        
        算法步骤:
        1. 检查是否有原始数据，没有则抛出异常
        2. 根据inplace参数决定是操作原始数据还是创建副本
        3. 根据选择的策略执行对应的缺失值处理
        4. 记录处理的缺失值数量到元数据
        5. 根据inplace参数决定返回值
        
        参数说明:
        - strategy: 处理策略，默认为'fill_zero'
        - fill_value: 当strategy为'fill_value'时使用的填充值
        - axis: 当strategy为'drop'时，0表示删除行，1表示删除列
        - inplace: 是否在原地修改，True则修改self.original_data，False则返回副本
        
        返回值:
        - Optional[pd.DataFrame]: 如果inplace=False，返回处理后的数据框；否则返回None
        
        编程技巧（学习重点）:
        - 使用早期返回模式，提前处理异常情况
        - 使用select_dtypes()方法筛选数值列，避免对非数值列执行统计操作
        - 采用copy()方法创建数据副本，避免意外修改原始数据
        """
        # 步骤1：验证前置条件（早期返回）
        # 学习点：早期返回模式，减少嵌套层级，提高代码可读性
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：决定操作对象：原始数据或副本（原地修改vs副本）
        # 学习点：inplace参数是pandas的经典设计，平衡性能和数据安全
        # inplace=True节省内存，但会修改原始数据；False返回副本，更安全
        df = self.original_data if inplace else self.original_data.copy()
        
        # 步骤3：根据策略执行缺失值处理（策略模式）
        # 学习点：将不同的处理算法封装在条件分支中，实现算法互换
        if strategy == 'fill_zero':
            # 策略1：用0填充所有缺失值
            # 学习点：fillna()是pandas处理缺失值的核心方法，支持多种填充方式
            df = df.fillna(0)
        elif strategy == 'fill_mean':
            # 策略2：用平均值填充（仅对数值列）
            # 学习点：select_dtypes筛选数值列，避免对字符串列执行均值计算
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'fill_median':
            # 策略3：用中位数填充（仅对数值列）
            # 学习点：中位数比平均值更稳健，不受异常值影响（统计知识点）
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'fill_value':
            # 策略4：用用户指定的值填充
            df = df.fillna(fill_value)
        elif strategy == 'drop':
            # 策略5：删除包含缺失值的行或列
            # 学习点：axis=0删除行（默认），axis=1删除列
            df = df.dropna(axis=axis)
        else:
            # 如果策略不在支持列表中，抛出异常（参数验证）
            raise ValueError(f"不支持的策略: {strategy}")
        
        # 步骤4：记录处理的缺失值数量（数据溯源）
        # 学习点：计算处理前后缺失值的差值，量化处理效果
        self.metadata['missing_values_removed'] = self.original_data.isna().sum().sum() - df.isna().sum().sum()
        
        # 步骤5：更新实例属性并返回
        if inplace:
            # 如果是原地修改，更新original_data和processed_data
            self.original_data = df
            self.processed_data = df
        else:
            # 如果不是原地修改，只更新processed_data
            self.processed_data = df
        
        # 根据inplace参数决定返回值（Optional类型的应用）
        return self.processed_data if not inplace else None
    
    def detect_outliers(self, 
                        method: str = 'iqr',
                        threshold: float = 1.5,
                        columns: Optional[List[str]] = None) -> Dict:
        """
        检测异常值（统计分析核心方法）
        
        设计思路:
        提供两种常用的异常值检测方法，让用户根据数据分布选择合适的方法。
        不直接删除异常值，而是先检测并报告，让用户决定如何处理。
        
        支持的检测方法（统计学重点）:
        1. 'iqr': 四分位距方法
           - 优点：对异常值不敏感，适合大多数数据分布（非参数方法）
           - 原理：Q1-1.5*IQR ~ Q3+1.5*IQR范围外的数据视为异常值
           - 适用场景：数据分布不对称或有明显异常值
        
        2. 'zscore': Z-score方法（标准化分数）
           - 优点：计算简单，基于正态分布假设（参数方法）
           - 原理：数据点与均值的距离超过多少个标准差视为异常值
           - 适用场景：数据近似服从正态分布
        
        IQR算法步骤（核心学习点）:
        1. 计算第一四分位数(Q1)：25%分位数（数据从小到大排列后，前25%的分界点）
        2. 计算第三四分位数(Q3)：75%分位数（数据从小到大排列后，前75%的分界点）
        3. 计算四分位距(IQR)：IQR = Q3 - Q1（中间50%数据的范围）
        4. 计算下界：lower_bound = Q1 - threshold * IQR
        5. 计算上界：upper_bound = Q3 + threshold * IQR
        6. 标记超出[lower_bound, upper_bound]范围的数据为异常值
        
        Z-score算法步骤:
        1. 计算数据的均值(μ)和标准差(σ)
        2. 计算每个数据点的Z分数：Z = (x - μ) / σ
        3. 绝对值超过threshold的Z分数视为异常值（通常threshold=3）
        
        参数说明:
        - method: 检测方法，'iqr'或'zscore'，默认为'iqr'
        - threshold: 异常值判定阈值，IQR方法默认为1.5，Z-score默认为3.0
        - columns: 指定要检测的列，None表示所有数值列
        
        返回值:
        - Dict: 包含异常值信息的字典（列名: 异常值数量、索引、具体值）
        
        编程技巧（学习重点）:
        - 使用布尔掩码技术高效筛选异常值（向量化操作，无显式循环）
        - 采用向量化操作避免显式循环，提高性能（比for循环快100倍+）
        - 使用字典存储结果，结构化地组织异常值信息（便于后续处理）
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据（优先使用已处理的数据）
        df = self.processed_data if self.processed_data is not None else self.original_data
        
        # 步骤3：确定要检测的列（自动筛选数值列）
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 步骤4：初始化异常值信息字典（结构化存储结果）
        outliers_info = {}
        
        # 步骤5：逐个列检测异常值（向量化操作）
        for col in columns:
            # 跳过不存在的列（防御性编程）
            if col not in df.columns:
                continue
                
            # 根据方法选择检测算法
            if method == 'iqr':
                # IQR方法（非参数，稳健性好）
                Q1 = df[col].quantile(0.25)  # 第一四分位数
                Q3 = df[col].quantile(0.75)  # 第三四分位数
                IQR = Q3 - Q1                # 四分位距
                lower_bound = Q1 - threshold * IQR  # 下界
                upper_bound = Q3 + threshold * IQR  # 上界
                # 布尔掩码：标记异常值（向量化操作，无循环）
                outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            elif method == 'zscore':
                # Z-score方法（参数，基于正态分布）
                # 计算Z分数：(值-均值)/标准差
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                # 绝对值超过阈值的视为异常值
                outliers_mask = z_scores > threshold
            else:
                raise ValueError(f"不支持的方法: {method}")
            
            # 步骤6：统计异常值信息（量化结果）
            outliers_count = outliers_mask.sum()  # 统计异常值数量
            if outliers_count > 0:
                outliers_info[col] = {
                    'count': int(outliers_count),          # 异常值数量
                    'indices': df[outliers_mask].index.tolist(),  # 异常值行索引
                    'values': df[col][outliers_mask].tolist()     # 异常值具体数值
                }
        
        # 步骤7：记录元数据并返回结果（数据溯源）
        self.metadata['outliers_detected'] = outliers_info
        return outliers_info
    
    def remove_outliers(self,
                       method: str = 'iqr',
                       threshold: float = 1.5,
                       columns: Optional[List[str]] = None,
                       inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        移除异常值（数据清洗进阶方法）
        
        设计思路:
        在detect_outliers()的基础上，实际执行移除操作。
        采用先检测后移除的两步策略，确保用户了解将被移除的数据。
        
        参数说明:
        - method: 检测方法，'iqr'或'zscore'
        - threshold: 异常值判定阈值
        - columns: 指定要处理的列
        - inplace: 是否在原地修改
        
        返回值:
        - Optional[pd.DataFrame]: 处理后的数据框（如果inplace=False）
        
        编程技巧（学习重点）:
        - 使用|=（按位或赋值）操作符累积异常值掩码
        - 使用pd.Series()创建布尔序列，确保与DataFrame索引对齐
        - 使用~（逻辑非）操作符反转掩码，选择非异常值
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据（创建副本避免污染原始数据）
        df = self.processed_data if self.processed_data is not None else self.original_data.copy()
        
        # 步骤3：确定要处理的列
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 步骤4：初始化全局异常值掩码（全为False）
        # 学习点：pd.Series确保掩码与DataFrame索引对齐，避免索引错位问题
        outliers_mask = pd.Series(False, index=df.index)
        
        # 步骤5：逐个列检测异常值并更新全局掩码
        for col in columns:
            if col not in df.columns:
                continue
                
            # 使用与detect_outliers相同的逻辑检测异常值
            if method == 'iqr':
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                col_outliers = (df[col] < lower_bound) | (df[col] > upper_bound)
            elif method == 'zscore':
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                col_outliers = z_scores > threshold
            else:
                raise ValueError(f"不支持的方法: {method}")
            
            # 学习点：|= 按位或赋值，累积异常值掩码（只要任一列为异常值，就标记为异常）
            outliers_mask |= col_outliers
        
        # 步骤6：移除异常值（逻辑非操作~，选择非异常值）
        # 学习点：~操作符反转布尔掩码，df[~mask]选择非异常行
        removed_count = int(outliers_mask.sum())
        df_clean = df[~outliers_mask]
        
        # 步骤7：记录元数据（量化移除效果）
        self.metadata['outliers_removed'] = removed_count
        
        # 步骤8：更新实例属性并返回
        if inplace:
            if self.processed_data is None:
                self.processed_data = self.original_data.copy()
            self.processed_data = df_clean
        else:
            self.processed_data = df_clean
        
        return self.processed_data if not inplace else None
    
    def convert_data_types(self,
                          dtype_map: Optional[Dict[str, type]] = None,
                          numeric_only: bool = False,
                          inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        转换数据类型（数据预处理核心方法）
        
        设计思路:
        提供灵活的数据类型转换功能，支持显式映射和自动推断两种方式。
        使用try-except捕获转换失败，避免因个别列导致整个程序崩溃。
        
        参数说明:
        - dtype_map: 列名到数据类型的映射字典（如{'销量': int, '金额': float}）
        - numeric_only: 是否只尝试转换为数值类型
        - inplace: 是否在原地修改
        
        返回值:
        - Optional[pd.DataFrame]: 处理后的数据框（如果inplace=False）
        
        学习重点:
        - pd.to_numeric()的errors='ignore'参数：转换失败时忽略，不抛出异常
        - try-except捕获转换异常，保证程序鲁棒性
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据
        df = self.processed_data if self.processed_data is not None else self.original_data.copy()
        
        # 步骤3：显式类型映射转换（用户指定的类型）
        if dtype_map:
            for col, dtype in dtype_map.items():
                if col in df.columns:
                    try:
                        # 尝试转换列类型
                        df[col] = df[col].astype(dtype)
                    except Exception as e:
                        # 转换失败时发出警告，不终止程序（鲁棒性设计）
                        warnings.warn(f"转换列 {col} 失败: {str(e)}")
        
        # 步骤4：自动数值化转换（仅转换为数值类型）
        if numeric_only:
            for col in df.columns:
                try:
                    # 学习点：pd.to_numeric的errors='ignore'参数，转换失败时保留原值
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
                    # 静默失败，保证程序继续运行
                    pass
        
        # 步骤5：更新实例属性并返回
        if inplace:
            if self.processed_data is None:
                self.processed_data = self.original_data.copy()
            self.processed_data = df
        else:
            self.processed_data = df
        
        return self.processed_data if not inplace else None
    
    def validate_data(self,
                     min_rows: int = 2,
                     min_cols: int = 1,
                     check_positive: bool = True,
                     check_numeric: bool = True) -> Tuple[bool, List[str]]:
        """
        验证数据有效性（数据质量检查核心方法）
        
        设计思路:
        在绘图前验证数据质量，避免因数据问题导致绘图失败。
        采用收集所有错误后统一返回的策略，让用户一次性了解所有问题。
        
        参数说明:
        - min_rows: 最小行数要求，默认为2（至少2年数据才能计算环比）
        - min_cols: 最小列数要求，默认为1（至少1个区域）
        - check_positive: 是否检查数值是否为非负（柱状图数据不能为负）
        - check_numeric: 是否检查所有数据是否为数值型
        
        返回值:
        - Tuple[bool, List[str]]: (是否有效, 错误信息列表)
        
        学习重点:
        - 批量错误收集：不立即抛出异常，而是收集所有错误后返回
        - 防御性编程：提前检查数据质量，避免后续绘图崩溃
        """
        # 步骤1：确定要验证的数据
        df = self.processed_data if self.processed_data is not None else self.original_data
        
        # 步骤2：检查数据是否存在
        if df is None:
            return False, ["请先读取数据"]
        
        # 步骤3：初始化错误列表（批量收集错误）
        errors = []
        
        # 步骤4：验证行数（至少2行才能计算环比）
        if len(df) < min_rows:
            errors.append(f"数据行数不足，至少需要 {min_rows} 行，当前有 {len(df)} 行")
        
        # 步骤5：验证列数（至少1列）
        if len(df.columns) < min_cols:
            errors.append(f"数据列数不足，至少需要 {min_cols} 列，当前有 {len(df.columns)} 列")
        
        # 步骤6：验证数值类型（确保是数值型数据）
        if check_numeric:
            non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
            if non_numeric_cols:
                errors.append(f"存在非数值列: {non_numeric_cols}")
        
        # 步骤7：验证非负值（柱状图数据不能为负）
        if check_positive:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if (df[col] < 0).any():
                    errors.append(f"列 {col} 包含负值")
        
        # 步骤8：确定验证结果
        is_valid = len(errors) == 0
        
        # 步骤9：记录元数据（审计追踪）
        self.metadata['validation_result'] = is_valid
        self.metadata['validation_errors'] = errors
        
        # 步骤10：返回结果
        return is_valid, errors
    
    def calculate_statistics(self, 
                            columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        计算统计指标（描述性统计核心方法）
        
        设计思路:
        提供丰富的描述性统计信息，帮助用户了解数据特征。
        在pandas内置describe()的基础上，添加额外的统计指标。
        
        参数说明:
        - columns: 指定要计算的列，None表示所有数值列
        
        返回值:
        - pd.DataFrame: 包含统计信息的数据框
        
        学习重点:
        - pd.describe()的扩展：补充sum、median、variance等指标
        - 统计指标的业务意义：sum（总和）、median（中位数）、variance（方差）
        """
        # 步骤1：确定要处理的数据
        df = self.processed_data if self.processed_data is not None else self.original_data
        
        # 步骤2：验证前置条件
        if df is None:
            raise ValueError("请先读取数据")
        
        # 步骤3：确定要计算的列
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 步骤4：使用pandas内置的describe()获取基础统计信息
        # 学习点：describe()默认返回count, mean, std, min, 25%, 50%, 75%, max
        stats = df[columns].describe()
        
        # 步骤5：计算并添加额外的统计指标（扩展describe）
        additional_stats = pd.DataFrame(index=['sum', 'median', 'variance'])
        for col in columns:
            additional_stats.loc['sum', col] = df[col].sum()          # 总和
            additional_stats.loc['median', col] = df[col].median()    # 中位数
            additional_stats.loc['variance', col] = df[col].var()     # 方差
        
        # 步骤6：合并基础统计和额外统计
        stats = pd.concat([stats, additional_stats])
        
        # 步骤7：记录元数据
        self.metadata['statistics'] = stats.to_dict()
        
        # 步骤8：返回统计结果
        return stats
    
    def prepare_chart_data(self,
                          data: Optional[Union[List, np.ndarray, pd.DataFrame]] = None,
                          years: Optional[List[str]] = None,
                          regions: Optional[List[str]] = None) -> Tuple[pd.DataFrame, np.ndarray]:
        """
        准备图表数据，保持与现有代码的兼容性
        
        参数说明:
        - data: 原始数据（可选，如果提供则不从文件读取）
        - years: 年份标签列表（可选）
        - regions: 区域名称列表（可选）
        
        返回值:
        - Tuple[pd.DataFrame, np.ndarray]: (处理后的数据框, 数值数组)
        
        学习重点:
        - 多类型输入兼容：支持List/np.ndarray/pd.DataFrame三种输入格式
        - 数据标准化：统一转换为DataFrame+np.ndarray格式，方便后续绘图
        """
        # 步骤1：处理用户提供的数据（如果有）
        if data is not None:
            if isinstance(data, pd.DataFrame):
                df = data.copy()
            else:
                # 转换为numpy数组，方便维度操作
                data = np.array(data)
                # 自动生成年份标签（如果未提供）
                if years is None:
                    years = [f'Year_{i+1}' for i in range(data.shape[0])]
                # 自动生成区域标签（如果未提供）
                if regions is None:
                    regions = [f'Region_{i+1}' for i in range(data.shape[1])]
                # 转换为DataFrame（结构化数据）
                df = pd.DataFrame(data, index=years, columns=regions)
            self.original_data = df
            self.processed_data = df
        else:
            # 步骤2：使用DataProcessor已有的数据
            if self.processed_data is None:
                raise ValueError("请先提供数据或读取文件")
            df = self.processed_data.copy()
        
        # 步骤3：数据清洗（最终清洗，确保绘图数据质量）
        df = df.fillna(0)          # 填充缺失值
        df = df.astype(float)      # 转换为浮点型
        df_clean = df[(df >= 0).all(axis=1)]  # 筛选非负数据
        processed_data = df_clean.values      # 提取数值数组
        
        # 步骤4：更新实例属性
        if self.original_data is None:
            self.original_data = df_clean
        self.processed_data = df_clean
        
        # 步骤5：返回结果（结构化数据+数值数组）
        return df_clean, processed_data
    
    def get_metadata(self) -> Dict:
        """
        获取处理元数据（数据溯源/审计追踪）
        
        返回值:
        - Dict: 处理元数据的副本（返回副本避免外部修改）
        
        学习重点:
        - 数据封装：返回副本而不是原字典，避免外部修改实例内部状态
        """
        return self.metadata.copy()
    
    def reset(self):
        """
        重置处理器状态（资源释放）
        
        学习重点:
        - 资源管理：重置所有属性，释放内存，便于重复使用实例
        """
        self.original_data = None
        self.processed_data = None
        self.metadata = {}


# =============================================================================
# set_chinese_font函数：配置中文字体（跨平台兼容核心函数）
# 学习重点：解决Matplotlib中文显示乱码问题的标准方案
# =============================================================================
def set_chinese_font():
    """
    配置中文字体设置
    
    功能概述:
    根据不同操作系统自动选择合适的中文字体，确保图表中的中文能正常显示。
    这是Matplotlib中文显示问题的标准解决方案。
    
    算法原理（学习重点）:
    1. 获取当前操作系统名称
    2. 根据操作系统选择对应的字体列表（优先级从高到低）
    3. 逐个尝试设置字体，直到找到可用的字体
    4. 同时设置负号显示为正常字符（解决负号显示为方块的问题）
    
    操作系统字体策略:
    - Windows系统：优先使用黑体(SimHei)、微软雅黑(Microsoft YaHei)、宋体(SimSun)
    - macOS系统：优先使用华文黑体(Heiti TC/SC)、Arial Unicode MS
    - Linux系统：优先使用文泉驿微米黑(WenQuanYi Micro Hei)
    - 回退方案：如果所有字体都不可用，则回退到DejaVu Sans（无中文，但不会崩溃）
    """
    # 获取当前操作系统名称（platform.system()返回Windows/Darwin/Linux）
    system_name = platform.system()
    
    # 根据操作系统选择字体列表（优先级排序）
    if system_name == 'Windows':
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']
    elif system_name == 'Darwin':  # Darwin是macOS的内核名称
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS']
    else:  # Linux/Unix
        font_names = ['WenQuanYi Micro Hei', 'Droid Sans Fallback']
    
    # 逐个尝试设置字体（容错机制）
    for font_name in font_names:
        try:
            # 设置默认字体为选中的中文字体
            plt.rcParams['font.sans-serif'] = [font_name]
            # 解决负号显示为方块的问题（关键配置）
            plt.rcParams['axes.unicode_minus'] = False
            return  # 成功设置后立即返回
        except:
            # 字体不可用时继续尝试下一个
            continue
    
    # 如果所有字体都不可用，使用回退方案（保证程序不崩溃）
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


# =============================================================================
# load_and_process_data函数：数据加载和处理（兼容旧版接口）
# 学习重点：数据标准化流程，从原始数据到绘图数据的转换
# =============================================================================
def load_and_process_data(data, years, regions):
    """
    使用pandas读取、清洗和转换数据（兼容旧版接口）
    
    功能概述:
    将原始数据转换为 pandas DataFrame 格式，并进行数据清洗，确保数据质量。
    
    算法步骤（学习重点）:
    1. 创建 DataFrame，将年份设为索引，区域设为列名（结构化）
    2. 填充缺失值为 0（数据清洗）
    3. 转换数据类型为浮点型（统一数值类型）
    4. 筛选出所有值都非负的行（柱状图数据要求）
    5. 提取纯数值数组供后续计算使用（numpy数组运算更快）
    
    参数说明:
    - data: 原始数据二维列表或数组
    - years: 年份标签列表
    - regions: 区域名称列表
    
    返回值:
    - pandas.DataFrame: 处理后的数据框（结构化，便于查看）
    - numpy.ndarray: 处理后的数值数组（便于快速计算）
    """
    # 创建DataFrame（结构化数据，索引=年份，列=区域）
    df = pd.DataFrame(data, index=years, columns=regions)
    
    # 填充缺失值为0（柱状图不支持缺失值）
    df = df.fillna(0)
    
    # 转换为浮点类型（统一数值类型，避免整数/浮点混合计算问题）
    df = df.astype(float)
    
    # 筛选出所有值都非负的行（(df >= 0).all(axis=1)：每行所有列都非负）
    df_clean = df[(df >= 0).all(axis=1)]
    
    # 提取数值数组（numpy数组，便于后续向量化计算）
    processed_data = df_clean.values
    
    # 返回处理后的数据（结构化DataFrame + 数值数组）
    return df_clean, processed_data


# =============================================================================
# StackedBarChartWithArrow类：带环比箭头的堆叠柱状图（核心绘图类）
# 设计模式：面向对象封装，将绘图逻辑封装为类，便于复用和扩展
# =============================================================================
class StackedBarChartWithArrow:
    """
    带环比箭头的堆叠柱状图类（核心可视化类）
    
    功能概述:
    核心功能类，用于生成商业级别的堆叠柱状图，并在年份之间添加直角样式的环比增长率箭头。
    
    主要属性（学习重点）:
    - self.df: pandas.DataFrame，清洗后的数据框（结构化数据）
    - self.data: numpy.ndarray，清洗后的数值数组（快速计算）
    - self.years: list，年份标签列表（X轴标签）
    - self.regions: list，区域名称列表（图例标签）
    - self.colors: list，各区域对应的颜色列表（视觉区分）
    - self.config: dict，完整的配置字典（个性化配置）
    - self.data_processor: DataProcessor，数据处理器实例（数据清洗）
    """
    
    def __init__(self, data=None, years=None, regions=None, colors=None, config=None, data_processor=None):
        """
        初始化堆叠柱状图实例（构造函数）
        
        初始化流程（学习重点）:
        1. 保存data_processor引用（如果提供）
        2. 如果提供了data_processor，使用其prepare_chart_data()方法准备数据
        3. 否则使用传统方式load_and_process_data()加载并处理原始数据
        4. 从DataFrame中提取years和regions（保证数据一致性）
        
        参数说明:
        - data: 原始数据（二维列表/数组/DataFrame）
        - years: 年份标签列表
        - regions: 区域名称列表
        - colors: 区域颜色列表
        - config: 配置字典（覆盖默认配置）
        - data_processor: DataProcessor实例（可选，高级数据处理）
        """
        # 1. 保存数据处理器实例（依赖注入）
        self.data_processor = data_processor
        
        # 2. 初始化默认配置（后续可被用户配置覆盖）
        self.default_config = {
            'figsize': (10, 8),          # 图表尺寸
            'bar_width': 0.55,           # 柱状图宽度
            'dpi': 150,                  # 输出分辨率
            'output_path': 'stacked_bar_chart.png',  # 默认输出路径
            'title_fontsize': 16,        # 标题字体大小
            'data_label_fontsize': 10,   # 数据标签字体大小
            'percentage_fontsize': 10,   # 增长率标签字体大小
            'arrow_color': '#333333',    # 箭头颜色
            'percentage_background': '#2c3e50'  # 增长率标签背景色
        }
        
        # 3. 合并用户配置和默认配置（用户配置优先）
        self.config = self.default_config.copy()
        if config:
            self.config.update(config)
        
        # 4. 处理数据（支持两种数据处理方式）
        if self.data_processor is not None:
            # 使用高级数据处理器准备数据
            self.df, self.data = self.data_processor.prepare_chart_data(data, years, regions)
            # 从DataFrame中提取年份和区域（保证一致性）
            self.years = self.df.index.tolist()
            self.regions = self.df.columns.tolist()
        else:
            # 使用传统方式处理数据（兼容旧接口）
            if data is None or years is None or regions is None:
                raise ValueError("未提供必要的数据源信息")
            self.df, self.data = load_and_process_data(data, years, regions)
            self.years = years
            self.regions = regions
        
        # 5. 处理颜色配置（默认颜色或用户指定颜色）
        self.colors = colors if colors else self._get_default_colors()
        
        # 6. 验证颜色数量与区域数量匹配（防御性编程）
        if len(self.colors) != len(self.regions):
            raise ValueError(f"颜色数量({len(self.colors)})与区域数量({len(self.regions)})不匹配")
        
        # 7. 设置中文字体（确保中文正常显示）
        set_chinese_font()
    
    def _get_default_colors(self):
        """
        获取默认颜色列表（私有辅助方法）
        学习重点：
        1. 私有方法命名规范：Python中以下划线开头标识私有方法，仅类内部调用，封装内部逻辑
        2. 商业配色原则：选择高对比度、视觉舒适、符合商业可视化审美的配色方案
        3. 可扩展性设计：默认配色列表预留足够数量，适配不同区域数量的场景
        
        设计思路：
        - 避免硬编码散落在各处，通过私有方法统一管理默认颜色，符合"单一职责原则"
        - 选择matplotlib官方推荐的商业配色，兼顾专业性和可读性
        - 颜色数量（8种）覆盖绝大多数业务场景的区域数量需求
        
        返回值：
        - list[str]：十六进制格式的颜色字符串列表，每个字符串对应一种RGB颜色
        """
        # 预设的商业配色方案（对比度高，视觉效果好）
        # 配色选择逻辑：
        # 1. 前4种：matplotlib经典配色，区分度极高，适合核心维度
        # 2. 后4种：补充配色，与前4种无视觉冲突，适配更多维度
        default_colors = [
            '#1f77b4',  # 深蓝（主色，代表核心区域/基础数据）
            '#ff7f0e',  # 橙黄（辅助色，对比强烈）
            '#2ca02c',  # 深绿（辅助色，代表增长/正向数据）
            '#d62728',  # 深红（警示色，代表下降/负向数据）
            '#9467bd',  # 紫（补充色）
            '#8c564b',  # 棕（补充色）
            '#e377c2',  # 粉（补充色）
            '#7f7f7f'   # 灰（中性色）
        ]
        return default_colors

    def _setup_config(self, config):
        """
        初始化图表配置（私有辅助方法）
        学习重点：
        1. 配置合并策略：默认配置 + 用户自定义配置，用户配置优先级更高
        2. 默认值设计：为所有关键参数设置合理默认值，降低使用门槛
        3. 类型安全：通过字典合并确保配置项完整性，避免KeyError
        
        算法步骤：
        1. 定义基础默认配置字典，覆盖图表所有可配置维度
        2. 合并用户传入的自定义配置（如果有），覆盖默认值
        3. 将合并后的配置赋值给实例属性，供其他方法调用
        
        参数说明：
        - config: dict | None：用户自定义配置字典，可为None（使用全量默认值）
        
        编程技巧：
        - 使用字典解包（**）合并配置，简洁高效
        - 所有默认值经过业务验证，适配大多数商业可视化场景
        """
        # 定义默认配置字典，覆盖图表所有核心参数
        default_config = {
            'figsize': (10, 8),          # 图表尺寸：宽10英寸，高8英寸（黄金比例）
            'bar_width': 0.55,           # 柱状图宽度：适配年份标签间距，避免过宽/过窄
            'dpi': 150,                  # 图片分辨率：150DPI兼顾清晰度和文件大小
            'output_path': 'stacked_bar_chart.png',  # 默认输出路径
            'title_fontsize': 14,        # 标题字体大小：符合视觉层级
            'data_label_fontsize': 10,   # 数据标签字体大小：保证可读性
            'percentage_fontsize': 9,    # 增长率标签字体大小：略小于数据标签，突出主次
            'arrow_color': '#333333',    # 箭头颜色：深灰，不抢主体视觉焦点
            'percentage_background': '#2c3e50'  # 增长率标签背景：深蓝灰，突出文字
        }
        
        # 合并配置：用户配置覆盖默认配置（核心技巧）
        # 逻辑：如果用户传入config，则更新默认配置；否则使用纯默认值
        if config is not None and isinstance(config, dict):
            default_config.update(config)
        
        # 将最终配置赋值给实例属性，供类内其他方法调用
        self.config = default_config

    def _calculate_totals(self):
        """
        计算每年的总计值（私有辅助方法）
        学习重点：
        1. 向量化计算：使用numpy的sum方法，比Python循环高效10倍以上
        2. 维度控制：指定axis=1，按行（年份）求和，适配数据结构
        3. 结果存储：将计算结果保存为实例属性，避免重复计算
        
        算法原理：
        - 数据结构：self.data是二维数组，shape=(年份数, 区域数)
        - 按行求和：axis=1表示沿着"区域"维度求和，得到每个年份的总计
        
        返回值：
        - numpy.ndarray：一维数组，长度=年份数，每个元素对应每年的总计值
        
        编程技巧：
        - 优先使用numpy内置方法，利用C语言底层优化，提升计算效率
        - 结果缓存到self.totals，后续绘制总计标签、计算增长率时直接调用
        """
        # 按行求和：计算每个年份所有区域的数值总和
        # axis=1：对每行（年份）的所有列（区域）求和
        self.totals = self.data.sum(axis=1)
        return self.totals

    def _calculate_growth_rates(self):
        """
        计算环比增长率（私有辅助方法）
        学习重点：
        1. 环比公式：(本期值 - 上期值) / 上期值 × 100%
        2. 边界处理：避免除零错误（防御性编程）
        3. 数值格式化：保留两位小数，符合商业数据展示习惯
        
        算法步骤：
        1. 获取每年总计值（从self.totals）
        2. 遍历总计值，逐个计算相邻年份的增长率
        3. 处理特殊情况：上期值为0时，增长率设为0（避免报错）
        4. 格式化结果：保留两位小数，便于后续展示
        
        返回值：
        - list[float]：增长率列表，长度=年份数-1（因为至少需要2年才能计算环比）
        
        异常处理：
        - 防御性编程：判断上期值是否为0，避免ZeroDivisionError
        """
        # 初始化增长率列表
        growth_rates = []
        
        # 遍历总计值，计算相邻年份的环比增长率
        # 范围：len(self.totals)-1，因为最后一年没有下一期
        for i in range(len(self.totals) - 1):
            previous = self.totals[i]    # 上期值（第i年）
            current = self.totals[i+1]   # 本期值（第i+1年）
            
            # 防御性编程：避免除零错误
            if previous == 0:
                rate = 0.0
            else:
                # 核心公式：环比增长率 = (本期 - 上期) / 上期 × 100%
                rate = ((current - previous) / previous) * 100
            
            # 保留两位小数，符合商业数据展示规范
            growth_rates.append(round(rate, 2))
        
        # 缓存增长率结果到实例属性
        self.growth_rates = growth_rates
        return self.growth_rates

    def _plot_stacked_bars(self):
        """
        绘制堆叠柱状图（私有核心方法）
        学习重点：
        1. 堆叠原理：通过bottom参数逐层叠加，实现堆叠效果
        2. 坐标轴控制：x轴为年份，y轴为数值，动态适配数据范围
        3. 循环绘制：按区域循环，逐层构建堆叠柱
        
        算法原理（堆叠核心）：
        - 初始bottom为全0数组（柱的底部从0开始）
        - 每绘制一个区域的柱，更新bottom为当前bottom + 该区域数值
        - 最终bottom累加为每年的总计值，形成完整堆叠
        
        编程技巧：
        - 使用enumerate同时获取索引和区域名称，便于关联颜色
        - 动态计算y轴上限（1.2倍最大值），预留箭头绘制空间
        """
        # 设置中文字体（确保中文标签正常显示）
        set_chinese_font()
        
        # 创建图表和坐标轴对象：plt.subplots返回(图表对象, 坐标轴对象)
        self.fig, self.ax = plt.subplots(figsize=self.config['figsize'], dpi=self.config['dpi'])
        
        # 初始化bottom数组（堆叠的底部位置），初始为0
        bottom = np.zeros(len(self.years))
        
        # 遍历每个区域，逐层绘制堆叠柱
        # enumerate(regions)：同时获取区域索引i和区域名称region
        for i, region in enumerate(self.regions):
            # 获取当前区域的颜色（用户指定或默认）
            color = self.colors[i] if i < len(self.colors) else self._get_default_colors()[i % len(self._get_default_colors())]
            
            # 核心：绘制堆叠柱
            # x：年份位置（0,1,2...），height：当前区域的数值，bottom：堆叠底部
            # width：柱宽度，color：柱颜色，label：图例标签
            self.ax.bar(
                x=range(len(self.years)),
                height=self.data[:, i],  # 取第i列（当前区域）的所有年份数据
                bottom=bottom,           # 堆叠底部位置
                width=self.config['bar_width'],
                color=color,
                label=region
            )
            
            # 更新bottom：当前bottom + 该区域数值，作为下一层的底部
            bottom += self.data[:, i]
        
        # 设置x轴标签：替换默认的0,1,2为实际年份
        self.ax.set_xticks(range(len(self.years)))
        self.ax.set_xticklabels(self.years)
        
        # 动态设置y轴上限：1.2倍最大值，预留箭头绘制空间
        y_max = bottom.max() if bottom.max() > 0 else 100  # 避免0值导致的异常
        self.ax.set_ylim(0, y_max * 1.2)
        
        # 添加图例：loc='upper right'确保不遮挡数据，frameon=False去掉边框
        self.ax.legend(loc='upper right', frameon=False)
        
        # 隐藏顶部和右侧的边框，提升视觉简洁度
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)

    def _add_data_labels(self):
        """
        为堆叠柱添加数值标签（私有辅助方法）
        学习重点：
        1. 标签定位：计算每个分段的中心位置，确保标签居中显示
        2. 文本渲染：设置字体大小、颜色，保证可读性
        3. 循环嵌套：外层遍历年份，内层遍历区域，精准定位每个分段
        
        算法步骤：
        1. 初始化累计高度（current_bottom），记录每个分段的底部
        2. 遍历每个年份，再遍历每个区域
        3. 计算标签位置：x=年份索引，y=当前分段的中心（bottom + 高度/2）
        4. 绘制文本标签，显示保留1位小数的数值
        
        视觉优化：
        - 标签颜色为白色，与柱颜色形成对比
        - 字体大小统一，保证视觉一致性
        """
        # 初始化累计高度，用于计算每个分段的底部
        current_bottom = np.zeros(len(self.years))
        
        # 外层循环：遍历每个区域
        for i, region in enumerate(self.regions):
            # 内层循环：遍历每个年份
            for j in range(len(self.years)):
                # 获取当前分段的数值
                value = self.data[j, i]
                
                # 仅当数值>0时显示标签（避免0值标签冗余）
                if value > 0:
                    # 计算标签y坐标：分段底部 + 分段高度/2（居中）
                    y_pos = current_bottom[j] + value / 2
                    # 计算标签x坐标：年份索引（与柱对齐）
                    x_pos = j
                    
                    # 绘制文本标签
                    self.ax.text(
                        x_pos, y_pos,
                        f'{value:.1f}',  # 保留1位小数，简洁易读
                        ha='center',     # 水平居中
                        va='center',     # 垂直居中
                        fontsize=self.config['data_label_fontsize'],
                        color='white'    # 白色文字，对比强烈
                    )
            
            # 更新累计高度：加上当前区域的数值，作为下一个区域的底部
            current_bottom += self.data[:, i]

    def _add_total_labels(self):
        """
        为柱状图顶部添加总计标签（私有辅助方法）
        学习重点：
        1. 总计定位：在每个柱的顶部（总计值位置）添加标签
        2. 偏移优化：y轴偏移1%的最大值，避免标签与柱顶重叠
        3. 格式统一：总计标签显示整数，符合商业数据展示习惯
        
        算法步骤：
        1. 遍历每个年份的总计值
        2. 计算标签位置：x=年份索引，y=总计值 + 偏移量（避免重叠）
        3. 绘制总计标签，显示整数
        
        视觉优化：
        - 标签颜色为深灰，突出但不刺眼
        - 偏移量动态计算（基于y轴最大值），适配不同数据范围
        """
        # 计算偏移量：y轴最大值的1%，避免标签与柱顶重叠
        y_max = self.totals.max() if self.totals.max() > 0 else 100
        offset = y_max * 0.01
        
        # 遍历每个年份，添加总计标签
        for i, total in enumerate(self.totals):
            # 绘制总计标签
            self.ax.text(
                i, total + offset,       # x=年份索引，y=总计值+偏移
                f'总计: {int(total)}',   # 显示整数，符合商业习惯
                ha='center',             # 水平居中
                va='bottom',             # 垂直靠下（与柱顶对齐）
                fontsize=self.config['data_label_fontsize'] + 1,  # 比数据标签大1号，突出层级
                color='#333333'          # 深灰，视觉舒适
            )

    def _draw_arrows_and_percentages(self):
        """
        绘制环比增长率箭头和百分比标签（私有核心方法）
        学习重点：
        1. 直角箭头绘制：分三段（上→平→下）绘制，模拟直角效果
        2. 标签背景：使用bbox创建圆形背景，突出增长率标签
        3. 动态偏移：根据数据范围自动调整箭头高度，适配不同数据
        
        算法原理（直角箭头）：
        1. 第一段（垂直向上）：从第i年柱顶 → 峰值点（柱顶+偏移）
        2. 第二段（水平向右）：从峰值点 → 第i+1年上方的峰值点
        3. 第三段（垂直向下）：从第i+1年上方峰值点 → 第i+1年柱顶
        4. 箭头终点添加指示符，明确增长/下降方向
        
        视觉优化：
        - 增长率标签带圆形背景，突出显示
        - 正负增长率自动添加+/-符号，直观区分涨跌
        """
        # 计算箭头垂直偏移量：y轴最大值的8%，保证箭头高度适中
        y_max = self.totals.max() if self.totals.max() > 0 else 100
        arrow_offset = y_max * 0.08
        
        # 遍历所有需要绘制箭头的年份对（共len(growth_rates)组）
        for i, rate in enumerate(self.growth_rates):
            # 第1年柱顶y坐标
            y1 = self.totals[i]
            # 第2年柱顶y坐标
            y2 = self.totals[i+1]
            
            # 峰值点y坐标（箭头最高点）：取两年柱顶的最大值 + 偏移
            peak_y = max(y1, y2) + arrow_offset
            
            # ========== 第一段：垂直向上箭头（从第i年柱顶到峰值） ==========
            self.ax.plot(
                [i, i], [y1, peak_y],          # x固定为i，y从y1到peak_y
                color=self.config['arrow_color'],
                linewidth=1.5,                 # 箭头线宽，保证清晰
                solid_capstyle='round'         # 线端点圆润，视觉更友好
            )
            
            # ========== 第二段：水平箭头（从第i年峰值到第i+1年峰值） ==========
            horizontal_line = self.ax.plot(
                [i, i+1], [peak_y, peak_y],    # y固定为peak_y，x从i到i+1
                color=self.config['arrow_color'],
                linewidth=1.5,
                solid_capstyle='round'
            )
            
            # ========== 第三段：垂直向下箭头（从第i+1年峰值到柱顶） ==========
            self.ax.plot(
                [i+1, i+1], [peak_y, y2],      # x固定为i+1，y从peak_y到y2
                color=self.config['arrow_color'],
                linewidth=1.5,
                solid_capstyle='round'
            )
            
            # ========== 添加箭头指示符（在第三段终点） ==========
            # 箭头样式：'<'表示指向下方，适配垂直向下的线段
            self.ax.arrow(
                i+1, y2 + (peak_y - y2) * 0.1,  # 箭头起点（略高于柱顶）
                0, -5,                          # x方向无偏移，y方向向下5个单位
                head_width=0.05,                # 箭头宽度
                head_length=arrow_offset * 0.3, # 箭头长度
                fc=self.config['arrow_color'],  # 箭头填充色
                ec=self.config['arrow_color'],  # 箭头边框色
                length_includes_head=True       # 长度包含箭头头部
            )
            
            # ========== 添加增长率百分比标签 ==========
            # 计算标签位置：水平线段中点，y轴略高于峰值（避免重叠）
            label_x = i + 0.5                  # 水平中点
            label_y = peak_y + arrow_offset * 0.2
            
            # 格式化增长率标签：自动添加+/-符号，保留1位小数
            if rate >= 0:
                percentage_text = f'+{rate:.1f}%'  # 正增长加+号，更直观
            else:
                percentage_text = f'{rate:.1f}%'   # 负增长直接显示-号
            
            # 绘制带圆形背景的标签（核心视觉优化）
            self.ax.text(
                label_x, label_y,
                percentage_text,
                ha='center',
                va='center',
                fontsize=self.config['percentage_fontsize'],
                color='white',                   # 白色文字
                # 圆形背景配置：boxstyle='circle'创建圆形，fc=背景色，ec=边框色
                bbox=dict(
                    boxstyle='circle',
                    fc=self.config['percentage_background'],
                    ec='none',                   # 无边框，更简洁
                    alpha=0.9                   # 透明度，避免遮挡背景
                )
            )

    def save_chart(self):
        """
        保存图表到指定路径（公有方法）
        学习重点：
        1. 路径处理：使用Path类创建父目录，避免路径不存在报错
        2. 图片保存：设置bbox_inches='tight'，裁剪空白区域
        3. 异常处理：捕获保存异常，给出友好提示
        
        算法步骤：
        1. 获取输出路径，转换为Path对象（跨平台兼容）
        2. 创建父目录（如果不存在）
        3. 保存图表，设置dpi和bbox_inches参数
        4. 打印保存成功提示
        
        编程技巧：
        - 使用Path.mkdir(parents=True, exist_ok=True)，安全创建目录
        - bbox_inches='tight'：自动裁剪图表周围的空白，节省空间
        """
        try:
            # 转换为Path对象，支持跨平台路径操作
            output_path = Path(self.config['output_path'])
            
            # 创建父目录（如果不存在）：parents=True创建所有上级目录，exist_ok=True避免重复创建报错
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # 保存图表
            self.fig.savefig(
                output_path,
                dpi=self.config['dpi'],          # 分辨率
                bbox_inches='tight',            # 裁剪空白区域
                facecolor='white',              # 背景色为白色
                edgecolor='none'                # 无边框
            )
            
            # 打印提示信息，提升用户体验
            print(f"图表已成功保存到：{output_path.absolute()}")
        
        except Exception as e:
            # 捕获所有保存异常，给出友好提示
            raise RuntimeError(f"保存图表失败：{str(e)}") from e

    def plot(self):
        """
        主绘图方法（公有入口方法）
        学习重点：
        1. 流程封装：将所有绘图步骤封装为一个入口，降低使用复杂度
        2. 执行顺序：严格的步骤顺序，保证逻辑正确性
        3. 用户友好：入口方法简洁，无需关注内部实现
        
        执行流程（核心）：
        1. 初始化配置 → 2. 计算总计 → 3. 计算增长率 → 4. 绘制堆叠柱 → 
        5. 添加数据标签 → 6. 添加总计标签 → 7. 绘制箭头和增长率 → 8. 保存图表
        
        设计思路：
        - 公有方法仅负责调用私有方法，符合"封装"和"最小知识原则"
        - 步骤顺序不可打乱（例如：必须先计算总计，才能绘制总计标签）
        """
        # 步骤1：初始化配置
        self._setup_config(self.config if hasattr(self, 'config') else None)
        
        # 步骤2：计算每年总计
        self._calculate_totals()
        
        # 步骤3：计算环比增长率（至少2年数据才计算）
        if len(self.totals) >= 2:
            self._calculate_growth_rates()
        
        # 步骤4：绘制堆叠柱状图
        self._plot_stacked_bars()
        
        # 步骤5：添加数据标签
        self._add_data_labels()
        
        # 步骤6：添加总计标签
        self._add_total_labels()
        
        # 步骤7：绘制箭头和增长率（至少2年数据才绘制）
        if len(self.totals) >= 2:
            self._draw_arrows_and_percentages()
        
        # 步骤8：保存图表
        self.save_chart()


# =============================================================================
# main函数：示例入口
# =============================================================================
def main():
    """
    示例主函数：演示如何使用StackedBarChartWithArrow类生成图表
    学习重点：
    1. 数据准备：符合格式要求的二维数据、年份列表、区域列表
    2. 类的使用：实例化 → 调用plot方法，极简使用流程
    3. 自定义配置：通过config字典覆盖默认值，灵活定制
    
    示例数据说明：
    - 年份：2021-2024（4年）
    - 区域：华北、华东、华南、西南（4个区域）
    - 数据：二维列表，shape=(4,4)，对应[年份数, 区域数]
    """
    # ========== 1. 准备数据 ==========
    # 年份列表
    years = ['2021', '2022', '2023', '2024']
    # 区域列表
    regions = ['华北', '华东', '华南', '西南']
    # 颜色列表（与区域一一对应）
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
    # 核心数据：[年份][区域]
    data = [
        [120, 150, 90, 80],   # 2021年各区域数据
        [130, 160, 100, 85],  # 2022年各区域数据
        [140, 170, 110, 90],  # 2023年各区域数据
        [150, 180, 120, 95]   # 2024年各区域数据
    ]
    
    # ========== 2. 自定义配置（可选） ==========
    custom_config = {
        'figsize': (12, 9),                # 更大的图表尺寸
        'output_path': '环比箭头柱状图_示例.png',  # 自定义输出路径
        'title_fontsize': 16,              # 更大的标题字体
        'arrow_color': '#2c3e50',          # 自定义箭头颜色
        'percentage_background': '#ff7f0e' # 自定义增长率标签背景
    }
    
    # ========== 3. 初始化数据处理器（可选，演示高级用法） ==========
    processor = DataProcessor()
    # 准备图表数据（使用DataProcessor处理）
    df, processed_data = processor.prepare_chart_data(data, years, regions)
    
    # ========== 4. 实例化图表类并生成图表 ==========
    chart = StackedBarChartWithArrow(
        data=processed_data,
        years=years,
        regions=regions,
        colors=colors,
        config=custom_config,
        data_processor=processor
    )
    # 调用主绘图方法
    chart.plot()


# ========== 程序入口 ==========
if __name__ == '__main__':
    # 执行示例主函数
    main()
