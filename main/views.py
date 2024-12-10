from django.contrib.auth import logout as auth_logout
from database.models import Modules
from .models import info_modules
from .forms import regForm, Serial_NumbersForm, info_modulesForm,UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import proverka, poverka, kalibrovka, transportirovka, remont, Serial_Numbers
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import datetime, qrcode
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont
from io import BytesIO
from reportlab.lib.utils import ImageReader
from reportlab.lib.pagesizes import portrait
from math import ceil
from reportlab.lib.units import mm
def history_of_registration(request):
    if request.method == 'POST':
        record_id = request.POST.get('delete_id')
        if record_id:
            record = get_object_or_404(Serial_Numbers, id=record_id)
            record.delete()
            messages.success(request, 'Изделие успешно удалено из базы данных.')
            return redirect('history_of_registration')

    form = Serial_NumbersForm()
    records = Serial_Numbers.objects.all()
    context = {
        'form': form,
        'records': records,
    }
    return render(request, 'main/history_of_registration.html', context)

def new_info_modules (request):
    error = ''  # Инициализирует пустую строку для хранения сообщения об ошибке.
    if request.method == 'POST':    # Проверяет, был ли запрос методом POST (обычно используется для отправки формы)
        form = info_modulesForm(request.POST)    # Создает экземпляр формы regForm, передавая данные, полученные из POST-запроса.
        if form.is_valid():     # Проверяет, является ли форма валидной (все обязательные поля заполнены и данные корректны).
            form.save()     # Сохраняет данные формы в базу данных.
            messages.success(request, 'Изделие успешно занесено в базу данных.')
            return redirect('new_info_modules')   # Перенаправляет пользователя на страницу с именем 'status' после успешного сохранения.
        else:
            error = 'ахтунг ошибка'     # Устанавливает сообщение об ошибке.
    else:       # Если метод запроса не POST, выполняется этот блок.
        form = info_modulesForm()  # Создает пустую форму для GET-запросов (когда пользователь просто загружает страницу).

    context = {     # Начинает создание словаря context, который будет передан в шаблон.
        'form': form,       # Добавляет объект формы в словарь context.
        'error': error      # Добавляет сообщение об ошибке в словарь context.
    }
    return render(request,'main/new_info_modules.html',context)
def modules (request):
    error = ''  # Инициализирует пустую строку для хранения сообщения об ошибке.
    if request.method == 'POST':    # Проверяет, был ли запрос методом POST (обычно используется для отправки формы)
        form = regForm(request.POST)    # Создает экземпляр формы regForm, передавая данные, полученные из POST-запроса.
        if form.is_valid():     # Проверяет, является ли форма валидной (все обязательные поля заполнены и данные корректны).
            form.save()     # Сохраняет данные формы в базу данных.
            messages.success(request,'Изделие успешно занесено в базу данных.')
            return redirect('modules')   # Перенаправляет пользователя на страницу с именем 'status' после успешного сохранения.
        else:
            error = 'ахтунг ошибка'     # Устанавливает сообщение об ошибке.
    else:       # Если метод запроса не POST, выполняется этот блок.
        form = regForm()  # Создает пустую форму для GET-запросов (когда пользователь просто загружает страницу).

    context = {     # Начинает создание словаря context, который будет передан в шаблон.
        'form': form,       # Добавляет объект формы в словарь context.
        'error': error      # Добавляет сообщение об ошибке в словарь context.
    }
    return render(request,'main/modules.html',context) # Возвращает ответ с отрисованным шаблоном 'main/modules.html', используя созданный контекст.

# для регистрации несуществующего изделия

def index(request):
    return render(request,'main/index.html')

def logout_view(request):
    auth_logout(request)
    return redirect('home')

# Модель для формы регистрации пользователя
def registration (request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST) # Создается экземпляр формы UserRegisterForm, и в него передаются данные, полученные из request.POST
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username') # Извлекается имя пользователя (username) из очищенных данных формы
            return redirect('user')
    else:
        form = UserRegisterForm()
    return render(request, 'main/registration.html', {'form': form})

# Модель для формы входа в аккаунт пользователя
def user(request):
    if request.method == 'POST':
        username_or_email = request.POST['auth_login']
        password = request.POST['auth_pass']

        # Попробуйте аутентифицировать пользователя по имени пользователя
        user = authenticate(request, username=username_or_email, password=password)

        if user is None:
            # Попробуйте найти пользователя по email
            try:
                user = User.objects.get(email=username_or_email)
                if user.check_password(password):
                    login(request, user)
                    return redirect('home')  # Перенаправление на главную страницу
                else:
                    messages.error(request, "Неверный пароль")
            except User.DoesNotExist:
                messages.error(request, "")
        else:
            # Успешная аутентификация
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу

    return render(request, 'main/user.html')  # Отображение формы входа

