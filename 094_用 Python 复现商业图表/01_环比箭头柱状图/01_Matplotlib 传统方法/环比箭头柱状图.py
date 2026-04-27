"""
环比箭头柱状图生成器

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
import matplotlib.pyplot as plt
# numpy: 高效的数值计算库，提供数组操作和数学函数
import numpy as np
# pandas: 强大的数据处理库，提供DataFrame数据结构和文件读写功能
import pandas as pd
# 从matplotlib.patches导入图形补丁类，用于创建特殊形状（本代码中未直接使用，但保留以便扩展）
from matplotlib.patches import FancyArrowPatch, ConnectionPatch
# 从pathlib导入Path类，提供面向对象的路径操作，比os.path更现代、更安全
from pathlib import Path
# platform: 用于获取操作系统信息，便于跨平台兼容
import platform
# 从typing导入类型提示工具，提高代码可读性和IDE支持
from typing import Union, List, Dict, Tuple, Optional
# warnings: 用于发出警告信息，而不是直接抛出异常
import warnings


# =============================================================================
# DataProcessor类：专业的数据处理工具
# =============================================================================
class DataProcessor:
    """
    DataProcessor类 - 专业的数据处理工具
    
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
        初始化数据处理器
        
        设计思路:
        初始化时仅创建空容器，不进行任何计算，遵循惰性加载原则。
        这样可以避免不必要的资源消耗，只有在真正需要时才进行处理。
        
        关键变量说明:
        - self.original_data: 存储原始数据，保留原始状态便于回溯
        - self.processed_data: 存储处理后的数据，用于实际使用
        - self.metadata: 存储处理元数据，记录数据变化过程
        """
        # 初始化原始数据为None，等待后续赋值
        self.original_data = None
        # 初始化处理后的数据为None，等待后续处理
        self.processed_data = None
        # 初始化元数据字典，用于记录数据处理的各个步骤和结果
        self.metadata = {}
    
    def read_file(self, file_path: Union[str, Path], **kwargs) -> pd.DataFrame:
        """
        读取CSV或Excel文件
        
        设计思路:
        提供统一的文件读取接口，自动识别文件格式并选择合适的读取方法。
        使用多态思想，让用户无需关心具体的文件格式细节。
        
        算法步骤:
        1. 将输入的文件路径转换为Path对象，确保跨平台兼容性
        2. 检查文件是否存在，不存在则抛出FileNotFoundError
        3. 根据文件后缀名判断文件格式（.csv或.xlsx/.xls）
        4. 使用对应的pandas函数读取文件内容
        5. 记录元数据，便于后续追踪
        6. 返回读取的DataFrame
        
        参数说明:
        - file_path: 文件路径，可以是字符串或Path对象
        - **kwargs: 额外参数，传递给pandas的读取函数
        
        返回值:
        - pandas.DataFrame: 读取的数据框
        
        异常处理:
        - FileNotFoundError: 文件不存在时抛出
        - ValueError: 不支持的文件格式时抛出
        - RuntimeError: 读取失败时抛出，并包含原始异常信息
        
        编程技巧:
        - 使用from e语法保留原始异常的堆栈信息，便于调试
        - 采用守卫子句模式，提前处理异常情况
        """
        # 步骤1：将输入的文件路径转换为Path对象
        # Path对象提供了更现代、更安全的路径操作方式，相比os.path有很多优势
        file_path = Path(file_path)
        
        # 步骤2：检查文件是否存在
        # 这是防御性编程的体现，在操作前先验证前置条件
        if not file_path.exists():
            raise FileNotFoundError(f"文件不存在: {file_path}")
        
        # 步骤3：获取文件后缀名并转为小写
        # suffix属性返回文件的扩展名（包括点号），lower()确保大小写不敏感
        suffix = file_path.suffix.lower()
        
        # 步骤4：根据文件格式选择读取方法
        try:
            # 如果是CSV文件，使用pd.read_csv()读取
            if suffix == '.csv':
                self.original_data = pd.read_csv(file_path, **kwargs)
            # 如果是Excel文件，使用pd.read_excel()读取
            elif suffix in ['.xlsx', '.xls']:
                self.original_data = pd.read_excel(file_path, **kwargs)
            # 如果是其他格式，抛出不支持的异常
            else:
                raise ValueError(f"不支持的文件格式: {suffix}")
            
            # 步骤5：记录元数据
            # 将文件路径、格式和原始形状记录到metadata字典中，便于调试和审计
            self.metadata['file_path'] = str(file_path)
            self.metadata['file_format'] = suffix
            self.metadata['original_shape'] = self.original_data.shape
            
            # 步骤6：返回读取的数据
            return self.original_data
            
        # 步骤7：异常处理
        except Exception as e:
            # 使用from e语法保留原始异常，方便定位问题根源
            raise RuntimeError(f"读取文件失败: {str(e)}") from e
    
    def handle_missing_values(self, 
                               strategy: str = 'fill_zero',
                               fill_value: Union[int, float, str] = 0,
                               axis: int = 0,
                               inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        处理缺失值
        
        设计思路:
        提供多种缺失值处理策略，让用户根据数据特点选择最适合的方法。
        这是策略模式的一个典型应用，将算法族封装起来，使它们可以互换。
        
        支持的处理策略:
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
        
        编程技巧:
        - 使用早期返回模式，提前处理异常情况
        - 使用select_dtypes()方法筛选数值列，避免对非数值列执行统计操作
        - 采用copy()方法创建数据副本，避免意外修改原始数据
        """
        # 步骤1：验证前置条件：必须先读取数据
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：决定操作对象：原始数据或副本
        # 如果inplace=True，直接操作原始数据；否则创建副本进行操作
        df = self.original_data if inplace else self.original_data.copy()
        
        # 步骤3：根据策略执行缺失值处理
        # 使用if-elif-else结构实现策略选择
        if strategy == 'fill_zero':
            # 策略1：用0填充所有缺失值
            # fillna()是pandas处理缺失值的核心方法
            df = df.fillna(0)
        elif strategy == 'fill_mean':
            # 策略2：用平均值填充（仅对数值列）
            # select_dtypes(include=[np.number])筛选出所有数值列
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            # 对每个数值列，用该列的平均值填充缺失值
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        elif strategy == 'fill_median':
            # 策略3：用中位数填充（仅对数值列）
            # 中位数比平均值更稳健，不受异常值影响
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
        elif strategy == 'fill_value':
            # 策略4：用用户指定的值填充
            # 这是最灵活的方式，用户可以指定任何值
            df = df.fillna(fill_value)
        elif strategy == 'drop':
            # 策略5：删除包含缺失值的行或列
            # axis=0删除行，axis=1删除列
            df = df.dropna(axis=axis)
        else:
            # 如果策略不在支持列表中，抛出异常
            raise ValueError(f"不支持的策略: {strategy}")
        
        # 步骤4：记录处理的缺失值数量
        # 计算原始数据的缺失值总数减去处理后的缺失值总数
        self.metadata['missing_values_removed'] = self.original_data.isna().sum().sum() - df.isna().sum().sum()
        
        # 步骤5：更新实例属性并返回
        if inplace:
            # 如果是原地修改，更新original_data和processed_data
            self.original_data = df
            self.processed_data = df
        else:
            # 如果不是原地修改，只更新processed_data
            self.processed_data = df
        
        # 根据inplace参数决定返回值
        return self.processed_data if not inplace else None
    
    def detect_outliers(self, 
                        method: str = 'iqr',
                        threshold: float = 1.5,
                        columns: Optional[List[str]] = None) -> Dict:
        """
        检测异常值
        
        设计思路:
        提供两种常用的异常值检测方法，让用户根据数据分布选择合适的方法。
        不直接删除异常值，而是先检测并报告，让用户决定如何处理。
        
        支持的检测方法:
        1. 'iqr': 四分位距方法
           - 优点：对异常值不敏感，适合大多数数据分布
           - 原理：Q1-1.5*IQR ~ Q3+1.5*IQR范围外的数据视为异常值
           - 适用场景：数据分布不对称或有明显异常值
        
        2. 'zscore': Z-score方法（标准化分数）
           - 优点：计算简单，基于正态分布假设
           - 原理：数据点与均值的距离超过多少个标准差视为异常值
           - 适用场景：数据近似服从正态分布
        
        算法步骤（IQR方法）:
        1. 计算第一四分位数(Q1)：25%分位数
        2. 计算第三四分位数(Q3)：75%分位数
        3. 计算四分位距(IQR)：IQR = Q3 - Q1
        4. 计算下界：lower_bound = Q1 - threshold * IQR
        5. 计算上界：upper_bound = Q3 + threshold * IQR
        6. 标记超出[lower_bound, upper_bound]范围的数据为异常值
        
        参数说明:
        - method: 检测方法，'iqr'或'zscore'，默认为'iqr'
        - threshold: 异常值判定阈值，IQR方法默认为1.5
        - columns: 指定要检测的列，None表示所有数值列
        
        返回值:
        - Dict: 包含异常值信息的字典
        
        编程技巧:
        - 使用布尔掩码技术高效筛选异常值
        - 采用向量化操作避免显式循环，提高性能
        - 使用字典存储结果，结构化地组织异常值信息
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据
        # 如果processed_data存在，使用它；否则使用original_data
        df = self.processed_data if self.processed_data is not None else self.original_data
        
        # 步骤3：确定要检测的列
        # 如果用户没有指定列，自动选择所有数值列
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 步骤4：初始化异常值信息字典
        outliers_info = {}
        
        # 步骤5：逐个列检测异常值
        for col in columns:
            # 跳过不存在的列（防御性编程）
            if col not in df.columns:
                continue
                
            # 根据方法选择检测算法
            if method == 'iqr':
                # IQR方法
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - threshold * IQR
                upper_bound = Q3 + threshold * IQR
                outliers_mask = (df[col] < lower_bound) | (df[col] > upper_bound)
            elif method == 'zscore':
                # Z-score方法
                z_scores = np.abs((df[col] - df[col].mean()) / df[col].std())
                outliers_mask = z_scores > threshold
            else:
                raise ValueError(f"不支持的方法: {method}")
            
            # 步骤6：统计异常值信息
            outliers_count = outliers_mask.sum()
            if outliers_count > 0:
                outliers_info[col] = {
                    'count': int(outliers_count),
                    'indices': df[outliers_mask].index.tolist(),
                    'values': df[col][outliers_mask].tolist()
                }
        
        # 步骤7：记录元数据并返回结果
        self.metadata['outliers_detected'] = outliers_info
        return outliers_info
    
    def remove_outliers(self,
                       method: str = 'iqr',
                       threshold: float = 1.5,
                       columns: Optional[List[str]] = None,
                       inplace: bool = False) -> Optional[pd.DataFrame]:
        """
        移除异常值
        
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
        
        编程技巧:
        - 使用|=（按位或赋值）操作符累积异常值掩码
        - 使用pd.Series()创建布尔序列，确保与DataFrame索引对齐
        - 使用~（逻辑非）操作符反转掩码，选择非异常值
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据
        df = self.processed_data if self.processed_data is not None else self.original_data.copy()
        
        # 步骤3：确定要处理的列
        if columns is None:
            columns = df.select_dtypes(include=[np.number]).columns.tolist()
        
        # 步骤4：初始化全局异常值掩码
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
            
            # 使用|=操作符将当前列的异常值合并到全局掩码
            outliers_mask |= col_outliers
        
        # 步骤6：移除异常值
        removed_count = int(outliers_mask.sum())
        df_clean = df[~outliers_mask]
        
        # 步骤7：记录元数据
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
        转换数据类型
        
        设计思路:
        提供灵活的数据类型转换功能，支持显式映射和自动推断两种方式。
        使用try-except捕获转换失败，避免因个别列导致整个程序崩溃。
        
        参数说明:
        - dtype_map: 列名到数据类型的映射字典
        - numeric_only: 是否只尝试转换为数值类型
        - inplace: 是否在原地修改
        
        返回值:
        - Optional[pd.DataFrame]: 处理后的数据框（如果inplace=False）
        """
        # 步骤1：验证前置条件
        if self.original_data is None:
            raise ValueError("请先读取数据")
        
        # 步骤2：确定要处理的数据
        df = self.processed_data if self.processed_data is not None else self.original_data.copy()
        
        # 步骤3：显式类型映射转换
        if dtype_map:
            for col, dtype in dtype_map.items():
                if col in df.columns:
                    try:
                        df[col] = df[col].astype(dtype)
                    except Exception as e:
                        warnings.warn(f"转换列 {col} 失败: {str(e)}")
        
        # 步骤4：自动数值化转换
        if numeric_only:
            for col in df.columns:
                try:
                    df[col] = pd.to_numeric(df[col], errors='ignore')
                except:
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
        验证数据有效性
        
        设计思路:
        在绘图前验证数据质量，避免因数据问题导致绘图失败。
        采用收集所有错误后统一返回的策略，让用户一次性了解所有问题。
        
        参数说明:
        - min_rows: 最小行数要求，默认为2
        - min_cols: 最小列数要求，默认为1
        - check_positive: 是否检查数值是否为非负，默认为True
        - check_numeric: 是否检查所有数据是否为数值型，默认为True
        
        返回值:
        - Tuple[bool, List[str]]: (是否有效, 错误信息列表)
        """
        # 步骤1：确定要验证的数据
        df = self.processed_data if self.processed_data is not None else self.original_data
        
        # 步骤2：检查数据是否存在
        if df is None:
            return False, ["请先读取数据"]
        
        # 步骤3：初始化错误列表
        errors = []
        
        # 步骤4：验证行数
        if len(df) < min_rows:
            errors.append(f"数据行数不足，至少需要 {min_rows} 行，当前有 {len(df)} 行")
        
        # 步骤5：验证列数
        if len(df.columns) < min_cols:
            errors.append(f"数据列数不足，至少需要 {min_cols} 列，当前有 {len(df.columns)} 列")
        
        # 步骤6：验证数值类型
        if check_numeric:
            non_numeric_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
            if non_numeric_cols:
                errors.append(f"存在非数值列: {non_numeric_cols}")
        
        # 步骤7：验证非负值
        if check_positive:
            numeric_cols = df.select_dtypes(include=[np.number]).columns
            for col in numeric_cols:
                if (df[col] < 0).any():
                    errors.append(f"列 {col} 包含负值")
        
        # 步骤8：确定验证结果
        is_valid = len(errors) == 0
        
        # 步骤9：记录元数据
        self.metadata['validation_result'] = is_valid
        self.metadata['validation_errors'] = errors
        
        # 步骤10：返回结果
        return is_valid, errors
    
    def calculate_statistics(self, 
                            columns: Optional[List[str]] = None) -> pd.DataFrame:
        """
        计算统计指标
        
        设计思路:
        提供丰富的描述性统计信息，帮助用户了解数据特征。
        在pandas内置describe()的基础上，添加额外的统计指标。
        
        参数说明:
        - columns: 指定要计算的列，None表示所有数值列
        
        返回值:
        - pd.DataFrame: 包含统计信息的数据框
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
        stats = df[columns].describe()
        
        # 步骤5：计算并添加额外的统计指标
        additional_stats = pd.DataFrame(index=['sum', 'median', 'variance'])
        for col in columns:
            additional_stats.loc['sum', col] = df[col].sum()
            additional_stats.loc['median', col] = df[col].median()
            additional_stats.loc['variance', col] = df[col].var()
        
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
        """
        # 步骤1：处理用户提供的数据（如果有）
        if data is not None:
            if isinstance(data, pd.DataFrame):
                df = data.copy()
            else:
                data = np.array(data)
                if years is None:
                    years = [f'Year_{i+1}' for i in range(data.shape[0])]
                if regions is None:
                    regions = [f'Region_{i+1}' for i in range(data.shape[1])]
                df = pd.DataFrame(data, index=years, columns=regions)
            self.original_data = df
            self.processed_data = df
        else:
            # 步骤2：使用DataProcessor已有的数据
            if self.processed_data is None:
                raise ValueError("请先提供数据或读取文件")
            df = self.processed_data.copy()
        
        # 步骤3：数据清洗
        df = df.fillna(0)
        df = df.astype(float)
        df_clean = df[(df >= 0).all(axis=1)]
        processed_data = df_clean.values
        
        # 步骤4：更新实例属性
        if self.original_data is None:
            self.original_data = df_clean
        self.processed_data = df_clean
        
        # 步骤5：返回结果
        return df_clean, processed_data
    
    def get_metadata(self) -> Dict:
        """
        获取处理元数据
        
        返回值:
        - Dict: 处理元数据的副本
        """
        return self.metadata.copy()
    
    def reset(self):
        """
        重置处理器状态
        """
        self.original_data = None
        self.processed_data = None
        self.metadata = {}


