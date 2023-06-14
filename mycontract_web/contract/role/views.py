from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Contract, Customer, File, User, CounterSign, Approve, Sign, HaveAuthority, Authority
from django.http import HttpResponse

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}



@csrf_exempt
def distribute_role_click(request):
    response = {**headers}
    if request.method == 'POST':

        user_name = request.POST['user_name']

        user_name_list = []
        user_roleID_list = []

        if user_name == 'admin' :
            query_set = User.objects.exclude(name = 'admin') 
            print(query_set.count())
            for i in query_set :
                user_name_list.append(i.name)
                user_roleID_list.append(i.roleID)
            response['user_name'] = user_name_list
            response['user_roleID'] = user_roleID_list
    
        else :
            query_set = User.objects.filter(roleID__in=[0,1]) 
            for i in query_set :
                user_name_list.append(i.name)
                user_roleID_list.append(i.roleID)
            response['user_name'] = user_name_list
            response['user_roleID'] = user_roleID_list

        return JsonResponse(response)
    
@csrf_exempt
def distribute_role_change(request):
    response = {**headers}

    user_name = request.POST['user_name']
    user_new_roleID = request.POST['user_new_roleID']

    query_set = User.objects.filter(name=user_name) 
    change_user = query_set[0]
    change_user.roleID = user_new_roleID
    change_user.save()

    if int(user_new_roleID) == 2 :
        print(change_user.id)
        query_set = HaveAuthority.objects.filter(user=change_user) 
        if query_set.count() == 0 :
            right = Authority.objects.get(id=2)
            new_authority = HaveAuthority(user=change_user, right=right)
            new_authority.save()
    response['operate_state'] = 1
    return JsonResponse(response)