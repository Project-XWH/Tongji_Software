# -*- coding: utf-8 -*- 
# report download
from django.shortcuts import render
from django.http import HttpResponse
from parts_design import codon_optimization,homo_sequence
from enzyme_selection import selenzyme
import datetime
import pickle
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph,SimpleDocTemplate
from django.template import Context, loader
#字体库
import reportlab.lib.fonts              
#canvas画图的类库
from reportlab.pdfgen.canvas import Canvas  
#用于定位的inch库，inch将作为我们的高度宽度的单位
from reportlab.lib.units import inch    

from reportlab.lib.styles import getSampleStyleSheet ,ParagraphStyle
from reportlab.lib import  colors

import os
path = os.path.dirname(__file__)

def new_page(position):
    if position  < 1*inch:
        c.showPage()
        position = 10.5*inch
        pdf_head_footer(c,username, "Pathlab", '39.106.27.234/pathlab/ '+'    '*27 + time, 1)
    return position

def write_content(c, position, content, font_size,font_type, x, username):
    if position < 1.5*inch:
        c.showPage()
        position = 10.5*inch
        time = str(datetime.datetime.now())[0:10]
        pdf_head_footer(c, username, "Pathlab", '39.106.27.234/pathlab/ '+'    '*27 + time, 1)
    c.setFont(font_type, font_size)
    c.drawString(x*inch, position, content)
    position -= 0.3*inch
    return position

def pdf_head_footer(canvas, username, headtext, foottext, flag):
    #setFont是字体设置的函数，第一个参数是类型，第二个是大小
    canvas.setFont("Helvetica-Bold", 13.5)  
    canvas.drawString(0.5*inch, 11*inch, username) 
    canvas.drawString(7*inch, 11*inch, headtext)  #抬头
    canvas.setFont("Helvetica-Bold", 20)
    if flag == 0:  
        canvas.drawString(2.5*inch, 10.4*inch, "Pathway  Construct  Report")    #标题
    canvas.setFont("Helvetica-Bold", 11.5) 
    canvas.drawString(0.5*inch, 0.8*inch, foottext)     #脚注 
    canvas.line(0.5*inch, 10.8*inch, 7.8*inch, 10.8*inch)  #页眉
    canvas.line(0.5*inch, 1*inch, 7.8*inch, 1*inch)     #页脚

def pdf_pathway(position, c, data,username):
    
    position = write_content(c, position, "Pathway information", 17,"Helvetica-Bold", 0.6,username)
    
    for i in range(len(data[0])):
        content = "compound" + str(i)+": "+ data[0][i]
        position = write_content(c, position, content, 16,"Helvetica", 0.6, username)
        if i < len(data[0])-1:
           content = "↓ " + data[1][i]
           position = write_content(c, position, content, 13,"Helvetica-Bold", 2, username)
    return position

def pdf_enzyme(position, c, enzymes_data,username):
#     enzymes_data = {'1.1.1.1':{'org':'ecj', 'ID':'ID', 'seq':'ATG', 'PHO':7, 'PHR':7, 'TR':7, 'TO':7}, '2.2.2.2':{'org':'ecj', 'ID':'ID', 'seq':'ATG', 'PHO':7, 'PHR':7, 'TR':7, 'TO':7}}
    ecs = enzymes_data.keys()
    
    c.setFont("Helvetica-Bold", 17)
    c.drawString(0.6*inch, position,"Enzyme information")
    position -= 0.3*inch
    
    for ec in ecs:
        data = enzymes_data[ec]
#         pt = list(data.keys())
        # pt = ['org', 'PHO', 'PHR', 'TR', 'TO']
        pt = ['org', 'KKM', 'KM', 'PH', 'T']
        content = "------------------------------------EC:%s------------------------------------"%(ec.split('_')[0])
        position = write_content(c, position, content, 16,"Helvetica-Bold", 1, username)
        position = write_content(c, position, "-Physical and chemical properties", 16,"Helvetica-Bold", 0.6, username)
        
        for i in range(5):
            content = str(pt[i]) +": "+ str( data[pt[i]] )
            position = write_content(c, position, content, 16,"Helvetica", 0.7, username)
        seq = data['seq']
        ID = data['ID']
        ORG = data['org']
        position = pdf_sequence(position, c, seq, ID,ORG,username)
#         position = write_content(c, position, , 16,"Helvetica", 0.7)
    return position

def pdf_sequence(position, c, seq, ID,ORG,username):
    l = len(seq)
    seq = seq.upper()
    position = write_content(c, position, "-Sequence", 16,"Helvetica-Bold", 0.6, username)
    content = "> %s | %s | %sbp"%(ID,ORG,str(l))
    position = write_content(c, position, content, 16, "Helvetica-Bold",0.7,username)
    i = 0
    for i in range(int(l/40)):
        s1 = seq[40*i:40*(i+1)]
        s = ''
        for j in range(int(len(s1)/10)): 
            s = s + s1[10*j:(j+1)*10]+ "  " 
        position = write_content(c, position, s, 16,"Helvetica", 0.7,username)
    if l < 40:
        s1 = seq[0:]
    else:
        s1 = seq[40*(i+1):]
    s = ''
    for j in range(int(len(s1)/10)): 
        s = s  + s1[10*j:(j+1)*10]+ "  "
    if len(s1) == 0:
        s = ''
    elif len(s1) < 10 and len(s1) >0:
        s = seq
    else:
        s = s  + s1[(j+1)*10:]
    position = write_content(c, position, s, 16,"Helvetica", 0.7,username)
    return position

