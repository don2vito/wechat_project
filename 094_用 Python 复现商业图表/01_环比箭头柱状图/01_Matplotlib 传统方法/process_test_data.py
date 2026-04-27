import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from 环比箭头柱状图 import DataProcessor


def main():
    print("=" * 70)
    print("使用 DataProcessor 类处理 test_data.csv 文件")
    print("=" * 70)
    
    # 创建 DataProcessor 实例
    processor = DataProcessor()
    
    # 步骤1: 读取文件
    print("\n[步骤1] 读取 test_data.csv 文件...")
    try:
        df = processor.read_file(Path(__file__).parent / 'test_data.csv')
        # 将年份列设置为索引
        df.set_index('年份', inplace=True)
        processor.original_data = df
        print("✓ 文件读取成功!")
        print("\n原始数据:")
        print(df)
    except Exception as e:
        print(f"✗ 文件读取失败: {str(e)}")
        return
    
    # 步骤2: 检测异常值
    print("\n[步骤2] 检测异常值...")
    try:
        outliers = processor.detect_outliers(method='iqr')
        if outliers:
            print("⚠️  检测到异常值:")
            for col, info in outliers.items():
                print(f"  - 列 {col}: {info['count']} 个异常值")
        else:
            print("✓ 未检测到异常值")
    except Exception as e:
        print(f"✗ 异常值检测失败: {str(e)}")
    
    # 步骤3: 处理缺失值
    print("\n[步骤3] 处理缺失值...")
    try:
        df_processed = processor.handle_missing_values(strategy='fill_zero')
        print("✓ 缺失值处理完成!")
    except Exception as e:
        print(f"✗ 缺失值处理失败: {str(e)}")
        return
    
    # 步骤4: 验证数据
    print("\n[步骤4] 验证数据有效性...")
    try:
        is_valid, errors = processor.validate_data(min_rows=2, min_cols=1)
        if is_valid:
            print("✓ 数据验证通过!")
        else:
            print("⚠️  数据验证警告:")
            for error in errors:
                print(f"  - {error}")
    except Exception as e:
        print(f"✗ 数据验证失败: {str(e)}")
        return
    
    # 步骤5: 计算统计信息
    print("\n[步骤5] 计算统计信息...")
    try:
        stats = processor.calculate_statistics()
        print("✓ 统计信息计算完成!")
        print("\n统计信息:")
        print(stats)
    except Exception as e:
        print(f"✗ 统计信息计算失败: {str(e)}")
    
    # 步骤6: 准备图表数据
    print("\n[步骤6] 准备图表数据...")
    try:
        df_chart, data_array = processor.prepare_chart_data()
        print("✓ 图表数据准备完成!")
    except Exception as e:
        print(f"✗ 图表数据准备失败: {str(e)}")
        return
    
    # 打印最终处理结果
    print("\n" + "=" * 70)
    print("数据处理完成! 处理后的数据结构如下:")
    print("=" * 70)
    print("\n📊 处理后的 DataFrame:")
    print(df_chart)
    
    print("\n📈 数值数组:")
    print(data_array)
    
    print("\n🏷️  年份标签:", list(df_chart.index))
    print("🏷️  区域标签:", list(df_chart.columns))
    
    print("\n" + "=" * 70)
    print("元数据信息:")
    print("=" * 70)
    metadata = processor.get_metadata()
    for key, value in metadata.items():
        print(f"  {key}: {value}")
    
    print("\n" + "=" * 70)
    print("数据处理成功，无异常!")
    print("=" * 70)


if __name__ == "__main__":
    main()
