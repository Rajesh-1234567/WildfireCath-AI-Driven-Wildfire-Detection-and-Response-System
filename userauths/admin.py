from django.contrib import admin
from userauths.models import User
from userauths.models import Profile

from import_export.admin import ImportExportModelAdmin

class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']
admin.site.register(User,UserAdmin)


class ProfileAdmin(ImportExportModelAdmin):
    list_display=['user']
admin.site.register(Profile,ProfileAdmin)