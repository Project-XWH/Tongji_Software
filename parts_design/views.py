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
    #EC = req.POST['ec']
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

    # l_sel = int(len(req.POST.keys())/2)
    # SEL_builder = {'creation_date':'2000-01-01 - now','type':'*', 'name':''}

    # SEL_builder[req.POST['sel_builder'+str(l_sel)]] = req.POST['content'+str(l_sel)]

    # for i in range(l_sel):
    #     SEL_builder[req.POST['sel_builder'+str(i+1)]] = req.POST['content'+str(i+1)]
        # SEL_builder.append([req.POST['sel_builder'+str(i)], req.POST['content'+str(i)]])


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

    # result = browser(db_name, name=search[0][1],type='RBS',keyword=search[keyword])
    return render(req,'parts_result.html',
                  {'result':result[0]})


    # if SEL_builder['name'] != '':
    #     result = name_search(db_name, SEL_builder['name'] ,type = None,out_num = 20)
    #     return render(req,'parts_result.html',
    #                  {'result':result,'path':path, 'flag':'parts_name'})
    # else:
        
    #     result = browser(db_name,"searching.name, type, uses, status, description, categories, sequence", type=SEL_builder['type'], creation_date=SEL_builder['creation_date'],reverse=[True,False])
    #     return render(req,'parts_result.html',
    #                  {'result':result[0],'path':path, 'flag':'parts'})

    
    # result = SQL.selectPartsByPID(ID)
    
    # result = browser(db_name,"searching.name, type, uses, status, description, categories, sequence",searching.name=name,reverse=[True,False])
    # result = name_search(db_name,name,type = None,out_num = 20)
    # *parts ID  *nickname   *type  *uses  *short_desc  *description  *categories  *sequence  *iGEMstatus
    
    # browser()
    



# (48588, 'BBa_K2656026', 'Terminator', 9, 'Planning', 0, 0, "It's complicated", '2018-09-20', 27, 0, 'BBa_K2656026', 'Double transcriptional terminator (B0010-B0012) ', 'Part BBa_B0015 domesticated to the Golden Braid 3.0 grammar. The most commonly used terminator domesticated to be used to assembly transcriptional units with the Golden Gate assembly method. It can be used as a Biobrick too.', 'Adri??n Requena Guti?©rrez', 'It has been designed adding to the promoter sequence:GCGCCGTCTCGCTCGGCTT upstream and CGCTTGAGCGAGACGGCGC downstream. These sequences allow the assembly of the part into BBa_P10500 with a Golden Gate reaction using BsmbI endonuclease.', 'The original sequence has been obtained from the Registry of Standard Biological Parts and it has been synthetized by IDT.', 'Null', 'Not Given', 'gcttccaggcatcaaataaaacgaaaggctcagtcgaaagactgggcctttcgttttatctgttgtttgtcggtgaacgctctctactagagtcacactggctcaccttcgggtgggcctttctgcgtttatacgct'), 
# (49787, 'BBa_K2675030', 'Terminator', 9, 'Unavailable', 0, 0, 'Not in stock', '2018-10-05', 27, 0, 'BBa_K2675030', 'L3S2P56 Terminator', 'ECK120029600 Terminator', 'Esteban Lebrun', 'ECK120029600 Terminator', 'DNA synthesis', 'Null', 'Not Given', 'ctcggtaccaaattttcgaaaaaagacgctgaaaagcgtcttttttcgttttggtcc'), 
# (50269, 'BBa_K2621038', 'RBS', 9, 'Planning', 0, 0, "It's complicated", '2018-10-07', 25, 0, 'BBa_K2621038', 'CAT-Seq Ribosome Binding Site (RBS)', 'a', 'Irmantas Mogila', 'c', 'Not Given', 'Null', 'Not Given', 'aaggag'), 
# (52306, 'BBa_K2685025', 'RBS', 9, 'Available', 0, 0, 'In stock', '2018-10-14', 22, 0, 'BBa_K2685025', 'RBS', 'It is a ribosomebinding site', 'WANG,MENG', 'It is a ribosomebinding site', 'It from Kit Plate', 'Null', 'Not Given', 'aaagaggagaaa')], 4)

# create table searching(
#     id int not null,
#     name char(30) not null,
#     type char(30) not null check(type in ('Terminator','Promoter','RBS')),
#     owning_group_id int,
#     status char(30) not null check(status in ('Available', 'Deleted', 'Unavailable', 'Planning')),
#     dominant int not null check(dominant in (0,1)),
#     discontinued int not null,
#     sample_status char(30) not null check(sample_status in ('In stock','Discontinued', 'Not in stock', "It's complicated", 'No part sequence')),
#     creation_date char(10) not null,
#     uses int,
#     favorite int check(favorite in (0,1)),
#     primary key(id,name))
# (searching.name, type, uses, status, description, categories, sequence)

# create table text(
# name char(30) not null primary key,
# short_desc char(1000),
# description char(5000),
# author char(500),
# notes char(5000),
# source char(1000),
# nickname char(100),
# categories char(200),
# sequence char(5000)
