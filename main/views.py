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

                # Добавьте отладочные принты здесь
                print("Parts:", parts)
                print("Manufacturer code:", manufacturer_code)
                print("Product family code:", product_family_code)
                print("Product type code:", product_type_code)
                print("Revision code:", revision_code)
                print("Module info query:", info_modules.objects.filter(
                    info_manufacturer_code=manufacturer_code,
                    info_product_family_code=product_family_code,
                    info_product_type_code=product_type_code,
                    info_revision_code=revision_code
                ))

                # Ищем соответствие в таблице info_modules
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
                messages.error(request, "Пользователь не найден")
        else:
            # Успешная аутентификация
            login(request, user)
            return redirect('home')  # Перенаправление на главную страницу

    return render(request, 'main/user.html')  # Отображение формы входа

