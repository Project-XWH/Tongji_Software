# -*- coding:utf-8 -*-

#-------------information---------------
'''
输入小写的名字，输出几个候选列表
'''

#---------------packages----------------
import pickle
import difflib
import time
import datetime

#---------------------------------------


def search_cnum(name,name_dic):
    '''

    :param name: 名字
    :return: list

    '''

def insert(name_tuple,candidate_list,max_length=5):
    '''
        insert the name_tuple into the correct site in given list

    :param name_tuple:
    :param list:
    :param max_length:
    :return:
    '''

    flag = 0
    score = name_tuple[-1]
    if len(candidate_list) < max_length:
        if len(candidate_list) == 0:
            candidate_list.append(name_tuple)
            return candidate_list
        else:
            for candidate in candidate_list:
                if score >= candidate[-1]:
                    index = candidate_list.index(candidate)
                    candidate_list = candidate_list[:index] + [name_tuple] + candidate_list[index:]
                    flag = 1
                    break
            if flag == 0:
                candidate_list.append(name_tuple)
            return candidate_list
    else:
        if score <= candidate_list[-1][-1]:
            return candidate_list
        else:
            for candidate in candidate_list:
                if score >= candidate[-1]:
                    index = candidate_list.index(candidate)
                    candidate_list = candidate_list[:index] + [name_tuple] + candidate_list[index:]
                    break
            candidate_list.pop()
            return candidate_list


if __name__ == '__main__':

    with open('kegg_name.pkl','rb') as f:
        name_dic = pickle.load(f)

    with open('cnum2name_dic.pkl','rb') as f:
        cnum2name_dic = pickle.load(f)

    #输入的都是小写的
    name_input = 'butenal'
    max_length = 5
    flag = 0

    #start1 = time.process_time()
    candidate_list = []
    for name in name_dic[name_input.lower()[0]]:
        score = difflib.SequenceMatcher(None, name[0], name_input).quick_ratio()
        candidate_list = insert((name[0],name[-1], score), candidate_list, max_length)


    if candidate_list[0][-1] <= 0.9:
        for key in name_dic:
            for name in name_dic[key]:
                score = difflib.SequenceMatcher(None, name[0], name_input).quick_ratio()
                candidate_list = insert((name[0], name[-1], score), candidate_list, max_length)
    #end1 = time.process_time()
    print(candidate_list)
    cnum_list =[]
    for candidate in candidate_list:
        if candidate[1] not in cnum_list:
            cnum_list.append(candidate[1])
    for cnum in cnum_list:
        print('{} --- {}'.format(cnum,cnum2name_dic[cnum]))
    #print(end1-start1)





