from search import search
search('C00099', 'C00043',9,5,'(1,1,1)')

����������ʽ����search.py�ļ���
����ֵΪ�б��б���ÿԪ��Ϊһ�����������Ԫ��������Ϊ�������б���Ӧ�б�ø�б�
�������ݿɲο��������ӡ�
search����������������Ԥ�������û�����ֱ�Ӵ��뼴�ɡ�
��1������C001������water������Water���ȶ��ܱ��ɹ�ת��Ϊ��C00001����
�ڻ������޷���ת��Ϊ��š���־���������㡢��ʼ�����ﲻ����ʱ�����׳����ݷֱ�Ϊ"Error Compound"��"Insufficient coefficient"��"Start compound not exist"���쳣������ǰ�˽��в�׽������

Call the search.py file in the above format.


The return value is a list, each tuple in the list is a search result, and in the tuple is a list of compounds, a list of reactions and a list of enzymes in turn.


The specific content can be referred to the following examples.


Search function has built-in data preprocessing, user input can be directly imported.


"1", "C001", "water", "Water" and so on can be successfully transformed into "C00001".


When the compound can not be converted into a number, the scoring matrix parameters are insufficient, and the starting compound does not exist, the abnormal contents are "Error Compound", "Insufficient coefficient", "Start compound does not exist". Please capture and process the abnormal contents at the front end.

e.g.
��Index of tuples
0 CompoundName0-------CompoundName1-------CompoundName2
1	    ReactionName0       ReactionName1
2	       1.1.1.1             2.2.2.2