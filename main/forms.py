from .models import reg, info_modules, Serial_Numbers, proverka, poverka, \
    kalibrovka, transportirovka, remont
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class Serial_NumbersForm(ModelForm):
    class Meta:
        model = Serial_Numbers
        fields = ["combined_field"]
        widgets = {
            "combined_field": forms.Textarea(attrs={
                'id': 'combined-field',  # ID для автозаполнения
                'required': 'required',
            }),
        }

class poverkaForm(ModelForm):
    class Meta:
        model = poverka
        fields = ["serial_number","poverka_id", "poverka_otchet", "poverka_info", "poverka_error"]
        widgets = {
            "serial_number": forms.Textarea(attrs={
                'id': 'serial-number',  # ID для автозаполнения
                'required': 'required',
            }),
            "poverka_id": forms.Textarea(attrs={
                'id': 'poverka-id',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_otchet": forms.Textarea(attrs={
                'id': 'proverka-otchet',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_info": forms.Textarea(attrs={
                'id': 'proverka-info',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_error": forms.Textarea(attrs={
                'id': 'proverka-error',  # ID для автозаполнения
                'required': 'required',
            }),
        }

class proverkaForm(ModelForm):
    class Meta:
        model = proverka
        fields = ["serial_number","proverka_id", "proverka_otchet", "proverka_info", "proverka_error"]
        widgets = {
            "serial_number": forms.Textarea(attrs={
                'id': 'serial-number',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_id": forms.Textarea(attrs={
                'id': 'proverka-id',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_otchet": forms.Textarea(attrs={
                'id': 'proverka-otchet',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_info": forms.Textarea(attrs={
                'id': 'proverka-info',  # ID для автозаполнения
                'required': 'required',
            }),
            "proverka_error": forms.Textarea(attrs={
                'id': 'proverka-error',  # ID для автозаполнения
                'required': 'required',
            }),
        }

class kalibrovkaForm(ModelForm):
    class Meta:
        model = kalibrovka
        fields = ["serial_number","kalibrovka_id", "kalibrovka_otchet", "kalibrovka_info", "kalibrovka_error","kalibrovka_koeff"]
        widgets = {
            "serial_number": forms.Textarea(attrs={
                'id': 'serial-number',  # ID для автозаполнения
                'required': 'required',
            }),
            "kalibrovka_id": forms.Textarea(attrs={
                'id': 'kalibrovka-id',  # ID для автозаполнения
                'required': 'required',
            }),
            "kalibrovka_otchet": forms.Textarea(attrs={
                'id': 'kalibrovka-otchet',  # ID для автозаполнения
                'required': 'required',
            }),
            "kalibrovka_info": forms.Textarea(attrs={
                'id': 'kalibrovka-info',  # ID для автозаполнения
                'required': 'required',
            }),
            "kalibrovka_error": forms.Textarea(attrs={
                'id': 'kalibrovka-error',  # ID для автозаполнения
                'required': 'required',
            }),
            "kalibrovka_koeff": forms.Textarea(attrs={
                'id': 'kalibrovka-koeff',  # ID для автозаполнения
                'required': 'required',
            }),
        }

class transportirovkaForm(ModelForm):
    class Meta:
        model = transportirovka
        fields = ["serial_number","transportirovka_id", "transportirovka_nakladnaya", "transportirovka_iz", "transportirovka_v","transportirovka_date"]
        widgets = {
            "serial_number": forms.Textarea(attrs={
                'id': 'serial-number',  # ID для автозаполнения
                'required': 'required',
            }),
            "transportirovka_id": forms.Textarea(attrs={
                'id': 'transportirovka-id',  # ID для автозаполнения
                'required': 'required',
            }),
            "transportirovka_nakladnaya": forms.Textarea(attrs={
                'id': 'transportirovka-nakladnaya',  # ID для автозаполнения
                'required': 'required',
            }),
            "transportirovka_iz": forms.Textarea(attrs={
                'id': 'transportirovka-iz',  # ID для автозаполнения
                'required': 'required',
            }),
            "transportirovka_v": forms.Textarea(attrs={
                'id': 'transportirovka-v',  # ID для автозаполнения
                'required': 'required',
            }),
            "transportirovka_date": forms.Textarea(attrs={
                'id': 'transportirovka-date',  # ID для автозаполнения
                'required': 'required',
            }),
        }

