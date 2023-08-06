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


valid_rmap_verbs = [
   "代理",
   "管理",
   "教育",
   "工程",
   "技服",
   "技推",
   "种植",
   "制造",
   "咨询",
   "安装",
   "开采",
   "采选",
   "投资",
   "施工",
   "服务",
   "租赁",
   "维修",
   "设计",
   "运输",
   "销售",
   "技开",
   "养殖"
]

rmap_files = os.listdir("rmap")
for rmap_file_name in rmap_files:
    if rmap_file_name.startswith("rmap_"):
        pass
    else:
        print("error file:"+rmap_file_name)


gbbs_rmap = {}
for rmap_file_name in rmap_files:
    print("loaing... "+rmap_file_name)
    rmap_json =  ml3.tools.load_json_file("rmap/"+rmap_file_name)
    for k,v in rmap_json.items():
        if k not in gbbs_rmap:
            gbbs_rmap[k] = v
        else:
            gbbs_rmap[k].extend(v)

gbbs_rmap_other = {}

for k,v in gbbs_rmap.items():
    if len(v) > 5 and k in valid_rmap_verbs:
        print(k)
        ml3.tools.dump_json_file({k:v},"rmap_new/rmap_"+k+".json",indent = 4)
    else:
        gbbs_rmap_other[k] = v 

ml3.tools.dump_json_file(gbbs_rmap_other,"rmap_new/rmap_其它.json",indent = 4)
