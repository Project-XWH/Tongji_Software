# -*- coding: utf-8 -*-
import os
import sys
import pickle

import numpy as np
from operator import itemgetter, attrgetter
from collections import Counter
from parts_design import codon_optimization,homo_sequence

path = os.path.dirname(__file__)
data = pickle.load(open(path + '/../data/enzyme_selection/enzyme.pkl', 'rb'))


ph_score = {'ecj':{2.0: 0.0009487666034155598, 2.5: 0.001265022137887413, 3.0: 0.0028462998102466793, 3.5: 0.003795066413662239, 4.0: 0.00980392156862745, 4.5: 0.009487666034155597, 5.0: 0.024667931688804552, 5.5: 0.023402909550917138, 6.0: 0.06704617330803289, 6.5: 0.07147375079063885, 7.0: 0.1691967109424415, 7.5: 0.19955724225173938, 8.0: 0.16793168880455406, 8.5: 0.09139784946236558, 9.0: 0.07495256166982922, 9.5: 0.034471853257431996, 10.0: 0.028462998102466795, 10.5: 0.008538899430740038, 11.0: 0.007906388361796331, 11.5: 0.0009487666034155598, 12.0: 0.0015812776723592662, 12.5: 0, 13.0: 0.00031625553447185326, 13.5: 0},
            'sce' :{1.0: 0, 1.5: 0.0005743825387708214, 2.0: 0.00402067777139575, 2.5: 0.00402067777139575, 3.0: 0.0080413555427915, 3.5: 0.0068925904652498565, 4.0: 0.02125215393452039, 4.5: 0.014933946008041356, 5.0: 0.03561171740379093, 5.5: 0.04709936817920736, 6.0: 0.08041355542791499, 6.5: 0.11028144744399769, 7.0: 0.18495117748420448, 7.5: 0.17633543940264215, 8.0: 0.14302125215393452, 8.5: 0.06260769672601951, 9.0: 0.053417576105686385, 9.5: 0.024124066628374498, 10.0: 0.016082711085583, 10.5: 0.002871912693854107, 11.0: 0.002871912693854107, 11.5: 0.0005743825387708214, 12.0: 0, 12.5: 0, 13.0: 0, 13.5: 0}
            }
t_score  = {'ecj':{0: 0.005772005772005772, 5: 0.00505050505050505, 10: 0.007936507936507938, 15: 0.010101010101010102, 20: 0.08585858585858586, 25: 0.15512265512265513, 30: 0.14141414141414144, 35: 0.34199134199134207, 40: 0.05844155844155845, 45: 0.049062049062049064, 50: 0.04184704184704184, 55: 0.026695526695526692, 60: 0.02958152958152958, 65: 0.010822510822510824, 70: 0.011544011544011544, 75: 0.005772005772005772, 80: 0.007936507936507936, 85: 0.001443001443001443, 90: 0.0021645021645021645, 95: 0.0007215007215007215, 100: 0.0007215007215007215},
            'sce':{0: 0.004431314623338257, 5: 0.01624815361890694, 10: 0.005908419497784343, 15: 0.007385524372230429, 20: 0.08124076809453472, 25: 0.137370753323486, 30: 0.3190546528803545, 35: 0.23042836041358938, 40: 0.05760709010339734, 45: 0.03840472673559823, 50: 0.04283604135893648, 55: 0.022156573116691284, 60: 0.0206794682422452, 65: 0.004431314623338257, 70: 0.007385524372230428, 75: 0.0014771048744460858, 80: 0.0014771048744460858, 85: 0.0014771048744460858, 90: 0, 95: 0, 100: 0}
            }
organism_catalog = pickle.load(open(path+'/../data/enzyme_selection/organism_catalog.pkl','rb'))
Name = {}
for i in organism_catalog:
    name = ' '.join(organism_catalog[i][-1].split(' ')[0:2])
    Name[i] = name
Name['-'] = '-'

def sort_by_kkm(enzyme):
    '''
    a pathway with just one reation
    '''
    path = os.path.dirname(__file__)
    organism = data[enzyme]
    selections = []
    for org in organism:
        kkm = data[enzyme][org]['KKM']
        if len(kkm) == 0:
            kkm = 0
        else:
            kkm = sum(kkm) /  len(kkm)
        selections.append([org,kkm])
    return sorted(selections, key=itemgetter(1), reverse=True)

'''
用别的值替换
同一物种中其他所有酶的值的中指替换
'''
def get_km_default(substrate, org):
    km = []
    for ec in data.keys():
        km_infor = {}
        if org in data[ec].keys():
            km_infor = data[ec][org]['KM']
        else:
            continue
        if substrate in km_infor.keys():
            km.append(float(km_infor[substrate]))
        elif '' in km_infor.keys():
            km.append(float(km_infor['']))
        else:
            km.append(999)
    count = dict(Counter(km))
    #print(count)
    return max(count, key=count.get)


def get_pH_default(org):
    pH = []
    for ec in data.keys():
        if org in data[ec].keys():
            pH_ = data[ec][org]['PH']
            pH.append(pH_[-1])
    count = dict(Counter(pH))
    return max(count, key=count.get)

