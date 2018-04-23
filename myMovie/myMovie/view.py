
from django.shortcuts import render
 
def hello(request):
    context          = {}
    context['hello'] = 'Hello Worldsdafsdafsa!'
    return render(request, 'hello.html', context)