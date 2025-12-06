from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from ..models.payout import Payout
import json


class PayoutAPITest(APITestCase):
    def setUp(self):
        self.payout_data = {
            'amount': '1000.50',
            'currency': 'RUB',
            'recipient_details': {
                'bank_name': 'Сбербанк',
                'account_number': '40817810099910004312',
                'recipient_name': 'Иванов Иван Иванович'
            },
            'description': 'Тестовая выплата'
        }

    @patch('payouts.api.views.PayoutService.process_payout_async')
    def test_create_payout_success(self, mock_process_payout):
        """Тест успешного создания заявки и вызова Celery задачи"""
        response = self.client.post(
            '/api/v1/payouts/',
            data=json.dumps(self.payout_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Payout.objects.count(), 1)

        payout = Payout.objects.first()
        self.assertEqual(str(payout.amount), '1000.50')
        self.assertEqual(payout.status, Payout.Status.PENDING)

        # Проверяем, что Celery задача была вызвана
        mock_process_payout.assert_called_once_with(str(payout.id))

    def test_create_payout_validation_error(self):
        """Тест валидации при создании заявки"""
        invalid_data = self.payout_data.copy()
        invalid_data['amount'] = '-100'  # Отрицательная сумма

        response = self.client.post(
            '/api/v1/payouts/',
            data=json.dumps(invalid_data),
            content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('amount', response.data)

    def test_get_payout_list(self):
        """Тест получения списка заявок"""
        # Создаем тестовую заявку
        Payout.objects.create(
            amount='500.00',
            currency='USD',
            recipient_details={
                'bank_name': 'Bank of America',
                'account_number': '123456789',
                'recipient_name': 'John Smith'
            }
        )

        response = self.client.get('/api/v1/payouts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)