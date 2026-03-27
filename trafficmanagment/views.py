from django.shortcuts import render

def basefunction(request):
    return render(request,'base.html')