let
    Դ = Excel.CurrentWorkbook(){[Name="��1"]}[Content],
    ����ͨ������ = Table.AddColumn(Դ,"����ͨ������",each Table.RowCount(Table.SelectRows(Դ,(x)=>x[�ı���1]=[�ı���1] and x[��ֵ]>[��ֵ]))+1),
    �й�ʽ���� = Table.AddColumn(����ͨ������,"�й�ʽ����",each Table.RowCount(Table.Distinct(Table.SelectRows(Դ,(x)=>x[�ı���1]=[�ı���1] and x[��ֵ]>[��ֵ]),"��ֵ"))+1)
in  �й�ʽ����