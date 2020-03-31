from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render,HttpResponse
from .models import History

# Create your views here.

def index(request):
    return render(request,"calculator/index.html")

def result(request):
    result = request.GET.get("result",0)
    input_str = request.GET.get("input_str","").replace("2B%","+")
    history = History.objects.all()
    # print(input_str)
    return render(request,"calculator/result.html",
                  {"result":result,"input_str":input_str,"history":history})


def calculate(request):
    input_str = request.POST.get("input_str")
    try:
        result = eval(input_str)
    except Exception as e:
        return JsonResponse({"status": "false", "message": str(e)})
    history = History.objects.create(input_str=input_str,result=result)

    return JsonResponse({"status": "true", "message": model_to_dict(history)})