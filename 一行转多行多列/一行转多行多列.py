import pandas as pd
from openpyxl import load_workbook

def read_data(file):
    df = pd.read_excel(file, sheet_name='data',header=None)
    return df

def method_1(df,col_num):
    df1 = df.T
    rows = df1.shape[0]
    rows_divide = rows // col_num
    df1['index1'] = sorted([i for i in range(0,rows_divide)] * col_num)
    df1['index2'] = [i for i in range(0,col_num)] * rows_divide
    df1['index1'] = df1['index1'].astype(str)
    df1['index2'] = df1['index2'].astype(str)
    df1.rename(columns={0:'value'},inplace=True)
    df1.set_index(['index1','index2'],inplace=True)
    df1 = df1.unstack()
    df1.columns = ['_'.join(col) for col in df1.columns.values]
    return df1

def method_2(df, col_num):
    df2 = pd.DataFrame(df.values.reshape(-1, col_num))
    return df2

def generate_data(file, df1, df2):
    with pd.ExcelWriter(file,mode='a',engine='openpyxl') as writer:
        wb = load_workbook(file)
        writer.book = wb
        try:
            df1.to_excel(writer, sheet_name='方法一',index=False)
            df2.to_excel(writer, sheet_name='方法二',index=False)
        except ValueError:
            pass

def main(file,col_num):
    df = read_data(file)
    df1 = method_1(df, col_num)
    df2 = method_2(df, col_num)
    generate_data(file, df1, df2)
    print(f'转换成功！！')

if __name__ == '__main__':
    file = './一行转多行多列.xlsx'
    col_num = 5
    main(file,col_num)