# =============================================================================
# set_chinese_font函数：配置中文字体
# =============================================================================
def set_chinese_font():
    """
    配置中文字体设置
    
    功能概述:
    根据不同操作系统自动选择合适的中文字体，确保图表中的中文能正常显示。
    这是Matplotlib中文显示问题的标准解决方案。
    
    算法原理:
    1. 获取当前操作系统名称
    2. 根据操作系统选择对应的字体列表
    3. 逐个尝试设置字体，直到找到可用的字体
    4. 同时设置负号显示为正常字符
    
    操作系统字体策略:
    - Windows系统：优先使用黑体、微软雅黑、宋体
    - macOS系统：优先使用华文黑体、黑体
    - Linux系统：优先使用文泉驿微米黑
    - 回退方案：如果所有字体都不可用，则回退到DejaVu Sans
    """
    # 获取当前操作系统名称
    system_name = platform.system()
    
    # 根据操作系统选择字体列表
    if system_name == 'Windows':
        font_names = ['SimHei', 'Microsoft YaHei', 'SimSun']
    elif system_name == 'Darwin':
        font_names = ['Heiti TC', 'Heiti SC', 'Arial Unicode MS']
    else:
        font_names = ['WenQuanYi Micro Hei', 'Droid Sans Fallback']
    
    # 逐个尝试设置字体
    for font_name in font_names:
        try:
            plt.rcParams['font.sans-serif'] = [font_name]
            plt.rcParams['axes.unicode_minus'] = False
            return
        except:
            continue
    
    # 如果所有字体都不可用，使用回退方案
    plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False