def sequence_download(req):
#     创建带有PDF头部定义的HttpResponse对象
    sequence = req.POST['seq'].upper()
    ID = req.POST['gene_id']
    name = ID + '.pdf'
    response =HttpResponse(sequence)
    response['Content-Type']='application/pdf'
    response['Content-Disposition']='attachment;filename=%s'%name
    c = canvas.Canvas(response)
    
    time = str(datetime.datetime.now())[0:10] #str(datetime.datetime.now())[:-7].replace(' ', '.')
    pdf_head_footer(c, username ,"Pathlab", '39.106.27.234/pathlab/ '+'    '*27 + time,0)
    position = 10*inch  # 正文范围：10.5-1
    pdf_sequence(position, c, sequence, ID)
    c.showPage()
    c.save()
    return response




def Report(req):
    # username = req.POST['username']
    username = str(req.user)
    ECS = req.POST['enzy']
    ECS = ECS.split(',')
    Reactions = []
    Compounds=[]
    Orgs = []
    enzymes_data = {}
    # org = 'ecj'
    org = req.POST['org']
    for k in range(len(ECS)):
        ec = ECS[k]
        ec = ec+'_'+str(k+1)
        enzymes_data[ec] = {}
        # {'org':'ecj', 'ID':'ID', 'seq':'ATG', 'PHO':7, 'PHR':7, 'TR':7, 'TO':7}
        Selections = req.POST.get(ec)
        Selections = Selections.split('|')
        Reactions.append(Selections[0])
        Compounds.append(Selections[1])
        Orgs.append(Selections[3])

        sel_infor = selenzyme.sort_by_default(ec.split('_')[0], Selections[1], org)[1]
        for i in range(len(sel_infor[0])):
            infor = sel_infor[0][i]
            seq_infor = sel_infor[1][i]
            if infor[0]==Selections[3]:
                enzymes_data[ec]['org'] = Selections[3]
                enzymes_data[ec]['KKM'] = infor[1]
                enzymes_data[ec]['KM'] = infor[2]
                enzymes_data[ec]['PH'] = infor[3]
                enzymes_data[ec]['T'] = infor[4]
            if seq_infor[0]==Selections[3]:
                enzymes_data[ec]['ID'] = seq_infor[1]
                enzymes_data[ec]['seq'] = seq_infor[2]

    Compounds.append(Selections[2])

    # compounds = compounds.split(',')
    # ecs = enzymes.split(',')
    
    name = username+"_Pathlab_Report.pdf"
    ID = '123'
    response =HttpResponse()
    response['Content-Type']='application/pdf'
    response['Content-Disposition']='attachment;filename=%s'%name
    c = canvas.Canvas(response)
            
    position = 10*inch  # 正文范围：10.5-1
    time = str(datetime.datetime.now())[0:10] #str(datetime.datetime.now())[:-7].replace(' ', '.')
    pdf_head_footer(c, username, "Pathlab", '39.106.27.234/pathlab/ '+'    '*27 + time,0,)
    #showpage将保留之前的操作内容之后新建一张空白页
    
#     data = [["beta-Alanine","3-Oxopropanoate","Acetyl-CoA","Acetate","UDP-3-O-(3-hydroxytetradecanoyl)-N-acetylglucosamine","UDP-N-acetyl-alpha-D-glucosamine"],["2.6.1.18","1.2.1.18","3.1.2.1","3.5.1.108","2.3.1.129"]]
    path_data = [Compounds, ECS]
    position = pdf_pathway(position, c, path_data,username)
    position = pdf_enzyme(position, c, enzymes_data,username)

    c.showPage()                  
    #将所有的页内容存到打开的pdf文件里面。
    c.save()    
    return response

    
    
    
    
# #     enzyme = {'PHO':34, 'PHR':34, 'TR':34, 'TO':34}
#     data = pickle.load(open(path+'/../data/enzyme_selection/enzyme.pkl', 'rb'))
#     organism_catalog = pickle.load(open(path+'/../data/enzyme_selection/organism_catalog.pkl','rb'))
#     Name = {}
#     for i in organism_catalog:
#         name = ' '.join(organism_catalog[i][-1].split(' ')[0:2])
#         Name[i] = name
#     enzymes_data = {}
#     for i in range(len(ecs)):
#         ec_info = {}
#         ec = ecs[i]
#         seqrg = req.POST[ec]
#         homo_seq = homo_sequence.Get_Homo_Seq(ec)
#         org = list(homo_seq.keys())[0]
#         seq_infor = homo_seq[org][0]
#         if len(seq_infor) <=1:
#             homo_org = '-'
#             seq_id = '-'
#             seq = '-'
#         else:
#             homo_org = seq_infor[0]
#             seq_id = seq_infor[1]
#             seq = seq_infor[2]

