import pandas as pd
import warnings
from itertools import combinations
import time

pd.set_option('display.max_columns', 100)
pd.set_option('precision', 3)

warnings.filterwarnings('ignore')
#
# df = pd.read_table('./0.txt',sep='\t',header=None)
#
# df[29] = df[9] + ' & ' + df[10] + ' & ' + df[11]
#
# x = [9,10,11]
# df.drop(df.columns[x],axis=1,inplace=True)
# print(df.head())

def get_data():
    df = pd.read_excel('./销售基础表查询.xlsx',sheet_name='销售基础表查询',header=0)
    # print(df.head())
    # print(df.shape)
    bool_content = ((df['实销数量'] > 0) & (df['实销金额'] > 0))
    df = df[bool_content]

    df2 = pd.DataFrame([(i,df[df['单据号'] == i]['商品'].tolist()) for i in df['单据号'].unique()])
    # print(df2.head())

    #                 0                                                  1
    # 0  CK201301010144  [A82707207|长款羊毛大衣, 2012Q1|大号牛皮纸袋, A82131204|中长...
    # 1  CK201301010058                  [Z52636111|针织长袖T恤, 2012Q2|中号牛皮纸袋]
    # 2  CK201301010085  [200609|西服罩袋, Z52101108|短款棉服, A82020103|休闲类便装,...
    # 3  CK201301010167  [2012Q2|中号牛皮纸袋, 200609|西服罩袋, A82707205|长款羊毛大衣,...
    # 4  CK201301010164  [A82707205|长款羊毛大衣, 200602|塑料衣架, 2012Q1|大号牛皮纸袋,...

    data_list = []
    for i in df2[1]:
        data_list.append(i)
    # print(data_list[:5])

# [['A82707207|长款羊毛大衣', '2012Q1|大号牛皮纸袋', 'A82131204|中长款羽绒服'], ['Z52636111|针织长袖T恤', '2012Q2|中号牛皮纸袋'], ['200609|西服罩袋', 'Z52101108|短款棉服', 'A82020103|休闲类便装', '2012Q1|大号牛皮纸袋', '200602|塑料衣架', 'A82707205|长款羊毛大衣'], ['2012Q2|中号牛皮纸袋', '200609|西服罩袋', 'A82707205|长款羊毛大衣', '200602|塑料衣架'], ['A82707205|长款羊毛大衣', '200602|塑料衣架', '2012Q1|大号牛皮纸袋', '200609|西服罩袋']]

    return data_list[:5]

def comb(lst):
    ret=[]
    for i in range(1,len(lst)+1):
        ret+=list(combinations(lst,i))
    return ret
class AprLayer(object):
    d=dict()
    def __init__(self):
        self.d=dict()
class AprNode(object):
    def __init__(self,node):
        self.s=set(node)
        self.size=len(self.s)
        self.lnk_nodes=dict()
        self.num=0
    def __hash__(self):
        return hash("__".join(sorted([str(itm) for itm in list(self.s)])))
    def __eq__(self, other):
        if "__".join(sorted([str(itm) for itm in list(self.s)]))=="__".join(sorted([str(itm) for itm in list(other.s)])):
            return True
        return False
    def isSubnode(self,node):
        return self.s.issubset(node.s)
    def incNum(self,num=1):
        self.num+=num
    def addLnk(self,node):
        self.lnk_nodes[node]=node.s

class AprBlk():
    def __init__(self,data):
        cnt=0
        self.apr_layers = dict()
        self.data_num=len(data)
        for datum in data:
            cnt+=1
            datum=comb(datum)
            nodes=[AprNode(da) for da in datum]
            for node in nodes:
                if not node.size in self.apr_layers:
                    self.apr_layers[node.size]=AprLayer()
                if not node in self.apr_layers[node.size].d:
                    self.apr_layers[node.size].d[node]=node
                self.apr_layers[node.size].d[node].incNum()
            for node in nodes:
                if node.size==1:
                    continue
                for sn in node.s:
                    sub_n=AprNode(node.s-set([sn]))
                    self.apr_layers[node.size-1].d[sub_n].addLnk(node)

    def getFreqItems(self,thd=1,hd=1):
        freq_items=[]
        for layer in self.apr_layers:
            for node in self.apr_layers[layer].d:
                if self.apr_layers[layer].d[node].num<thd:
                    continue
                freq_items.append((self.apr_layers[layer].d[node].s,self.apr_layers[layer].d[node].num))
        freq_items.sort(key=lambda x:x[1],reverse = True)
        return freq_items[:hd]

    def getConf(self,low=True, h_thd=10, l_thd=1, hd=1):
        confidence = []
        for layer in self.apr_layers:
            for node in self.apr_layers[layer].d:
                if self.apr_layers[layer].d[node].num < h_thd:
                    continue
                for lnk_node in node.lnk_nodes:
                    if lnk_node.num < l_thd:
                        continue
                    conf = float(lnk_node.num) / float(node.num)
                    confidence.append([node.s, node.num, lnk_node.s, lnk_node.num, conf])

        confidence.sort(key=lambda x: x[4])
        if low:
            return confidence[:hd]
        else:
            return confidence[-hd::-1]

class AssctAnaClass():
    def fit(self,data):
        self.apr_blk=AprBlk(data)
        return self
    def get_freq(self,thd=1,hd=1):
        return self.apr_blk.getFreqItems(thd=thd,hd=hd)
    def get_conf_high(self,thd,h_thd=10):
        return self.apr_blk.getConf(low=False, h_thd=h_thd, l_thd=thd)
    def get_conf_low(self,thd,hd,l_thd=1):
        return self.apr_blk.getConf(h_thd=thd,l_thd=l_thd,hd=hd)

def main():
    data = get_data()
    print("Freq",AssctAnaClass().fit(data).get_freq(thd=3,hd=10))
    print("Conf",AssctAnaClass().fit(data).get_conf_high(thd=3,h_thd=3))

if __name__ == '__main__':
    t1 = time.time()
    main()
    t2 = time.time()
    print('运行共耗时 {}秒'.format(t2 - t1))