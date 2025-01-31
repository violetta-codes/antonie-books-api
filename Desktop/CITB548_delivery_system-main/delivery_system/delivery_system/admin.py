from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Office, Package
from .forms import UserRegisterForm

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    add_form = UserRegisterForm
    model = CustomUser
    list_display = ['username', 'email']

@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ('name', 'location')
    search_fields = ('name', 'location')

@admin.register(Package)
class PackageAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'sender', 'receiver', 'weight', 'status', 'price')
    list_filter = ('delivery_type', 'status', 'created_at')
    search_fields = ('sender__username', 'receiver__username', 'delivery_address', 'office__name')
