# 造 n 条数据输出到 Excel 完整脚本如下：

# 方法一
from faker import Faker

fake = Faker(locale='zh_CN')

def save_to_excel(file_path, n):

    res = []
    for i in range(n):
        name = fake.name()
        phone = fake.phone_number()
        id_card = fake.ssn()

        res.append([name, phone, id_card, fake.company(), fake.address(), fake.credit_card_number(), fake.job(), fake.email()])

    # list转dataFrame
    df = pd.DataFrame(data=res, columns=['name', 'phone', 'id_card', 'comp', 'addr', 'bank_card', 'title', 'email'])
    print(df)
    # 保存到本地excel
    df.to_excel(file_path, index=False)

save_to_excel('./方法一结果.xlsx',5)





# 方法二
from faker import Faker
from faker_pandas import PandasProvider

fake = Faker()
fake.add_provider(PandasProvider)

colgen = fake.pandas_column_generator()

df2 = fake.pandas_dataframe(
    colgen.first_name('First Name', empty_value='', empty_ratio=.5),
    colgen.last_name('Last Name'),
    colgen.pandas_int('Age', 18, 80, empty_ratio=.2),
    rows=7
)

print(df2)
df2.to_excel('./方法二结果.xlsx', index=False)
