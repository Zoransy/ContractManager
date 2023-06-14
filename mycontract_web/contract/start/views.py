from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
# import the table 
from contract.models import User, HaveAuthority

import uuid

loginSuccess = {
    # 状态码，0表示成功
    "state": 0,
    # 令牌，用uuid模块生成一个唯一的字符串
    "token": uuid.uuid4().hex
}

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

# Create your views here.
@csrf_exempt
def login(request):
    # POST enter the body
    types = int(request.POST.get('types'))
    if types == 1 :
        response = {**headers}
        user_name = request.POST.get('user')
        user_pwd = request.POST.get('passwd')
        query_name = User.objects.filter(name=user_name).first()
        # when query_name is none, then not found the user
        if query_name == None:
            response["state"] = 1
            print('the user is not found!')
            return JsonResponse(response)
        else:
            query_row = User.objects.filter(name=user_name, password=user_pwd).first()
            # password is wrong
            if query_row == None:
                response["state"] = -1
                print('the password is wrong!')
                return JsonResponse(response)
            # find the user
            response.update(**loginSuccess)
            if query_row.roleID == 2:
                # group == 2 is administrator
                response['group'] = 2
            else :
                # group == 1 is operator
                if query_row.roleID == 1:
                    response['group'] = 1 
                else :
                    # group == 0 is the new one
                    response['group'] = 0
            query_right = HaveAuthority.objects.filter(user_id=query_row.id)
            rights = []
            if not query_right.exists():
                # this is meaning he hasn't rights
                rights.append(0)
            else :
                for row in query_right:
                    rights.append(row.right_id)
            response['right'] = rights
            return JsonResponse(response)
            
@csrf_exempt
def register(request):
    user_name = request.POST.get('user')
    user_pwd = request.POST.get('passwd')
    email = request.POST.get('email')
    # judge is there the user_name, if it exists, then refuse the creation
    query_row = User.objects.filter(name=user_name).first()

    response = {**headers}
    if query_row != None:
        # state == -1 is meaning that the person has existed.
        response['state'] = -1
        return JsonResponse(response)
    else:
        # succeed to insert the user who is the new one
        User.objects.create(name=user_name, password=user_pwd, email=email)
        response['state'] = 0
        return JsonResponse(response)
