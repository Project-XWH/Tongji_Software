# coding: utf-8
import os
import sys
import csv
import time
import pickle
import threading

max_eco = {}        #吉布斯
freq_dict = {}      #频率
neighbor_dict = {}  #反应对
toxicity_dict = {}  #毒性
compound_data = {}  #编号英文名对
compound_name_num = {}
cPair_rNum = {}
Rnum_ec = {}

path = os.path.dirname(__file__) 
print('ojbk')

with open(r'./data/path_search/adj_map2.pk', 'rb') as f:
    neighbor_dict = pickle.load(f)

with open(r'./data/path_search/max_eco.pkl', 'rb') as f:
    max_eco = pickle.load(f)

with open(r'./data/path_search/frequency.pkl', 'rb') as f:
    freq_dict = pickle.load(f)
        
with open("./data/path_search/reaction_dictionary.pk","rb") as file:
    cPair_rNum = pickle.load(file)    
    
with open('./data/path_search/D_name_Cnum.pkl', 'rb') as f:
    compound_name_num = pickle.load(f)

with open(r'./data/path_search/eco_Toxicity.csv','r') as f:
    for line in f:
        line = line.strip().split(',')
        toxicity_dict[line[0]] = float(line[1])

with open("./data/path_search/reaction_enzyme_pair.csv") as f:
    for line in f:
        line = line.strip().split(',')
        if len(line) > 1:
            Rnum_ec[line[0]] = line[1]
        else:
            Rnum_ec[line[0]] = "NA"
        
with open("./data/path_search/compound_data.csv") as nodes_file:
    node_reader = csv.reader(nodes_file)
    for node in node_reader:
        node[1]=node[1].split(';')[0]
        compound_data[node[0]] = node[1]

def GetToxicity(compound):
    temp = toxicity_dict.get(compound)
    if  temp != None:
        return float(temp)
    else:
        return 0
    
def GetGibbs(lastCompound, nextCompound):
    return float(max_eco[lastCompound + "_" + nextCompound])

def GetFreq(lastCompound, nextCompound):
    temp = freq_dict.get(lastCompound + "_" + nextCompound)
    if temp != None:
        return float(temp)
    else:
        return -400
    
#默认二阶列表
def OrderlyInsert(_list, insertion, asc = True, column = 0):
    #二分查找
    lo = 0
    hi = len(_list)
    insertedNum = insertion[column]
    while lo < hi:
        mid = (lo + hi) // 2
        if (insertedNum > _list[mid][column]) ^ asc:
            hi = mid
        else:
            lo = mid + 1
    _list.insert(lo, insertion)
    
def CheckCompoundCanReach(compound):
    for i in neighbor_dict.values():
        if compound in i:
            return True
    return False

#weightArray=(吉布斯，毒性，频率)
def OptimizedA(startCompound, targetCompound, depth = 10, neededPaths = 1, weightArray=(1,1,1)):
    result = []
    if neighbor_dict.get(startCompound) == None:
        raise Exception("Start compound not exist!")
    if not CheckCompoundCanReach(targetCompound):
        return result
    #初始化,将起始化合物置入列表
    pathList = [[[startCompound], GetToxicity(startCompound)*weightArray[1]]]
    #列表非空时进行循环
    while pathList:
        #保存并pop出目前最优路径
        currentPath = pathList[0][0]
        currentScore = pathList[0][1]
        pathList.pop(0)
        endCompound = currentPath[-1] #获取目前路径末尾的化合物
        #找到目标化合物则计数加一
        if endCompound == targetCompound:
            result.append([currentPath, currentScore])
            neededPaths -= 1
            if neededPaths <= 0:
                break
            else:
                continue
        #过长则放弃当前路径
        if len(currentPath) > depth:
            continue
        nextCompoundList = neighbor_dict[endCompound]
        #循环访问后续化合物
        for nextCompound in nextCompoundList:
            #防止循环
            if nextCompound in currentPath:
                continue
            #路径后加入后续化合物，重新打分，将新路径有序插入列表
            OrderlyInsert(pathList, [currentPath + [nextCompound], 
                                     weightArray[0] * GetGibbs(endCompound, nextCompound)
                                     +weightArray[1] * GetToxicity(nextCompound)
                                     +weightArray[2] * GetFreq(endCompound, nextCompound) 
                                     + currentScore], False, 1)
    return result
        
def CNumToName(resultList):
    output = []
    for item in resultList:
        path = []
        for compound in item[0]:
            path.append(compound_data[compound])
        output.append(path)
    return output
    print(output)

def NumToRnum(resultList):
    output = []
    for item in resultList:
        RnumList = []
        for i in range(len(item[0])-1):
            RnumList.append(cPair_rNum[item[0][i]+'_'+item[0][i+1]][0])
        output.append(RnumList)
    return output

def RnumToEc(reactionNum):
    output = []
    for path in reactionNum:
        ecList = []
        for rNum in path:
            ecList.append(Rnum_ec[rNum])
        output.append(ecList)
    return output
    