def records_view(request):
    if request.method == "POST" and "delete_id" in request.POST:
        delete_id = request.POST.get("delete_id")
        record = get_object_or_404(Serial_Numbers, id=delete_id)
        record.delete()  # Удаление записи из базы данных
        messages.success(request, "Запись успешно удалена!")
        return redirect("records_view")

    records = Serial_Numbers.objects.all()  # Получение всех записей из базы данных
    return render(request, "main/history_of_registration.html", {"records": records})

def get_module_info(serial_number):
    """
    Возвращает информацию о модуле на основе серийного номера.
    """
    module_info = None
    production_date_formatted = None
    module_number = None
    product_type = None
    info_ec_number = None  # Добавляем переменную

    # Разбиваем серийный номер на части
    parts = serial_number.split(":")
    if len(parts) >= 6:
        try:
            manufacturer_code = int(parts[1])
            product_family_code = int(parts[2][:2])
            product_type_code = int(parts[2][2:])
            revision_code = int(parts[3])
            production_date = int(parts[4])  # Неделя + год (3524)
            module_number = int(parts[5])  # Номер изделия (00009)

            # Преобразование недели и года в формат "мм/гг"
            production_date_str = str(production_date)

            # Извлекаем неделю и год
            week = int(production_date_str[:2])  # Первые две цифры — это неделя
            year = 2000 + int(production_date_str[2:])  # Последние две цифры — это год

            # Находим первый день года
            first_day_of_year = datetime.date(year, 1, 1)

            # Считаем первый день недели, с учетом того, что неделя начинается с понедельника
            first_week_start = first_day_of_year - datetime.timedelta(days=first_day_of_year.weekday())

            # Находим дату начала недели
            production_date_as_date = first_week_start + datetime.timedelta(weeks=week - 1)

            # Форматируем в "мм/гг"
            production_date_formatted = production_date_as_date.strftime("%m/%y")

            # Получаем информацию о модуле из базы данных
            module_info = info_modules.objects.filter(
                info_manufacturer_code=manufacturer_code,
                info_product_family_code=product_family_code,
                info_product_type_code=product_type_code,
                info_revision_code=revision_code
            ).first()

            if module_info:
                product_type = module_info.info_product_type  # Извлекаем тип изделия
                info_ec_number = module_info.info_ec_number  # Извлекаем Номер еЦ

        except (ValueError, info_modules.DoesNotExist):
            module_info = None

    return {
        'module_info': module_info,
        'info_ec_number': info_ec_number,  # Добавляем Номер еЦ
        'production_date': production_date_formatted,
        'product_type': product_type,
        'revision_code': revision_code,
        'module_number': module_number,
    }


# Регистрация шрифта DejaVuSans
pdfmetrics.registerFont(TTFont('DejaVuSans', 'DejaVuSans.ttf'))

