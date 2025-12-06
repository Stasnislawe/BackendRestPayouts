from celery import shared_task
from django.utils import timezone
from ..models.payout import Payout
import logging
import random
import time

logger = logging.getLogger(__name__)


class PayoutService:
    @staticmethod
    @shared_task(bind=True, max_retries=3)
    def process_payout_task(self, payout_id: str) -> None:
        try:
            payout = Payout.objects.get(id=payout_id)
            logger.info(f'Начата обработка выплаты {payout_id}')

            payout.status = Payout.Status.PROCESSING
            payout.save(update_fields=['status', 'updated_at'])

            # Имитация сложной обработки
            time.sleep(random.uniform(1, 5))

            # 85% успешных, 15% неудачных для демонстрации
            if random.random() < 0.85:
                payout.status = Payout.Status.COMPLETED
                payout.metadata['processed_at'] = timezone.now().isoformat()
            else:
                payout.status = Payout.Status.FAILED
                payout.metadata['error'] = 'Ошибка процессинга'
                payout.metadata['failed_at'] = timezone.now().isoformat()

            payout.save()
            logger.info(f'Завершена обработка выплаты {payout_id}')

        except Payout.DoesNotExist:
            logger.error(f'Выплата {payout_id} не найдена')
            raise
        except Exception as exc:
            logger.error(f'Ошибка обработки выплаты {payout_id}: {exc}')
            self.retry(exc=exc, countdown=60)

    @staticmethod
    def process_payout_async(payout_id: str) -> None:
        PayoutService.process_payout_task.delay(payout_id)