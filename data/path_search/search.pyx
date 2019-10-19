from re import findall
import pickle
#加载数据
cdef dict neighbor_dict, gibbs_dict, freq_dict, cPair_rNum, compound_name_num, \
    toxicity_dict, Rnum_ec, compound_data
with open('/home/xubo/sites/Pathlab/data/path_search/search_data.pkl', 'br') as file:
    
    #反应对、       吉布斯、     频率、     反应-反应编号对、化合物名称-编号对
    #毒性、         反应编号-酶编号对、编号-英文名对
    neighbor_dict, gibbs_dict, freq_dict, cPair_rNum, compound_name_num, \
    toxicity_dict, Rnum_ec, compound_data = pickle.load(file)
    
    _toxicity_dict_get = toxicity_dict.get
    _freq_dict_get = freq_dict.get
    
cpdef list search(str startCompound, str endCompound, str depth = '10', str neededPaths = '1', str weightArray='(1,1,1)'):
    cdef int _depth
    cdef int _neededPaths
    cdef tuple _weightArray
    startCompound, endCompound, _depth, _neededPaths, _weightArray =  \
        _inputDataProcess(startCompound, endCompound, depth, neededPaths, weightArray)
    return _outputDataProcess(_OptimizedA(startCompound, endCompound, _depth, _neededPaths, _weightArray))
    
#weightArray=(吉布斯，毒性，频率)
cdef list _OptimizedA(str startCompound, str targetCompound, int depth = 10, int neededPaths = 1, tuple weightArray=(1,1,1)):
    if not neighbor_dict.get(startCompound):
        raise Exception("Start compound not exist")
    if not _CheckCompoundCanReach(targetCompound):
        return []
    
    #初始化,将起始化合物置入列表
    cdef list result = []
    cdef MaxHeap pathList = MaxHeap()
    cdef str endCompound
    cdef list tmp
    cdef list currentPath
    cdef float currentScore
    pathList.insert([[startCompound], _GetToxicity(startCompound)*weightArray[1]])
    #列表非空时进行循环
    while True:
        #pop目前最优路径,为None时说明路径列表空，结束循环
        tmp = pathList.pop()
        if tmp:
            currentPath, currentScore = tmp
        else:
            break
        endCompound = currentPath[-1] #获取目前路径末尾的化合物
        #找到目标化合物则计数减一
        if endCompound == targetCompound:
            result.append(tmp)
            neededPaths -= 1
            if neededPaths <= 0:
                break
            else:
                continue
        #过长则放弃当前路径
        if len(currentPath) > depth:
            continue
        #循环访问后续化合物
        for nextCompound in neighbor_dict[endCompound]:
            #防止循环
            if nextCompound in currentPath:
                continue
            #路径后加入后续化合物，重新打分，将新路径有插入大根堆
            pathList.insert([currentPath + [nextCompound], 
                             weightArray[0] * _GetGibbs(endCompound, nextCompound) + 
                             weightArray[1] * _GetToxicity(nextCompound) +
                             weightArray[2] * _GetFreq(endCompound, nextCompound) +
                             currentScore])
    return result

cdef class MaxHeap:
    cdef list __list
    cdef int __len
    
    def __init__(self):
        self.__list = []
        self.__len = 0
        
    cdef void insert(self, list value):
        self.__list.append(value)
        cdef int p1 = self.__len
        cdef list li = self.__list
        self.__len += 1
        cdef float newVal = value[1]
        while p1 > 0:
            p2 = (p1-1) >> 1
            if newVal > li[p2][1]:
                li[p1] = li[p2]
            else:
                break
            p1 = p2
        li[p1] = value
    
    cdef list pop(self):
        cdef int length = self.__len
        cdef list li = self.__list
        #特殊情况处理
        if length == 0:
            return None
        elif length == 1:
            self.__len = 0
            return self.__list.pop()
        #保存末尾值，弹出首值
        cdef list endVal = li[-1]
        li[-1] = li[0]
        self.__len -= 1
        length -= 1
        cdef int current = 0
        cdef int child = 1
        cdef list save = self.__list.pop()
        cdef int r
        #将比末尾值大的值上浮并重新插入末尾值
        while child < length:
            r = child + 1
            if r < length and li[r][1] > li[child][1]:
                child = r
            if li[child][1] > endVal[1]:
                li[current] = li[child]
            else:
                break
            current, child = child, child * 2 + 1
        li[current] = endVal
        return save