def generate_pdf(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("scales[]")
        selected_records = Serial_Numbers.objects.filter(id__in=selected_ids)  # Фильтрация записей по ID

        # Генерация данных для PDF
        label_height = 23 * mm  # Высота одной этикетки (включая отступы)
        qr_size = 10 * mm       # Размер QR-кода
        margin_left = 4 * mm    # Левый отступ
        column_gap = 5 * mm     # Расстояние между колонками
        margin_top = 35 * mm     # Верхний отступ

        # Рассчитываем количество строк и длину страницы
        num_labels = len(selected_records)  # Количество записей
        labels_per_row = 2  # Количество колонок
        num_rows = ceil(num_labels / labels_per_row)  # Считаем количество строк
        # page_height = (num_rows * label_height) + (2 * margin_top)  # Общая длина страницы
        page_height = max(num_rows * label_height, 100 * mm)
        page_width = 85 * mm  # Фиксированная ширина страницы (ширина бабины)

        buffer = BytesIO()
        p = canvas.Canvas(buffer, pagesize=portrait((page_width, page_height)))

        # Устанавливаем шрифт DejaVuSans
        p.setFont("DejaVuSans", 5)

        # Начальная позиция
        y = page_height - margin_top + 30 * mm
        line_spacing = 2 * mm
        x_offsets = [margin_left, margin_left + (page_width - 2 * margin_left - column_gap) / 2 + column_gap]

        column_index = 0  # Текущая колонка

        for record in selected_records:
            # Получаем данные о модуле
            module_data = get_module_info(record.combined_field)
            module_info = module_data['module_info']
            info_product_type = module_data['product_type'] if module_data['product_type'] else "Неизвестный тип"
            info_ec_number = module_data['info_ec_number'] if module_data['info_ec_number'] else "Неизвестный еЦ"
            production_date = module_data['production_date']
            revision_code = module_data['revision_code']
            module_number = module_data['module_number']

            # Создание QR-кода
            qr_data = [
                record.combined_field,  # Серийный номер
                info_product_type,  # Тип изделия
                info_ec_number,  # Номер еЦ
                production_date,  # Дата производства
                revision_code,  # Код ревизии
            ]
            qr_text = ",".join(map(str, qr_data))  # Преобразуем все значения в строку
            qr = qrcode.make(qr_text)

            # Конвертируем QR-код в формат, совместимый с reportlab
            qr_buffer = BytesIO()
            qr.save(qr_buffer, format="PNG")
            qr_buffer.seek(0)
            qr_image = ImageReader(qr_buffer)

            # Координаты текущей колонки
            x = x_offsets[column_index]

            # Отрисовка QR-кода
            p.drawImage(qr_image, x, y - qr_size, width=qr_size, height=qr_size)

            # Отрисовка текста
            text_x_offset = x + qr_size + 0.5 * mm  # Смещение для текста справа от QR
            p.drawString(text_x_offset, y - 2.5 * mm, info_product_type)
            p.drawString(text_x_offset, y - 3 * mm - line_spacing, info_ec_number)
            p.drawString(text_x_offset, y - 3.5 * mm - 2 * line_spacing, f"№{module_number}")
            p.drawString(x + 0.9 * mm, y - qr_size - 1 * mm, f"S/N {record.combined_field}")

            # Отрисовка revision_code и production_date
            rightmost_x = text_x_offset + 16 * mm
            p.drawString(rightmost_x, y - 2.3 * mm, f"rev.{revision_code}")
            p.drawString(rightmost_x, y - 2.3 * mm - line_spacing, production_date)

            # Переход к следующей колонке
            column_index += 1
            if column_index >= labels_per_row:  # Если колонки закончились, переходим на новую строку
                column_index = 0
                y -= label_height

        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="detailed_records_with_qr.pdf"'
        return response

def status(request):
    # Получаем серийный номер из GET-запроса
    serial_number = request.GET.get('serial_number')
    module_info = None
    tasks2 = []
    tasks3 = []
    tasks4 = []
    tasks5 = []
    tasks6 = []

    # Определяем переменные заранее, чтобы избежать ошибки
    production_date_formatted = None
    module_number = None

    if serial_number:  # Проверяем, если серийный номер введен
        # Разбиваем серийный номер на части
        parts = serial_number.split(":")
        if len(parts) >= 6:
            try:
                manufacturer_code = int(parts[1])
                product_family_code = int(parts[2][:2])
                product_type_code = int(parts[2][2:])
                revision_code = int(parts[3])
                production_date = int(parts[4])  # Неделя + год (3524)
                module_number = int(parts[5])  # Номер изделия (00009)

                # Преобразование недели и года в формат "месяц.год"
                year = 2000 + production_date % 100  # Последние две цифры - год
                week = production_date // 100  # Первые две цифры - неделя
                first_day_of_year = datetime.date(year, 1, 1)
                first_week_start = first_day_of_year + datetime.timedelta(days=-first_day_of_year.weekday())
                production_date_as_date = first_week_start + datetime.timedelta(weeks=week - 1)
                production_date_formatted = production_date_as_date.strftime("%m.%Y")  # Формат "месяц.год"

                module_info = info_modules.objects.filter(
                    info_manufacturer_code=manufacturer_code,
                    info_product_family_code=product_family_code,
                    info_product_type_code=product_type_code,
                    info_revision_code=revision_code
                ).first()
            except (ValueError, info_modules.DoesNotExist):
                module_info = None

        # Загружаем связанные данные для текущего серийного номера
        tasks2 = proverka.objects.filter(serial_number__combined_field=serial_number)
        tasks3 = poverka.objects.filter(serial_number__combined_field=serial_number)
        tasks4 = kalibrovka.objects.filter(serial_number__combined_field=serial_number)
        tasks5 = transportirovka.objects.filter(serial_number__combined_field=serial_number)
        tasks6 = remont.objects.filter(serial_number__combined_field=serial_number)

    # Передаем данные в шаблон
    return render(request, 'main/status.html', {
        'title': 'Статус модуля',
        'module_info': module_info,
        'tasks2': tasks2,
        'tasks3': tasks3,
        'tasks4': tasks4,
        'tasks5': tasks5,
        'tasks6': tasks6,
        'production_date': production_date_formatted,
        'module_number': module_number,
        'serial_number': serial_number,  # Чтобы передать введенный серийный номер в шаблон
    })
def delete_records(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("scales[]")
        if selected_ids:
            # Удаляем записи с выбранными ID
            Serial_Numbers.objects.filter(id__in=selected_ids).delete()
            messages.success(request, "Выбранные записи успешно удалены!")
        else:
            messages.error(request, "Не выбраны записи для удаления.")
        return redirect("records_view")
