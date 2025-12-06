import django.core.validators
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Payout",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Идентификатор",
                    ),
                ),
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        max_digits=15,
                        validators=[django.core.validators.MinValueValidator(0.01)],
                        verbose_name="Сумма выплаты",
                    ),
                ),
                (
                    "currency",
                    models.CharField(
                        default="RUB", max_length=3, verbose_name="Валюта"
                    ),
                ),
                (
                    "recipient_details",
                    models.JSONField(verbose_name="Реквизиты получателя"),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "В ожидании"),
                            ("processing", "В обработке"),
                            ("completed", "Выполнено"),
                            ("failed", "Ошибка"),
                            ("cancelled", "Отменено"),
                        ],
                        default="pending",
                        max_length=20,
                        verbose_name="Статус заявки",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "description",
                    models.TextField(blank=True, null=True, verbose_name="Описание"),
                ),
                (
                    "metadata",
                    models.JSONField(
                        blank=True, default=dict, verbose_name="Метаданные"
                    ),
                ),
            ],
            options={
                "verbose_name": "Заявка на выплату",
                "verbose_name_plural": "Заявки на выплату",
                "ordering": ["-created_at"],
            },
        ),
        migrations.AddIndex(
            model_name="payout",
            index=models.Index(
                fields=["status", "created_at"], name="payouts_pay_status_dd1f82_idx"
            ),
        ),
        migrations.AddIndex(
            model_name="payout",
            index=models.Index(
                fields=["created_at"], name="payouts_pay_created_b65d12_idx"
            ),
        ),
    ]
