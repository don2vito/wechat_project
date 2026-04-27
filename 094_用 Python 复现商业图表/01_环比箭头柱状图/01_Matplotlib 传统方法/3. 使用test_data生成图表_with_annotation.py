# 导入系统模块，用于处理Python解释器相关的配置和路径
import sys
# 从pathlib模块导入Path类，用于便捷地处理文件和目录路径（面向对象的路径操作）
from pathlib import Path
# 将当前脚本所在目录添加到Python的系统路径中
# 目的：让Python能找到同目录下的自定义模块（如"环比箭头柱状图"）
sys.path.append(str(Path(__file__).parent))

# 从自定义模块"环比箭头柱状图"中导入三个核心组件：
# StackedBarChartWithArrow：带箭头的堆叠柱状图绘制类
# DataProcessor：数据处理工具类（负责读取、清洗数据等）
# set_chinese_font：设置Matplotlib显示中文的函数（解决中文乱码问题）
from 环比箭头柱状图 import StackedBarChartWithArrow, DataProcessor, set_chinese_font


def main():
    """
    主函数：程序的核心执行逻辑
    功能：读取test_data.csv数据 → 配置图表参数 → 生成带箭头的堆叠柱状图 → 验证文件保存
    返回值：0表示执行成功，1表示执行失败
    """
    # 打印分隔线，提升控制台输出的可读性（视觉分隔）
    print("=" * 70)
    print("使用 StackedBarChartWithArrow 类和 test_data.csv 生成图表")
    print("=" * 70)
    
    try:
        # 第一步：设置Matplotlib的中文字体
        # 解决图表中中文标签、标题显示为方块/乱码的问题
        set_chinese_font()
        
        # 获取当前脚本所在的目录路径（Path对象）
        # Path(__file__)：当前脚本文件的路径；.parent：获取父目录（即脚本所在文件夹）
        base_dir = Path(__file__).parent
        
        # 定义堆叠柱状图的配色方案（RGB十六进制颜色码）
        # 按顺序为不同系列的柱子分配颜色，提升图表视觉区分度
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        
        # 第二步：配置图表的核心参数（字典形式，便于维护和修改）
        config = {
            'figsize': (12, 10),          # 图表画布尺寸：宽12英寸，高10英寸
            'output_path': str(base_dir / 'test_data_生成结果.png'),  # 图表保存路径（拼接目录+文件名）
            'title_fontsize': 18,         # 图表标题字体大小
            'label_fontsize': 14,         # 坐标轴标签（x/y轴名称）字体大小
            'tick_fontsize': 13,          # 坐标轴刻度（x/y轴数值）字体大小
            'data_label_fontsize': 13,    # 柱子上数据标签的字体大小
            'percentage_fontsize': 12,    # 百分比标签的字体大小
            'bar_width': 0.55,            # 柱状图柱子的宽度（0-1之间，越大越宽）
            'dpi': 150                    # 图表保存的分辨率（dots per inch），150为高清常用值
        }
        
        # 第三步：读取并处理数据
        print("\n[1] 读取 test_data.csv 文件...")
        # 创建数据处理器实例（初始化DataProcessor类）
        processor = DataProcessor()
        # 调用read_file方法读取CSV文件，传入文件路径（当前目录下的test_data.csv）
        # 返回值为pandas的DataFrame（表格型数据结构）
        df = processor.read_file(str(base_dir / 'test_data.csv'))
        # 将"年份"列设置为DataFrame的索引（行标签），方便后续按年份筛选/展示数据
        # inplace=True：直接修改原DataFrame，不创建新副本
        df.set_index('年份', inplace=True)
        # 将原始数据赋值给processor的属性（便于后续图表类调用）
        processor.original_data = df
        # 将处理后的数据（此处未清洗，直接复用）赋值给processor的属性
        processor.processed_data = df
        print("✓ 文件读取成功!")
        
        # 打印数据关键信息，用于控制台校验数据是否正确读取
        years = list(df.index)          # 提取所有年份（索引转列表）
        regions = list(df.columns)      # 提取所有区域（列名转列表）
        print(f"年份: {years}")         # 打印年份列表
        print(f"区域: {regions}")       # 打印区域列表
        print(f"数据:")
        print(df)                       # 打印完整的DataFrame数据
        
        # 第四步：创建并绘制图表
        print("\n[2] 创建图表实例...")
        # 实例化带箭头的堆叠柱状图类，传入三个核心参数：
        # colors：柱子配色；config：图表样式配置；data_processor：数据处理器（含数据）
        chart = StackedBarChartWithArrow(
            colors=colors,
            config=config,
            data_processor=processor
        )
        
        print("[2] 开始绘制图表...")
        # 调用plot方法执行图表绘制（核心操作，包含绘图、添加标签、箭头、保存等逻辑）
        chart.plot()
        
        # 第五步：验证图表保存结果
        print("\n✅ 图表生成成功!")
        print(f"📁 保存路径: {config['output_path']}")
        
        # 将保存路径转为Path对象，用于文件存在性校验
        output_file = Path(config['output_path'])
        if output_file.exists():
            # 获取文件大小（字节），转换为KB并保留2位小数，打印供参考
            file_size = output_file.stat().st_size
            print(f"📊 文件大小: {file_size / 1024:.2f} KB")
        else:
            # 文件不存在时打印警告
            print("⚠️  警告: 文件未找到!")
        
        # 打印结束分隔线，标识程序执行完成
        print("\n" + "=" * 70)
        print("程序执行完成，无崩溃或异常!")
        print("=" * 70)
        
    # 捕获所有异常（防止程序崩溃，便于调试）
    except Exception as e:
        # 打印异常信息
        print(f"\n❌ 程序运行出错: {str(e)}")
        # 导入traceback模块，打印详细的异常堆栈信息（定位错误行）
        import traceback
        traceback.print_exc()
        # 返回1表示程序执行失败（供脚本退出码判断）
        return 1
    
    # 返回0表示程序执行成功
    return 0


# 脚本入口判断：仅当脚本被直接运行时（而非被导入为模块），才执行main函数
if __name__ == "__main__":
    # 调用main函数，并将返回值作为脚本的退出码（0=成功，1=失败）
    exit(main())
