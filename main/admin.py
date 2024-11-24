from django.contrib import admin

# Register your models here.

from .models import reg
admin.site.register(reg);

from .models import info_modules
admin.site.register(info_modules);

from .models import Serial_Numbers
admin.site.register(Serial_Numbers);

from .models import proverka
admin.site.register(proverka);

from .models import poverka
admin.site.register(poverka);

from .models import kalibrovka
admin.site.register(kalibrovka);

from .models import transportirovka
admin.site.register(transportirovka);

from .models import remont
admin.site.register(remont);