#         if homo_org in Name.keys():
#             homo_name = Name[homo_org]
#         else:
#             homo_name = '-'

#         if homo_name not in data[ec].keys():
#             enzyme_info = {'PH':['-'], 'T':['-']}
#             ec_info['PHO'] = '-'
#             ec_info['PHR'] = '-'
#             ec_info['TR'] = '-'
#             ec_info['TO'] = '-'
#         else:
#             enzyme_info = data[ec][Name[homo_org]]
#             ec_info['PHO'] = str(enzyme_info['PH'][1])
#             ec_info['PHR'] = '-'.join([str(enzyme_info['PH'][0]),str(enzyme_info['PH'][-1])])
#             ec_info['TR'] = '-'.join( [str(enzyme_info['T'][0]),str(enzyme_info['T'][-1])])
#             ec_info['TO'] = str(enzyme_info['T'][1])
#         ec_info['org'] = homo_name
#         ec_info['ID'] = seq_id
#         ec_info['seq'] = seq
        
#         enzymes_data[ec] = ec_info
        
#     position = pdf_enzyme(position, c, enzymes_data)
    
    #seq="ACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTAC"
    #position = pdf_sequence(position, c, seq, ID)
    
    # c.showPage()                  
    # #将所有的页内容存到打开的pdf文件里面。
    # c.save()    
    # return response






# def Report(req, compounds, enzymes, seq_data):
#     compounds = compounds.split(',')
#     ecs = enzymes.split(',')
    
#     name = "report.pdf"
#     ID = '123'
#     response =HttpResponse()
#     response['Content-Type']='application/pdf'
#     response['Content-Disposition']='attachment;filename=%s'%name
#     c = canvas.Canvas(response)
            
#     position = 10*inch  # 正文范围：10.5-1
#     time = str(datetime.datetime.now())[0:10] #str(datetime.datetime.now())[:-7].replace(' ', '.')
#     pdf_head_footer(c, "Pathlab", '39.106.27.234/pathlab/ '+'    '*27 + time,0)
#     #showpage将保留之前的操作内容之后新建一张空白页
    
# #     data = [["beta-Alanine","3-Oxopropanoate","Acetyl-CoA","Acetate","UDP-3-O-(3-hydroxytetradecanoyl)-N-acetylglucosamine","UDP-N-acetyl-alpha-D-glucosamine"],["2.6.1.18","1.2.1.18","3.1.2.1","3.5.1.108","2.3.1.129"]]
#     path_data = [compounds, ecs]
#     position = pdf_pathway(position, c, path_data)
    
    
    
# #     enzyme = {'PHO':34, 'PHR':34, 'TR':34, 'TO':34}
#     data = pickle.load(open(path+'/../data/enzyme_selection/enzyme.pkl', 'rb'))
#     organism_catalog = pickle.load(open(path+'/../data/enzyme_selection/organism_catalog.pkl','rb'))
#     Name = {}
#     for i in organism_catalog:
#         name = ' '.join(organism_catalog[i][-1].split(' ')[0:2])
#         Name[i] = name
#     enzymes_data = {}
#     for i in range(len(ecs)):
#         ec_info = {}
#         ec = ecs[i]
#         homo_seq = homo_sequence.Get_Homo_Seq(ec)
#         org = list(homo_seq.keys())[0]
#         seq_infor = homo_seq[org][0]
#         if len(seq_infor) <=1:
#             homo_org = '-'
#             seq_id = '-'
#             seq = '-'
#         else:
#             homo_org = seq_infor[0]
#             seq_id = seq_infor[1]
#             seq = seq_infor[2]

#         if homo_org in Name.keys():
#             homo_name = Name[homo_org]
#         else:
#             homo_name = '-'

#         if homo_name not in data[ec].keys():
#             enzyme_info = {'PH':['-'], 'T':['-']}
#             ec_info['PHO'] = '-'
#             ec_info['PHR'] = '-'
#             ec_info['TR'] = '-'
#             ec_info['TO'] = '-'
#         else:
#             enzyme_info = data[ec][Name[homo_org]]
#             ec_info['PHO'] = str(enzyme_info['PH'][1])
#             ec_info['PHR'] = '-'.join([str(enzyme_info['PH'][0]),str(enzyme_info['PH'][-1])])
#             ec_info['TR'] = '-'.join( [str(enzyme_info['T'][0]),str(enzyme_info['T'][-1])])
#             ec_info['TO'] = str(enzyme_info['T'][1])
#         ec_info['org'] = homo_name
#         ec_info['ID'] = seq_id
#         ec_info['seq'] = seq
        
#         enzymes_data[ec] = ec_info
        
#     position = pdf_enzyme(position, c, enzymes_data)
    
#     #seq="ACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTACACTAGCGATGCGTAGCGTAGACCAGGATGACCAGGTAC"
#     #position = pdf_sequence(position, c, seq, ID)
    
#     c.showPage()                  
#     #将所有的页内容存到打开的pdf文件里面。
#     c.save()    
#     return response
    
    
    
    
    
    
