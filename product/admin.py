from django.contrib import admin
from product.models import Category, Menu, MenuItem, Choices, Options
from orders.models import OrderItem, Order, SelectedOption, SelectedChoice

# Register your models here.

admin.site.register(Category)
admin.site.register(Menu)
admin.site.register(MenuItem)
admin.site.register(Choices)
admin.site.register(Options)

admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(SelectedOption)
admin.site.register(SelectedChoice)