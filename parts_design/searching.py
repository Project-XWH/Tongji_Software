# -*- coding:utf-8 -*-

#-------------information---------------


#---------------packages----------------
import sqlite3
import difflib
import re
#---------------------------------------


def name_search(db,name,type = None,out_num = 20):
    '''
    searching data use name
    :param db:
    :param name:
    :param out_num:
    :return:
    '''

    conection = sqlite3.connect(db)
    cursor = conection.cursor()

    cs = cursor.execute("""
    select * from searching,text 
    where searching.name = text.name and searching.name ='""" + name + "'")
    if len(cs.fetchall()) == 0:
        cs = cursor.execute('select name from searching')
        name_list = [c[0] for c in cs]
        cand_list = []
        for n in name_list:
            score = difflib.SequenceMatcher(None, n, name).ratio()
            if score > 0.6:
                cand_list.append((n, score))
        cand_list = sorted(cand_list, key=lambda x: x[1], reverse=True)[:out_num]
        cand_list = ["'" + x[0] + "'" for x in cand_list]

        if type != None:
            headle = "select distinct * from searching,text where type = '" +type+"' and searching.name = text.name and searching.name = "
        else:
            headle = "select distinct * from searching,text where searching.name = text.name and searching.name = "
        #headle += " or searching.name = ".join(cand_list)
        #headle += ")"
        #print(headle)
        result_list = []
        for cand in cand_list:
            cs = cursor.execute(headle+cand)
            back_list = cs.fetchall()
            if len(back_list) > 0:
                result_list.append(back_list[0])
        conection.close()
        return result_list
    else:
        cs = cursor.execute("""
        select * from searching,text 
        where searching.name = text.name and searching.name ='""" + name + "'")
        back = cs.fetchall()
        conection.close()
        return back


def browser(db_name,requests = "searching.name,type,uses,status,description,categories,sequence",start=0,length=25,**kw):
    '''

    :param db_name: 数据库名字
    :param requests: 需要返回什么 默认全返回 ，若有选择直接以字符串形式输入需要的列名，中间用 ，隔开 （ps. parts_id,parts_name分别对应列名id,searching.name，其他不变）
    :param start: 从哪开始返回
    :param length: 返回多少，每页最多显示多少
    :param kw: 用于browser的关键词，和数据库的关键词一致
            kw in [type,owning_group_id,status,dominant,discontinued,sample_status,creation_date,uses,favorite,sort,reverse,keywords]
                    sort 提供关键字的list,即需要排序的列名，提供字符串格式,顺便还要提交一个reverse
                    reverse 提供True/False的list，顺序和sort中对应, True为降序
                    uses 提供使用度阈值 字符串格式 '操作符 数字[ 操作符 数字]' e.g.'>= 10' '> 100 < 200'
                    creation_date 输入字符串格式 '0000-00-00 - 0000-00-00' 或者 '0000-00-00 - now'
                    keywords: 进行查找的位置有 short desc, description, author, part_type, notes,source, nickname, categories
    :return: （result_list，total_legth)
    '''

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    handle = "select %s from searching,text where searching.name = text.name"%(requests)
    #print(handle)
    #handle + "limit "+str(start)+","+str(length)

    kw_list = list(kw.keys())

    if len(kw_list) == 0:
        cs = cursor.execute(handle)
        total = len(cs.fetchall())
        cs = cursor.execute(handle+" limit %s,%s"%(start,length))
        back = cs.fetchall()
    else:
        for keyword in kw_list:
            if keyword not in ['creation_date','sort','reverse','uses','keyword','name']:
                if keyword in ['type','status','sample_status']:
                    handle += " and %s = '%s'"%(keyword,kw[keyword])
                else:
                    handle += " and %s = %s"%(keyword,kw[keyword])

        if 'name' in kw_list:
            cs_try = cursor.execute("select name from searching where name = '%s'"%(kw['name']))
            try_back = cs_try.fetchall()
            if len(try_back) == 0:
                search_list, name= [], kw['name']
                for i in range(len(name)):
                    l = list(name)
                    l[i] = '_%'
                    search_list.append("'" + ''.join(l) + "'")
                    search_list.append("'" + name[:i] + '_%' + name[i:] + "'")
                search_list.append("'" + name + "_%'")
                search_list = ["searching.name like %s"%(x) for x in search_list]
                handle += " and (%s)"%(' or '.join(search_list))
            else:
                handle += " and searching.name = '%s'"%(kw['name'])

        if 'keyword' in kw_list:
            kword_input = kw['keyword']
            if type(kword_input) == type(' '):
                kword_input = [kword_input]
            for kword in kword_input:
                kword_list = list(set([kword, kword.title(), kword.upper(), kword.lower()]))
                if kword.count(' ') > 0:
                    kword_list.append(kword.replace(' ', '-'))
                    kword_list.append(kword.replace(' ', '_'))
                    kword_list.append(kword.replace(' ', ''))
                    kword_list.append(kword.replace(' ','_%'))
                # print(kword_list)
                sub_str_list = []
                for kword in kword_list:
                    for request in ["short_desc", "description", "author", "type", "notes", "source", "nickname",
                                    "categories"]:
                        sub_str_list.append("%s like '%s'" % (request, '_% ' + kword + ' _%'))
                        sub_str_list.append("%s like '%s'" % (request, '_% ' + kword + '_%'))
                handle += " and (%s)" % (' or '.join(sub_str_list))

        if 'creation_date' in kw_list:
            date_range = kw['creation_date'].split(' - ')
            handle += " and creation_date > '%s' and creation_date < '%s'"%(date_range[0],date_range[1])

        if 'uses' in kw_list:
            op_list = kw['uses'].split(' ')
            if len(op_list) > 2:
                handle += " and uses %s %s and uses %s %s"%(op_list[0],op_list[1],op_list[2],op_list[3])
            else:
                handle += " and uses %s %s"%(op_list[0],op_list[1])

        if 'sort' in kw_list:
            cols ,ops = kw['sort'],[]
            for op in kw['reverse']:
                if op == True:
                    ops.append('desc')
                else:
                    ops.append('asc')
            handle += " order by "
            inserts = [cols[i]+' '+ops[i] for i in range(len(cols))]
            handle += ', '.join(inserts)
            '''if 'reverse' in kw_list and kw['reverse'] == True:
                handle += " order by %s desc"%(kw['sort'])
            else:
                handle += " order by %s"%(kw['sort'])'''

        print(handle)
        cs = cursor.execute(handle)
        back = cs.fetchall()
        total = len(back)
    connection.close()
    return (back[start:start+length],total)


if __name__ == '__main__':

    db_name = 'parts.db'

    # 用名字搜索

    #res = search_name(db_name,'BBa_B1003')
    #res = name_search(db_name,'BB_100') #BBa_B1003
    #res = name_search(db_name, 'BB_100', 'Promoter')  # BBa_B1003
    """res = name_search(db_name,'BB_100','Terminator') #BBa_B1003
    if len(res) > 0:
        for r in res:
            print(r)
    else:
        print('Parts not found')"""

    #rs = browser(db_name,"searching.name,creation_date,uses",creation_date='2018-01-01 - now',sort=['uses','creation_date'],uses='>= 20 <= 30',reverse=[True,False])
    rs = browser(db_name,name='BBa_B10',type='RBS',keyword='weak')
    #rs = browser(db_name)
    for r in rs[0]:
        print(r)
    print(rs[1])












