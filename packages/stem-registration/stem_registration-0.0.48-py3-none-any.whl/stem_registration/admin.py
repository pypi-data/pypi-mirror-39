
from django.contrib import admin

from stem_registration.models import RegistrationData


class RegistrationDataAdmin(admin.ModelAdmin):
    list_display = ['user', 'contractor_type', 'country', 'number', 'name_legal', ]
    search_fields = ['user__username', 'number', 'user__email']


admin.site.register(RegistrationData, RegistrationDataAdmin)