def get_temp_default(org):
    temp = []
    for ec in data.keys():
        if org in data[ec].keys():
            temp_ = data[ec][org]['T']
            temp.append(temp_[-1])
    count = dict(Counter(temp))
    return max(count, key=count.get)

def Score_ph(ph,org):
    if ph - int(ph) >0.5:
        score = ph_score[org][int(ph) + 0.5]
    else:
        score = ph_score[org][int(ph)]
    return score

def Score_t(t,org):

    if t - t//10*10 >5:
        score = t_score[org][t//10*10 + 5]
    else:
        if t > 100:
           t = 100
        score = t_score[org][t//10*10]
    return score

def brenda_info(enzyme, org, substrate):
    #---ph---#
    ph = data[enzyme][org]['PH']
    if ph != [999]:
        ph_ = round(ph[-1],2)
    else:
        ph_ = round(get_pH_default(org),2)
    #---t---#
    t = data[enzyme][org]['T']
    if t != [999]:
        t_ = round(t[-1],2)
    else:
        t_ = round(get_temp_default(org),2)
    #---kkm---#
    kkm = data[enzyme][org]['KKM']
    if len(kkm) == 0:
        kkm = 0
    else:
        kkm = round(sum(kkm) / len(kkm), 2)
    #---km---#
    if substrate in data[enzyme][org]['KM'].keys():
        km = data[enzyme][org]['KM'][substrate]
    else:
        km = get_km_default(substrate, org)
    if km == 999:
        km = 0

    score_info = [org, kkm, km, ph_, t_]

    if kkm == 0:
        kkm = '-'
    if km == 999:
        km = '-'
    if ph_ == 999:
        ph_ = '-'
    if t_ == 999:
        t_ = '-'
    str_info = [org, kkm, km, ph_, t_]

    return [score_info,str_info]

def sort_by_default(enzyme, substrate, org):

    sele_org = org

    organism_kegg = [] #[ Name[h[0]] for h in homo_sequence.Get_Homo_Seq(enzyme)[org]]
    for h in homo_sequence.Get_Homo_Seq(enzyme)[org]:
        if h[0] != '':
            organism_kegg.append(Name[h[0]])
    
    enzyme = enzyme.replace('-','1')
    organism_brenda = data[enzyme]
    organisms = list(set(organism_brenda).union(set(organism_kegg)))

    selections_score = []
    selections_result = []
    homology_sequence = []

    KKM_Score = []
    KM_Score = []

    homology = homo_sequence.Get_Homo_Seq(enzyme)[org]
    homology_infor = {}
    for infor in homology:
        if infor[0] != '':
            homology_infor[Name[infor[0]]] = infor[1:]

    for org in organisms:
        if org in organism_brenda and org not in organism_kegg:
            seq_id = '-'
            seq = '-'

            result = brenda_info(enzyme, org, substrate)
            score_info = result[0]
            str_info = result[1]

        elif org in organism_kegg and org not in organism_brenda:
            if org == '-':
                seq_id = '-'
                seq = '-'
            else:
                seq_id = homology_infor[org][0]
                seq = homology_infor[org][1]

            score_info = [org, 0, 0, 999, 999]
            str_info = [org, '-', '-', '-', '-']  

        else:
            seq_id = homology_infor[org][0]
            seq = homology_infor[org][1]

            result = brenda_info(enzyme, org, substrate)
            score_info = result[0]
            str_info = result[1]


        KKM_Score.append(score_info[1])
        KM_Score.append(score_info[2])
        # score_info.append(score(seq))
        score_info.append(0)
        selections_score.append(score_info)        
        
        str_info.append(seq_id)
        # str_info.append(seq)
        selections_result.append(str_info)

        homology_sequence.append([org, seq_id, seq])
        
    KKM_Score = sorted(list(set(KKM_Score)))
    min_kkm = min(KKM_Score)
    max_kkm = max(KKM_Score)
    l_kkm = max_kkm-min_kkm
    if l_kkm == 0:
        l_kkm = 1

    KM_Score = sorted(list(set(KM_Score)))
    min_km = min(KM_Score)
    max_km = max(KM_Score)
    l_km = max_km-min_km
    if l_km == 0:
        l_km = 1

    for k in range(len(selections_score)):
        SCORE = 0.00
        selections_score[k][1] = round((selections_score[k][1]-min_kkm)/l_kkm,2)
        selections_score[k][2] = round((selections_score[k][2]-min_km)/l_km,2)
        if selections_score[k][3] == 999:
            selections_score[k][3] = 0.00
        else:
            selections_score[k][3] = round(Score_ph(selections_score[k][3],sele_org),2)
        if selections_score[k][4] == 999:
            selections_score[k][4] = 0.00
        else:
            selections_score[k][4] = round(Score_t(selections_score[k][4], sele_org),2)
        SCORE = round(sum(selections_score[k][1:]),2)
        selections_result[k].append(SCORE)
        selections_score[k].append(SCORE)

    
    return [sorted(selections_score, key=lambda x: (x[-1]),reverse=True), homology_sequence],[sorted(selections_result, key=lambda x: (x[-1]),reverse=True),homology_sequence]




