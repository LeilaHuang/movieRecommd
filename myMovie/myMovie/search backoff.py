# -*- coding: utf-8 -*-
# 
from django.http import HttpResponse
from django.shortcuts import render_to_response
 
# 表单
def search_form(request):
    return render_to_response('search_form.html')
 
# 接收请求数据
def search(request):  
    request.encoding='utf-8'
    if 'userID' in request.GET:
        message = 'the userId: ' + request.GET['userID']
    else:
        message = 'no userId submitted'
    return HttpResponse(message)

