#Wikicivi Crawler Client SDK
import os
import time
import datetime
import os,sys
import json
import re
import pymongo
from pymongo import MongoClient
import traceback
from bson import ObjectId
from .getcomlogo import getcomlogoname

def get_allow_combasic_dict():
    allow_combasic_dict = {
        "addr":"企业地址",
        "email":"公司邮箱",
        "name":"公司名称",
        "name_en":"英文名",
        "name_used":"曾用名",
        "name_logo":"特色名",
        "ctime":"数据时间",
        "cbrs":"参保人数",
        "code":"统一社会信用代码",
        "code_reg":"注册号",
        "code_tax":"纳税人识别号",
        "code_org":"组织机构代码",
        "date_est":"成立日期",
        "date_aprv":"核准日期",
        "district":"所属地区",
        "industry":"所属行业",
        "from":"信息来源",
        "intro":"公司简介",
        "legalp":"法人",
        "status":"经营状态",
        "staff":"人员规模",
        "site":"企业网站",
        "type":"公司类型",
        "capital_reg":"注册资本",
        "capital_paid":"实缴资本",
        "validity":"营业期限",
        "issuer":"登记机关",
        "scope":"经营范围",
        "tel":"电话",
        "url":"来源网址",
        "bank":"开户银行",
        "account":"银行账户",
        "incr":"自增字段",
        "utime":"更新时间",
        "cthr":"创建时间",
        "uthr":"更新时间",
        "html":"快照地址"
    }
    return allow_combasic_dict

def get_must_keys():
    must_keys = {
        "name",
        "code","code_reg",
        "legalp",
        "status",
        "type",
        "date_aprv",
        "date_est",
        "capital_reg",
        "validity",
        "issuer",
        "addr",
        "scope",
        "from"
    }
    return must_keys

def is_combasic(com):
    allow_combasic_dict = get_allow_combasic_dict()
    must_keys = get_must_keys()
    try:
        com_keys = com.keys()
        allow_keys = allow_combasic_dict.keys()
        
        for must_key in must_keys:
            if must_key not in com_keys:
                print(must_key+"("+allow_combasic_dict[must_key]+") not in com info")
                return False 
        
        for com_key in com_keys:
            if com_key not in allow_keys:
                print("意料之外的字段 "+com_key)
                return False
        
        #接下来把有"-"的字段变为""
        for k,v in com.items():
           if v == "-":com[k] = ""
        
        #把不存在的字段补为空字符串
        for k in allow_keys:
           if k not in com:
               com[k] = ""
        
        if com["name"] == "":
            print(allow_combasic_dict["name"] +"不能为空")
            return False
 
        if type(com["name_used"]) is not type(""):
            print("name_used("+allow_combasic_dict["name_used"] +")必须是字符串")
            return False
        
        if com["from"] not in ["企查查gs","企查查cbase","天眼查"]:
            print("意外的来源页面")
            return False
        if com["site"] in ["暂无"]:
            com["site"] = ""
        
        if com["site"] is not "" and not com["site"].startswith("http"):
            print("公司网址格式错误")
            return False

        if com["name_logo"] == "":
            com["name_logo"] = getcomlogoname(com["name"])
 
    except Exception as err:
        print(err)
        return False
    return True 

#判断一个统一社会信用码是否正确
def is_combasic_item(key,value):
    
    return True


