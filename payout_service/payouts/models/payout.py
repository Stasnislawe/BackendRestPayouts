from django.db import models
from django.core.validators import MinValueValidator
import uuid
from typing import TypedDict, Optional
from decimal import Decimal


class RecipientDetails(TypedDict):
    bank_name: str
    account_number: str
    swift_code: Optional[str]
    recipient_name: str


class Payout(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', 'В ожидании'
        PROCESSING = 'processing', 'В обработке'
        COMPLETED = 'completed', 'Выполнено'
        FAILED = 'failed', 'Ошибка'
        CANCELLED = 'cancelled', 'Отменено'

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name='Идентификатор'
    )

    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Сумма выплаты'
    )

    currency = models.CharField(
        max_length=3,
        default='RUB',
        verbose_name='Валюта'
    )

    recipient_details = models.JSONField(
        verbose_name='Реквизиты получателя'
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        verbose_name='Статус заявки'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    description = models.TextField(
        blank=True,
        null=True,
        verbose_name='Описание'
    )

    metadata = models.JSONField(
        default=dict,
        blank=True,
        verbose_name='Метаданные'
    )

    class Meta:
        verbose_name = 'Заявка на выплату'
        verbose_name_plural = 'Заявки на выплату'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'created_at']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self) -> str:
        return f'Payout {self.id} - {self.amount} {self.currency}'