# -*- coding:utf-8 -*-
import pandas
import pickle
import re,os
import math
import random
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from operator import itemgetter

path = os.path.dirname(__file__)
def get_sequence(file='merged.csv'):
    raw = pandas.read_csv(file)
    raw = raw.head(10)
    dic = {}
    for i in range(10):
        ec_num,pubid,gene = raw.loc[i,['ec_num','pubid','gene']]
        gene_dic = {}
        pubid_list = []
        id_pattern = re.compile("[0-9]{1,}")
        pubid_list = id_pattern.findall(pubid)
        gene = gene[1:-1].split(',')
        gene_pattern1 = re.compile("''")
        dic.update({ec_num:{'pubid':pubid,'gene':gene}})
    return dic

def get_cds(seq):
    seq = seq.upper()
    cds = ''
    #cds_list = []
    for i in range(20):
        if seq[i:i+3] == 'ATG':
            cds = seq[i:]
            break
    if len(cds) == 0:
        return None
    else:
        if len(cds)%3 ==0:   #does it really need to control the length to be the multiple of 3 ????
            return cds
        else:
            return None
        #for i in range(0,len(cds),3):
         #   cds_list.append(cds[i:i+3])
    #return cds_list

def replace_codon(cds,org):
    '''replace'''
    with open(path+'/../data/parts_design/replace_dic_'+org,'rb') as f:
        replace_dic = pickle.load(f)
    cds_list = []
    for i in range(0,len(cds),3):
        cds_list.append(cds[i:i+3])

    for i in range(1,len(cds_list)-1,1): #除去 atg & *stop
        triplet = cds_list[i]
        if triplet in replace_dic :
            if cds_list[i-1] == replace_dic[triplet][0]:
                if len(replace_dic[triplet]) > 1:
                    cds_list[i] = replace_dic[triplet][1]
                else:
                    cds_list[i] = replace_dic[triplet][0]
            else:
                cds_list[i] = replace_dic[triplet][0]
    cds = ''.join(cds_list)
    return cds


def get_gc(seq):
    gc = seq.count('G')+seq.count('C')
    length = len(seq)
    return float(gc/length)


def get_cai(seq,org):  #seq should be upper
    with open(path+'/../data/parts_design/cai_calculation_dic_'+org,'rb') as f:   #org: ecoli/yeast
        calculation_dic = pickle.load(f)
    L = (len(seq) - 3) / 3
    w = 1
    for i in range(0, len(seq) - 3, 3):
        triplet = seq[i:i + 3]
        w *= calculation_dic[triplet]
    cai = math.pow(w, 1 / L)
    return round(cai,2)


def gc_optimization(seq,org,n=1,a=0.05):
    seq = seq.upper()
    gc_mean = {'ecoli':0.58,'yeast':0.383}
    gc_range = [gc_mean[org]*(1-a),gc_mean[org]*(1+a)]
    #print('GC range {}'.format(gc_range))

    with open(path+'/../data/parts_design/gc_replace_dic_'+org,'rb') as f:
        dic = pickle.load(f)
    replace_list = []
    balance_list = []
    codon_list = []
    gc_raw = get_gc(seq)
    #print('GC raw {}'.format(gc_raw))
    if gc_raw > gc_range[0] and gc_raw < gc_range[1]:
        return [seq,gc_raw,get_cai(seq,org)]
    else:
        for i in range(0, len(seq), 3):
            codon_list.append(seq[i:i + 3])  # codon_list = ['triplet1','triplet2',...]
        max_step = math.fabs(int(gc_raw * len(seq)) - int((gc_range[0] + gc_range[1]) / 2 * len(seq)))
        #print('max step {}'.format(max_step))
        if gc_raw < gc_range[0]:
            case = 'up'
        elif gc_raw > gc_range[1]:
            case = 'down'
        elif gc_raw >= gc_range[0] and gc_raw <= gc_range[1]:
            case = 'stable'
        for i in range(1, len(codon_list) - 2, 1):
            if codon_list[i] in [x for x in dic[case].keys()]:
                replace_list.append(i)
            elif codon_list[i] in [x for x in dic['stable'].keys()]:
                balance_list.append(i)
        #print('replace list {}'.format(replace_list))
        #print('balance list {}'.format(balance_list))
        step = 0
        while step < max_step and (gc_raw < gc_range[0] or gc_raw > gc_range[1]) and len(replace_list) > 0:
            max_cai = 0
            r_index = 0
            for i in range(10):
                index = random.choice(replace_list)
                t_seq = ''.join(codon_list[:index] + dic[case][codon_list[index]][:1] + codon_list[index + 1:])
                cai = get_cai(t_seq, org)
                if cai > max_cai:
                    max_cai = cai
                    r_index = index
            codon_list[r_index] = dic[case][codon_list[r_index]][0]
            replace_list.remove(r_index)
            step += 1
            gc = get_gc(''.join(codon_list))
        subseq = ''.join(codon_list)
        # seq = seq[3:]+''.join(codon_list)+seq[-3:]
        while get_cai(subseq, org) < 0.8:
            if len(balance_list) > 0:
                i = random.choice(balance_list)
                subseq = ''.join(codon_list[:i] + dic['stable'][codon_list[i]][:1] + codon_list[i + 1:])
                balance_list.remove(i)
            else:
                #print('no balance list')
                break

        return [subseq, gc, max_cai]


# input  seq & org[ecj|sac]
def Codon_Optimization(seq, org):
    op_results = []
    cds = get_cds(seq)
    new_cds = replace_codon(cds,org)

    pool = ThreadPoolExecutor(10)
    seqs = [new_cds]*10
    gc_optimization_ = partial(gc_optimization,org=org)

    results = pool.map(gc_optimization_, seqs)
    outputs = []
    list = []
    for result in results:
        if result[0] not in list:
            outputs.append(result)
    outputs  =sorted(outputs,key=itemgetter(2),reverse=True)
    for output in outputs:
        result = []
        new_seq = output[0]
        difference = []
        before = ''
        for i in range(0, len(cds), 3):
            common = 0
            if cds[i:i + 3] == new_seq[i:i + 3]:
                difference.append('   ')
            else:
                difference.append('^^^')
            if new_seq[i:i + 3] == before:
                common += 1
            before = new_seq[i:i + 3]
        diff = ''.join(difference)
        result.append('{}'.format(new_seq))
        result.append('{}'.format(get_gc(cds)))
        result.append('{}'.format(output[1]))
        result.append('{}'.format(get_cai(cds, org)))
        result.append('{}'.format(output[2]))
        op_results.append(result)
        with open(path+'/../data/parts_design/test_data_out.txt','a') as f:
           f.write(new_seq+'\n')
    return op_results
