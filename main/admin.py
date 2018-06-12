from django.contrib import admin

# Register your models here.
from main.models import alarm, address


class AlarmAdmin(admin.ModelAdmin):
    list_display = ('alarm_id', 'first_type', 'second_type', 'third_type', 'fourth_type', 'content', 'date_time')


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_id', 'name', 'fitst_type', 'second_type', 'url', 'location', 'contact')


admin.site.register(alarm.Alarm, AlarmAdmin)
admin.site.register(address.Address, AddressAdmin)
