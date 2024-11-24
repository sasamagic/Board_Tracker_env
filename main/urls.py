
from django.urls import path, include #подключили новый метод
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('user', views.user, name='user'),
    path('modules', views.modules, name='modules'),
    path('status', views.status, name='status'),
    path('logout/', views.logout_view, name='logout'),
    path('registration', views.registration, name='registration'),
    path('new_info_modules', views.new_info_modules, name='new_info_modules'), # для регистрации несуществующего изделия
    path('history_of_registration', views.history_of_registration, name='history_of_registration'), # ИСТОРИЯ РЕГИСТРАЦИИ
]