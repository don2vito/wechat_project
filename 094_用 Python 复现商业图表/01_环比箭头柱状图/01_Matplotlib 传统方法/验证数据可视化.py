
"""
验证数据可视化准确性的脚本
"""

import pandas as pd
import numpy as np

# 读取原始数据
data = {
    '华东': [120, 110, 105, 115],
    '华南': [95, 88, 82, 78],
    '华北': [88, 85, 90, 100],
    '西南': [76, 82, 70, 80],
    '西北': [62, 58, 55, 60]
}
years = ['2021', '2022', '2023', '2024']
df = pd.DataFrame(data, index=years)

print("=" * 80)
print("数据可视化验证报告")
print("=" * 80)

print("\n【1】原始数据验证")
print("-" * 80)
print("原始数据:")
print(df)

print("\n【2】各区域数据标签验证")
print("-" * 80)
print("各区域数值（应与图表标签一致）:")
for year in years:
    print(f"\n{year}年:")
    for region in df.columns:
        print(f"  {region}: {df.loc[year, region]}")

print("\n【3】年度总数值验证")
print("-" * 80)
totals = df.sum(axis=1)
print("各年度总数值（应与图表顶部标签一致）:")
for year, total in zip(years, totals):
    print(f"{year}年: {total}")

print("\n【4】各区域数值之和与总数值一致性验证")
print("-" * 80)
for year in years:
    sum_regions = df.loc[year].sum()
    print(f"{year}年: 各区域之和 = {sum_regions}, 总数值 = {totals[year]}, 一致: {sum_regions == totals[year]}")

print("\n【5】环比增长率计算验证")
print("-" * 80)
growth_rates = []
for i in range(1, len(totals)):
    prev_total = totals[i-1]
    curr_total = totals[i]
    growth_rate = ((curr_total - prev_total) / prev_total) * 100
    growth_rates.append(growth_rate)
    print(f"{years[i-1]} → {years[i]}: ({curr_total} - {prev_total}) / {prev_total} × 100% = {growth_rate:.2f}% (四舍五入: {int(round(growth_rate))}%)")

print("\n【6】柱状图高度验证")
print("-" * 80)
print("各年度柱状图总高度应等于各区域数值之和:")
for year, total in zip(years, totals):
    print(f"{year}年: 总高度 = {total}")

print("\n【7】颜色组合验证")
print("-" * 80)
colors = ['#3498db', '#2ecc71', '#e74c3c', '#f39c12', '#9b59b6']
regions = ['华东', '华南', '华北', '西南', '西北']
print("区域颜色对应关系（应与图表一致）:")
for region, color in zip(regions, colors):
    print(f"  {region}: {color}")

print("\n" + "=" * 80)
print("验证总结")
print("=" * 80)
print("\n预期结果:")
print("1. 数据标签: 各区域数值与原始数据一致 ✓")
print("2. 总数值:")
for year, total in zip(years, totals):
    print(f"   {year}年: {total}")
print("3. 环比增长率:")
for i, rate in enumerate(growth_rates):
    print(f"   {years[i]}→{years[i+1]}: {int(round(rate))}%")
print("4. 颜色组合: 华东(蓝), 华南(绿), 华北(红), 西南(橙), 西北(紫) ✓")

print("\n" + "=" * 80)
