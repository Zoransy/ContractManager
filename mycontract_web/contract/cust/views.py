
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Customer

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

@csrf_exempt
def add_cust(request):
    types = int(request.POST.get('types'))
    if types == 1 :
        response = {**headers}

        cust_name = request.POST.get('name')

        cust_addr = request.POST.get('address')

        cust_telep = request.POST.get('telephone')

        cust_pcode = request.POST.get('postcode')

        cust_bank = request.POST.get('bank')

        cust_acnt = request.POST.get('account')

        query_row = Customer.objects.filter(name=cust_name).first()

        # if the customer exists, the person can't be insert
        if query_row != None:
            # wrong return state = -1
            response['state'] = -1
            return JsonResponse(response)
        
        Customer.objects.create(name=cust_name, 
                                address=cust_addr, 
                                telephone=cust_telep,
                                postcode=cust_pcode,
                                bank=cust_bank,
                                account=cust_acnt)
        response['state'] = 1
        return JsonResponse(response)
