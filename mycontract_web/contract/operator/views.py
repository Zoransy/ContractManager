from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Contract, Customer, File, User, CounterSign, Approve, Sign, Log
from contract.methods.method import send

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

@csrf_exempt
def draft(request):
    # if the request is get, I return the all customer name
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        customer_set = []
        query_set = Customer.objects.all()
        for customer in query_set:
            customer_set.append(customer.name)
        response['customers'] = customer_set
        return JsonResponse(response)
    else :
        # the behaviour is that create the contract, but not to counter
        contract_name = request.POST.get('contract_name')
        customer_name = request.POST.get('customer')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        content = request.POST.get('content')
        file_name = request.POST.get('file_name')
        user_name = request.POST.get('user_name')

        row = Contract.objects.filter(name=contract_name).first()
        if row != None:
            response['state'] = 1
        else :
            response['state'] = 0

            qeury_user = User.objects.filter(name=user_name).first()

            query_file = File.objects.filter(fileName=file_name).first()
    
            qeury_customer = Customer.objects.filter(name=customer_name).first()
            
            Log.objects.create(user_id=qeury_user.id, behaviour='起草了《%s》合同'%(contract_name))

            Contract.objects.create(name=contract_name,
                                    start_time=start_time,
                                    end_time=end_time,
                                    content=content,
                                    customer_id=qeury_customer.id,
                                    file_id=query_file.id,
                                    user_id=qeury_user.id)
            
        
        # state = 0 mean that succeed to create the file
        return JsonResponse(response)
 