cdef float _GetToxicity(str compound):
    temp = _toxicity_dict_get(compound)
    if  temp:
        return temp
    else:
        return 0.0
    
cdef float _GetGibbs(str lastCompound, str nextCompound):
    return float(gibbs_dict[lastCompound + "_" + nextCompound])

cdef float _GetFreq(str lastCompound, str nextCompound):
    temp = _freq_dict_get(lastCompound + "_" + nextCompound)
    if temp:
        return float(temp)
    else:
        return -400.0
    
cdef _CheckCompoundCanReach(str compound):
    cdef list i
    for i in neighbor_dict.values():
        if compound in i:
            return True
    return False
    
cdef tuple _inputDataProcess(str startCompound, str endCompound, str depth, str neededPaths, str weightArray):
    startCompound = _compoundTransfer(startCompound)
    endCompound = _compoundTransfer(endCompound)
    cdef int _depth = int(depth)
    cdef int _neededPaths = int(neededPaths)
    cdef tuple _weightArray = tuple([int(x) for x in findall("[0-9]+", weightArray)])
    if len(weightArray) < 3:
        raise Exception("Insufficient coefficient")
    return startCompound, endCompound, _depth, _neededPaths, _weightArray

cdef str _compoundTransfer(str s):
    s = s.upper()
    if s in compound_name_num:
        return compound_name_num[s]
    if s[0]=='C' and len(s)==6 and s[1:].isdigit():
        return s
    if s[0] == 'C':
        s = s[1:]
    if s.isdigit() and len(s) <= 5:
        return 'C' + '0'*(5-len(s)) + s
    else:
        raise Exception("Error Compound")

cdef list _outputDataProcess(list ans):
    cdef list compoundName = _CNumToName(ans)
    cdef list reactionNum = _NumToRnum(ans)
    cdef list ecNum = _RnumToEc(reactionNum)
    return [_ for _ in zip(compoundName, reactionNum, ecNum)]
    
cdef list _CNumToName(list resultList):
    return [[compound_data[compound] for compound in item[0]] for item in resultList]

cdef list _NumToRnum(list resultList):
    cdef list output = []
    cdef list RnumList = []
    for item in resultList:
        RnumList = []
        for i in range(len(item[0])-1):
            RnumList.append(cPair_rNum[item[0][i]+'_'+item[0][i+1]][0])
        output.append(RnumList)
    return output

cdef list _RnumToEc(list reactionNum):
    return [[Rnum_ec[rNum] for rNum in path] for path in reactionNum]

def test():
    import time
    testList = [['C00099', 'C00043'], ['C00047', 'C00104'], ['C00135', 'C00090'], 
                ['C00005', 'C00116'], ['C00021', 'C00140'], ['C00132', 'C00020'], 
                ['C00073', 'C00106'], ['C00106', 'C00049'], ['C00176', 'C00054'], 
                ['C00011', 'C00196'], ['C00163', 'C00061'], ['C00089', 'C00130'], 
                ['C00129', 'C00021'], ['C00114', 'C00127'], ['C00103', 'C00121'], 
                ['C00168', 'C00181'], ['C00052', 'C00109'], ['C00042', 'C00128'], 
                ['C00086', 'C00090'], ['C00158', 'C00074'],]
    with open('/home/xubo/sites/Pathlab/data/path_search/testResult.txt','w') as file:
        for i, (start, ed) in enumerate(testList):
            a = time.perf_counter()
            ans = _OptimizedA(start, ed, 9, 3, (1,1,1))
            file.write(str(i)+'\n')
            file.write(str(time.perf_counter()-a)+'\n')
            file.write(str(ans)+'\n')

if __name__ == "__main__":
    test()
