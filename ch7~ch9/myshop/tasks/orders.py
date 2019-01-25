from django.conf import settings
from celery import task
from django.core.mail import send_mail
from orders.models import Order


@task
def order_created(order_id):
    order = Order.objects.get(id=order_id)
    subject = 'Order {}'.format(order.id)
    message = '{} Order ID is {}'.format(order.first_name, order_id)

    mail_sent = send_mail(subject, message, settings.EMAIL_HOST_USER, [order.email])
    return mail_sent