"""
从数据库combasic和本地combasic中获取更新结构
diff_dict = {
    "update":{要直接写入数据库的更新信息},
    "from":{如果发生有意义的变更,那么变更要记录下来},
    "to:{变更时从from到to}"
}
"""
def diff_combasic(dbcom,com):
    try:
        if not is_combasic(dbcom):
            print("意料之外的公司属性(数据库)")
            return None
        if not is_combasic(com):
            print("意料之外的公司属性(本地)")
            return None
        allow_combasic_keys = get_allow_combasic_dict().keys()
        diff_dict = {
            "update":{},
            "log":{},
        }
        diff_update ={}
        diff_log = {}
        ignore_diff_keys = ["ctime","utime","cthr","uthr","incr"] 
        for com_k,com_v in com.items():
            if com_k in ignore_diff_keys:
                continue
            if com_v is "":
                continue
            if com_k not in dbcom:
                #本来数据库没有这项,那么一定要加上,但不记录入diff
                diff_update[com_k] = com_v
                continue
            #dbcom[com_k]存在
            if dbcom[com_k] is not "":
                dbcom_v = dbcom[com_k]
                if dbcom_v == com_v:
                    continue
                if com_k != "name_used":
                    diff_update[com_k] = com_v
                    diff_log[com_k] = {"from":dbcom_v,"to":com_v}
                else:
                    dbcom_v_list = dbcom_v.split(",")
                    if com_v not in dbcom_v_list:
                        new_dbcom_v = dbcom_v+","+com_v
                        diff_update[com_k] = new_dbcom_v
                        diff_log[com_k] = {"from":dbcom_v,"to":new_dbcom_v}
        diff_dict = {
            "update":diff_update,
            "log":diff_log,
        }
        return diff_dict
    except Exception as err:
        print(tracebck.format_exc())
        return None

def has_combasic_name(com_name,com_from = ""):
    env_dict = os.environ # environ是在os.py中定义的一个dict environ = {}
    if "MONGO_DAT_URI" not in env_dict:
        print("missing mongo_dat_uri in environment parameters")
        return 0
    mongo_dat_uri = env_dict["MONGO_DAT_URI"]

    try:
        mongo_dat_client = pymongo.MongoClient(mongo_dat_uri)
        find_condition = {"name":com_name}
        if com_from != "":
            find_condition["from"] = com_from
        dbcom = mongo_dat_client.comdb.combasic.find_one(find_condition)
        if dbcom is None:
            return False
        else:
            return True
    except Exception as err:
        return False
    return False 




def add_combasic(combasic_list,**kwargs):
    env_dict = os.environ # environ是在os.py中定义的一个dict environ = {}
    """
    #如果print(env_dist)就打印如下的结果 
    print (env_dist)
    environ({'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'HOSTNAME': '4deb392e9e8c', 'TERM': 'xterm', 'accessKeyID': 'STS.NJojWkbGonZCdnaMmxrtfbL6e', 'accessKeySecret': '4JPHTDuDfi635noMSwWEWhrv9gvg7gtcdL2A4J77NEJa', 'securityToken': 'CAIS7QF1q6Ft5B2yfSjIr4naIe3fj5hO2ZioZkjQqW0tfvtKjYmdhzz2IHFOdXVoBe4Zs/k/lGhZ6vcalqZdVplOWU3Da+B364xK7Q75z2kJD1fxv9I+k5SANTW5KXyShb3/AYjQSNfaZY3eCTTtnTNyxr3XbCirW0ffX7SClZ9gaKZ8PGD6F00kYu1bPQx/ssQXGGLMPPK2SH7Qj3HXEVBjt3gX6wo9y8Tkn5XEtEKG02eXkLFF+97DRbG/dNRpMZtFVNO44fd7bKKp0lQLukIbqP8q0vMZpGeX5oDBUgFLjBWPNezR/8d/koL44SSn+sUagAGtCzSUW4FmsSv6J8gU5L8wDktzx0UP40iR86ojiqYYXutCvoRcYc9BtkHlwrrnRY8QTMARCV1W54dmMrc2FyGFg4ol2kTcJ7VU0VbEWM9dwdlcfA5mFMe4fOjUkyoeNvS4SpW72MlUkLYjjNlDO+0q+fq9ejB3hPOPDMa+R7fIqg==', 'topic': 'HAM', 'example_env_key': 'example_env_value', 'LANG': 'C.UTF-8', 'GPG_KEY': '0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D', 'PYTHON_VERSION': '3.6.3', 'PYTHON_PIP_VERSION': '9.0.1', 'FC_FUNC_CODE_PATH': '/code/', 'LD_LIBRARY_PATH': '/code/:/code//lib:/usr/local/lib', 'HOME': '/tmp'})
    其中example_env_key是我们自定义的环境变量
    """
    if "MONGO_DAT_URI" not in env_dict:
        print("missing mongo_dat_uri in environment parameters")
        return 0
    mongo_dat_uri = env_dict["MONGO_DAT_URI"]

    insert_count = 0
    ignore_count = 0
    update_count = 0
    except_count = 0

    try:
        mongo_dat_client = pymongo.MongoClient(mongo_dat_uri)
        for combasic in combasic_list:
            try:
                if not is_combasic(combasic):
                    print(combasic)
                    raise Exception("企业信息格式错误")
                combasic["incr"]  = int(time.time()*1000*1000*1000)
                combasic["cthr"]  = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) 
                combasic["uthr"]  = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                combasic["ctime"] = int(time.time())
                combasic["utime"] = int(time.time())
                dbcombasic = mongo_dat_client.comdb.combasic.find_one({"name":combasic["name"],"from":combasic["from"]})
                if dbcombasic is None:
                    mongo_dat_client.comdb.combasic.insert_one(combasic)
                    #mongo的引用会给结构体带来_id属性.
                    if "_id" in combasic:combasic.pop("_id")
                    insert_count +=1
                    continue
                else:
                    #如果有新的code,那么替换新的
                    
                    dbcom = dict(dbcombasic)
                    com   = combasic
                    db_objid = dbcom.pop("_id")
                    
                    diff_dict = diff_combasic(dbcom,com)
                    if diff_dict is None:
                        raise Exception("DIFF失败")
                    if diff_dict["update"]  == {}:
                        ignore_count+=1
                    else:
                        diff_update = diff_dict["update"]
                        diff_update["utime"] = int(time.time())
                        diff_update["uthr"] = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                        mongo_dat_client.comdb.combasic.update_one({"_id":db_objid},{"$set":diff_update})
                        update_count +=1
                        if diff_dict["log"] is not {}:
                            diff_log = {
                                "diff":diff_dict["log"],
                                "ctime":int(time.time()),
                                "cthr":time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()),
                                "incr":int(time.time()*1000*1000*1000)
                            }
                            mongo_dat_client.comdb.combasic_dif.insert_one(diff_log)
 
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                except_count +=1
                continue
    except Exception as err:
        print(traceback.format_exc())
        print(err)
    return insert_count,update_count,ignore_count,except_count




