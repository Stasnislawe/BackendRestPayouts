from decimal import Decimal
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payouts", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payout",
            name="amount",
            field=models.DecimalField(
                decimal_places=2,
                max_digits=15,
                validators=[django.core.validators.MinValueValidator(Decimal("0.01"))],
                verbose_name="Сумма выплаты",
            ),
        ),
    ]
