from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from contract.models import Contract, Customer, File, User, CounterSign, Approve, Sign, HaveAuthority, Authority
from django.http import HttpResponse
import json

headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'POST',
    'Access-Control-Allow-Headers': 'Content-Type'
}

from django.http import FileResponse

@csrf_exempt
def file_upload(request):
    print("hahha")
    response = {**headers}
    if request.method == 'POST':
    #if request.method == 'GET':

        # print(request.POST)
        # print(request.FILES)

        if "file" not in request.FILES:
            return HttpResponse("Empty file")
        file = request.FILES.get("file")
        
        file_name = file.name
        contract_name = request.POST.get('contract_name', 0)
        # chunks = request.POST.get('chunks', 0)
        print(contract_name)
        # print(file_name)
        # print(chunk)
        # print(chunks)

        f = open('H:/python/web/contract_files' + '/' + file_name, mode='ab')
        for chunk in file.chunks():
            f.write(chunk)
        f.close()

        # response = FileResponse(open('D:\\MyContract\\my_files\\1.zip', "rb"))
        # response['Content-Type'] = 'application/octet-stream'
        # response['Content-Disposition'] = "attachment;filename=music.zip"  # 注意filename不支持中文
        # return response




    # file_json = json.dumps(file_data)
    # f.close()
    # return JsonResponse(file_json, safe=False)
    return JsonResponse(response)
    
@csrf_exempt
def file_download(request):
    response = {**headers}
    if request.method == 'GET':
        contract_name = request.GET.get('contract_name')
        print(contract_name)
    # if request.method == 'GET':    
        # contract_name = request.POST.get('contract_name', 0)
        print("hahha")
        # print(contract_name)
        file_name = File.objects.filter(id=Contract.objects.filter(name=contract_name).first().file_id).first().fileName
        print(file_name)
        response = FileResponse(open('H:/python/web/contract_files/' + file_name, "rb"))
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = 'attachment;filename=' + file_name  # 注意filename不支持中文
        # response['url'] = 'D:\\MyContract\\my_files\\3.txt';#"attachment;filename=" + "3.txt" 
        return response