def add_comnames(com_list,**kwargs):
    #priority越高的企业是优先级越高的企业，将来在更新信息上，优先级高的企业肯定是频繁先更新的.
    priority = 0.0
    merge_tags = False

    if "priority" in kwargs:
        priority = kwargs["priority"]
    else:
        print("没有指定priority参数,假设这批数据是垃圾圾企业名录,范围0到10")
        print("0:不知名的企业")
        print("9.9:非常重要的企业")
        priority = 0.0
        return 0

    if "merge_tags" in kwargs:
        merge_tags = kwargs["merge_tags"]
    else:
        print("没有指定merge_tags参数,忽略merge_tags")
        return 0

    do_update = False
    if merge_tags:
        do_update = True

    insert_count = 0
    update_count = 0
    except_count = 0
    comname_list = []
    com_dict = {}
    for com in com_list:
        if "name" not in com:
            print("缺少Name字段:"+str(com))
            return 0
        if com["name"] is None:
            #print("name字段为none")
            continue
        if "url" in com:
            com["url"] = [com["url"]]
        else:
            com["url"] = []
        if "tags" not in com:
            com["tags"] = []
        if "loc" in com:
            com["loc"] = [com["loc"]]
        else:
            com["loc"] = []



    for com in tqdm(com_list):
        if "name" not in com:
            print("缺少Name字段:"+str(com))
            return 0
        if com["name"] is None:
            #print("name字段为none")
            continue
        com_name = com["name"]
        if com_name not in com_dict:
            com_dict[com_name] = com
        else:
            tags1 = com_dict[com_name]["tags"]
            tags2 = com["tags"]
            com_dict[com_name]["tags"]  = list(set(tags1+tags2))
            url1 = com_dict[com_name]["url"]
            url2 = com["url"]
            com_dict[com_name]["url"]  = list(set(url1 + url2))
            loc1 = com_dict[com_name]["loc"]
            loc2 = com["loc"]
            com_dict[com_name]["loc"]  = list(set(loc1 + loc2))
         
    for k,com in tqdm(com_dict.items()):
        try:
            if "name" not in com:
                print("缺少Name字段:"+str(com))
                return 0

            if com["name"] is None:
                #print("name字段为none")
                continue
            com_name = com["name"]
            com_name = com_name.replace("（","(").replace("）",")")
            com_name = com_name.replace(" ","")
            com["name"] = com_name
            if "公司" not in com_name and "门市部" not in com_name and "":
                print("警告，例外的公司名称:"+com["name"])
            com_tags = com["tags"]
            com_tags = list(set(com_tags))
            com_urls = com["url"]
            com_locs = com["loc"]
            com_locs = list(set(com_locs))
            cur_time_incr = int(time.time()*1000*1000*1000)
            comname_list.append({"name":com_name,"tags":com_tags,"priority":priority,"url":com_urls,"loc":com_locs,"incr":cur_time_incr})
        except Exception as err:
            print(com)
            print(err)

    env_dict = os.environ # environ是在os.py中定义的一个dict environ = {}
    """
    #如果print(env_dist)就打印如下的结果 
    print (env_dist)
    environ({'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'HOSTNAME': '4deb392e9e8c', 'TERM': 'xterm', 'accessKeyID': 'STS.NJojWkbGonZCdnaMmxrtfbL6e', 'accessKeySecret': '4JPHTDuDfi635noMSwWEWhrv9gvg7gtcdL2A4J77NEJa', 'securityToken': 'CAIS7QF1q6Ft5B2yfSjIr4naIe3fj5hO2ZioZkjQqW0tfvtKjYmdhzz2IHFOdXVoBe4Zs/k/lGhZ6vcalqZdVplOWU3Da+B364xK7Q75z2kJD1fxv9I+k5SANTW5KXyShb3/AYjQSNfaZY3eCTTtnTNyxr3XbCirW0ffX7SClZ9gaKZ8PGD6F00kYu1bPQx/ssQXGGLMPPK2SH7Qj3HXEVBjt3gX6wo9y8Tkn5XEtEKG02eXkLFF+97DRbG/dNRpMZtFVNO44fd7bKKp0lQLukIbqP8q0vMZpGeX5oDBUgFLjBWPNezR/8d/koL44SSn+sUagAGtCzSUW4FmsSv6J8gU5L8wDktzx0UP40iR86ojiqYYXutCvoRcYc9BtkHlwrrnRY8QTMARCV1W54dmMrc2FyGFg4ol2kTcJ7VU0VbEWM9dwdlcfA5mFMe4fOjUkyoeNvS4SpW72MlUkLYjjNlDO+0q+fq9ejB3hPOPDMa+R7fIqg==', 'topic': 'HAM', 'example_env_key': 'example_env_value', 'LANG': 'C.UTF-8', 'GPG_KEY': '0D96DF4D4110E5C43FBFB17F2D347EA6AA65421D', 'PYTHON_VERSION': '3.6.3', 'PYTHON_PIP_VERSION': '9.0.1', 'FC_FUNC_CODE_PATH': '/code/', 'LD_LIBRARY_PATH': '/code/:/code//lib:/usr/local/lib', 'HOME': '/tmp'})
    其中example_env_key是我们自定义的环境变量
    """
    if "MONGO_DAT_URI" not in env_dict:
        print("missing mongo_dat_uri in environment parameters")
        return 0
    mongo_dat_uri = env_dict["MONGO_DAT_URI"]

    try:
        mongo_dat_client = pymongo.MongoClient(mongo_dat_uri)
        for com in tqdm(comname_list):
            try:
                dbcom = mongo_dat_client.comdb.comnames.find_one({"name":com["name"]})
                if dbcom is None:
                    mongo_dat_client.comdb.comnames.insert_one(com)
                    insert_count +=1
                elif do_update:
                    if "tags"  not in dbcom: dbcom["tags"] = []
                    com_tags = list(set(dbcom["tags"] + com["tags"]))
 
                    if "loc"  not in dbcom: dbcom["loc"] = []
                    if "url"  not in dbcom: dbcom["url"] = []
                   
                    if "priority"  not in dbcom: dbcom["priority"] = 0
                    if dbcom["priority"] > com["priority"]:
                        com["priority"] = dbcom["priority"]
                   
                    com_locs = []
                    com_urls = []
                    try:
                        com_urls.extend(com["url"])
                        com_urls.extend(dbcom["url"])
                        com_urls = list(set(com_urls))
                        if "" in com_urls:com_urls.remove("")
                    except Exception as err:
                        print(com_urls)
                    
                    try:
                        com_locs.extend(com["loc"])
                        com_locs.extend(dbcom["loc"])
                        com_locs = list(set(com_locs))
                        if "" in com_locs:com_locs.remove("")
                    except Exception as err:
                        print(com_locs)

                    com["url"] = com_urls
                    com["loc"] = com_locs
                    com["tags"] = com_tags
                    mongo_dat_client.comdb.comnames.update_one({"name":com["name"]},{"$set":com})
                    update_count +=1
            except Exception as err:
                print(traceback.format_exc())
                print(err)
                except_count +=1
                continue
        """
        ordered (optional): If True (the default) documents will be inserted on the server serially, in the order provided. If an error occurs all remaining inserts are aborted. If False, documents will be inserted on the server in arbitrary order, possibly in parallel, and all document inserts will be attempted.
        """
    except Exception as err:
        print(traceback.format_exc())
        print(err)
    #print("insert:"+str(insert_count))
    #print("update:"+str(update_count))
    #print("except:"+str(except_count))
    return insert_count,update_count,except_count


