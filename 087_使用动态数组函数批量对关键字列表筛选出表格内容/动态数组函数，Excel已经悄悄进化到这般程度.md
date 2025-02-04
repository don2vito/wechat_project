# 动态数组函数，Excel 已经悄悄进化到这般程度

## 一、引子

最近几年，我对 Excel 的新增功能关注比较少，一来觉得新功能还没有稳定，时不时新增一两个函数，学习起来过于碎片化，二来自从印度人接手开发之后，体感明显下降，BUG 不少。这次春节我抽空到“B 站大学”补习了一下 365 函数，确实能够显著提升效率，市面上这方面的系统性资料太少了，酒香也怕巷子深呐。

这一系列的新函数应该叫做`动态数组函数`，区别于常规的数组函数有两点显著的特点。一是具有`自动溢出`功能，不再需要选定固定区域，只需要在单元格中回车，就会返回一个数组。二是不再需要进行“**Ctrl + Shift + Enter**”三键操作。如果说普通函数是“单元格函数”，那么动态数组函数就是“**表函数**”。通过函数直接生成“表”，这对于数据清洗和处理中间表来说效率大为提高，可以通过函数直接生成自动化报表，而不需要手动干预，可以说是背刺了 PQ 啊！（微软今年来经常干这种自己打自己的行为，草台班子见怪不怪了）

从另一角度看，函数的发展有“**编程化趋势**”，`LET`和`LAMBDA`的引入就是明显的特点，结合以下三个`加载项`使用效果会更佳。

![image-20250204151804357](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041518485.png)

## 二、案例分享（模糊查询）

在之前的文章中，我分享过使用 Python 解决类似的问题，可以点击以下链接回顾学习。

[面对眼花缭乱的商品名，看我快速匹配出关键词](https://mp.weixin.qq.com/s/L6Vhsp2LRiY3VqrUEEKJkg)

[遇到相似的内容，如何顺利匹配？](https://mp.weixin.qq.com/s/EyQ8rZxvO46XosfdSvlm8g)

### 1. 问题描述

有两张表，一张是商品明细宽表，一张是产地参数表。

![image-20250204153110412](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041531575.png)

![image-20250204152725730](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041527834.png)

需求根据产地参数表中的产地名称，将商品明细宽表中的“产地”列中对应的产地筛选出，最后通过产地对销售额分组求和。

下面我分别用常规的函数和动态数组函数来解决该问题，算是抛砖引玉。

### 2. 常规函数方法

添加辅助列，再进行透视。

```
=IFERROR(LOOKUP(1,0/FIND(参数表区域,raw!AW2),原始表待模糊匹配字段区域),"")
```

![image-20250204155311499](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041553644.png)

### 3. 动态数组函数方法

#### （1）情况一：表头和原始数据完全一致

```
=FILTER(原始表区域,REGEXTEST(原始表区域,TEXTJOIN("|",TRUE,参数表区域)))
```

![image-20250204154135900](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041541045.png)

#### （2）自定义表头顺序，但列名要一致

```
=FILTER(CHOOSECOLS(原始表区域,MATCH(自定义表头区域,原始表区域,0)),REGEXTEST(原始表区域,TEXTJOIN("|",TRUE,参数表区域)))
```

结合`sumifs`就能直接算出结果了。

![image-20250204154235404](https://cdn.jsdelivr.net/gh/don2vito/picgo_warehouse/pic/202502041542445.png)