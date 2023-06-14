from django.core.mail import send_mail

from_email = 'm13808437449@163.com'

def send(subject, content, list_send):
    send_mail(
        subject,
        content,
        from_email,
        list_send
    )