def main():
    com_list = [
        {'name':'测试1_北京科技有限公司','tags':["tag1","tag2"]},
        {'name':'测试3_北京科技有限公司','tags':["tag1","tag2"]}
    ]
    #add_comnames(com_list)
    #ret = add_combasic(com_list)
    ret = hascombasic_name()
    print(ret)

def verify_has_combasic_name(com_name):
    ret = has_combasic_name(com_name)
    print(ret)


def verify_is_combasic():
    target = {
        "name": "comcom测试公司",
        "legalp": "安秀民",
        "site": "暂无",
        "email": "",
        "intro": "",
        "capital_reg": "10万元人民币",
        "capital_paid": "-",
        "status": "吊销，未注销",
        "date_est": "1992-11-13",
        "code": "-",
        "code_tax": "-",
        "code_reg": "90125317-9",
        "code_org": "-",
        "type": "非公司私营企业",
        "industry": "批发和零售业",
        "date_aprv": "2004-03-31",
        "issuer": "海南省工商行政管理局",
        "district": "海南省",
        "name_en": "-",
        "name_used": [],
        "cbrs": "-",
        "staff": "-",
        "validity": "1992-11-13至1997-11-12",
        "addr": "海口市大同路3号",
        "scope": "打字,复印.,酒类,食品,百货",
        "tel": "",
        "bank": "",
        "account": "",
        "from": "企查查cbase",
        "ctime": 1544250895,
        "url": "https://www.qichacha.com/cbase_dda84e97e3ed9e07484a9cf757ed775e.html",
        "text": "html_text" 
    }
   
    ret = is_combasic(target)
    print(ret)
    print(target)

