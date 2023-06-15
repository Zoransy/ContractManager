from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Contract, HaveAuthority, User, CounterSign, Approve, Sign, Log
from contract.methods.method import send


headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

@csrf_exempt
def search_contract(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 1:
        # user_name = request.POST.get('user_name')
        # convert the contract name I can search dimly the contract which is not finished that means state != 3
        # contract_name = request.POST.get('contract_name')
        # get all of the contract which contains the name
        # query_set = Contract.objects.filter(name__contains='%s'%(contract_name))
        query_set = Contract.objects.exclude(distribute=1).all()

        # judge the contract's state 
        contracts = []
        for row in query_set:
            if row.distribute == 0:
                contracts.append({'name' : row.name, 
                                  'beginTime' : row.start_time,
                                  'id' : row.id})
        response['contracts'] = contracts
        
        return JsonResponse(response)

@csrf_exempt
def distribute(request):
    response = {**headers}
    # when click the 分配 跳转此界面 get request
    types = int(request.POST.get('types'))
    if types == 0 :
        # contract_name = request.POST.get('contract_name')
        # return who can counter, approve, sign
        counters = []
        approves = []
        signs = []
        query_counter = HaveAuthority.objects.filter(right_id=4)
        query_approve = HaveAuthority.objects.filter(right_id=5)
        qeury_sign = HaveAuthority.objects.filter(right_id=6)

        for row in query_counter:
            name = User.objects.filter(id=row.user_id).first().name
            counters.append({'name' : name, 
                             'id' : row.user_id})
        for row in query_approve:
            name = User.objects.filter(id=row.user_id).first().name
            approves.append({'name' : name,
                             'id' : row.user_id})
        for row in qeury_sign:
            name = User.objects.filter(id=row.user_id).first().name
            signs.append({'name' : name,
                          'id' : row.user_id})

        response['counters'] = counters
        response['approves'] = approves
        response['signs'] = signs

        return JsonResponse(response)
    else :
        contract_name = request.POST.get('contract_name')
        print(contract_name)
        counter_name = str(request.POST.get('counter_names'))
        approve_name = str(request.POST.get('approve_names'))
        sign_name = str(request.POST.get('sign_names'))
        
        counter_names = counter_name.split(',')
        approve_names = approve_name.split(',')
        sign_names = sign_name.split(',')

        contract_id = Contract.objects.filter(name=contract_name).first().id
        for id in counter_names:
            # send the email
            email = User.objects.filter(id=id).first().email
            send('待会签', '《%s》等待你会签'%(contract_name), email)
            # user_id = User.objects.filter(name=name).first().id
            CounterSign.objects.create(user_id=id, contract_id=contract_id)
        
        for id in approve_names:
            # # send the email
            # email = User.objects.filter(name=name).first().email
            # send('待审核', '{}等待你审核'%(contract_name), email)
            # user_id = User.objects.filter(name=name).first().id
            Approve.objects.create(user_id=id, contract_id=contract_id)

        for id in sign_names:
            # # send the email
            # email = User.objects.filter(name=name).first().email
            # send('待签订', '{}等待你签订'%(contract_name), email)
            # user_id = User.objects.filter(name=name).first().id
            Sign.objects.create(user_id=id, contract_id=contract_id)

        # change the distribution state of the contract
        Contract.objects.filter(name=contract_name).update(distribute=1)

        return JsonResponse(response)

@csrf_exempt
def get_operators(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        operators = []
        # get the all of operators
        query_set = User.objects.filter(roleID=1)
        for row in query_set:
            operators.append({'name' : row.name,
                              'id': row.id})

        response['operators'] = operators
        return JsonResponse(response)
    
@csrf_exempt
def contribute(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 1:
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        # draft_right = int(request.POST.get('isDraft'))
        # acounter_right = int(request.POST.get('isAcounter'))
    
        # approve_right = int(request.POST.get('isApprove'))
        # sign_right = int(request.POST.get('isSign'))
        user_right = str(request.POST.get('permissions'))
        user_rights = user_right.split(',')
        
        query_set = HaveAuthority.objects.filter(user_id=user_id)
        rights = []
        for row in query_set:
            rights.append(row.right_id)

        for right in user_rights:
            if int(right) not in rights:
                HaveAuthority.objects.create(user_id=user_id, right_id=int(right))
        
        # contribute the right
        # if draft_right == 1:
            
        #     # print(1)
        #     if 3 not in rights:
        #         HaveAuthority.objects.create(user_id=user_id, right_id=3)
        # if acounter_right == 1:
        #     # print(2)
        #     if 4 not in rights:
        #         HaveAuthority.objects.create(user_id=user_id, right_id=4)
        # if approve_right == 1:
        #     # print(3)
        #     if 5 not in rights:
        #         HaveAuthority.objects.create(user_id=user_id, right_id=5)
        # if sign_right == 1:
        #     # print(4)
        #     if 6 not in rights:
        #         HaveAuthority.objects.create(user_id=user_id, right_id=6)

        return JsonResponse(response)

@csrf_exempt       
def checkContractState(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 1 :
        contracts = []

        # get all of the contract's information
        query_set = Contract.objects.all()
        for row in query_set:
            if row.distribute == 0 : 
                state = -1
            else :
                state = row.state
            contracts.append({'name' : row.name,
                              'start_time' : row.start_time,
                              'end_time' : row.end_time,
                              'state' : state})
        
        response['contracts'] = contracts
        # 待分配(-1)， 待会签(0)，待定稿(1)，待审批(2)，待签定(3)，已完成(4)
        return JsonResponse(response)

@csrf_exempt
def checkLog(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        logs = []

        # get all of the logs
        query_set = Log.objects.all()
        for row in query_set:
            logs.append({'name' : User.objects.filter(id=row.user_id).first().name,
                         'time' : row.time,
                         'behaviour' : row.behaviour})
        response['logs'] = logs
        return JsonResponse(response)
        