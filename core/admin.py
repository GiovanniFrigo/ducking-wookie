from django.contrib import admin
from core.models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email')
admin.site.register(User, UserAdmin)

class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date', 'place')
admin.site.register(Booking, BookingAdmin)

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Menu, MenuAdmin)

class CookAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
admin.site.register(Cook, CookAdmin)