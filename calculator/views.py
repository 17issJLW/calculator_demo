from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse, redirect
from .models import History, MyUser
import logging

logger = logging.getLogger("log")


# Create your views here.
@login_required(login_url="/login")
def index(request):
    logger.info(request.user)
    return render(request,"calculator/index.html")

@login_required
def result(request):
    """
    计算结果，历史记录页
    :param request:
    :return:
    """
    result = request.GET.get("result",0)
    input_str = request.GET.get("input_str","").replace("2B%","+")
    history = History.objects.filter(myuser__user=request.user)
    logger.info("{} 查看了历史记录".format())
    return render(request,"calculator/result.html",
                  {"result":result,"input_str":input_str,"history":history})

def user_login(request):
    """
    用户登陆
    :param request:
    :return:
    """
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("username")
        user = MyUser.objects.filter(user__username=username,user__password=password).first()
        if user is not None:
            login(request,user.user)
            logger.info("{} 登陆成功！".format(user.user.username))
            return JsonResponse({"status":"true","message": model_to_dict(user)})
        return JsonResponse({"status":"false","message":"用户名/密码错误"})

    return render(request,"calculator/login.html")


def user_register(request):
    """
    用户注册
    :param request:
    :return:
    """
    if request.method == "POST":
        try:
            username = request.POST.get("username")
            password = request.POST.get("password")
            sex = request.POST.get("sex")

            user = User(username=username)
            user.set_password(password)
            myUser = MyUser.objects.create(user=user,sex=sex)


        except Exception as e:
            status = "false"
            message = repr(e)
            logger.info("{} 注册失败！{}".format(username,repr(e)))
        else:
            status = "true"
            message = "成功注册！"
        return JsonResponse({"status":status,"message":message})


def user_logout(request):
    """
    注销
    :param request:
    :return:
    """
    logout(request)
    logger.info("{} 注销登陆！".format(request.user.username))
    return redirect("/")



@login_required
def calculate(request):
    """
    计算表达式
    :param request:
    :return:
    """
    input_str = request.POST.get("input_str")
    try:
        result = eval(input_str)
    except Exception as e:
        return JsonResponse({"status": "false", "message": str(e)})
    history = History.objects.create(input_str=input_str,result=result)

    return JsonResponse({"status": "true", "message": model_to_dict(history)})