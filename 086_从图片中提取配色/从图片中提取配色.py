from pathlib import Path
from haishoku.haishoku import Haishoku
import xlwings as xw

# 获取指定文件夹中所有图片的文件路径列表
folder = Path("C:\\Users\\don2vito\\Desktop\\从图片中提取配色\\pictures")
file_list = list(folder.glob("*.jpg"))

# 启动 Excel 并新建工作簿
app = xw.App(visible=True,add_book=False)
wb = app.books.add()

# 依次从图片中提取配色，将提取结果写入新建的工作表中
for i in file_list:
    # 提取图片中的配色
    palette = Haishoku.getPalette(str(i))
    data = []
    
    for p,rgb in palette:
        # 将颜色比例值转换为百分数形式
        percent = f"{p:.2%}"
        # 将 RGB 色值的元组转换为字符串形式
        rgbcolor = f"{rgb}"
        # 将 RGB 色值转换为十六进制色值
        hexcolor = f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"
        row = [percent,rgbcolor,hexcolor]
        data.append(row)
    
    # 新建工作表，以当前图片的名称命名
    ws = wb.sheets.add(name=i.stem)
    ws.range("A1").value = ["比例","RGB色值","十六进制色值","颜色"]
    ws.range("A1").expand("right").font.bold = True
    ws.range("A2").value = data
    
    # 将"十六进制色值"列中的色值依次取出，并设置为"颜色"列中单元格的背景色
    for c in ws.range("C2").expand("down"):
        c.offset(0,1).color = c.value
    
    ws.autofit()
    ws.pictures.add(i,left=ws.range("F1").left,width=200)
    
wb.save("./配色表.xlsx")
wb.close()
app.quit()    