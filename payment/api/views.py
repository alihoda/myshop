import braintree
from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from orders.models import Order

gateway = braintree.BraintreeGateway(settings.BRAINTREE_CONF)


class PaymentViewSet(viewsets.ViewSet):
    """
    Endpoint for payment.
    """
    @action(methods=['GET', 'POST'], detail=False)
    def process(self):
        """
        Handle the payment process.
        """
        order_id = self.request.session['order_id']
        order = get_object_or_404(Order, id=order_id)
        total_cost = order.get_total_cost()

        if self.request.method == 'POST':
            nonce = self.request.POST.get('payment_method_nonce', None)
            result = gateway.transaction.sale({
                'amount': f'{total_cost:.2f}',
                'payment_method_nonce': nonce,
                'options': {
                    'submit_for_settlement': True
                }
            })
            if result.is_success:
                order.paid = True
                order.braintree_id = result.transaction.id
                order.save()
                return Response('Payment was successfully done.', status=status.HTTP_200_OK)
            else:
                return Response('Payment was unsuccessfull!', status=status.HTTP_400_BAD_REQUEST)

        else:
            client_token = gateway.client_token.generate()
            # TODO: send the client_token with api
