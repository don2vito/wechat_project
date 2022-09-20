from faker import Faker
import pandas as pd
from prettytable import PrettyTable
from rich_dataframe import prettify
from rich.table import Table
from rich.console import Console
from rich.progress import track
from rich import print
import time
from rich.pretty import pprint
# from pprint import pprint
from rich.markdown import Markdown
from rich.syntax import Syntax
import json


# 构建虚拟的 dataframe
fake = Faker(['zh_CN'])
Faker.seed(100)

def get_data():
    key_list = ['姓名','地址','手机号','身份证号']
    name = fake.name()
    address = fake.address()
    number = fake.phone_number()
    id_card = fake.ssn()
    info_list = [name,address,number,id_card]
    person_info = dict(zip(key_list,info_list))
    return person_info

df = pd.DataFrame(columns=['姓名','地址','手机号','身份证号'])
for i in range(10):
    person_info = [get_data()]
    df_temp = pd.DataFrame(person_info)
    df = pd.concat([df,df_temp],ignore_index=True)
    
df.to_excel('example.xlsx',index=False)


# 使用原始的 print 输出 datamefra
print(f'使用原始的 print 输出 datamefra：\n{df}')

# 使用 prettytable 美化输出 dataframe
pt = PrettyTable()
pt.add_column('index',df.index)
for col in df.columns.values:
    pt.add_column(col, df[col])
print(f'使用 prettytable 美化输出 dataframe：\n{pt}')


# 使用 rich_dataframe 美化输出 dataframe
tb = prettify(df,row_limit=10,delay_time=1)
print('使用 rich_dataframe 美化输出 dataframe：\n')
print(tb)


# 使用 rich 美化输出 dataframe
console = Console()

table = Table(title='rich table example',expand=True,show_header=True, header_style="bold magenta")

for col in df.columns.values:
    table.add_column(col, justify='center', style='cyan', no_wrap=True)
    
for index,row in df.iterrows():          
    table.add_row(row['姓名'],row['地址'],row['手机号'], row['身份证号'])

print('使用 rich 美化输出 dataframe：\n')

console.print(table)


# 使用 rich 美化输出 进度条
for i in track(range(5), description='Processing...'):
    time.sleep(1)
    
    
# 使用 rich 美化输出 markdown
console = Console()
with open('如何打造爆品.md',encoding='UTF-8') as readme:
    markdown = Markdown(readme.read())

print('使用 rich 美化输出 markdown：\n')
console.print(markdown)


# 使用 rich 实现语法高亮显示
my_code = '''
def iter_first_last(values: Iterable[T]) -&gt; Iterable[Tuple[bool, bool, T]]:
    """Iterate and generate a tuple with a flag for first and last value."""
    iter_values = iter(values)
    try:
        previous_value = next(iter_values)
    except StopIteration:
        return
    first = True
    for value in iter_values:
        yield first, False, previous_value
        first = False
        previous_value = value
    yield first, True, previous_value
'''
syntax = Syntax(my_code, 'python', theme='monokai', line_numbers=True)
console = Console()

print('使用 rich 实现语法高亮显示：\n')
console.print(syntax)


# 使用 rich 美化输出 JSON
data = {
    "foo": [
        3.1427,
        (
            "Paul Atreides",
            "Vladimir Harkonnen",
            "Thufir Hawat",
        ),
    ],
    "atomic": (False, True, None),
} 

data = json.dumps(data, sort_keys=True, indent=2)
data = data.encode('utf-8').decode('unicode_escape')

print('使用 rich 美化输出 JSON：\n')
print(data)