# =============================================================================
# load_and_process_data函数：数据加载和处理
# =============================================================================
def load_and_process_data(data, years, regions):
    """
    使用pandas读取、清洗和转换数据
    
    功能概述:
    将原始数据转换为 pandas DataFrame 格式，并进行数据清洗，确保数据质量。
    
    算法步骤:
    1. 创建 DataFrame，将年份设为索引，区域设为列名
    2. 填充缺失值为 0
    3. 转换数据类型为浮点型
    4. 筛选出所有值都非负的行
    5. 提取纯数值数组供后续计算使用
    
    参数说明:
    - data: 原始数据二维列表或数组
    - years: 年份标签列表
    - regions: 区域名称列表
    
    返回值:
    - pandas.DataFrame: 处理后的数据框
    - numpy.ndarray: 处理后的数值数组
    """
    # 创建DataFrame
    df = pd.DataFrame(data, index=years, columns=regions)
    
    # 填充缺失值为0
    df = df.fillna(0)
    
    # 转换为浮点类型
    df = df.astype(float)
    
    # 筛选非负数据
    df_clean = df[(df >= 0).all(axis=1)]
    
    # 提取数值数组
    processed_data = df_clean.values
    
    # 返回处理后的数据
    return df_clean, processed_data


# =============================================================================
# StackedBarChartWithArrow类：带环比箭头的堆叠柱状图
# =============================================================================
class StackedBarChartWithArrow:
    """
    带环比箭头的堆叠柱状图类
    
    功能概述:
    核心功能类，用于生成商业级别的堆叠柱状图，并在年份之间添加直角样式的环比增长率箭头。
    
    主要属性:
    - self.df: pandas.DataFrame，清洗后的数据框
    - self.data: numpy.ndarray，清洗后的数值数组
    - self.years: list，年份标签列表
    - self.regions: list，区域名称列表
    - self.colors: list，各区域对应的颜色列表
    - self.config: dict，完整的配置字典
    - self.data_processor: DataProcessor，数据处理器实例
    """
    
    def __init__(self, data=None, years=None, regions=None, colors=None, config=None, data_processor=None):
        """
        初始化堆叠柱状图实例
        
        初始化流程:
        1. 保存data_processor引用（如果提供）
        2. 如果提供了data_processor，使用其prepare_chart_data()方法准备数据
        3. 否则使用传统方式load_and_process_data()加载并处理原始数据
        4. 从DataFrame中提取years和regions
        5. 保存colors
        6. 加载默认配置
        7. 用用户配置覆盖默认配置
        8. 验证输入参数的有效性
        
        参数说明:
        - data: 二维列表或数组
        - years: 年份标签列表
        - regions: 区域名称列表
        - colors: 每个区域的颜色列表
        - config: 可选的配置字典
        - data_processor: DataProcessor实例
        """
        # 保存data_processor引用
        self.data_processor = data_processor
        
        # 根据是否有data_processor选择数据准备方式
        if data_processor is not None:
            self.df, self.data = data_processor.prepare_chart_data(data, years, regions)
        else:
            self.df, self.data = load_and_process_data(data, years, regions)
        
        # 从DataFrame中提取years和regions
        self.years = list(self.df.index)
        self.regions = list(self.df.columns)
        
        # 保存colors
        self.colors = colors
        
        # 加载默认配置
        self.config = self._default_config()
        
        # 用用户配置覆盖默认配置
        if config:
            self.config.update(config)
        
        # 验证输入参数
        self._validate_inputs()
    
    @classmethod
    def from_file(cls, file_path, colors, config=None, **read_kwargs):
        """
        从文件创建图表实例（使用DataProcessor）
        
        参数说明:
        - file_path: 文件路径
        - colors: 每个区域的颜色列表
        - config: 可选的配置字典
        - **read_kwargs: 传递给文件读取函数的额外参数
        
        返回值:
        - StackedBarChartWithArrow: 创建的图表实例
        """
        processor = DataProcessor()
        processor.read_file(file_path, **read_kwargs)
        return cls(colors=colors, config=config, data_processor=processor)
    
    def _validate_inputs(self):
        """
        验证输入参数的有效性
        """
        if self.data.ndim != 2:
            raise ValueError("数据必须是二维数组或列表")
        
        if self.data.shape[0] != len(self.years):
            raise ValueError(f"数据行数({self.data.shape[0]})必须与年份数量({len(self.years)})匹配")
        
        if self.data.shape[1] != len(self.regions):
            raise ValueError(f"数据列数({self.data.shape[1]})必须与区域数量({len(self.regions)})匹配")
        
        if len(self.colors) != len(self.regions):
            raise ValueError(f"颜色数量({len(self.colors)})必须与区域数量({len(self.regions)})匹配")
        
        if self.data.shape[0] < 2:
            raise ValueError("至少需要2年的数据才能计算环比增长率")
    
    def _default_config(self):
        """
        获取默认配置
        
        返回值:
        - dict: 包含所有默认配置项的字典
        """
        return {
            'figsize': (10, 10),
            'title': '',
            'xlabel': '',
            'ylabel': '',
            'ylabel_rotation': 90,
            'bar_width': 0.55,
            'title_fontsize': 18,
            'label_fontsize': 14,
            'tick_fontsize': 13,
            'data_label_fontsize': 13,
            'dpi': 150,
            'output_path': 'output.png',
            'arrow_color': '#333333',
            'percentage_background': '#2c3e50',
            'percentage_color': 'white',
            'percentage_fontsize': 12
        }
    
    def calculate_totals(self):
        """
        计算每年的总数值
        
        返回值:
        - numpy.ndarray: 每年的总值数组
        """
        return np.sum(self.data, axis=1)
    
    def calculate_growth(self):
        """
        计算环比增长率（百分比）
        
        数学公式:
        环比增长率 = (本期值 - 上期值) / 上期值 × 100%
        
        返回值:
        - numpy.ndarray: 环比增长率数组
        """
        totals = self.calculate_totals()
        growth = ((totals[1:] - totals[:-1]) / totals[:-1]) * 100
        return growth
    
    def plot(self):
        """
        绘制堆叠柱状图并保存
        
        绘图流程:
        1. 创建图形和轴对象
        2. 计算x轴位置
        3. 初始化bottom数组
        4. 循环绘制每个区域的柱状图
        5. 添加总数值标签
        6. 添加环比箭头和增长率标签
        7. 设置坐标轴和图例
        8. 调整布局
        9. 保存图片
        10. 关闭图形
        """
        try:
            # 创建图形和轴对象
            fig, ax = plt.subplots(
                figsize=self.config['figsize'],
                dpi=self.config['dpi']
            )
            
            # 计算x轴位置
            x = np.arange(len(self.years))
            
            # 初始化bottom数组
            bottom = np.zeros(len(self.years))
            
            # 循环绘制每个区域的柱状图
            for i in range(len(self.regions)):
                # 绘制当前区域的柱状图
                bars = ax.bar(
                    x,
                    self.data[:, i],
                    self.config['bar_width'],
                    bottom=bottom,
                    color=self.colors[i],
                    label=self.regions[i]
                )
                # 添加数据标签
                self._add_data_labels(ax, bars, bottom, self.data[:, i])
                # 更新bottom数组
                bottom += self.data[:, i]
            
            # 添加总数值标签
            self._add_total_labels(ax, x, bottom)
            
            # 添加环比箭头和增长率标签
            self._add_arrows(ax, x, bottom)
            
            # 设置坐标轴
            ax.set_xticks(x)
            ax.set_xticklabels(self.years, fontsize=self.config['tick_fontsize'])
            ax.set_yticks([])
            
            # 隐藏上、右、左边框
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            
            # 设置图例
            ax.legend(
                loc='upper center',
                bbox_to_anchor=(0.5, 1.12),
                ncol=3,
                frameon=False,
                fontsize=11
            )
            
            # 调整布局
            plt.tight_layout()
            
            # 保存图片
            output_path = Path(self.config['output_path'])
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            plt.savefig(
                str(output_path),
                dpi=self.config['dpi'],
                bbox_inches='tight'
            )
            
            # 关闭图形
            plt.close(fig)
            
        except Exception as e:
            plt.close('all')
            raise RuntimeError(f"绘图过程中发生错误: {str(e)}") from e
    
    def _add_data_labels(self, ax, bars, bottom, values):
        """
        在堆叠柱状图的每个分段上添加数据标签
        
        数据格式说明:
        - 使用带千分位分隔符的整数格式
        """
        for bar, b, val in zip(bars, bottom, values):
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,
                    b + height / 2,
                    f'{int(val):,}',
                    ha='center',
                    va='center',
                    fontsize=self.config['data_label_fontsize'],
                    color='white',
                    fontweight='semibold'
                )
    
    def _add_total_labels(self, ax, x, totals):
        """
        在每个堆叠柱状图顶部添加总数值标签
        """
        for i, total in enumerate(totals):
            ax.text(
                x[i],
                total + 3,
                f'{int(total):,}',
                ha='center',
                va='bottom',
                fontsize=self.config['data_label_fontsize'] + 2,
                fontweight='bold',
                color='#333333'
            )
    
    def _add_arrows(self, ax, x, totals):
        """
        在年份之间添加直角样式环比增长率箭头和百分比标签
        """
        growth = self.calculate_growth()
        num_arrows = len(growth)
        
        if num_arrows == 0:
            return
        
        # 计算基础几何参数
        max_total = np.max(totals)
        BASE_OFFSET_Y = 18
        VERTICAL_RISE_FACTOR = 0.22
        LABEL_OFFSET_FROM_PEAK = 12
        ARROW_HEAD_WIDTH = 0.06
        ARROW_HEAD_LENGTH = 6
        LINE_WIDTH = 1.2
        ENDPOINT_SPACING = 0.15
        
        base_offset = max_total * VERTICAL_RISE_FACTOR
        arrow_info = []
        
        # 收集所有箭头信息
        for i in range(num_arrows):
            start_x = x[i] + ENDPOINT_SPACING
            start_y = totals[i] + BASE_OFFSET_Y
            end_x = x[i + 1] - ENDPOINT_SPACING
            end_y = totals[i + 1] + BASE_OFFSET_Y
            base_peak_y = max(start_y, end_y)
            peak_y = base_peak_y + base_offset
            
            arrow_info.append({
                'index': i,
                'start_x': start_x,
                'start_y': start_y,
                'end_x': end_x,
                'end_y': end_y,
                'peak_y': peak_y,
                'growth': growth[i],
                'adjusted_peak_y': peak_y
            })
        
        # 检测并解决坐标冲突
        self._detect_and_resolve_conflicts(arrow_info, base_offset)
        
        # 逐个绘制箭头
        for info in arrow_info:
            i = info['index']
            start_x = info['start_x']
            start_y = info['start_y']
            end_x = info['end_x']
            end_y = info['end_y']
            peak_y = info['adjusted_peak_y']
            
            # 计算折线路径的中间点
            mid1_x = start_x
            mid1_y = peak_y
            mid2_x = end_x
            mid2_y = peak_y
            
            # 绘制完整的直角折线路径
            ax.plot(
                [start_x, mid1_x, mid2_x, end_x],
                [start_y, mid1_y, mid2_y, end_y],
                color=self.config['arrow_color'],
                linewidth=LINE_WIDTH,
                zorder=3,
                solid_capstyle='round'
            )
            
            # 绘制终点箭头
            arrow_start_x = mid2_x
            arrow_start_y = mid2_y
            arrow_end_y = end_y
            arrow_length = arrow_end_y - arrow_start_y
            
            ax.arrow(
                arrow_start_x,
                arrow_start_y,
                0,
                arrow_length - ARROW_HEAD_LENGTH,
                head_width=ARROW_HEAD_WIDTH,
                head_length=ARROW_HEAD_LENGTH,
                fc=self.config['arrow_color'],
                ec=self.config['arrow_color'],
                length_includes_head=True,
                zorder=3,
                linewidth=0
            )
            
            # 绘制增长率标签
            label_x = (start_x + end_x) / 2
            label_y = peak_y
            
            bbox = dict(
                boxstyle="circle,pad=0.35",
                facecolor=self.config['percentage_background'],
                edgecolor='none',
                alpha=1.0
            )
            
            growth_value = info['growth']
            if growth_value >= 0:
                rate_text = f'+{int(round(growth_value))}%'
            else:
                rate_text = f'{int(round(growth_value))}%'
            
            ax.text(
                label_x,
                label_y,
                rate_text,
                ha='center',
                va='center',
                color=self.config['percentage_color'],
                fontsize=self.config['percentage_fontsize'] + 1,
                fontweight='bold',
                bbox=bbox,
                zorder=4
            )
    
    def _detect_and_resolve_conflicts(self, arrow_info, base_offset):
        """
        检测箭头坐标冲突并自动调整
        """
        if len(arrow_info) < 2:
            return
        
        max_iterations = 50
        step_size = base_offset * 0.5
        label_height = base_offset * 0.3
        
        for iteration in range(max_iterations):
            has_conflict = False
            
            for i in range(len(arrow_info) - 1):
                arrow1 = arrow_info[i]
                arrow2 = arrow_info[i + 1]
                
                y1_top = arrow1['adjusted_peak_y'] + label_height
                y1_bottom = arrow1['adjusted_peak_y'] - label_height
                y2_top = arrow2['adjusted_peak_y'] + label_height
                y2_bottom = arrow2['adjusted_peak_y'] - label_height
                
                overlap = (y1_bottom < y2_top) and (y2_bottom < y1_top)
                
                if overlap:
                    has_conflict = True
                    
                    if i % 2 == 0:
                        arrow1['adjusted_peak_y'] += step_size
                        arrow2['adjusted_peak_y'] -= step_size
                    else:
                        arrow1['adjusted_peak_y'] -= step_size
                        arrow2['adjusted_peak_y'] += step_size
            
            if not has_conflict:
                break
        
        min_peak = min(info['peak_y'] for info in arrow_info)
        for info in arrow_info:
            if info['adjusted_peak_y'] < min_peak:
                info['adjusted_peak_y'] = min_peak