@csrf_exempt
def counter(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        user_name = request.POST.get('user_name')
        
        user_id = User.objects.filter(name=user_name).first().id
        # this query_set represent those contracts which is needed to be acounter by the user
        query_set = CounterSign.objects.filter(user_id=user_id)

        contracts = []

        # check these contracts state that 'is it finished'
        for row in query_set:
            contract = Contract.objects.filter(id=row.contract_id).first()
            if row.content is None:
                contracts.append(contract.name)
        response['contracts'] = contracts
        return JsonResponse(response)
    else :
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        contract_name = request.POST.get('contract_name')
        content = request.POST.get('content')
        contract_id = Contract.objects.filter(name=contract_name).first().id
        # the behaviour is recorded in the log
        Log.objects.create(user_id=user_id, behaviour='会签了《%s》合同'%(contract_name))
        CounterSign.objects.filter(contract_id=contract_id, user_id=user_id).update(content=content)
        
        # judge all of the contract are countered
        query_set = CounterSign.objects.filter(contract_id=contract_id)
        flag = True
        for row in query_set:
            if row.content is None:
                flag = False
                break
        if flag:
            # change the state of the contract
            Contract.objects.filter(name=contract_name).update(state=1)
            # select the finalize people
            email = User.objects.filter(id=Contract.objects.filter(name=contract_name).first().user_id).first().email
            send('待定稿', '《%s》等待您定稿'%(contract_name), email)

        return JsonResponse(response)

@csrf_exempt
def get_finalize(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0:
        user_name = request.POST.get('user_name')

        finalizations = []
        # find all of contract which is drafted by the user
        user_id = User.objects.filter(name=user_name).first().id
        query_set = Contract.objects.filter(user_id=user_id)

        # find the contract which has countered that mean state is 1
        for row in query_set:
            if row.state == 1:
                finalizations.append(row.name)
        
        response['finalizations'] = finalizations
        
        return JsonResponse(response)



@csrf_exempt
def finalize(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        # get the content of the contract
        query_row = Contract.objects.filter(user_id=user_id).first()
        content = query_row.content
        customer = Customer.objects.filter(id=query_row.customer_id).first().name
        start_time = query_row.start_time
        end_time = query_row.end_time
        # get the file name of the contract
        file = File.objects.filter(id=query_row.file_id).first().fileName

        response['customer'] = customer
        response['start_time'] = start_time
        response['end_time'] = end_time
        response['content'] = content
        response['file'] = file
        
        return JsonResponse(response)
    
    else :
        contract_name = request.POST.get('contract_name')
        contract_id = Contract.objects.filter(name=contract_name).first().name
        content = request.POST.get('content')

        # query_row = Contract.objects.filter(name=contract_name).first()

        # the behaviour is recorded in the log
        Log.objects.create(user_id=user_id, behaviour='定稿了《%s》合同'%(contract_name))

        Contract.objects.filter(name=contract_name).update(content=content)
        
        Contract.objects.filter(name=contract_name).update(state=2)
        
        # find the approve people
        query_set = Approve.objects.filter(contract_id=contract_id)
        for row in query_set:
            email = User.objects.filter(id=row.user_id).first().email
            send('待审核', '《%s》等待你审核'%(contract_name), email)
        return JsonResponse(response)

@csrf_exempt
def approve(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        user_name = request.POST.get('user_name')
        approves = []
        
        # the user is responsible with the contracts
        user_id = User.objects.filter(name=user_name).first().id
        query_set = Approve.objects.filter(user_id=user_id)
        
        for row in query_set:
            # first the contract must be not accepted
            if row.judge == 0:
                # and secondly need to judge the contract has dinggao, state == 2
                flag = Contract.objects.filter(id=row.contract_id).first()
                if flag.state == 2:
                    approves.append(flag.name)
        
                response['approves'] = approves

        return JsonResponse(response)
    else :
        user_name = request.POST.get('user_name')
        contract_name = request.POST.get('contract_name')
        content = request.POST.get('content')
        accept = int(request.POST.get('accept'))

        contract_id = Contract.objects.filter(name=contract_name).first().id

        user_id = User.objects.filter(name=user_name).first().id
        Approve.objects.filter(user_id=user_id, contract_id=contract_id).update(content=content, judge=accept)

        # if accepting, change the state to state = 3
        if accept == 1:
            # the behaviour is recorded in the log
            Log.objects.create(user_id=user_id, behaviour='审核了《%s》合同,并且同意了'%(contract_name))
            query_set = Approve.objects.filter(contract_id=contract_id)
            flag = True
            for row in query_set:
                if row.judge == 0:
                    flag = False
                    break
            if flag:
                Contract.objects.filter(id=contract_id).update(state=3)
                query_set_email = Sign.objects.filter(contract_id=contract_id)
                for row in query_set_email:
                    email = User.objects.filter(id=row.user_id).first().email
                    send('待签订', '《%s》合同等待您签签订', email)
        else :
            # the behaviour is recorded in the log
            Log.objects.create(user_id=user_id, behaviour='审核了《%s》合同,但是拒绝了'%(contract_name))
            # if one refuse, dinggao again
            Approve.objects.filter(contract_id=contract_id).update(judge=0)
            
            Contract.objects.filter(id=contract_id).update(state=1)
            email = User.objects.filter(id=Contract.objects.filter(name=contract_name).first().user_id).first().email
            send('重新定稿', '《%s》合同等待您重新定稿', email)

        return JsonResponse(response)

@csrf_exempt
def get_signs(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        # the user is responsible for the contracts
        query_set = Sign.objects.filter(user_id=user_id)
        signs = []
        for row in query_set:
            if row.content is None:
                contract = Contract.objects.filter(id=row.contract_id).first()
                if contract.state == 3:
                    signs.append(contract.name)
        response['signs'] = signs
        return JsonResponse(response)

@csrf_exempt
def sign(request):
    response = {**headers}
    types = int(request.POST.get('types'))
    if types == 0 :
        contract_name = request.POST.get('contract_name')

        customer = Contract.objects.filter(name=contract_name).first().customer_id
        
        customer_name = Customer.objects.filter(id=customer).first().name

        response['customer'] = customer_name

        return JsonResponse(response)
    else :
        user_name = request.POST.get('user_name')
        user_id = User.objects.filter(name=user_name).first().id
        content = request.POST.get('content')
        contract_name = request.POST.get('contract_name')
        contract_id = Contract.objects.filter(name=contract_name).first().id
        # the behaviour is recorded in the log
        Log.objects.create(user_id=user_id, behaviour='签订了《%s》合同'%(contract_name))
        Sign.objects.filter(user_id=user_id, contract_id=contract_id).update(content=content)
        
        query_set = Sign.objects.filter(contract_id=contract_id)
        # check all finished then the contract is finished
        flag = True
        for row in query_set:
            if row.content is None:
                flag = False
                break
        if flag :
            # if all of the signs sign, the state changed to 4
            Contract.objects.filter(id=contract_id).update(state=4)
        return JsonResponse(response)




        