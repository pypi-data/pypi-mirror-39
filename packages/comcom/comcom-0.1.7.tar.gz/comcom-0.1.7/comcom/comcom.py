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
from tqdm import tqdm


def add_combasic(com_list,**kwargs):
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
    update_count = 0
    except_count = 0

    try:
        mongo_dat_client = pymongo.MongoClient(mongo_dat_uri)
        for com in tqdm(com_list):
            try:
                com["incr"]  = int(time.time()*1000*1000*1000)
                com["cthr"]  = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime()) 
                com["uthr"]  = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())
                com["ctime"] = int(time.time())
                com["utime"] = int(time.time())
                dbcom = mongo_dat_client.comdb.combasic.find_one({"name":com["name"]})
                if dbcom is None:
                    mongo_dat_client.comdb.combasic.insert_one(com)
                    insert_count +=1
                else:
                    pass
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
    return insert_count,update_count,except_count




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
    for com in tqdm(com_list):
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
    ret = add_combasic(com_list)
    print(ret)
if __name__ == '__main__':
    main()
