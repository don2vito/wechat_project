import pypandoc

output = pypandoc.convert_file('新营销3.0：bC一体数字化转型.html', 'epub', outputfile="新营销3.0：bC一体数字化转型.epub")

print("完成转换！")