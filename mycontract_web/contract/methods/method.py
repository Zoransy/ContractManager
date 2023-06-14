from django.core.mail import send_mail
from contract.models import Customer, Contract, File

from_email = 'm13808437449@163.com'

def send(subject, content, list_send):
    send_mail(
        subject,
        content,
        from_email,
        [list_send]
    )

def check(contract_name):
    customer_id = Contract.objects.filter(name=contract_name).first().customer_id

    customer = Customer.objects.filter(id=customer_id).first().name

    start_time =  Contract.objects.filter(name=contract_name).first().start_time

    end_time = Contract.objects.filter(name=contract_name).first().end_time

    content = Contract.objects.filter(name=contract_name).first().content
    return customer, start_time, end_time, content