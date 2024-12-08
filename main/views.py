from django.contrib.auth import logout as auth_logout
from database.models import Modules
from .models import info_modules
from .forms import regForm, Serial_NumbersForm
from .forms import info_modulesForm
from .forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .models import proverka, poverka, kalibrovka, transportirovka, remont, Serial_Numbers
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
import datetime
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing

from django.shortcuts import render

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

# def generate_pdf(request):
#     # Создаем HTTP-ответ с типом content-type для PDF
#     response = HttpResponse(content_type='application/pdf')
#     response['Content-Disposition'] = 'inline; filename="label.pdf"'
#
#     # Создаем объект canvas для генерации PDF
#     p = canvas.Canvas(response, pagesize=letter)
#     # Устанавливаем начальные координаты для этикетки
#     start_x, start_y = 10, 750  # Верхний левый угол этикетки
#
#     # Добавляем первый QR-код
#     qr1 = QrCodeWidget("123456789")
#     qr1_bounds = qr1.getBounds()
#     qr1_width = qr1_bounds[2] - qr1_bounds[0]
#     qr1_height = qr1_bounds[3] - qr1_bounds[1]
#     qr1_drawing = Drawing(60, 60)  # Размер QR-кода
#     qr1_drawing.add(qr1)
#     qr1_drawing.drawOn(p, start_x, start_y - 60)
#
#     # Добавляем текстовые элементы
#     text_x = start_x + 70  # Координата X для текста
#     p.setFont("Helvetica", 10)
#
#     # Текст справа от первого QR-кода
#     p.drawString(text_x, start_y, "KAC")
#     p.drawString(text_x, start_y - 15, "eЦ6.641.733")
#
#     # Текст ниже
#     p.drawString(start_x, start_y - 100, "pev.4")
#     p.drawString(start_x + 50, start_y - 100, "№00001")
#     p.drawString(start_x + 120, start_y - 100, "35/24")
#
#     # S/N текст
#     p.drawString(start_x, start_y - 115, "S/N 01:02:010203:01:3524:00009")
#
#     # Завершаем создание PDF
#     p.showPage()
#     p.save()
#     return response

# Список записей
from reportlab.pdfgen import canvas
from io import BytesIO
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Serial_Numbers  # Предполагается, что у вас есть модель Record

def records_view(request):
    if request.method == "POST" and "delete_id" in request.POST:
        delete_id = request.POST.get("delete_id")
        record = get_object_or_404(Serial_Numbers, id=delete_id)
        record.delete()  # Удаление записи из базы данных
        messages.success(request, "Запись успешно удалена!")
        return redirect("records_view")

    records = Serial_Numbers.objects.all()  # Получение всех записей из базы данных
    return render(request, "main/history_of_registration.html", {"records": records})

def generate_pdf(request):
    if request.method == "POST":
        selected_ids = request.POST.getlist("scales[]")
        selected_records = Serial_Numbers.objects.filter(id__in=selected_ids)  # Фильтрация записей по ID

        # Генерация PDF
        buffer = BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, "Список выбранных изделий:")
        y = 750

        for record in selected_records:
            p.drawString(100, y, record.combined_field)
            y -= 20

        p.save()
        buffer.seek(0)

        response = HttpResponse(buffer, content_type="application/pdf")
        response["Content-Disposition"] = 'attachment; filename="selected_records.pdf"'
        return response

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
