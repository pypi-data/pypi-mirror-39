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
        self.scopeverbs  = ml3.tools.load_json_file(os.path.join(self.module_path,"data","scopeverbs.json"))
        self.ignores     = ml3.tools.load_json_file(os.path.join(self.module_path,"data","ignores.json"))
        self.gbbs_dict   = ml3.tools.load_json_file(os.path.join(self.module_path,"data","gbt4547.json"))
        rmap_files = [
            "rmap_其它.json",
            "rmap_咨询.json",
            "rmap_基本.json",
            "rmap_开采.json",
            "rmap_教育.json",
            "rmap_服务.json",
            "rmap_制造.json",
            "rmap_种植.json",
            "rmap_管理.json",
            "rmap_其它.json",
            "rmap_销售.json",
            "rmap_饲养.json"
        ]
        rmap_files = os.listdir(os.path.join(self.module_path,"rmap"))
        self.gbbs_rmap = {"其它":[]}
        for rmap_file_name in rmap_files:
            #print("loaing... "+rmap_file_name)
            rmap_json =  ml3.tools.load_json_file(os.path.join(self.module_path,"rmap",rmap_file_name))
            self.gbbs_rmap.update(rmap_json)
 
    def GetRmapList(self,scopeseg_str):
        new_phrase_list = []
        bad_verbs_list = []
        bad_phrase_list = []
        gbbs_dict = self.gbbs_dict
        gbbs_rmap = self.gbbs_rmap
 
        #对scopeseg_str文本进行动词提取,提取的动词作为经营范围分析的关键成分.
        scope_verbs = self.get_scopeverbs_from_scopeseg(scopeseg_str)
        #从scopeseg_str中提取经营范围短语列表
        phrase_list = self.get_phrases_from_scopeseg(scopeseg_str)
      
        all_rmap_list = []
        for verb in scope_verbs:
            if verb not in gbbs_rmap.keys():
                continue
            rmap_list = gbbs_rmap[verb]
            all_rmap_list.extend(rmap_list)

        for phrase in phrase_list:
            if phrase not in gbbs_rmap:
                bad_phrase_list.append(phrase)
            else:
                all_rmap_list.extend(gbbs_rmap[phrase])

        for rmap_item in all_rmap_list:
            if rmap_item["cond"] == "":
                new_phrase_list.extend(rmap_item["name"].split(";"))
            else:
                if re.findall(rmap_item["cond"],scopeseg_str) != []:
                    new_phrase_list.extend(rmap_item["name"].split(";"))

        if new_phrase_list != []:
            new_phrase_list = list(set(new_phrase_list))

        if bad_phrase_list != []:
            bad_phrase_list = list(set(bad_phrase_list))
        
        if bad_verbs_list != []:
            bad_verbs_list = list(set(bad_verbs_list))
        
        return new_phrase_list,bad_phrase_list,bad_verbs_list

       


    #通过scope_str_original获取分组
    def scope2list(self,scope_str_original):
        #--------------------------------------------------------------
        #对scope_str_original进行预处理
        #标点符号替换
        #参考 https://doc.xuehai.net/b5be0648181b6ac0d88440106.html
        #括号常用的形式是圆括号“()”。此外还有方括号“[ ]”、六角括号“〔〕”和方头括号“【】”。公文编号中的发文年份，用六角括号标示。尽量避免括号套用。同一形式的括号不得套用。必须套用时，可采取六角括号与圆括号配合使用。一般情况下，里面用圆括号，外面用六角括号。
        scope_str = scope_str_original
        
        scope_str = scope_str.replace("\n",";")
        scope_str = scope_str.replace("\r",";")
        scope_str = scope_str.replace("\t",";")
 
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
        scope_segs = re.split("[;.]",scope_str)
        if "" in scope_segs:scope_segs.remove("")
        for scope_seg in scope_segs:
            translated_scopes_part = self.scopeseg2list(scope_seg)
            if translated_scopes_part is not []:
                translated_scopes.extend(translated_scopes_part)
        return translated_scopes

    #从经营范围片段中提取到经营范围动词列表
    def get_scopeverbs_from_scopeseg(self,scopeseg_str):
        scope_verbs = [] 
        for k,v in self.scopeverbs.items():
            if k in scopeseg_str and v not in scope_verbs:
                scope_verbs.append(v)
        if scope_verbs == []:
            scope_verbs = ["其它","销售"]
        return scope_verbs

    
    def get_phrases_from_scopeseg(self,scopeseg_str):
        phrase_list =  re.split('、|,',scopeseg_str)
        phrase_list = list(set(phrase_list))
        if "" in phrase_list:
            phrase_list.remove("")
        
        if phrase_list == []:
            phrase_list = ["其它"]
        return phrase_list
         

    def scopeseg2list(self,scope_str_original):
        if scope_str_original == None:
            print("None scope ")
            return []
        #关键词列表要单独提取出来做分析
        module_path = self.module_path
        stop_list   = self.stop_list 
        scopeverbs  = self.scopeverbs
        ignores     = self.ignores
        gbbs_dict   = self.gbbs_dict
        gbbs_rmap   = self.gbbs_rmap
        
        lost_scope_dict = {}
        
        #在stop_list.json里存放了大量无关经营范围里的短语，这些短语都要从经营范围里直接删掉.
        scope_str = scope_str_original
        for stop_word in stop_list:
            if stop_word in scope_str:
                scope_str = scope_str.replace(stop_word,"")
        
      
        #开始进行翻译
        translated_list = [] 
        #存放每个公司的翻译后的向量
        translated_dict = {} 
        new_scope_list,bad_scope_list,bad_verbs_list = self.GetRmapList(scope_str)
        scope_list = new_scope_list
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
        
        scopes1_list= []
        scopes2_list= []
        scopes3_list= []
        scopes4_list= []
        
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
                
                scopes1_list.append(name1)
                scopes2_list.append(name2)
                scopes3_list.append(name3)
                scopes4_list.append(name4)

                vector1_list[tmpl1.index(name1)] = 1
                vector2_list[tmpl2.index(name2)] = 1
                vector3_list[tmpl3.index(name3)] = 1
                vector4_list[tmpl4.index(name4)] = 1
            except Exception as err:
                pass
        if scopes1_list != []:scopes1_list = list(set(scopes1_list))
        if scopes2_list != []:scopes2_list = list(set(scopes2_list))
        if scopes3_list != []:scopes3_list = list(set(scopes3_list))
        if scopes4_list != []:scopes4_list = list(set(scopes4_list))


        result = {
            "scopes1":scopes1_list,        
            "scopes2":scopes2_list,        
            "scopes3":scopes3_list,
            "scopes4":scopes4_list, 
            "vector1":vector1_list,        
            "vector2":vector2_list,        
            "vector3":vector3_list,        
            "vector4":vector4_list        
        }
        
        return result   


def main():
    #com_list = ml3.tools.load_json_file("com_list_demo.json")
    scope_str = "为市场提供管理服务，初级农产品、冻鲜禽肉、五金交电、建筑材料的销售。赤湾农副水产品批发市场的经营管理。"
    result = ComScoper().scope2vector(scope_str)
    print(scope_str)
    print(result)

if __name__ == '__main__':
    main()
