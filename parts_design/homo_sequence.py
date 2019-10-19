# -*- coding: utf-8 -*-
# homo sequence
import pickle,os
path = os.path.dirname(__file__)

data = pickle.load(open(path+'/../data/parts_design/sequence.pkl', 'rb'))

def Get_Homo_Seq(EC):
    if EC not in data.keys():
        info = {'sce':'-', 'ecj':'-'}
        return info
    info = data[EC]
    seq_sce = info['sce']
    seq_ecj = info['ecj']
    
    gene_sce = seq_sce.split('|')
    gene_ecj = seq_ecj.split('|')

    gene_sce_info = [infor.split(':') for infor in gene_sce]
    gene_ecj_info = [infor.split(':') for infor in gene_ecj]
        
    info = {'sce':gene_sce_info, 'ecj':gene_ecj_info}
    return info
    