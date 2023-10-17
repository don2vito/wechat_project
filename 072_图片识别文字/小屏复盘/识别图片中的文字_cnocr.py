from pathlib import Path
from cnocr import CnOcr
  

this_dir = Path(__file__).resolve().parent

for path in (this_dir).rglob("*.png*"):
    print(f"Reading {path.name}")

    # 打开图片并使用 cnocr 进行 OCR 识别
    img_fp = path.name
    ocr = CnOcr(det_model_name='naive_det')
    out = ocr.ocr(img_fp)
    
    data_key = "text"
    for key in out[0].keys():
        if key == data_key:
            title = out[0][key]
            print(f"标题：{out[0][key]}")
            with open("./合并文本输出.txt","a") as f:
                f.writelines(title)
                f.writelines("\n")
    
    for i in out[25:]:
        for key in i.keys():
            if key == data_key:
                context = i[key]
                print(f"内容：{i[key]}")
                with open("./合并文本输出.txt","a") as f:
                    f.writelines(context)
                    f.writelines("\n")

print("处理已完成！！")