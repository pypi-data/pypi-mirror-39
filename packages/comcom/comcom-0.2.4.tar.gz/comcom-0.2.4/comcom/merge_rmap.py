# coding:utf-8
#功能：最后用于判断得的范围
#https://www.sohu.com/a/163372936_622516
#工商登记对于经营范围要怎么写并没有明确的规定，不要求字数也没有类别限制。但是通常来说，经营范围的填写最好规范、易懂。如果真的不知道怎么写呢。就到国家统计局上去，找到“国民经济行业分类”，在这里可以看到比较规范的描述。

import logging
import json
import re
import datetime
import json
import re
import string
import ml3
import copy
import os
import numpy
import traceback
res_files_bak = [
    "rmap_0.json",
    "rmap_1.json",
    "rmap_2.json",
    "rmap_3.json",
    "rmap_4.json",
    "rmap.json",
    "rmap_咨询.json",
    "rmap_基本.json",
    "rmap_开采.json",
    "rmap_教育.json",
    "rmap_服务.json",
    "rmap_生产制造加工.json",
    "rmap_种植.json",
    "rmap_管理.json",
    "rmap_通用1.json",
    "rmap_通用2.json",
    "rmap_通用3.json",
    "rmap_销售.json",
    "rmap_饲养养殖.json"
]

       
res_files2 = [
    "rmap_0.json",
    "rmap_1.json",
    "rmap_2.json",
    "rmap_3.json",
    "rmap_4.json",
    "rmap.json",
]

res_files = [
    "rmap_咨询.json",
    "rmap_开采.json",
    "rmap_教育.json",
    "rmap_服务.json",
    "rmap_制造.json",
    "rmap_种植.json",
    "rmap_管理.json",
    "rmap_销售.json",
    "rmap_饲养.json"
]




files = []
for file_name in res_files:
    if file_name.startswith("rmap_"):
        files.append(file_name)


for rmap_file_name in files:
    gbbs_rmap = {}
    print("loaing... "+rmap_file_name)
    rmap_json =  ml3.tools.load_json_file(os.path.join("data",rmap_file_name))
    gbbs_rmap.update(rmap_json)
    new_gbbs_rmap = {}

    for k,v in gbbs_rmap.items():
        new_gbbs_rmap[k] = []
        for v2 in v:
            if "com" in v2:
                v2.pop("com")
            if "explain" in v2:
                v2.pop("explain")
            new_v2 = {
                #"name":v2["name"],
                "name":";".join(v2["name"]),
                "cond":v2["cond"]
            }
            new_gbbs_rmap[k].append(new_v2)
        ml3.tools.dump_json_file(new_gbbs_rmap,"data/"+rmap_file_name,indent = 4)
