from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Contract, Customer, File, User, CounterSign, Approve, Sign, HaveAuthority, Authority
from django.http import HttpResponse

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

# user_struct = {
#     'id' : 1, 
#     'name' : 'haha'
#     "role"
# }


@csrf_exempt
def distribute_role_click(request):
    response = {**headers}
    if request.method == 'POST':

        # user_name = request.POST['user_name']
        user_name = request.POST.get('user_name')
        right = 0
        if user_name == 'admin':
            right = 1
        response['right'] = right
        user_package = []

        # user_ID_list = []
        # user_name_list = []
        # user_roleID_list = []

        # if user_name == 'admin' :
        query_set = User.objects.exclude(name = 'admin') 
        # print(query_set.count())
        for i in query_set :
            temp = {
                'user_ID' : i.id,
                'user_name' : i.name,
                'user_RoleID' : i.roleID,
            }
            user_package.append(temp)

        response['item'] = user_package
        #     user_ID_list.append(i.id)
        #     user_name_list.append(i.name)
        #     user_roleID_list.append(1)
        # response['user_ID'] = user_ID_list
        # response['user_name'] = user_name_list
        # response['user_roleID'] = user_roleID_list
    
        # else :
        #     query_set = User.objects.filter(roleID__in=[0,1]) 
        #     for i in query_set :
        #         user_name_list.append(i.name)
        #         user_roleID_list.append(i.roleID)
        #     response['user_name'] = user_name_list
        #     response['user_roleID'] = user_roleID_list

        return JsonResponse(response)
    
@csrf_exempt
def distribute_role_change_left_to_right(request):
    response = {**headers} 

    user_name_list = str(request.POST.get('list'))
    user_name_lists = user_name_list.split(',')
    print(user_name_list)
    print(2)

    for i in user_name_lists :
        query_set = User.objects.filter(id=int(i)) 
        change_user = query_set[0]
        change_user.roleID = 2

        change_user.save()

    response['list'] = 10086
    return JsonResponse(response)

@csrf_exempt
def distribute_role_change_right_to_left(request):
    
    
    response = {**headers} 

    user_name_list = str(request.POST.get('list'))
    user_name_lists = user_name_list.split(',')
    print(1)

    for i in user_name_lists :
        query_set = User.objects.filter(id=int(i)) 
        change_user = query_set[0]
        change_user.roleID = 1

        change_user.save()

    response['list'] = 10087
    return JsonResponse(response)