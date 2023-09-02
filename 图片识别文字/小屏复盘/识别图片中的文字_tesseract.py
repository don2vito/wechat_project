from pathlib import Path
import pytesseract  
from PIL import Image  
  

this_dir = Path(__file__).resolve().parent

for path in (this_dir).rglob("*.png*"):
    print(f"Reading {path.name}")

    # 打开图片并使用Tesseract进行OCR识别  
    image = Image.open(path.name) # 将'image.png'替换为你的图片文件名  
    text = pytesseract.image_to_string(image, lang="chi_sim") # 使用中文简体语言进行识别
    
    # 提取标题和今日措施  
    title = text.split("\n")[0] # 提取第一行内容作为标题  
    contexts = text.split("\n")[1:] # 提取第二行及以后的内容作为今日措施  
    
    # 输出标题和今日措施  
    print("标题:", title)  
    for context in contexts:  
        print("内容:",context)
        
    with open("./合并文本输出.txt","a") as f:
        f.writelines(text)
        f.writelines("\n")
            
print("处理已完成！！")