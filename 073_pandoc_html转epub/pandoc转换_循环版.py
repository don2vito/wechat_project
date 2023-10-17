import pypandoc
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")


this_dir = Path(__file__).resolve().parent

for path in (this_dir).rglob("*.html*"):
    print(f"Reading 《{path.stem}》")
    try:
        new_stem = path.stem + ".epub"
        output = pypandoc.convert_file(path.name, "epub", outputfile=new_stem, encoding="utf-8")
        print(f"Finished 《{path.stem}》")
    except:
        pass

print("完成转换！")


# 初次安装后，自动下载 pandoc，可以运行以下代码：
# from pypandoc.pandoc_download import download_pandoc
# download_pandoc()