kegg_name.pkl 和 cnum2name_dic.pkl 是kegg_name2cnum.py 里面用的，都是字典

kegg_name.pkl键是首字母，值是嵌套list，[['name','cnum']]
cnum2name_dic.pkl 键是cnum，值是列表 就是这个cnum有的一堆名字

kegg_name2cnum.py 就是输入名字输出可能的cnum（相似度0.9以上）的列表

full_name_list 就是一个 cnum --- name 的文本文件