def verify_add_combasic():
    target = {
        "name": "北京测试测试网络科技有限公司",
        "legalp": "安秀民",
        "site": "暂无",
        "email": "",
        "intro": "",
        "capital_reg": "10万元人民币",
        "capital_paid": "-",
        "status": "吊销，未注销",
        "date_est": "1992-11-13",
        "code": "-",
        "code_tax": "-",
        "code_reg": "90125317-9",
        "code_org": "-",
        "type": "非公司私营企业",
        "industry": "批发和零售业",
        "date_aprv": "2004-03-31",
        "issuer": "海南省工商行政管理局",
        "district": "海南省",
        "name_en": "-",
        "name_used": "新的曾用名4",
        "cbrs": "-",
        "staff": "-",
        "validity": "1992-11-13至1997-11-12",
        "addr": "海口市大同路3号",
        "scope": "打字,复印.,酒类,食品,百货",
        "tel": "",
        "bank": "",
        "account": "",
        "from": "企查查cbase",
        "ctime": 1544250895,
        "url": "https://www.qichacha.com/cbase_dda84e97e3ed9e07484a9cf757ed775e.html"
    }
   
    ret = add_combasic([target])
    print(ret)
    print(target)

if __name__ == '__main__':
    #main()
    #verify_is_combasic()
    verify_add_combasic()
    name =  "海南裕通工贸公司中英文打字影印服务部"
    #verify_has_combasic_name(name)
