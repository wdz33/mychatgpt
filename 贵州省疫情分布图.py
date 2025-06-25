import json
from pyecharts.charts import Map
from pyecharts.options import *
f=open(r"E:\python\资料\资料\可视化案例数据\地图数据\疫情.txt","r",encoding="UTF-8")
data=f.read()
f.close()

data_dict=json.loads(data)
citys_data=data_dict["areaTree"][0]["children"][29]["children"]

city_data_list=[]
for city_data in citys_data:
    city_name=city_data["name"]+ "市"
    city_confirm = city_data["total"]["confirm"]
    city_data_list.append((city_name,city_confirm))
    city_data_list.append(("黔西南布依族苗族自治州",city_confirm))
    city_data_list.append(("黔南布依族苗族自治州",city_confirm))
    city_data_list.append(("黔东南苗族侗族自治州",city_confirm))


map=Map()
map.add("贵州省疫情分布图",city_data_list,"贵州")

map.set_global_opts(
    title_opts=TitleOpts(title="贵州省疫情分布图"),
    visualmap_opts=VisualMapOpts(
        is_show=True, #是否显示
        is_piecewise=True, #是否分段
        pieces=[
            {"min":1,"max":99,"lable":"1-99人","color":"#CCFFFF"},
            {"min":100,"max":999,"lable":"100-999人","color":"#FFFF99"},
            {"min":1000,"max":4999,"lable":"1000-4999人","color":"#FF9966"},
            {"min":5000,"max":9999,"lable":"5000-9999人","color":"#FF6666"},
            {"min":10000,"max":99999,"lable":"10000-99999人","color":"#CC3333"},
            {"min":100000,"lable":"100000+","color":"#99003"}
        ]
    )
)
map.render("贵州省疫情分布图.html")