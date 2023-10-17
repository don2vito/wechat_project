# 用 Python 调用 VBA，还得看 xlwings

##  一、字体

```Python
.api.Font.Size = 数值  # 设置单元格字体大小
.api.Font.Name = "字体名"  # 设置字体
.api.Font.Bold = True  # 设置单元格字体是否加粗
.api.Font.Italic= True  # 设置单元格字体是否斜体
.api.Font.Underline= True  # 设置单元格字体是否下划线
.api.Font.Color = 十六进制文本  # 设置字体颜色
.api.Font.ColorIndex = 数值 # 设置字体的颜色，具体颜色索引见下方
```

- **颜色索引值**对应颜色

![颜色索引对应表](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630134542907-ColorIndex.jpg.gif)

## 二、框线

```Python
.api.Borders(数值).LineStyle = 数值
.api.Borders(数值).Weight = 数值
.api.Borders(数值).Color = xw.utils.rgb_to_int((255,255,255))
```

- **Borders集合对象**代表单元格区域的各条边框，通过括号中的数字可指定不同的边框，**5 代表单元格内从左上角到右下角的线，6 代表单元格内从左下角到右上角的线，11 代表内部竖线，12 代表内部横线**

  ![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630135913922-epub_39602693_251.jpg)

- **LineStyle属性**可取的值

  ![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630135917814-epub_39602693_252.jpg)

- **Weight属性**可取的值

  ![](https://cdn.jsdelivr.net/gh/don2vito/pic_warehouse/2021-8-28/1630135920489-epub_39602693_253.jpg)

- **Color属性**的值为一个整数，将RGB色值转换为整数，调用xlwings模块的**utils子模块**中的`rgb_to_int()`函数来完成转换，该函数的参数是一个代表RGB色值的元组

## 三、对齐

```python
.api.HorizontalAlignment = 数值
.api.VerticalAlignment = 数值
```

- **HorizontalAlignment属性**用于设置水平对齐方式

  ![](https://gitee.com/don2vito/picture_warehourse/raw/master/2021-8-28/1630135580591-epub_39602693_247.jpg)

- **VerticalAlignment属性**用于设置垂直对齐方式

![](https://gitee.com/don2vito/picture_warehourse/raw/master/2021-8-28/1630135582670-epub_39602693_248.jpg)

## 四、格式

```python
.api.NumberFormat = '格式' # 设置单元格的数字格式

sht.range("C1").formula = "=SUM(A1:B1)"  # 引用公式
sht.range("A1:c3").columns.autofit()  # 自动根据单元格中内容调整单元格的宽度
sht.range("A1").color = [0, 0, 255]  # 设置单元格背景颜色
print(sht.range("A1").value)  # 返回单元格内容
print(sht.range("A1").color)  # 返回单元格颜色值
print(sht.range("C1").formula_array)  # 返回单元格中的引用公式
sht.range('A2').value = [['hello 1', 'hello 2', 'hello 3'], [1.0, 2.0, 3.0]]  # 批量填写数据

.api.Merge()  # 合并
.api.UnMerge()  # 取消合并单元格

.api.Tab.Color = 数值
# 设置工作表的标签颜色。Color属性的值为一个整数，Color属性整数值＝R＋G×256＋B×256×256
```

## 五、打印区域

```python
#改变页眉页脚
.api.PageSetup.LeftHeader = ' '
.api.PageSetup.LeftFooter = ' '
.api.PageSetup.CenterFooter = ' '
.api.PageSetup.RightFooter = ' '

#改变打印区域
.api.PageSetup.PrintArea = "$A$1:$J$200"

#设置打印顶部标题
.api.PageSetup.PrintTitleRows = "$1:$1"

# 打印工作簿，参数Copies用于指定打印份数，如果省略该参数，则只打印一份；参数ActivePrinter用于设置要使用的打印机的名称，如果省略该参数，则表示使用操作系统的默认打印机；参数Collate如果为True，表示逐份打印
.api.PrintOut(Copies=数值,ActivePrinter='打印机名',Collate=True)

# 按指定缩放比例打印表（可取值为10 - 400）
.api.PageSetup.Zoom = 数值

# 设置水平居中打印
.api.PageSetup.CenterHorizontally = True

# 设置垂直居中打印
.api.PageSetup.CenterVertically = True

# 设置打印行号和列号
.api.PageSetup.PrintHeadings = True
```

## 六、另存格式

```python
.api.SaveAs(文件名,FileFormat=数值)
# 56 格式为.xls，51 格式为.xlsx
```

## 七、保护结构

```python
.api.Protect(Password='密码',Structure=Ture,Windows=True,Contents=True)
# 参数Password用于设置保护密码，参数Structure为True时表示保护工作簿结构不被修改，参数Windows为True时表示保护工作簿窗口不被修改，参数Contents为True时表示保护工作表的内容不被修改；如果要取消保护，可使用Unprotect()函数，将密码放在括号中

.api.Password='密码'
# 可将Password属性赋值为空字符串，然后保存工作簿可将Password属性赋值为空字符串，然后保存工作簿
```

