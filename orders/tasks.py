from celery import shared_task
from django.core.mail import send_mail

from orders.models import Order


@shared_task
def order_created(order_id):
    """
    A task to send e-mail notification when a order
    is created successfully.
    """
    order = Order.objects.get(id=order_id)
    subject = f'Order {order.id} created'
    message = f'Dear {order.first_name}, \n\n' \
        f'You have successfully placed an order.' \
        f'Your order ID is {order.id}'
    mail_sent = send_mail(subject, message, 'admin@mail.com', [order.email])
    return mail_sent
