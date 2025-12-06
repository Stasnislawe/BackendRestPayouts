from django.test import TestCase
from unittest.mock import patch
from ..models.payout import Payout
from ..services.payout_services import PayoutService


class PayoutTaskTest(TestCase):
    def setUp(self):
        self.payout = Payout.objects.create(
            amount='1000.00',
            currency='RUB',
            recipient_details={
                'bank_name': 'Тинькофф',
                'account_number': '5536911234567890',
                'recipient_name': 'Петров Петр Петрович'
            }
        )

    def test_process_payout_task_called_correctly(self):
        """Тест проверяет что задача вызывается с правильными аргументами"""
        from ..services.payout_services import PayoutService

        with patch.object(PayoutService.process_payout_task, 'delay') as mock_delay:
            # Вызываем асинхронную обработку
            PayoutService.process_payout_async(str(self.payout.id))

            # Проверяем что задача была вызвана с правильным ID
            mock_delay.assert_called_once_with(str(self.payout.id))

    @patch('payouts.services.payout_services.time.sleep')
    @patch('payouts.services.payout_services.random.random')
    def test_process_payout_task_success(self, mock_random, mock_sleep):
        """Тест успешной обработки выплаты"""
        # Настраиваем моки
        mock_random.return_value = 0.5  # Всегда успешный результат
        mock_sleep.return_value = None  # Не ждем

        # Вызываем задачу синхронно (без .delay)
        PayoutService.process_payout_task.apply(args=(str(self.payout.id),)).get()

        # Обновляем объект из БД
        self.payout.refresh_from_db()

        # Проверяем что статус изменился
        self.assertEqual(self.payout.status, Payout.Status.COMPLETED)  # ИСПРАВЛЕНО
        self.assertIn('processed_at', self.payout.metadata)

    @patch('payouts.services.payout_services.time.sleep')
    @patch('payouts.services.payout_services.random.random')
    def test_process_payout_task_failure(self, mock_random, mock_sleep):
        """Тест неудачной обработки выплаты"""
        # Настраиваем моки для неудачи
        mock_random.return_value = 0.9  # > 0.85 = неудача
        mock_sleep.return_value = None

        # Вызываем задачу
        PayoutService.process_payout_task.apply(args=(str(self.payout.id),)).get()

        self.payout.refresh_from_db()
        self.assertEqual(self.payout.status, Payout.Status.FAILED)  # ИСПРАВЛЕНО
        self.assertIn('error', self.payout.metadata)