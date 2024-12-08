# Тут описана модель для хранения информации формы "Регистрация модуля"
from django.db import models

class reg(models.Model):
    ec_number = models.ForeignKey(
        'info_modules',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        related_name='regs',  # Опционально, если нужно обратное имя для связи
        verbose_name='Номер еЦ',
        to_field='info_ec_number',  # Ссылка на поле info_ec_number вместо id
        db_column='ec_number',  # Настройка названия столбца в базе данных
        default='еЦ_.___.___-__'
    )
    module_count = models.PositiveIntegerField(verbose_name='Количество изделий')
    production_date = models.DateField(verbose_name='Дата производства')
    history = models.TextField(max_length=10000, verbose_name='История изделия')
    number_of_module = models.PositiveIntegerField(verbose_name='Номер изделия')
    def str(self):
        return f"{self.ec_number} - {self.number_of_module}"  # Изменение в строковом представлении

class info_modules(models.Model):
    info_ec_number = models.CharField(max_length=100, verbose_name='Номер еЦ', unique=True, default='еЦ_.___.___-__')
    info_product_family = models.CharField(max_length=100, verbose_name='Семейство изделия')
    info_product_family_code = models.PositiveIntegerField(verbose_name='Код семейства изделия')
    info_revision = models.PositiveIntegerField(verbose_name='Ревизия')
    info_revision_code = models.PositiveIntegerField(verbose_name='Код ревизии')
    info_product_type = models.CharField(max_length=100, verbose_name='Тип изделия')
    info_product_type_code = models.PositiveIntegerField(verbose_name='Код типа изделия')
    info_manufacturer = models.CharField(max_length=100, verbose_name='Производитель')
    info_manufacturer_code = models.PositiveIntegerField(verbose_name='Код производителя')

    def str(self):
        return f"{self.info_ec_number} - {self.info_manufacturer_code}"

class Serial_Numbers(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)  # РАБОТАЮ С ЭТИМ
    combined_field = models.TextField(verbose_name='Объединенное поле', unique=True, blank=True)
    def str(self):
        return f"{self.combined_field}"


class proverka(models.Model):
    proverka_id = models.AutoField(primary_key=True)
    serial_number = models.ForeignKey(
        'Serial_Numbers',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        to_field='combined_field',  # Ссылка на поле info_ec_number вместо id
        db_column='serial_number',  # Настройка названия столбца в базе данных
        verbose_name='Серийный номер',
        null=True
    )
    proverka_otchet = models.CharField(max_length=1000000, verbose_name='Отчет')
    proverka_info = models.CharField(max_length=1000000, verbose_name='Информация')
    proverka_error = models.CharField(max_length=1000000, verbose_name='Возможная причина ошибки')
    def __str__(self):
        return f"{self.proverka_id} - {self.proverka_error}"  # Изменение в строковом представлении

class poverka(models.Model):
    poverka_id = models.AutoField(primary_key=True)
    serial_number = models.ForeignKey(
        'Serial_Numbers',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        to_field='combined_field',  # Ссылка на поле info_ec_number вместо id
        db_column='serial_number',  # Настройка названия столбца в базе данных
        verbose_name='Серийный номер',
        null=True
    )
    poverka_otchet = models.CharField(max_length=1000000, verbose_name='Отчет')
    poverka_info = models.CharField(max_length=1000000, verbose_name='Информация')
    poverka_error = models.CharField(max_length=1000000, verbose_name='Возможная причина ошибки')
    def __str__(self):
        return f"{self.poverka_id} - {self.poverka_error}"  # Изменение в строковом представлении

class kalibrovka(models.Model):
    kalibrovka_id = models.AutoField(primary_key=True)
    serial_number = models.ForeignKey(
        'Serial_Numbers',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        to_field='combined_field',  # Ссылка на поле info_ec_number вместо id
        db_column='serial_number',  # Настройка названия столбца в базе данных
        verbose_name='Серийный номер',
        null=True
    )
    kalibrovka_otchet = models.CharField(max_length=1000000, verbose_name='Отчет')
    kalibrovka_info = models.CharField(max_length=1000000, verbose_name='Информация')
    kalibrovka_error = models.CharField(max_length=1000000, verbose_name='Возможная причина ошибки')
    kalibrovka_koeff = models.CharField(max_length=1000000, verbose_name='Коэффициенты калибровки')
    def __str__(self):
        return f"{self.kalibrovka_id} - {self.kalibrovka_koeff}"  # Изменение в строковом представлении

class transportirovka(models.Model):
    transportirovka_id = models.AutoField(primary_key=True)
    serial_number = models.ForeignKey(
        'Serial_Numbers',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        to_field='combined_field',  # Ссылка на поле info_ec_number вместо id
        db_column='serial_number',  # Настройка названия столбца в базе данных
        verbose_name='Серийный номер',
        null=True
    )
    transportirovka_nakladnaya = models.CharField(max_length=1000000, verbose_name='Номер накладной')
    transportirovka_iz = models.CharField(max_length=1000000, verbose_name='Поступил из')
    transportirovka_v = models.CharField(max_length=1000000, verbose_name='Поступил в')
    transportirovka_date = models.DateField(verbose_name='Дата поступления')
    def __str__(self):
        return f"{self.transportirovka_id} - {self.transportirovka_date}"  # Изменение в строковом представлении

class remont(models.Model):
    remont_id = models.AutoField(primary_key=True)
    serial_number = models.ForeignKey(
        'Serial_Numbers',  # Ссылка на модель info_modules
        on_delete=models.CASCADE,  # Удаление связанных записей при удалении связанных объектов
        to_field='combined_field',  # Ссылка на поле info_ec_number вместо id
        db_column='serial_number',  # Настройка названия столбца в базе данных
        verbose_name='Серийный номер',
        null=True
    )
    remont_otchet = models.CharField(max_length=1000000, verbose_name='Отчет')
    remont_info = models.CharField(max_length=1000000, verbose_name='Информация')

    def __str__(self):
        return f"{self.remont_id} - {self.remont_info}"
