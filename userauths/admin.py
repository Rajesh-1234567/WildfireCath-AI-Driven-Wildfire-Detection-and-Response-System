from django.contrib import admin
from userauths.models import User
from userauths.models import Profile


class UserAdmin(admin.ModelAdmin):
    list_display=['username','email','bio']
admin.site.register(User,UserAdmin)


class ProfileAdmin(admin.ModelAdmin):
    list_display=['user']
admin.site.register(Profile,ProfileAdmin)