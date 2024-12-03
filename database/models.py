# Тут описана модель для хранения полной информации о модулях
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from main.models import reg, Serial_Numbers, info_modules
import uuid
class Modules(models.Model):
    module_id = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        editable=False,
        verbose_name='Идентификатор изделия'
    )
    product_family = models.ForeignKey(
        'main.info_modules',
        on_delete=models.CASCADE,
        verbose_name='Семейство изделия',
        null=True,
        related_name='modules_product_family'
    )
    product_type = models.ForeignKey(
        'main.info_modules',
        on_delete=models.CASCADE,
        verbose_name='Тип продукта',
        null=True,
        related_name='modules_product_type'
    )
    revision = models.ForeignKey(
        'main.info_modules',
        on_delete=models.CASCADE,
        verbose_name='Ревизия',
        null=True,
        related_name='modules_revision'
    )
    serial_number = models.ForeignKey(
        'main.Serial_Numbers',
        on_delete=models.CASCADE,
        verbose_name='Серийный номер',
        null=True,
        related_name='modules_serial_number'
    )
    sequence_number = models.ForeignKey(
        'main.reg',
        on_delete=models.CASCADE,
        verbose_name='Номер изделия',
        null=True,
        related_name='modules_sequence_number'
    )
    manufacturer = models.ForeignKey(
        'main.info_modules',
        on_delete=models.CASCADE,
        verbose_name='Производитель',
        null=True,
        related_name='modules_manufacturer'
    )
    number_ec = models.ForeignKey(
        'main.reg',
        on_delete=models.CASCADE,
        verbose_name='Номер еЦ',
        null=True,
        related_name='modules_number_ec'
    )
    date_of_production = models.ForeignKey(
        'main.reg',
        on_delete=models.CASCADE,
        verbose_name='Дата производства',
        null=True,
        related_name='modules_date_of_production'
    )
    history_of_module = models.ForeignKey(
        'main.reg',
        on_delete=models.CASCADE,
        verbose_name='История изделия',
        null=True,
        related_name='modules_history_of_module'
    )

    # Методы отображения остаются такими же
    def __str__(self):
        return f"{self.module_id} - {self.history_of_module}"

