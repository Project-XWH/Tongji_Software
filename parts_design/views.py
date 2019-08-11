from django.shortcuts import render, render_to_response
#import codon_optimization
# Create your views here.
import os
def parts(req):
    return render_to_response('parts_design.html')

def sequence_validation(req):
    seq = req.POST['sequence']
    organism = req.POST['organism']
    sequence = os.popen('python ./parts_design/codon_optimization.py %s %s'%(seq, organism)).readlines()
    return render_to_response('parts_result.html',
                             {'sequence':sequence})
