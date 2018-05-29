from django.contrib import admin

# Register your models here.
from main.models import alarm

class AlarmAdmin(admin.ModelAdmin):
    list_display = ('alarm_id','first_type','second_type','third_type','fourth_type','content', 'date_time')

admin.site.register(alarm.alarm, AlarmAdmin)