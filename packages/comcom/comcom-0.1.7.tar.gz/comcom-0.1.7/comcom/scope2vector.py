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

class ComScoper:
    #构造函数
    def __init__(self):
        #关键词列表要单独提取出来做分析
        self.module_path = os.path.dirname(__file__)
        self.stop_list   = ml3.tools.load_json_file(os.path.join(self.module_path,"data","stop_list.json"))
        self.keywords    = ml3.tools.load_json_file(os.path.join(self.module_path,"data","keywords.json"))
        self.ignores     = ml3.tools.load_json_file(os.path.join(self.module_path,"data","ignores.json"))
        self.gbbs_dict   = ml3.tools.load_json_file(os.path.join(self.module_path,"data","gbt4547.json"))
        
        res_files = [
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
        files = []
        for file_name in res_files:
            if file_name.startswith("rmap_"):
                files.append(file_name)
        
        self.gbbs_rmap = {}
        
        for rmap_file_name in files:
            #print("loaing... "+rmap_file_name)
            rmap_json =  ml3.tools.load_json_file(os.path.join(self.module_path,"data",rmap_file_name))
            self.gbbs_rmap.update(rmap_json)
        
        self.gbbs_last = {"通用":[]}
        for rmap_file_name in ["rmap_通用1.json","rmap_通用2.json","rmap_通用3.json"]:
            #print("loaing... "+rmap_file_name)
            rmap_json =  ml3.tools.load_json_file(os.path.join(self.module_path,"data",rmap_file_name))
            self.gbbs_last["通用"].extend(rmap_json["通用"])
 

    def GetRmapList(self,gbbs_dict,gbbs_rmap,gbbs_last,bs_verbs,scope_list,scope_str_original):
        new_scope_list = []
        bad_scope_list = []
        
       
        if bs_verbs == []:
            rmap_list = gbbs_last["通用"]
            for rmap in rmap_list:
                if rmap["cond"] == "":
                    continue
                if re.findall(rmap["cond"],scope_str_original) != []:
                    new_scope_list.extend(rmap["name"])
                    #一旦命中，相关的scope就要从
        if bs_verbs == []:
            bs_verbs = ["销售"]
        
        for bs_verb in bs_verbs:
            rmap_list = gbbs_rmap[bs_verb]
            for rmap in rmap_list:
                if rmap["cond"] == "": 
                    new_scope_list.extend(rmap["name"])
                elif re.findall(rmap["cond"],scope_str_original) != []:
                    new_scope_list.extend(rmap["name"])
        
        
        for scope in scope_list:
            if scope in gbbs_dict:
                new_scope_list.append(scope)
                continue
            if scope not in gbbs_rmap:
                bad_scope_list.append(scope)
                continue 
            rmap_list = gbbs_rmap[scope]
            for rmap in rmap_list:
                if rmap["cond"] == "": 
                    new_scope_list.extend(rmap["name"])
                elif re.findall(rmap["cond"],scope_str_original) != []:
                    new_scope_list.extend(rmap["name"])
                    #一旦命中，相关的scope就要从
        
        
        return new_scope_list,bad_scope_list

    #通过scope_str_original获取分组
    def scope2list(self,scope_str_original):
        #--------------------------------------------------------------
        #对scope_str_original进行预处理
        #标点符号替换
        #参考 https://doc.xuehai.net/b5be0648181b6ac0d88440106.html
        #括号常用的形式是圆括号“()”。此外还有方括号“[ ]”、六角括号“〔〕”和方头括号“【】”。公文编号中的发文年份，用六角括号标示。尽量避免括号套用。同一形式的括号不得套用。必须套用时，可采取六角括号与圆括号配合使用。一般情况下，里面用圆括号，外面用六角括号。
        scope_str = scope_str_original
        scope_str = scope_str.replace("，",",")
        scope_str = scope_str.replace("。",".")
        scope_str = scope_str.replace("【","[")
        scope_str = scope_str.replace("】","]")
        scope_str = scope_str.replace("〔","(")
        scope_str = scope_str.replace("〕",")")
        scope_str = scope_str.replace("[","(")
        scope_str = scope_str.replace("]",")")
        #把所有()里面的内容去掉
        rep = re.compile("\((.*)\)")
        m_strs = re.findall(rep, scope_str)
        m_strs = list(map(lambda x:"(" + str(x) + ")", m_strs))
        for i in m_strs:
            scope_str = scope_str.replace(i, "")
   
        #比如冒号有三种“︰﹕：”，分别是比号、英式冒号和中式冒号，在输入时应注意。另外，在经营范围中输入英文字母与数字时，应使用半角字符，如“ABC123”，而非“ＡＢＣ１２３”，否者格式就不美观，在数据的传递过程中也容易出现乱码。
        scope_str = scope_str.replace("︰",":")
        scope_str = scope_str.replace("﹕",":")
        scope_str = scope_str.replace("：",":")
        #分号
        scope_str = scope_str.replace("；",";")

        #--------------------------------------------------------------
        #;和.是金鹰范围描述的最大单位.
        translated_scopes = []
        scope_segs = scope_str.split(";|.")
        for scope_seg in scope_segs:
            translated_scopes_part = self.scopeseg2list(scope_seg)
            if translated_scopes_part is not []:
                translated_scopes.extend(translated_scopes_part)
        return translated_scopes

    def scopeseg2list(self,scope_str_original):
        if scope_str_original == None:
            print("None scope ")
            return []
        #关键词列表要单独提取出来做分析
        module_path = self.module_path
        stop_list   = self.stop_list 
        keywords    = self.keywords
        ignores     = self.ignores
        gbbs_dict   = self.gbbs_dict
        gbbs_rmap   = self.gbbs_rmap
        gbbs_last   = self.gbbs_last
        
        lost_scope_dict = {}
        
        replace2space_list = [
            "*","1、","2、","3、","4、","5、","6、","7、","8、","9、","〓","\n","\r","\t",")",",","【","】","”","“"
        ]
        replace2space_list_fast = ["*","〓","\n","\r","\t"]
        
        
        #把经营范围里的换行，回车等换成空格    
        for item in replace2space_list:
            scope_str_original = scope_str_original.replace(item," ")
        
        #在stop_list.json里存放了大量无关经营范围里的短语，这些短语都要从经营范围里直接删掉.
        scope_str = scope_str_original
        for stop_word in stop_list:
            if stop_word in scope_str:
                scope_str = scope_str.replace(stop_word,"")
        
        #对scope_str文本进行动词提取,提取的动词作为经营范围分析的关键成分.
        bs_verbs = [] 
        for k,v in keywords.items():
            if k in scope_str and v not in bs_verbs:
                bs_verbs.append(v)
        
        #对scope_str进行字符切分,切分分为两步，先是忽略、号，然后切、号
        #上面的操作保留了、号,这是经营范围里的一大符号，上面是没有去掉、号，我们为了能够把顿号里的也给内容分开，拿到。我们就在这里再把顿号分开
        #另外把销售:办公设备中的这个办公设备给区分出来.
        seg_list = re.split('[，：:；。.;,〔〕()（）的 ]',scope_str)
        seg_list = list(set(seg_list))
        if "" in seg_list:
            seg_list.remove("")
        scope_list = seg_list
        tmp_scope_list = copy.deepcopy(scope_list)
        for scope in scope_list:
            if "、" in scope:
                seg_list = re.split('、',scope)
                tmp_scope_list.extend(seg_list)
        scope_list = tmp_scope_list
        scope_list = list(set(scope_list))
        if "" in scope_list:
            scope_list.remove("")
        scope_list.extend(seg_list)
        if scope_list == []:
            return []
        scope_list = list(set(scope_list))
            
        
        #开始进行翻译
        translated_list = [] 
        #存放每个公司的翻译后的向量
        translated_dict = {} 
        
        new_scope_list,bad_scope_list = self.GetRmapList(gbbs_dict,gbbs_rmap,gbbs_last,bs_verbs,scope_list,scope_str_original)
        
        scope_list      = list(set(new_scope_list))
        bad_scope_list  = list(set(bad_scope_list))
        scope_list      = list(set(scope_list) - set(bad_scope_list))
        
        #这个时候,有大量："办公用品"，"五金产品" 这样名词，但是我们不知道它是生产还是销售。所以我们就要遍历一遍所有的关键词。
        for bad_scope in bad_scope_list:
            getback = 0
            for k,v in keywords.items():
                if k in scope_str and v in gbbs_rmap:
                    for item in gbbs_rmap[v]:
                        if  bad_scope in item["cond"]: #想象item["cond"]是劳保
                        #if  re.findall(item["cond"],bad_scope) != []: #想象item["cond"]是劳保
                            scope_list.extend(item["name"])
                            getback +=1
            if getback == 0:
                scope_list.append(bad_scope)
        
        scope_list = list(set(scope_list))
        
        for scope in scope_list:
            if scope == "":
                #有可能存在空的经营范围
                continue
            if scope == "n/a":
                #根本没有办法标注类别
                continue
            if scope in ignores:
                #如果scope在忽略列表里
                continue
            if scope not in gbbs_dict:
                #如果scope不在gbbs_dict字典里
                continue
            res_scope = gbbs_dict[scope]
            
            new_scope = {
                "gcode":res_scope["code1"] if "code1" in res_scope else "",        
                "gname":res_scope["name1"] if "name1" in res_scope else "",        
                "bcode":res_scope["code2"] if "code2" in res_scope else "",        
                "bname":res_scope["name2"] if "name2" in res_scope else "",        
                "mcode":res_scope["code3"] if "code3" in res_scope else "",        
                "mname":res_scope["name3"] if "name3" in res_scope else "",        
                "scode":res_scope["code4"] if "code4" in res_scope else "",        
                "sname":res_scope["name4"] if "name4" in res_scope else ""       
            }
            translated_list.append(new_scope)
        
        
        return translated_list

    def scope2vector(self,scope_str_original):
        module_path = os.path.dirname(__file__)
        scopes = self.scope2list(scope_str_original)
        gbt4547_tmpl = ml3.tools.load_json_file(os.path.join(module_path,"data","gbt4547_tmpl.json"))
        
        vector1_list=list(numpy.zeros(len(gbt4547_tmpl["vector1"])))
        vector2_list=list(numpy.zeros(len(gbt4547_tmpl["vector2"])))
        vector3_list=list(numpy.zeros(len(gbt4547_tmpl["vector3"])))
        vector4_list=list(numpy.zeros(len(gbt4547_tmpl["vector4"])))
        
        vector1_list = [int(i) for i in vector1_list]
        vector2_list = [int(i) for i in vector2_list]
        vector3_list = [int(i) for i in vector3_list]
        vector4_list = [int(i) for i in vector4_list]
         
        tmpl1 = gbt4547_tmpl["vector1"]
        tmpl2 = gbt4547_tmpl["vector2"]
        tmpl3 = gbt4547_tmpl["vector3"]
        tmpl4 = gbt4547_tmpl["vector4"]
        for scope in scopes:
            try:
                if "gname" not in scope:continue
                if "bname" not in scope:continue
                if "mname" not in scope:continue
                if "sname" not in scope:continue
                name1 = scope["gname"]
                name2 = scope["bname"]
                name3 = scope["mname"]
                name4 = scope["sname"]
                
                if name1 == "":continue
                if name2 == "":continue
                if name3 == "":continue
                if name4 == "":continue
                
                vector1_list[tmpl1.index(name1)] = 1
                vector2_list[tmpl2.index(name2)] = 1
                vector3_list[tmpl3.index(name3)] = 1
                vector4_list[tmpl4.index(name4)] = 1
            except Exception as err:
                print(err)
                print(scope)
                pass
        vector = {
            "vector1":vector1_list,        
            "vector2":vector2_list,        
            "vector3":vector2_list,        
            "vector4":vector2_list        
        }
        
        return vector    


