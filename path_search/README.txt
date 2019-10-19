from search import search
search('C00099', 'C00043',9,5,'(1,1,1)')

按照上述格式调用search.py文件。
返回值为列表，列表内每元组为一个搜索结果，元组内依次为化合物列表、反应列表、酶列表。
具体内容可参考下述例子。
search函数内已内置数据预处理，将用户输入直接传入即可。
“1”，“C001”，“water”，“Water”等都能被成功转化为“C00001”。
在化合物无法被转化为编号、打分矩阵参数不足、起始化合物不存在时，会抛出内容分别为"Error Compound"、"Insufficient coefficient"、"Start compound not exist"的异常，请在前端进行捕捉并处理。

Call the search.py file in the above format.


The return value is a list, each tuple in the list is a search result, and in the tuple is a list of compounds, a list of reactions and a list of enzymes in turn.


The specific content can be referred to the following examples.


Search function has built-in data preprocessing, user input can be directly imported.


"1", "C001", "water", "Water" and so on can be successfully transformed into "C00001".


When the compound can not be converted into a number, the scoring matrix parameters are insufficient, and the starting compound does not exist, the abnormal contents are "Error Compound", "Insufficient coefficient", "Start compound does not exist". Please capture and process the abnormal contents at the front end.

e.g.
↓Index of tuples
0 CompoundName0-------CompoundName1-------CompoundName2
1	    ReactionName0       ReactionName1
2	       1.1.1.1             2.2.2.2