from django.shortcuts import render, render_to_response
import sys
import pickle
import os
from operator import itemgetter, attrgetter

# Create your views here.
# def Enzyme_Selection(req):

def enzyme(req):
    return render_to_response('enzyme.html')

def Enzyme_Information(req):
    EC = req.POST['EC']
    substrate = req.POST['substrate']
    data = pickle.load(open('./data/enzyme_selection/enzyme.pkl','rb'))  
    organism = data[EC].keys()
    result = []
    for org in organism:
        org_info = data[EC][org]
        if substrate in data[EC][org][2].keys():
            result.append([org, org_info[2][substrate], org_info[0], org_info[1], org_info[3]])
    result  = sorted(result, key=itemgetter(1))
    return render_to_response('enzyme_result.html',
                               {'result':result[0]})




