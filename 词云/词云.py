import pandas as pd
import stylecloud
from PIL import Image
import jieba
from collections import Counter
import time

begin_time = time.time()

with open('./明朝那些事儿.txt',encoding='utf-8') as f:
    txt = f.read()
txt = txt.split()

# 语料机械压缩（先对长句进行压缩，适合 DataFrame 格式的 “评论” 语句场景）
def cut_words(txt):
    text = jieba.lcut(txt)
    text_duplicated = []
    text_join = []
    for i in text:
        if not i in text_duplicated:
            text_duplicated.append(i)
            text_join = ' '.join(text_duplicated)
    # print(text_join)
    return text_join

def stopwordslist():
    stopwords = [line.strip() for line in open('./常见中文停用词表.txt', 'r', encoding='gbk').readlines()]
    stopwords.append(' ') # 自定义添加停用词
    return stopwords

# 对句子去除停用词
def movestopwords(sentence):
    stopwords = stopwordslist()  # 这里加载停用词的路径
    santi_words =[x for x in sentence if len(x) >1 and x not in stopwords]
    return ' '.join(santi_words)

jieba.add_word('东方购物') # 增加自定义词语
jieba.del_word('东方购物') # 删除自定义词语
data_cut = jieba.lcut(str(txt))
word_list = movestopwords(data_cut)
# print(word_list.split(' '))

# 统计词频
mycount = {}
for word in word_list.split(' '):
    mycount[word] = mycount.get(word,0)+1
counts_df = pd.DataFrame(mycount.items(), columns=['label', 'counts'])
counts_df.sort_values(by='counts',inplace=True, ascending = False)
counts_df.to_csv('./词频统计.csv',encoding='utf-8')
print('输出词频统计 成功！！')
print(counts_df.iloc[:10])
# for key, value in mycount.most_common(10):  # 有序（返回前 10 个）
    # print(key, value)

'''
def gen_stylecloud(text=None,
                   file_path=None,   # 输入文本/CSV 的文件路径 (可以含词频数)
                   size=512,  # stylecloud 的大小（长度和宽度）
                   icon_name='fas fa-flag',  # stylecloud 形状的图标名称（如 fas fa-grin）。[default: fas fa-flag]
                   palette='cartocolors.qualitative.Bold_5',  # 调色板（通过 palettable 实现）。[default: cartocolors.qualitative.Bold_6]
                   colors=None,
                   background_color="white",  # 背景颜色
                   max_font_size=200,  # stylecloud 中的最大字号
                   max_words=2000,  # stylecloud 可包含的最大单词数
                   stopwords=True,  # 布尔值，用于筛除常见禁用词
                   custom_stopwords=STOPWORDS, # 去除停用词
                   icon_dir='.temp',
                   output_name='stylecloud.png',   # stylecloud 的输出文本名
                   gradient=None,  # 梯度方向
                   font_path=os.path.join(STATIC_PATH,'Staatliches-Regular.ttf'), # stylecloud 所用字体
                   random_state=None,  # 控制单词和颜色的随机状态
                   collocations=True,
                   invert_mask=False,
                   pro_icon_path=None,
                   pro_css_path=None)
'''

stylecloud.gen_stylecloud(
                            text=word_list,
                            palette='tableau.BlueRed_6',
                            icon_name='fas fa-apple-alt',
                            font_path='./田英章楷书3500字.ttf',
                            output_name='词云图.png',
                            # custom_stopwords=stopwords
                            )
Image.open('词云图.png')
print('成功生成词云图！！')

end_time = time.time()
print('运行共耗时 {:.1f}秒'.format(end_time - begin_time))