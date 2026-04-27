
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from 环比箭头柱状图 import StackedBarChartWithArrow, DataProcessor, set_chinese_font


def main():
    print("=" * 70)
    print("使用 StackedBarChartWithArrow 类和 test_data.csv 生成图表")
    print("=" * 70)
    
    try:
        set_chinese_font()
        base_dir = Path(__file__).parent
        
        # 定义颜色
        colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
        
        # 配置图表
        config = {
            'figsize': (12, 10),
            'output_path': str(base_dir / 'test_data_生成结果.png'),
            'title_fontsize': 18,
            'label_fontsize': 14,
            'tick_fontsize': 13,
            'data_label_fontsize': 13,
            'percentage_fontsize': 12,
            'bar_width': 0.55,
            'dpi': 150
        }
        
        # 创建 DataProcessor 实例
        print("\n[1] 读取 test_data.csv 文件...")
        processor = DataProcessor()
        df = processor.read_file(str(base_dir / 'test_data.csv'))
        # 将年份列设置为索引
        df.set_index('年份', inplace=True)
        processor.original_data = df
        processor.processed_data = df
        print("✓ 文件读取成功!")
        
        # 打印数据信息
        years = list(df.index)
        regions = list(df.columns)
        print(f"年份: {years}")
        print(f"区域: {regions}")
        print(f"数据:")
        print(df)
        
        # 创建图表
        print("\n[2] 创建图表实例...")
        chart = StackedBarChartWithArrow(
            colors=colors,
            config=config,
            data_processor=processor
        )
        
        print("[2] 开始绘制图表...")
        chart.plot()
        
        print("\n✅ 图表生成成功!")
        print(f"📁 保存路径: {config['output_path']}")
        
        # 验证文件是否成功保存
        output_file = Path(config['output_path'])
        if output_file.exists():
            file_size = output_file.stat().st_size
            print(f"📊 文件大小: {file_size / 1024:.2f} KB")
        else:
            print("⚠️  警告: 文件未找到!")
        
        print("\n" + "=" * 70)
        print("程序执行完成，无崩溃或异常!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ 程序运行出错: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
