from rest_framework import serializers
from ..models.payout import Payout
from decimal import Decimal


class RecipientDetailsSerializer(serializers.Serializer):
    bank_name = serializers.CharField(max_length=255)
    account_number = serializers.CharField(max_length=50)
    swift_code = serializers.CharField(max_length=11, required=False, allow_null=True)
    recipient_name = serializers.CharField(max_length=255)

    def validate_account_number(self, value: str) -> str:
        if not value.isalnum():
            raise serializers.ValidationError("Номер счета должен содержать только буквы и цифры")
        return value


class PayoutSerializer(serializers.ModelSerializer):
    recipient_details = RecipientDetailsSerializer()

    class Meta:
        model = Payout
        fields = [
            'id', 'amount', 'currency', 'recipient_details',
            'status', 'created_at', 'updated_at', 'description'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']

    def validate_amount(self, value: Decimal) -> Decimal:
        if value <= 0:
            raise serializers.ValidationError("Сумма должна быть положительной")
        if value > Decimal('1000000000'):  # 1 миллиард
            raise serializers.ValidationError("Сумма слишком большая")
        return value

    def validate_currency(self, value: str) -> str:
        valid_currencies = ['RUB', 'USD', 'EUR', 'GBP']
        if value not in valid_currencies:
            raise serializers.ValidationError(
                f"Неверная валюта. Допустимые значения: {', '.join(valid_currencies)}"
            )
        return value.upper()

    def create(self, validated_data: dict):
        recipient_details = validated_data.pop('recipient_details')
        payout = Payout.objects.create(
            recipient_details=recipient_details,
            **validated_data
        )
        return payout