# -*- coding: utf-8 -*-
# enzyme sequence 
from django.shortcuts import render
from django.http import HttpResponse
from parts_design import codon_optimization,homo_sequence
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from django.template import Context, loader
from parts_design.searching import browser,name_search
from data import SQL
import os

path = os.path.dirname(__file__)
# /home/xubo/sites/Pathlab/parts_design
def parts(req):
    return render(req, 'parts_design.html')

def sequence_validation(req, seq, organism):
    # seq = req.POST['seq']
    # organism = req.POST['organism']
    # sequence = [codon_optimization.Codon_Optimization(seq, organism),seq]

    try:
        sequence = [codon_optimization.Codon_Optimization(seq, organism),seq]
        return render(req,'parts_result.html',
                                {'sequence':sequence, 'flag':'sequence'})   
    except:
        return HttpResponse("Sorry about that can't validate this sequence.")

def sequence_validation_post(req):
    seq = req.POST['sequence']
    if seq=='-':
        return HttpResponse("Sorry about that can't validate this sequence.")
    organism = req.POST['org']
    sequence = [codon_optimization.Codon_Optimization(seq, organism),seq]
    return render(req,'parts_result.html',
                             {'sequence':sequence, 'flag':'sequence'})


def show_sequence(req, infor1):
    
    EC = infor1
    EC = EC.split(',')
    result = []
    for ec in EC:
        result.append([homo_sequence.Get_Homo_Seq(ec),ec])
    return render(req,'sequence_result.html',
                             {'result':result})


def full_sequence(req, seq):
    return HttpResponse(seq)



def parts_search(req):

    l_sel = int(len(req.POST.keys())/2)
    search = {'name':'','type':'','keyword':''}
    for i in range(l_sel):
        s_type = req.POST['sel_builder'+str(i+1)]
        s_content = req.POST['content'+str(i+1)]
        search[s_type] = s_content   
    
    db_name = path + '/../data/parts_design/parts.db'

    if search['name']  != '' and search['type'] != '':
        result = browser(db_name, name=search['name'],type=search['type'],keyword=search['keyword'])
    elif search['name']  == '' and search['type'] == '':
        result = browser(db_name, keyword=search['keyword'])
    elif search['name']  != '':
        result = browser(db_name, name=search['name'],keyword=search['keyword'])
    else:
        result = browser(db_name, type=search['type'],keyword=search['keyword'])    

    return render(req,'parts_result.html',
                  {'result':result[0]})
