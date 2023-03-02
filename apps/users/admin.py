from django.contrib import admin

from ..cart.admin import CartItemInline
from ..users.models import CustomUser


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    readonly_fields = ['password']
    inlines = (CartItemInline,)