# форма для регистрации пользователя
class info_modulesForm(ModelForm):
    class Meta:
        model = info_modules
        fields = ["info_ec_number", "info_product_family", "info_product_family_code",
                  "info_revision", "info_revision_code", "info_product_type",
                  "info_product_type_code", "info_manufacturer", "info_manufacturer_code"]
        widgets = {
            "info_ec_number": forms.Textarea(attrs={
                'id': 'info-ec-number',  # ID для автозаполнения
                'required': 'required',
                'maxlength': '10000',
            }),
            "info_product_family": forms.Textarea(attrs={
                'id': 'info-product-family',
                'min': '1',
                'required': 'required',
            }),
            "info_product_family_code": forms.NumberInput(attrs={
                'id': 'info-product-family-code',
                'required': 'required',
            }),
            "info_revision": forms.NumberInput(attrs={
                'id': 'info-revision',
                'maxlength': '10000',
                'required': 'required',
            }),
            "info_revision_code": forms.NumberInput(attrs={
                'id': 'info-revision-code',  # ID для автозаполнения
                'required': 'required',
            }),
            "info_product_type": forms.Textarea(attrs={
                'id': 'info-product-type',
                'min': '1',
                'required': 'required',
            }),
            "info_product_type_code": forms.NumberInput(attrs={
                'id': 'info-product-type-code',
                'required': 'required',
            }),
            "info_manufacturer": forms.Textarea(attrs={
                'id': 'info-manufacturer',
                'required': 'required',
                'maxlength': '10000',
            }),
            "info_manufacturer_code": forms.NumberInput(attrs={
                'id': 'info-manufacturer-code',
                'min': '1',
                'required': 'required',
            }),
        }
class regForm(ModelForm):
    class Meta:
        model = reg
        fields = ["ec_number", "module_count", "production_date", "history", "number_of_module"]
        widgets = {
            "ec_number": forms.TextInput(attrs={
                'id': 'ec-number',  # ID для автозаполнения
                'required': 'required',
                'maxlength': '10000',
            }),
            "module_count": forms.NumberInput(attrs={
                'id': 'modules',
                'min': '1',
                'required': 'required',
            }),
            "production_date": forms.DateInput(attrs={
                'id': 'production-date',
                'required': 'required',
                'type': 'date',
            }),
            "history": forms.Textarea(attrs={
                'id': 'history',
                'maxlength': '10000',
            }),
            "number_of_module": forms.NumberInput(attrs={
                'id': 'number-of-module',
                'min': '1',
                'required': 'required',
            }),
        }

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    class Meta:
        model = User
        # fields = ['username', 'email', 'password1', 'password2']
        fields = ['username', 'password1', 'password2']

class remontForm(ModelForm):
    class Meta:
        model = remont
        fields = ["serial_number","remont_id", "remont_otchet", "remont_info"]
        widgets = {
            "serial_number": forms.Textarea(attrs={
                'id': 'serial-number',  # ID для автозаполнения
                'required': 'required',
            }),
            "remont_id": forms.Textarea(attrs={
                'id': 'remont-id',  # ID для автозаполнения
                'required': 'required',
            }),
            "remont_otchet": forms.Textarea(attrs={
                'id': 'remont-otchet',  # ID для автозаполнения
                'required': 'required',
            }),
            "remont_info": forms.Textarea(attrs={
                'id': 'remont-info',  # ID для автозаполнения
                'required': 'required',
            }),
        }

