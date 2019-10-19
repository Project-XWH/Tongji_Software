# -*- coding:utf-8 -*-
# pathway

import os
import time
import pickle
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib import messages
from parts_design import codon_optimization,homo_sequence
import pyximport; pyximport.install()
from path_search import search
import report.views as pdf
from enzyme_selection import selenzyme

from .models import CompoundsName
from django.db.models import Q

path = os.path.dirname(__file__)
enzymeInfo = pickle.load(open(path+'/../data/enzyme_selection/enzyme_info.pkl', 'rb'))
data = pickle.load(open(path+'/../data/enzyme_selection/enzyme.pkl', 'rb'))
organism_catalog = pickle.load(open(path+'/../data/enzyme_selection/organism_catalog.pkl','rb'))
compounds_data = pickle.load(open(path+'/../data/path_search/compounds_data.pkl', 'rb'))
orgs = {'ecj':'ecoli','sce':'yeast'}


# /home/xubo/sites/Pathlab/path_search
def main(req):
    # return HttpResponse('<h1>Hello!<h1>')
    return render(req,'pathlab.html', {'username':req.user, 'operation':'login'})
 
def pathway(req):
    return render(req,'pathway.html')

def complete(req):
    name = req.GET['term']
    tags = CompoundsName.objects.filter(Q(name__icontains=name) |Q(cnum__icontains=name))[0:15]
    # result = []
    # for tag in 
    # return [tag.name for tag in tags]
    # return HttpResponse('\n'.join( tag.name +'  |  '+tag.cnum for tag in tags))
    result = [tag.name+' | '+tag.cnum for tag in tags]
    if len(result)>0:
        # return HttpResponse(['acid','acids'])
        return HttpResponse('*'.join(result).replace('<', ','))
    else:
        return HttpResponse('No Match')

def path_search_full(req):
    arg1 = req.POST.get('start_compound','')
    arg2 = req.POST.get('target_compound','')
    arg3 = req.POST['Search_Depth']
    arg4 = req.POST['Needed_Paths']
    arg5 = ','.join([req.POST['arg5_w1'], req.POST['arg5_w2'], req.POST['arg5_w3']])
    arg6 = req.POST['novel']

    if arg1 != '':
        arg1 = arg1.split('|')[1].strip()
    if arg2 != '':
        arg2 = arg2.split('|')[1].strip()

    org = req.POST['org']

    if arg1 != '' and arg2 != '':
        try:
            if arg6 == 'no':
                result = search.search(arg1, arg2, arg3, arg4, arg5)
#             else:
#                 result = search.novel_search(arg1, arg2, arg3, arg4, arg5)
            return render(req,'pathway_result.html',
                {'result':result,'compounds1':arg1,'compounds2':arg2, 'org':org})
        except Exception as err:
            return HttpResponse(err) #render(req,'pathway.html', {'err2':err})

    if arg2 == '':
        try:
            result = search.startSearch(arg1, arg3, arg5)
            if len(result) > int(arg3):
                n = int(arg2)
            else:
                n = len(result)
            return render(req,'pathway_result.html',
                               {'result':result[0:n],'compounds1':arg1,'compounds2':arg2, 'org':org})
        except Exception as err:
            return HttpResponse(arg2)
    

    if arg1 == '':
        result = search.endSearch(arg2, arg3, arg5)
        try:
            result = search.endSearch(arg2, arg3, arg5)
            if len(result) > int(arg3):
                n = int(arg3)
            else:
                n = len(result)
            return render(req,'pathway_result.html',
                               {'result':result[0:n],'compounds1':arg1,'compounds2':arg2, 'org':org})
        except Exception as err:
#             return  HttpResponse(arg2)
              return  HttpResponse(err)
    

def path_search_one(req):
    arg1 = req.POST.get('target_compound','').split('|')[1].strip()
    arg2 = req.POST['Needed_Paths']
    arg3 = req.POST['type']
    arg4 = ','.join([req.POST['arg5_w1'], req.POST['arg5_w2'], req.POST['arg5_w3']])

    org = req.POST['org']

    if arg3 == 'forward':
        try:
            result = search.startSearch(arg1,'1', arg4)
            if len(result) > int(arg2):
                n = int(arg2)
            else:
                n = len(result)
            return render(req,'pathway_result.html',
                               {'result':result[0:n],'compounds1':arg1,'compounds2':arg2, 'org':org})
        except Exception as err:
            return HttpResponse(err)
        
    else:
        try:
            result = search.endSearch(arg1, '1', arg4)
            if len(result) > int(arg2):
                n = int(arg2)
            else:
                n = len(result)
            return render(req,'pathway_result.html',
                               {'result':result[0:n],'compounds1':arg1,'compounds2':arg2, 'org':org})
        except Exception as err:
            return HttpResponse(err)

def path_show(req):
    compound = req.POST['compound']
    result = search.startSearch(compound, '1', '(1,1,1)')

    next_compound = []
    for i in range(len(result)):
        next_compound.append(result[i][0][1])
    
    return HttpResponse(','.join(next_compound))
    # 
    # 
    # if len(result)>0:
    #     return HttpResponse(','.join(result[1]))
    # else:
    #     return HttpResponse()


def compound_info(req):
    compound = req.POST['compound']
    infor = compounds_data[compound]
    infor[0] = infor[0].split(';')[0]
    return HttpResponse('|'.join(infor))


def pathway_information(req,cID, compounds, reactions, enzymes):

    # EC = req.POST['EC'].split(',')
    # Substrate = req.POST['compounds'].split(',')
    # org = req.POST['org']

    cID = cID.split('->')
    Compounds = compounds.split(',')
    Reactions = reactions.split(',')
    EC = enzymes.split('|')[0].split(',')

    # org = 'ecj'
    org = enzymes.split('|')[1]

    sel_result = []
    enzyme_information = []
    sequence = []
    compounds_infor = []
    for i in range(len(EC)):
        ec = EC[i]
        substrate = Compounds[i]
        cd = compounds_data[cID[i]]
        cd[0] = cd[0].split(';')[0]
        compounds_infor.append(cd)

        sel = selenzyme.sort_by_default(ec, substrate, org)[0]
        sel_result.append([ec,sel[0],sel[1]])
        # s_seq = []
        # for s in sel[1]:

        sequence.append([ec, sel[1]])

        # enzyme_information.append(enzymeInfo[ec].split('\n'))
    cd = compounds_data[cID[i]]
    cd[0] = cd[0].split(';')[0]
    compounds_infor.append(cd)
    path_data = compounds
    enzyme_data = sel_result
    seq_data = sequence
#     information = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    path_information = []
    for j in range(len(Reactions)):
        path_information.append([Reactions[j], Compounds[j], Compounds[j+1], enzyme_data[j], cID[j], cID[j+1], compounds_infor[j],compounds_infor[j+1] ] )

    return render(req,'pathway_information.html',
                               {"path_information":path_information, "org":org, "cID":cID, "compounds":Compounds, "reactions":Reactions,"enzymes":EC,"path_data":path_data, "enzyme_data":enzyme_data, "seq_data":seq_data, 'compounds_infor':compounds_infor})