def WriteFile(ans):
    compoundName = CNumToName(ans)
    reactionNum = NumToRnum(ans)
    ecNum = RnumToEc(reactionNum)
    with open("./path_search/.searchResult.tmp", 'w') as outfile:
        for i in range(len(compoundName)):
            outfile.write('\t'.join(compoundName[i]) + '\n')
            outfile.write('\t'.join(reactionNum[i]) + '\n')
            outfile.write('\t'.join(ecNum[i]) + '\n')
    with open("./path_search/result.txt", 'w') as outfile1:
        for i in range(len(compoundName)):
            outfile1.write('\t'.join(compoundName[i]) + '\n')
            outfile1.write('\t'.join(reactionNum[i]) + '\n')
            outfile1.write('\t'.join(ecNum[i]) + '\n')

def dfs(start_compound, target_compound, depth=10):
    path_list = []
    cur_depth = 0
    path_stack = []
    visited_nodes = {}

    visited_nodes[start_compound] = True
    path_stack.append([start_compound, 0])
    while cur_depth > -1:
        if cur_depth >= depth:#路径过长回退
            temp_top = path_stack.pop()
            cur_depth -= 1
            visited_nodes[temp_top[0]] = False
            continue
        cur_compound = path_stack[-1]
        temp_adj = neighbor_dict[cur_compound[0]] #{'Cxxx':['Cxxx','Cxxx']}

        length = len(temp_adj)
        if cur_compound[1] >= length:#已搜化合物数量大于等于可搜数量
            temp_top = path_stack.pop()
            visited_nodes[temp_top[0]] = False
            cur_depth -= 1
        else:
            next_compound = temp_adj[cur_compound[1]]
            path_stack[-1][1] += 1

            if next_compound == target_compound:
                path_list.append(path_stack+[[next_compound, 0]])
            else:
                if next_compound not in visited_nodes or not visited_nodes[next_compound]:
                    visited_nodes[next_compound] = True
                    path_stack.append([next_compound, 0])
                    cur_depth += 1
    #end while
    path_result = []
    for path in path_list:
        temp = []
        for item in path:
            temp.append(item[0])
        path_result.append(temp)

    return path_result

def rank_list(path_result, w_gibbs = 1, w_toxicity = 1, w_frequency = 1):
    #[['C00002', 'C00008'], ['C00002', 'C00020', 'C00008'], ['C00002', 'C00020', 'C00498', 'C00008']]
    rank_result = []
    for com_list in path_result:
        num = len(com_list)
        weight = 0.0
        for i in range(0, num - 1):
            tempstr = com_list[i] + "_" + com_list[i + 1]
            weight += w_gibbs*GetGibbs(tempstr)
            weight += w_frequency*GetFreq(tempstr)
        for item in com_list:
            weight += w_toxicity*GetToxicity(item)
        rank_result.append([com_list,weight])

    return sorted(rank_result,key=lambda w: w[1], reverse=True)

def DFS(startCompound, targetCompound, depth, neededPaths, weightArray):
    return rank_list(dfs(startCompound, targetCompound, depth),
                     weightArray[0], weightArray[1], weightArray[2])[:neededPaths]

def search(algorithm, startCompound, targetCompound, depth, neededPaths, weightArray):
    ans = algorithm(startCompound, targetCompound, depth, neededPaths, weightArray)
    WriteFile(ans)

def isCNum(string):
    return string[0]=='C' and len(string)==6 and string[1:].isdigit()

if __name__ == "__main__":
    #从控制台获取参数。要求参数全部都有。
    sys.argv=["","C00002","C00008","10","10","(1,1,1)"]
    length = len(sys.argv)
    if length < 6:
        raise Exception("Insufficient argument")
    startCompound = sys.argv[1]
    targetCompound = sys.argv[2]
    depth = int(sys.argv[3])
    neededPaths = int(sys.argv[4])
    weightArray = tuple([float(x) for x in sys.argv[5][1:-1].split(',')])
    
    if not isCNum(startCompound):
        if startCompound in compound_name_num:
            startCompound = compound_name_num[startCompound]
        else:
            raise Exception("Start compound name not in database")
    if not isCNum(targetCompound):
        if targetCompound in compound_name_num:
            targetCompound = compound_name_num[targetCompound]
        else:
            raise Exception("Target compound name not in database")
    #通过该输出文件判断是否出结果，所以要先删除
    if os.path.isfile("./path_search/.searchResult.tmp"):
        os.remove("./path_search/.searchResult.tmp")
    #创建线程；设为守护线程；启动线程
    AThread = threading.Thread(target=search, args=(OptimizedA, startCompound, targetCompound, depth, neededPaths, weightArray,))
    DThread = threading.Thread(target=search, args=(DFS, startCompound, targetCompound, depth, neededPaths, weightArray,))
    AThread.daemon = True
    DThread.daemon = True
    AThread.start()
    DThread.start()
    while AThread.is_alive() and DThread.is_alive():
        time.sleep(0.01)
    #出结果则退出，否则sleep
    if not os.path.isfile("./path_search/.searchResult.tmp"):
        raise Exception("Thread ERROR")
    print('ojbk')
print('ojbk')
