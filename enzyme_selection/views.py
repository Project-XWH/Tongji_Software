# -*- coding: utf-8 -*-
# enzyme information
from django.shortcuts import render
import sys
import pickle
import os
from operator import itemgetter, attrgetter
from enzyme_selection import selenzyme
from parts_design import codon_optimization,homo_sequence
from django.conf import settings
import pickle
# Create your views here.
# def Enzyme_Selection(req):
path = os.path.dirname(__file__)
enzymeInfo = pickle.load(open(path+'/../data/enzyme_selection/enzyme_info.pkl', 'rb'))
data = pickle.load(open(path+'/../data/enzyme_selection/enzyme.pkl', 'rb'))
organism_catalog = pickle.load(open(path+'/../data/enzyme_selection/organism_catalog.pkl','rb'))

orgs = {'ecj':'ecoli','sce':'yeast'}

def enzyme(req):
    return render(req,'enzyme.html', {'STATIC_ROOT':settings.STATIC_ROOT}) #, {'user':req.user})

# /home/xubo/sites/Pathlab/enzyme_selection
def Enzyme_Information(req):
    
    EC = req.POST['EC'].split(',')
    Substrate = req.POST['substrate'].split(',')
    org = req.POST['org']

    sel_result = []
    enzyme_information = []
    sequence = []
    for i in range(len(EC)):
        ec = EC[i]
        substrate = Substrate[i]

        sel = selenzyme.sort_by_default(ec, substrate,org)[0]
        sel_result.append([ec,sel[0]])
        sequence.append([ec, sel[1]])

        enzyme_information.append(enzymeInfo[ec].split('\n'))
    
    # ('6.3.3.6', '(2S,5S)-5-carboxymethylproline'
    return render(req,'enzyme_result.html',
                               {'sel_result':sel_result, 'enzyme_info':enzyme_information, 'sequence':sequence, 'org':orgs[org]})

