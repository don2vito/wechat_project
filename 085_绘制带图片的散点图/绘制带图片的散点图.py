# 导入库
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from pylab import *
from PIL import Image
import numpy as np

# 导入一个包含了国家、GDP和国债利率的数据集
df = pd.DataFrame(pd.read_excel('./样例数据.xlsx'))

# 利用循环获取每个不同国家国旗的图片路径
paths = list()
for i in range(0,len(df)):
    paths.append(str('./国旗/'+df['国家'][i]+'.jpg'))
    
# 定义一个函数，使得相应路径下的图片按比例缩小，修改后的最大值图片尺寸为 512像素 * 512像素
def getImage(path,zoom=0.2):
    img = Image.open(path)
    # 或者使用 Image.LANCZOS，Image.ANTIALIAS 已被弃用
    img.thumbnail((512,512),Image.Resampling.LANCZOS)
    return OffsetImage(img,zoom=zoom)

# 创建一个图形对象，添加这条可以让图形显示中文的微软雅黑
mpl.rcParams['font.sans-serif']=['Microsoft YaHei']

# 设置图形为 4x4 英寸，设置分辨率为 600点毎英寸
fig,ax= plt.subplots(figsize=(4,4),dpi=600)
# 使用 ax 对象创建一个散点图，前者 x 轴的数据，df['十年期国债收益率’]是 y 轴的数据
ax.scatter(df['GDP同比'],df['十年期国债收益率'])
# 设置 x 轴的标签 
ax.set_xlabel('GDP同比')
# 设置 y 轴的标签    
ax.set_ylabel('十年期国债收益率') 

# 计算 x 轴和 y 轴的平均值
mean_x = np.mean(df['GDP同比'])
mean_y = np.mean(df['十年期国债收益率'])

# 添加 x 轴和 y 轴的平均线，颜色为深蓝色，线型为虚线
ax.axhline(mean_y, color='blue', linestyle='--', linewidth=1)
ax.axvline(mean_x, color='blue', linestyle='--', linewidth=1)

# 获取 y 轴的最大值及其索引
max_y_value = df['十年期国债收益率'].max()
max_y_index = df['十年期国债收益率'].idxmax()

# 使用 zip 函数迭代三个对象并进行标注
for i, (gdp_val, interest_val, path, country) in enumerate(zip(df['GDP同比'], df['十年期国债收益率'], paths, df['国家'])):
    # 加载图片并缩放
    image = getImage(path)
    ab = AnnotationBbox(image, (gdp_val, interest_val), frameon=False)
    ax.add_artist(ab)

    # 在图片上方并右侧添加国家名称、x 值和 y 值，最大值标注为红色，其余为黑色
    offset_x = 0.3  # 设置 x 轴偏移量，使得文本向右偏移
    offset_y = 0.2  # 设置 y 轴偏移量，使得文本在图片上方
    
    if i == max_y_index:
        ax.text(gdp_val + offset_x, interest_val + offset_y, f'{country} ({gdp_val:.2f}, {interest_val:.2f})', 
                color='red', fontsize=8, ha='center')
    else:
        ax.text(gdp_val + offset_x, interest_val + offset_y, f'{country} ({gdp_val:.2f}, {interest_val:.2f})', 
                color='black', fontsize=8, ha='center')
    
# 保存图片，设置为 300 PPI
plt.savefig('./output_image.jpg', dpi=300)

# 显示图形
plt.show()