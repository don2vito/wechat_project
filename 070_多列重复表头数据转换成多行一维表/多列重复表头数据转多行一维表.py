import pandas as pd

def reshape_df(df,start_col_num,interval_num):
    # 提取待合并的所有列名，一会可以把它们 drop 掉
    merge_names = list(df.iloc[:,start_col_num:].columns.values)
    
    def merge_cols(x):
        '''
        x 是一个行 Series，把它们按分隔符合并
        '''
        # 删除为空的列
        x = x[x.notna()]
        # 使用 x.values 用于合并
        y = x.values
        # 合并后的列表，每个元素是'课程' + '成绩'对
        result = []
        # range 的步长为 2，目的是每 2 列做合并
        for idx in range(0, len(y), interval_num):
            # 使用竖线作为'课程' + '成绩'之间的分隔符
            result.append(f'{y[idx]}|{y[idx+1]}')
        # 将所有两两对，用 # 分割，返回一个大字符串
        return '#'.join(result)
    
    # 添加新列，把待合并的所有列变成一个大字符串
    df['merge'] = df.iloc[:,start_col_num:].apply(merge_cols, axis=1)
    
    # 把不用的列删除掉
    df.drop(merge_names, axis=1, inplace=True)
    
    # 先将 merge 列变成 list 的形式
    df['merge'] = df['merge'].str.split('#')
    
    # 执行 explode 变成多行
    df_explode = df.explode('merge')
    
    # 分别从 merge 中提取两列
    df_explode['课程']=df_explode['merge'].str.split('|').str[0]
    df_explode['成绩']=df_explode['merge'].str.split('|').str[1]
    
    # 把 merge 列删除掉，得到最终数据
    df_explode.drop('merge', axis=1, inplace=True)
    
    # 输出到结果 Excel
    df_explode.to_excel('./输出结果.xlsx', index=False)
    
    print('运行成功！！')


def main():
    file_path = './多列重复表头数据转多行一维表.xlsx'
    df = pd.read_excel(file_path)
    reshape_df(df,1,2)


if __name__ == '__main__':
    main()