
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

def getcomlogoname(com_name):
    #以下是要获取的企业Logo信息所需要的元素,企业Logo名应该由,
    #1. 企业所在的省, com_province
    #2. 企业所在的市, com_city
    #3. 企业特色命名, com_feature
    #4. 企业公司模板, com_type
    #5. 企业名字后缀, com_tail
    #   根据一定原则生成最好的logo名字，如果四个字更好
    #   企业的全名一定是:
    #   企业省 + 企业市 + 企业特色 + 企业模板 + 企名后缀 
    #   我们LOGO起名优先级是.
    """
    1. 企业特色,if 特色长于4个汉字,就取前四个汉字
                if 特色等于4个汉字,就取特色名
                if 特色等于3个汉字,就取三个汉字
                if 特色等于2个汉字
                    if com_feature有两个字的对应:
                        com_logo = com_feature + com_type_2
                    elif com_city是两个字的:
                        com_logo = com_city + com_feature
                    elif com_city是空的:
                        if com_province 是两个字的:
                            com_logo = com_province + com_feature
                        elif com_province =="":
                            if com_type_2不存在
                    如果com_city是两个字，结果=com_city+com_feature
                    如果com_city是大于两个字, 
    """
    com_name_original = com_name

    com_province = ""
    com_city = ""
    com_feature = ""
    com_type = ""
    com_type_s1 = ""
    com_type_s2 = ""
    com_type_s3 = ""
    com_tail = ""
    com_tail_s1 = ""
    com_tail_s2 = ""
    com_tail_s3 = ""
    com_logo = ""
    #录入省/城市数据
    
    module_path = os.path.dirname(__file__)
    city_list = ml3.tools.load_json_file(os.path.join(module_path,"json","com_cities.json"))
    city_flag = False
    province_flag = False
    for city_item in city_list:
        province_name       = city_item["province"]
        city_name           = city_item["city"]
        province_name_mini  = province_name.replace("省","")
        city_name_mini = city_name.replace("市","")
        if province_name_mini != "" and province_name_mini in com_name and not province_flag:
            com_province = province_name_mini
            com_name = com_name.replace(province_name,"")
            com_name = com_name.replace(province_name_mini,"")
            province_flag = True
        if city_name_mini != "" and city_name_mini in com_name and not city_flag :
            com_city = city_name_mini
            com_name = com_name.replace(city_name,"")
            com_name = com_name.replace(city_name_mini,"")
            city_flag = True

    #把公司名里的(),[],等去掉
    com_name = com_name.replace("【","[")
    com_name = com_name.replace("】","]")
    com_name = com_name.replace("〔","(")
    com_name = com_name.replace("〕",")")
    com_name = com_name.replace("[","(")
    com_name = com_name.replace("]",")")
    rep = re.compile("\((.*)\)")
    m_strs = re.findall(rep, com_name)
    m_strs = list(map(lambda x:"(" + str(x) + ")", m_strs))
    for i in m_strs:
        com_name = com_name.replace(i, "")

    #兰州中力商情信息咨询有限公司
    com_types = ml3.tools.load_json_file(os.path.join(module_path,"json","com_types.json"))
    for k,v in com_types.items():
        if k in com_name:
            com_type = k
            com_type_sx_list = com_type.split("|")
            for com_type_sx_item in com_type_sx_list:
                if len(com_type_sx_item) == 1:com_type_s1 = com_type_sx_item
                if len(com_type_sx_item) == 2:com_type_s2 = com_type_sx_item
                if len(com_type_sx_item) == 3:com_type_s3 = com_type_sx_item
            break
    if com_type != "":
        com_feature = com_name.split(com_type)[0] 


    com_tails = ml3.tools.load_json_file(os.path.join(module_path,"json","com_tails.json"))
    for k,v in com_tails.items():
        if k in com_name:
            com_tail = k
            com_tail_sx_list = com_tail.split("|")
            for com_tail_sx_item in com_tail_sx_list:
                if len(com_tail_sx_item) == 1:com_tail_s1 = com_tail_sx_item
                if len(com_tail_sx_item) == 2:com_tail_s2 = com_tail_sx_item
                if len(com_tail_sx_item) == 3:com_tail_s3 = com_tail_sx_item
            break
    com_debug = { 
        "com_province" : com_province,
        "com_city" : com_city    ,
        "com_feature" : com_feature ,
        "com_type" : com_type    ,
        "com_type_s1" : com_type_s1 ,
        "com_type_s2" : com_type_s2 ,
        "com_type_s3" : com_type_s3 ,
        "com_tail" : com_tail    ,
        "com_tail_s1" : com_tail_s1 ,
        "com_tail_s2" : com_tail_s2 ,
        "com_tail_s3" : com_tail_s3 
    }

    #有个默认的名字，就是公司的前四个汉字 
    com_logo  = ""

    #优先
    if len(com_feature) >= 4:
        com_logo = com_feature[:4]
        return com_logo

    if len(com_feature) == 3:
        if com_type_s1 != "":com_logo = com_feature + com_type_s1
        if com_tail_s1 != "":com_logo = com_feature + com_tail_s1
        else:
            com_logo = com_feature
        return com_logo

    #两个字的com_feature优先和com_type合作
    if len(com_feature) == 2:
        if com_type_s2 != "":com_logo = com_feature + com_type_s2
        if com_tail_s2 != "":com_logo = com_feature + com_tail_s2
        elif len(com_city) == 2:
            com_logo = com_city+ com_feature
        elif len(com_province) == 2:
            com_logo = com_province + com_feature
        elif com_type != "":
            com_logo = com_feature + com_type[:2]
        return com_logo

    #一个字的com_feature
    if len(com_feature) == 1:
        if len(com_city) == 2:
            com_logo = com_city+ com_feature
        elif len(com_province) == 2:
            com_logo = com_province + com_feature
        elif com_type != "":
            com_logo = com_feature + com_type[:3]
        return com_logo

    #空的com_feature
    if len(com_feature) == 0:
        if len(com_city) == 2 and com_type_s2 != "":
            com_logo = com_city+ com_type_s2
        elif len(com_city) == 2 and com_tail_s2 != "":
            com_logo = com_city+ com_tail_s2
        elif len(com_province) == 2 and com_type_s2 != "":
            com_logo = com_province + com_type_s2
        elif len(com_province) == 2 and com_tail_s2 != "":
            com_logo = com_province + com_tail_s2

    com_logo  = com_logo[:4]
    return com_logo

def main():
    test_names = [
        "兰州中力商情信息咨询有限公司",
        "成都千寻文化传媒有限公司",
        "绍兴市洁达工程渣土运输有限公司"
    ]
    for test_name in test_names:
        logo_name = getcomlogoname(test_name)
        
        print(test_name +" ->　"+logo_name) 
if __name__ == '__main__':
    main()
