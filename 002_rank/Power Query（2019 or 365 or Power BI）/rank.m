let
    源 = Excel.CurrentWorkbook(){[Name="表1"]}[Content],
    国际通用排名 = Table.AddColumn(源,"国际通用排名",each Table.RowCount(Table.SelectRows(源,(x)=>x[文本列1]=[文本列1] and x[数值]>[数值]))+1),
    中国式排名 = Table.AddColumn(国际通用排名,"中国式排名",each Table.RowCount(Table.Distinct(Table.SelectRows(源,(x)=>x[文本列1]=[文本列1] and x[数值]>[数值]),"数值"))+1)
in  中国式排名