from django.shortcuts import render
from django.shortcuts import render_to_response
from django.http import HttpResponse
import os

# Create your views here.
def main(req):
    # return HttpResponse('<h1>Hello!<h1>')
    return render_to_response('pathlab.html')
 
def pathway(req):
    return render_to_response('pathway.html')


def path_search(req):
    arg1 = req.POST['start_compound']
    arg2 = req.POST['target_compound']
    arg3 = req.POST['arg3']
    arg4 = req.POST['arg4']
    arg5 = req.POST['arg5']
    #os.system('python search.py %s %s %s %s %s'%(arg1,arg2,arg3,arg4,arg5))
    # result = os.popen('python ./path_search/test.py').readlines()
    result = os.popen("python ./path_search/search.py %s %s %s %s '%s' "%(arg1,arg2,arg3,arg4,arg5)).readlines()
    # result = "python search.py %s %s %s %s '%s'"%(arg1,arg2,arg3,arg4,arg5)
    result = open('./path_search/result.txt').readlines()
    return render_to_response('pathway_result.html',
                               {'result':result})
