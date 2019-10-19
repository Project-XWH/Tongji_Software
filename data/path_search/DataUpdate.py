# -*- coding: utf-8 -*-
import pickle

#gibbs_dict = {}        #吉布斯
#freq_dict = {}         #频率
#neighbor_dict = {}     #反应对
#toxicity_dict = {}     #毒性
#compound_data = {}     #编号-英文名对
#compound_name_num = {} #化合物名称-编号对
#cPair_rNum = {}        #反应-反应编号对
#Rnum_ec = {}           #反应编号-酶编号对
#
#with open('adj_map2.pk', 'rb') as f:
#    neighbor_dict = pickle.load(f)
#
#with open('max_eco.pkl', 'rb') as f:
#    gibbs_dict = pickle.load(f)
#
#with open('frequency.pkl', 'rb') as f:
#    freq_dict = pickle.load(f)
#        
#with open('reaction_dictionary.pk','rb') as f:
#    cPair_rNum = pickle.load(f)    
#    
#with open('D_name_Cnum.pkl', 'rb') as f:
#    compound_name_num = pickle.load(f)
#
#with open('eco_Toxicity.pkl', 'rb') as f:
#    toxicity_dict = pickle.load(f)
#    
#with open('reaction_enzyme_pair.pkl', 'rb') as f:
#    Rnum_ec = pickle.load(f)
#    
#with open('compound_data.pkl', 'rb') as f:
#    compound_data = pickle.load(f)

with open('search_data.pkl', 'br') as file:
    neighbor_dict, gibbs_dict, freq_dict, cPair_rNum, compound_name_num, \
    toxicity_dict, Rnum_ec, compound_data = pickle.load(file)
    
# 在以下区域添加代码，将所需更改的字典替换为新数据
# e.g.:
# compound_name_num = {k.upper():v for k, v in compound_name_num.items()}





# 在以上区域添加代码

with open('search_data.pkl', 'bw') as f:
    pickle.dump((neighbor_dict, gibbs_dict, freq_dict, cPair_rNum, compound_name_num, toxicity_dict, Rnum_ec, compound_data), f)