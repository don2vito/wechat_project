# A/B 测试及应用

[TOC]



> 本文介绍了 A/B 测试的统计学意义及其应用，通过封装好的通用化 Python 代码，可以快速输出结果，得出测试的结论，可以解决A/B 测试中的均值型和比率型两种类型的实验问题，具有普遍适用性的意义。



## 一、A/B 测试的统计学原理

### （一）用样本代表总体

#### 1. 大数定律

大数定律揭示了随机事件的均值具有长期稳定性，事件发生的频率可以近似替代事件发生的概率，样本均值可以近似替代总体均值。

#### 2. 中心极限定理

- **样本容量为 30 是大样本与小样本的区分标准。**

- 对于非正态分布总体，当样本容量达到 30 时，样本均值的分布形态都近似于正态分布。

> A/B 测试中的两类指标：
>
> - **均值类**：只要样本容量大于或等于 30，其抽样分布为正态分布
> - **比率类**：其抽样分布为二项式分布，当样本容量 n 足够大，且样本容量 n 和样本比率 p 满足 np ≥ 5 和 n(1-p)  ≥ 5 时，抽样分布可以用正态分布近似

#### 3. 3σ 准则

- 统计学上，通常把 ±3σ 的误差作为极限误差（概率为 99.74%）。
- 有 95% 的样本落在距离总体均值 1.96σ 的范围内。