# =============================================================================
# main函数：主函数
# =============================================================================
def main():
    """
    主函数：生成环比箭头柱状图
    """
    try:
        set_chinese_font()
        base_dir = Path(r'd:\project\用 Python 复现商业图表\01_环比箭头柱状图')
        regions = ['东南亚', '北欧', '美国']
        colors = ['#c82423', '#e97451', '#f8b195']
        
        print("=" * 60)
        print("方式一：使用Python列表直接生成图表（传统方式）")
        print("=" * 60)
        
        years = ['2024', '2025', '2026']
        data = [
            [48, 78, 80],
            [56, 120, 157],
            [61, 202, 260]
        ]
        
        config = {
            'figsize': (10, 10),
            'output_path': str(base_dir / '环比箭头柱状图_生成结果.png'),
            'title_fontsize': 18,
            'label_fontsize': 14,
            'tick_fontsize': 13,
            'data_label_fontsize': 13,
            'percentage_fontsize': 12,
            'bar_width': 0.55,
            'dpi': 150
        }
        
        chart = StackedBarChartWithArrow(data, years, regions, colors, config)
        chart.plot()
        print(f"图表已成功生成: {config['output_path']}")
        
        print("\n" + "=" * 60)
        print("方式二：使用DataProcessor从文件读取（示例代码，取消注释即可使用）")
        print("=" * 60)
        print("""
        # 示例：从CSV文件读取并生成图表
        processor = DataProcessor()
        processor.read_file(str(base_dir / 'data.csv'))
        chart_from_file = StackedBarChartWithArrow(
            colors=colors, 
            config=config, 
            data_processor=processor
        )
        chart_from_file.plot()
        """)
        
    except Exception as e:
        print(f"程序运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
