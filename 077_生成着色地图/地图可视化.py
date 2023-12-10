from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker
from pyecharts.globals import ThemeType
import pandas as pd


""" # 官方范例
c = (
    Map()
    .add("商家A", [list(z) for z in zip(Faker.provinces, Faker.values())], "china")
    .set_global_opts(
        # InitOpts=opts.InitOpts(width="2000px",height="1500px"),
        title_opts=opts.TitleOpts(title="Map-VisualMap（分段型）"),
        visualmap_opts=opts.VisualMapOpts(max_=200, is_piecewise=True,item_width=50,item_height=35),
    )
    .render("map_visualmap_piecewise.html")
)
"""

df = pd.read_excel("./样例数据.xlsx")
provinces = df["省"].tolist()
peoples = df["人数"].tolist()
result = list(zip(provinces,peoples))
# print(df.describe())

picture = (
    Map(init_opts=opts.InitOpts(theme=ThemeType.MACARONS,width="1800px",height="1000px"))
    .add("", result, "china",label_opts=opts.LabelOpts(font_size=24))
    .set_global_opts(
        title_opts=opts.TitleOpts(title="XX公司用户全国分布图"),
        visualmap_opts=opts.VisualMapOpts(pieces=[{"min": 1,"max":10000},{"min": 10001, "max": 100000},{"min": 100001, "max": 1000000},{"min": 1000001}],is_piecewise=True),
        toolbox_opts=opts.ToolboxOpts(is_show=True)
    )
    .render("XX公司用户全国分布图.html")
)