![](https://img0.baidu.com/it/u=402648996,2959513260&fm=253&fmt=auto&app=138&f=GIF?w=500&h=362)

### （二）确定足够的样本量

直观上说，A 和 B 即使有差异，也不一定能被观测出来，必须保证一定的条件（比如样本要充足）才能观测出统计量之间的差异；否则，结果也是不置信的。

> 设 n1 = n2 = n，σ1 = σ2 = σ，σ 平方根据经验预估，需要样本量为：
>
> - 均值类：
>
> ![](https://files.mdnice.com/user/1655/4b9e3c6b-6992-4558-b878-856c7341da7e.png)
>
> - 比率类：Δ = p1 − p2，
>
> ![](https://files.mdnice.com/user/1655/2005ac61-6376-4fa5-ae0d-e23c08dcb824.png)

### （三）用假设检验判断差异

#### 1. 原假设与备择假设

根据实际问题，确定出零假设 H0 和备择假设 H1，H0 和 H1 互为相反，非此即彼，不可能同时满足。

> **检验方向的判定**：
>
> - 如果H1中包含小于号"<"，则为左尾
> - 如果H1中包含大于号">"，则为右尾
> - 如果H1中包含不等号"≠"，则为双尾

> **A/B 测试采用双尾检验**：
>
> - H0 ： A、B没有本质差异（A= B)
> - H1 ： A、B确实存在差异（A ≠ B)

#### 2. 第 Ⅰ 类错误与第 Ⅱ 类错误

|         |           接受 H0           |           拒绝 H0           |
| :-----: | :-------------------------: | :-------------------------: |
| H0 为真 |      真阴性，决策正确       | 第 Ⅰ 类错误，假阳性，误判 α |
| H0 为假 | 第 Ⅱ 类错误，假阴性，漏报 β |      真阳性，决策正确       |

> **需要将犯第 Ⅰ 类错误和第 Ⅱ 类错误的概率降到最小**：
>
> - 当样本容量固定时，不可能同时减少犯两类错误的概率，有一个折中的办法，即选择较小的显著水平 α
> - 当样本容量不固定时，有效的办法是增大样本

- 发生第一类错误的概率为 **α**，即检验的显著水平，**通常取 5%** 。
- **功效 Power** = 1 - β，**通常取 80% 或 90% **，因此 **β 通常取 10% 或 20%**。

#### 3. Z 检验（通过样本估计总体）

Z 检验是一般用于大样本（即样本容量大于 30 ）平均值差异性检验的方法，它是用标准正态分布的理论来推断差异发生的概率，从而比较两个平均数的差异是否显著，又叫 U 检验。

> **A/B 测试需要采用双样本对照的 Z 检验公式**：
>
> ![](https://files.mdnice.com/user/1655/bc336ae4-926c-42dc-b693-3310cfd44987.png)
>
> - μ1、μ2是双样本均值
> - σ1、σ2是双样本标准差
> - n1、n2是样本数目

#### 4. 显著性

根据 Z 检验算出 p 值(查表)，通常会用 p 值和 0.05 比较，如果 p < 0.05，则接受 H0，认为 A 和 B 没有显著差异。

#### 5. 置信区间

置信区间是用来对一个概率样本的总体参数进行区间估计的样本均值范围，它展现了这个均值范围包含总体参数的概率，这个概率称为置信水平。

> **双样本的均值差置信区间估算公式**：
>
> ![](https://files.mdnice.com/user/1655/45c3a140-fb86-48a7-9406-2bd55fbee9e5.png)
>
> - ρ1 、ρ2 是双样本的观察均值
> - μ1、μ2是双样本均值
> - σ1、σ2是双样本标准差
> - n1、n2是样本数目

### （四）衡量测试效果

> **统计功效的计算公式**：
>
> ![](https://files.mdnice.com/user/1655/6be6c0e4-ecc8-4654-9dc4-331e68b8e1ee.png)
>
> - Δ=∣μ1 − μ2∣，Φ 是标准正态分布的概率累积函数(CDF)，有一个近似计算公式
>   ![](https://files.mdnice.com/user/1655/000761dd-e8a2-4d20-a505-650e126c479f.png)

- **功效 Power = 1 - β，通常取 80% 以上才有意义**。



## 二、Python 代码实现

### （一）计算实验样本量

```python
def sample_size_u(self, a: float, b: float, u: float, s: float) -> int:
	'''
	已知双样本(A/B)均数，求实验样本量
	:param a: alpha
	:param b: beta
	:param u: 均值的差值
	:param s: 经验标准差
	:return: 样本量
	'''
    n = 2 * pow(((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (u / s)), 2)
    return math.ceil(n)

def sample_size_p(self, a: float, b: float, p1: float, p2: float) -> int:
    '''
	已知双样本(A/B)频数，求实验样本量
	:param a: alpha
	:param b: beta
	:param p1: 样本的频数，例如点击率50%，次日留存率80%
	:param p2: 样本的频数
	:return: 样本量
	'''
    n = pow((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (p1 - p2), 2) * (p1 * (1 - p1) + p2 * (1 - p2))
    return math.ceil(n)
```

### （二）显著性检验

```python
def significance_u(self, x1: float, x2: float, s1: float, s2: float, n1: int, n2: int, a: float) -> (
        int, float, float):
    '''
    双样本双尾均值检验
    :param x1: 样本均值
    :param x2: 样本均值
    :param s1: 样本标准差
    :param s2: 样本标准差
    :param n1: 样本数量
    :param n2: 样本数量
    :param a: alpha
    :return: 显著性统计结果f，z-score， p-value
    '''
    z = (x1 - x2) / pow(s1 ** 2 / n1 + s2 ** 2 / n2, 1 / 2)
    if z > 0:
        p = (1 - norm.cdf(z)) * 2
        if p < a:  # 拒绝原假设，接受备选假设
            f = 1
        else:  # 接受原假设
            f = 0
    else:
        p = 2 * norm.cdf(z)
        if p < a:  # 拒绝原假设，接受备选假设
            f = 1
        else:  # 接受原假设
            f = 0
    return f, format(z, '.2f'), format(p, '.2f')

def significance_p(self, p1: float, p2: float, n1: int, n2: int, a: float) -> (int, float, float):
    '''
    双样本双尾频数检验
    :param p1: 样本频数
    :param p2: 样本频数
    :param n1: 样本量
    :param n2: 样本量
    :param a: alpha
    :return: 显著性统计结果f，z-score， p-value
    '''
    p_pool = (n1 * p1 + n2 * p2) / (n1 + n2)

    z = (p1 - p2) / pow(p_pool * (1 - p_pool) * (1 / n1 + 1 / n2), 1 / 2)

    if z > 0:
        p = (1 - norm.cdf(z)) * 2
        if p < a:  # 拒绝原假设，接受备选假设
            f = 1
        else:  # 接受原假设
            f = 0
    else:
        p = 2 * norm.cdf(z)
        if p < a:  # 拒绝原假设，接受备选假设
            f = 1
        else:  # 接受原假设
            f = 0
    return f, format(z, '.2f'), format(p, '.2f')
```

### （三）计算置信区间

```python
def confidence_u(self, x1: float, x2: float, s1: float, s2: float, n1: int, n2: int, a: float) -> tuple:
    '''
    双样本均值检验
    :param x1: 样本均值
    :param x2: 样本均值
    :param s1: 样本标准差
    :param s2: 样本标准差
    :param n1: 样本量
    :param n2: 样本量
    :param a: alpha
    :return: 置信区间
    '''
    d = norm.ppf(1 - a / 2) * pow(s1 ** 2 / n1 + s2 ** 2 / n2, 1 / 2)
    floor = x1 - x2 - d
    ceil = x1 - x2 + d
    return (format(floor, '.2f'), format(ceil, '.2f'))

def confidence_p(self, p1: float, p2: float, n1: int, n2: int, a: float) -> tuple:
    '''
    双样本频数检验
    :param p1: 样本频数
    :param p2: 样本频数
    :param n1: 样本量
    :param n2: 样本量
    :param a: alpha
    :return: 置信区间
    '''
    d = norm.ppf(1 - a / 2) * pow(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2, 1 / 2)
    floor = p1 - p2 - d
    ceil = p1 - p2 + d
    return (format(floor, '.2%'), format(ceil, '.2%'))
```

### （四）计算功效

```python
def power_u(self, u1: float, u2: float, s1: float, s2: float, n1: int, n2: int, a: float) -> float:
    '''
    双样本均数检验
    :param u1: 样本均值
    :param u2: 样本均值
    :param s1: 样本标准差
    :param s2: 样本标准差
    :param n1: 样本量
    :param n2: 样本量
    :param a: alpha
    :return: 功效
    '''
    z = abs(u1 - u2) / pow(s1 ** 2 / n1 + s2 ** 2 / n2, 1 / 2) - norm.ppf(1 - a / 2)
    b = 1 - norm.cdf(z)
    power = 1 - b
    return format(power, '.2%')

def power_p(self, p1: float, p2: float, n1: int, n2: int, a: float) -> float:
    '''
    双样本频数检验
    :param p1: 样本频数
    :param p2: 样本频数
    :param n1: 样本量
    :param n2: 样本量
    :param a: alpha
    :return: 功效
    '''
    z = abs(p1 - p2) / pow(p1 * (1 - p1) / n1 + p2 * (1 - p2) / n2, 1 / 2) - norm.ppf(1 - a / 2)
    b = 1 - norm.cdf(z)
    power = 1 - b
    return format(power, '.2%')
```

### （五）完整代码

```python
from scipy.stats import norm
import math


class Sample:
    '''
    计算样本量
    https://www.abtasty.com/sample-size-calculator/
    '''

    def sample_size_u(self, u: float, s: float, a: float = 0.05, b: float = 0.2) -> int:
        '''
        已知双样本(A/B)均数，求实验样本量
        :param a: alpha
        :param b: beta
        :param u: 均值的差值
        :param s: 经验标准差
        :return: 样本量
        '''
        n = 2 * pow(((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (u / s)), 2)
        return math.ceil(n)

    def sample_size_p(self, p1: float, p2: float, a: float = 0.05, b: float = 0.2) -> int:
        '''
        已知双样本(A/B)频数，求实验样本量
        :param a: alpha
        :param b: beta
        :param p1: 样本的频数，例如点击率50%，次日留存率80%
        :param p2: 样本的频数
        :return: 样本量
        '''
        n = pow((norm.ppf(1 - a / 2) + norm.ppf(1 - b)) / (p1 - p2), 2) * (p1 * (1 - p1) + p2 * (1 - p2))
        return math.ceil(n)


class ABtest_u():
    '''
    双样本双尾均值检验
    '''

    def __init__(self, x1: float, x2: float, s1: float, s2: float, n1: int, n2: int, a: float = 0.05, b: float = 0.2):
        self.x1 = x1  # 对照组均值
        self.x2 = x2  # 测试组均值
        self.s1 = s1  # 对照组标准差
        self.s2 = s2  # 测试组标准差
        self.n1 = n1  # 对照组样本量
        self.n2 = n2  # 测试组样本量
        self.a = a  # alpha
        self.b = b  # beta

    def significance_u(self) -> (int, float, float):
        '''
        双样本双尾均值显著性检验
        '''
        z = (self.x1 - self.x2) / pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2)
        if z > 0:
            p = (1 - norm.cdf(z)) * 2
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        else:
            p = 2 * norm.cdf(z)
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        return f, format(z, '.2f'), format(p, '.2f')

    def confidence_u(self) -> tuple:
        '''
        双样本均值置信区间
        '''
        d = norm.ppf(1 - self.a / 2) * pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2)
        floor = -(self.x1 - self.x2 - d)
        ceil = -(self.x1 - self.x2 + d)
        return (format(floor, '.2f'), format(ceil, '.2f'))

    def power_u(self) -> float:
        '''
        双样本均数功效
        '''
        z = abs(self.x1 - self.x2) / pow(self.s1 ** 2 / self.n1 + self.s2 ** 2 / self.n2, 1 / 2) - norm.ppf(
            1 - self.a / 2)
        b = 1 - norm.cdf(z)
        power = 1 - b
        return format(power, '.2%')

    def main(self):
        f, z, p = self.significance_u()
        ci = self.confidence_u()
        power = self.power_u()
        print(f'保留组均值：{self.x1}')
        print(f'测试组均值：{self.x2}')
        print('是否显著：' + ('统计效果显著，拒绝原假设' if f == 1 else '统计效果不显著，不能拒绝原假设'))
        print(f'变化度：' + format((self.x2 - self.x1) / self.x1, '.2%'))
        print(f'置信区间：{ci}')
        print(f'p-value：{p}')
        print(f'功效：{power}')


class ABtest_p():
    '''
    双样本双尾频数检验
    '''

    def __init__(self, p1: float, p2: float, n1: int, n2: int, a: float = 0.05, b: float = 0.2):
        self.p1 = p1
        self.p2 = p2
        self.n1 = n1
        self.n2 = n2
        self.a = a
        self.b = b

    def significance_p(self) -> (int, float, float):
        '''
        双样本双尾频数显著性检验
        '''
        p_pool = (self.n1 * self.p1 + self.n2 * self.p2) / (self.n1 + self.n2)

        z = (self.p1 - self.p2) / pow(p_pool * (1 - p_pool) * (1 / self.n1 + 1 / self.n2), 1 / 2)

        if z > 0:
            p = (1 - norm.cdf(z)) * 2
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        else:
            p = 2 * norm.cdf(z)
            if p < self.a:  # 拒绝原假设，接受备选假设
                f = 1
            else:  # 接受原假设
                f = 0
        return f, format(z, '.2f'), format(p, '.2f')

    def confidence_p(self) -> tuple:
        '''
        双样本频数置信区间
        '''
        d = norm.ppf(1 - self.a / 2) * pow(self.p1 * (1 - self.p1) / self.n1 + self.p2 * (1 - self.p2) / self.n2, 1 / 2)
        floor = -(self.p1 - self.p2 - d)
        ceil = -(self.p1 - self.p2 + d)
        return (format(floor, '.2%'), format(ceil, '.2%'))

    def power_p(self) -> float:
        '''
        双样本频数功效
        '''
        z = abs(self.p1 - self.p2) / pow(self.p1 * (1 - self.p1) / self.n1 + self.p2 * (1 - self.p2) / self.n2,
                                         1 / 2) - norm.ppf(1 - self.a / 2)
        b = 1 - norm.cdf(z)
        power = 1 - b
        return format(power, '.2%')

    def main(self):
        f, z, p = self.significance_p()
        ci = self.confidence_p()
        power = self.power_p()
        print(f'保留组均值：{self.p1}')
        print(f'测试组均值：{self.p2}')
        print('是否显著：' + ('统计效果显著，拒绝原假设' if f == 1 else '统计效果不显著，不能拒绝原假设'))
        print(f'变化度：' + format((self.p2 - self.p1) / self.p1, '.2%'))
        print(f'置信区间：{ci}')
        print(f'p-value：{p}')
        print(f'功效：{power}')


if __name__ == '__main__':
    # 计算样本量
    sample = Sample()
    
    n1 = sample.sample_size_p(p1=0.13, p2=0.14)
    print(n1)
    
    n2 = sample.sample_size_u(u=1, s=38)
    print(n2)

    # 双样本双尾均值检验
    test1 = ABtest_u(x1=5.08, x2=8.04, s1=2.06, s2=2.39, n1=32058,n2=34515)
    test1.main()

    # 双样本双尾频数检验
    test2 = ABtest_p(p1=0.4835, p2=0.5121, n1=972, n2=977)
    test2.main()
```

> **scipy.stats.norm 方法**：
>
> - **rvs**：对随机变量进行随机取值，可以通过size参数指定输出的数组的大小
> - **pdf**：随机变量的概率密度函数
> - **cdf**：随机变量的累积分布函数，它是概率密度函数的积分
> - **sf**：随机变量的生存函数，它的值是 1 - cdf(t)
> - **ppf**：累积分布函数的反函数
> - **stats**：计算随机变量的期望值和方差
> - **fit**：对一组随机采样进行拟合，找出最合适取样数据的概率密度函数的系数

## 三、应用案例

### （一）广告方案选择

> **数据集来源（Kaggle）**：https://www.kaggle.com/code/osuolaleemmanuel/starter-ad-a-b-testing-a563b1d3-6/data
>
> **场景**：通过观察智能广告的点击率与普通广告的点击率之间是否有差异，进而决定是否大规模推广智能广告。
> **问题**：智能广告相比普通广告是否更受用户欢迎？

#### 1. 探索数据集

```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import norm
import math

plt.rcParams['font.sans-serif'] = ['SimHei']    # 用来正常显示中文标签
plt.rcParams['axes.unicode_minus'] = False    # 用来正常显示负号

# 导入数据集
df = pd.read_csv('./AdSmartABdata.csv')
df.head()

# 查看数据
df.info()

# 查看数据信息
df.describe()

# 查看数据字段下的值
for column in df.drop(['auction_id','hour','device_make'],axis=1).columns:
    print(column,'-',df[column].unique())
    
# 查看试验组和对照组的样本容量以及是都均衡
fig,axes = plt.subplots(figsize=(5,4),dpi=300)
sns.countplot(x=df['experiment'],alpha=0.95)
plt.title('对于不同类型样本的计数')
```

![](https://files.mdnice.com/user/1655/5da74196-1990-4104-b996-a3435f4b193d.png)

![](https://files.mdnice.com/user/1655/3c6d898e-c26b-4f77-b731-09022f6d5a15.png)

![](https://files.mdnice.com/user/1655/ed494bbc-d929-4463-a788-1a6fee4859c9.png)

![](https://files.mdnice.com/user/1655/8e7bb277-fa07-4843-9b2e-7c78347db2e6.png)

![](https://files.mdnice.com/user/1655/5821c1e7-6f5f-4010-be34-8da774df3a84.png)

#### 2. 原假设与备择假设

- H0 ：智能广告的点击率与普通广告没有差别
- H1 ：智能广告的点击率与普通广告有差别

#### 3. 计算统计量

```python
# 计算统计量
control = df[df['experiment']=='control']
exposed = df[df['experiment']=='exposed']

# 计算样本量
total_control = control['auction_id'].count()
total_exposed = exposed['auction_id'].count()

# 计算点击广告的用户数量
clicks_control = control['auction_id'].loc[(control['yes']==1) & (control['no']==0)].count()
clicks_exposed = exposed['auction_id'].loc[(exposed['yes']==1) & (exposed['no']==0)].count()

# 计算广告点击率
p1 = clicks_control / total_control
p2 = clicks_exposed / total_exposed

# 输出
print(f'控制组的样本量：{total_control}\n试验组的样本量：{total_exposed}\n控制组点击广告的用户数量：{clicks_control}\n试验组点击广告的用户数量：{clicks_exposed}\n控制组广告点击率：' + format(p1,'.2%') + '\n试验组广告点击率：' + format(p2,'.2%'))
```

![](https://files.mdnice.com/user/1655/1f808499-6dc6-4a26-a49c-00b76758510d.png)

#### 4. 执行代码

```python
# 执行代码
test = ABtest_p(p1=p1, p2=p2, n1=total_control, n2=total_exposed)
test.main()
```

#### 5. 输出结果

![](https://files.mdnice.com/user/1655/71ee4ea6-e067-4582-8c2b-8fc6280d5414.png)

#### 6. 结论分析

- 描述统计分析
  控制组的样本量：4071个，广告点击率：6.48%
  试验组的样本量：4006个，广告点击率：7.69%
- 推论统计分析
  - 假设检验
    独立双样本 p-value = 0.04( α = 5% ) ，双尾检验
    统计显著，拒绝零假设，接受备择假设。即：智能广告和普通广告的点击率不同，两种广告的点击率是有差别的
  - 置信区间
    两个独立样本均值差值的置信区间，置信水平 95%，CI = (2.32%, 0.08%)
    控制组的点击率小于试验组，且通过读取置信区间的数值，区间边界值均为负值，证明控制组的点击率显著小于实验组，即 智能广告的点击率不同显著小于普通广告
- 功效
  power = 55.87%，效果不显著，结论：不建议大规模推广智能广告

### （二）键盘布局版本选择

> **场景**：两款版本不一样的手机应用(A 版本，B 版本)，你作为公司的产品经理，想在正式发布产品之前，知道哪个键盘布局对用户体验更好？
> 随机抽取实验者，将实验者分成 2 组，A 组使用键盘版本 A， B 组使用键盘版本 B。让他们在 30 秒内打出标准的 20 个单词文字消息，然后记录打错字的数量。
> **问题**：两种版本布局是否用户体验显著不同，哪种更好？

![](https://gimg2.baidu.com/image_search/src=http%3A%2F%2Fwww.fromgeek.com%2Fuploadfile%2F2012%2F2018%2F1116%2F20181116180147790G.jpg&refer=http%3A%2F%2Fwww.fromgeek.com&app=2002&size=f9999,10000&q=a80&n=0&g=0n&fmt=auto?sec=1658153082&t=00edb909cde132fa2953b3b19eeecb66)

#### 1. 原假设与备择假设

- H0 ：两种版本的用户体验相同

- H1 ：两种版本布局的用户体验不同

#### 2. 计算统计量

- 均值：x1 = 5.08，x2 = 8.04
- 标准差：s1 = 2.06，s2 = 2.39
- 样本量：n1 = 32058，n2 = 34515

#### 3. 执行代码

```python
test = ABtest_u(x1=5.08, x2=8.04, s1=2.06, s2=2.39, n1=32058, n2=34515)
test.main()
```

#### 4. 输出结果

保留组均值：5.08
测试组均值：8.04
是否显著：统计效果显著，拒绝原假设
变化度：58.27%
置信区间：(‘2.99’, ‘2.93’)
p-value：0.00
功效：100.00%

> 在统计效果显著情况下，需判断假设检验功效，只有 power ≥ 80%时，才能得出结论（样本量不足），否则应延长测试。

#### 5. 结论分析

- 描述统计分析

  A 版本打错字数量平均值：5.08个，标准差：2.06个

  B 版本打错字数量平均值：8.04个，标准差：2.39个

- 推论统计分析

  - 假设检验

    独立双样本 p-value = 0.00( α = 5% ) ，双尾检验

    统计显著，拒绝零假设，接受备择假设。即：A 版本和 B 版本打错字的均值不同，两种布局有显著差别

  - 置信区间

    两个独立样本均值差值的置信区间，置信水平 95%，CI = (2.99, 2.93)

    A 版本打错字的均值小于 B 版本，且通过读取置信区间的数值，区间边界值均为负值，证明 A 版本打错字数量均值显著小于 B 版本，即 A 布局版本更符合用户体验

- 功效

  power = 100.00%，效果显著，结论：A 版本更符合用户体验


