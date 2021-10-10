from django.utils.translation import override
from rest_framework import serializers


PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 21)]


class CartSerializer(serializers.Serializer):
    quantity = serializers.ChoiceField(choices=PRODUCT_QUANTITY_CHOICES)
    override_quantity = serializers.BooleanField(required=False, initial=False)

    def get_quantity(self, obj):
        return int(obj.get_quantity_display())
