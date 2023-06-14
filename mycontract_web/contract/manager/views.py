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
        contract_name = request.POST.get('contract_name')
        # get all of the contract which contains the name
        query_set = Contract.objects.filter(name__contains='%s'%(contract_name))

        # judge the contract's state 
        contracts = []
        for row in query_set:
            if row.distribute == 0:
                contracts.append(row.name)
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
        sign = []
        query_counter = HaveAuthority.objects.filter(right_id=4)
        query_approve = HaveAuthority.objects.filter(right_id=5)
        qeury_sign = HaveAuthority.objects.filter(right_id=6)

        for row in query_counter:
            name = User.objects.filter(id=row.user_id).first().name
            counters.append(name)
        for row in query_approve:
            name = User.objects.filter(id=row.user_id).first().name
            approves.append(name)
        for row in qeury_sign:
            name = User.objects.filter(id=row.user_id).first().name
            sign.append(name)

        response['counter'] = counters
        response['approve'] = approves
        response['sign'] = sign

        return JsonResponse(response)
    else :
        contract_name = request.POST.get('contract_name')
        counter_names = request.POST.getlist('counter_names')
        approve_names = request.POST.getlist('approve_names')
        sign_names = request.POST.getlist('sign_names')
        
        contract_id = Contract.objects.filter(name=contract_name).first().id
        for name in counter_names:
            # send the email
            email = User.objects.filter(name=name).first().email
            send('待会签', '《%s》等待你会签'%(contract_name), email)
            user_id = User.objects.filter(name=name).first().id
            CounterSign.objects.create(user_id=user_id, contract_id=contract_id)
        
        for name in approve_names:
            # # send the email
            # email = User.objects.filter(name=name).first().email
            # send('待审核', '{}等待你审核'%(contract_name), email)
            user_id = User.objects.filter(name=name).first().id
            Approve.objects.create(user_id=user_id, contract_id=contract_id)

        for name in sign_names:
            # # send the email
            # email = User.objects.filter(name=name).first().email
            # send('待签订', '{}等待你签订'%(contract_name), email)
            user_id = User.objects.filter(name=name).first().id
            Sign.objects.create(user_id=user_id, contract_id=contract_id)

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
            operators.append(row.name)

        response['operators'] = operators
        return JsonResponse(response)
    
@csrf_exempt
def contribute(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 1:
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        draft_right = int(request.POST.get('isDraft'))
        acounter_right = int(request.POST.get('isAcounter'))
    
        approve_right = int(request.POST.get('isApprove'))
        sign_right = int(request.POST.get('isSign'))
        
        query_set = HaveAuthority.objects.filter(user_id=user_id)
        rights = []
        for row in query_set:
            rights.append(row.right_id)

        # contribute the right
        if draft_right == 1:
            
            # print(1)
            if 3 not in rights:
                HaveAuthority.objects.create(user_id=user_id, right_id=3)
        if acounter_right == 1:
            # print(2)
            if 4 not in rights:
                HaveAuthority.objects.create(user_id=user_id, right_id=4)
        if approve_right == 1:
            # print(3)
            if 5 not in rights:
                HaveAuthority.objects.create(user_id=user_id, right_id=5)
        if sign_right == 1:
            # print(4)
            if 6 not in rights:
                HaveAuthority.objects.create(user_id=user_id, right_id=6)
        
        return JsonResponse(response)

@csrf_exempt       
def checkContractState(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 1 :
        contracts = []
        start_times = []
        end_times = []
        states = []

        # get all of the contract's information
        query_set = Contract.objects.all()
        for row in query_set:
            contracts.append(row.name)
            start_times.append(row.start_time)
            end_times.append(row.end_time)
            # judge the contract state of distribution
            if row.distribute == 0:
                states.append(-1)
            else :
                states.append(row.state)
        
        response['contracts'] = contracts
        response['start_times'] = start_times
        response['end_times'] = end_times
        response['states'] = states
        
        return JsonResponse(response)

@csrf_exempt
def checkLog(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        operators = []
        times = []
        behaviours = []

        # get all of the logs
        query_set = Log.objects.all()
        for row in query_set:
            operators.append(User.objects.filter(id=row.user_id).first().name)
            times.append(row.time)
            behaviours.append(row.behaviour)
        response['operators'] = operators
        response['times'] = times
        response['behaviours'] = behaviours
        return JsonResponse(response)
        