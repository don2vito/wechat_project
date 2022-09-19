import pandas as pd

df = pd.read_excel('test.xlsx',date_parser='date')

print(df.head())

def date(para):
    delta = pd.Timedelta(str(int(para))+'days')
    time = pd.to_datetime('1899-12-30') + delta
    return time

df['date'] = df['date'].apply(date).dt.date

print(df.head())

df.to_excel('result.xlsx',index=False)