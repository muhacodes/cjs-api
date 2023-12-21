from django.db import models
from product.models import MenuItem, Options, Category, Choices
from account.models import User

# class OrderedMenuItem(models.Model):
#     item        = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
#     quantity    = models.SmallIntegerField(null=True, blank=True)



class OrderItem(models.Model):
    item        = models.ForeignKey(MenuItem, on_delete=models.CASCADE, null=True, blank=True)
    quantity    = models.SmallIntegerField(null=True, blank=True)
    # item        = models.ManyToManyField(OrderedMenuItem, related_name='order_item', blank=True, null=True)

    # def __str__(self):
    #     return f" {self.quantity}x {self.item.title} ({self.item.price} USD each)"



class SelectedChoice(models.Model):
    choice              = models.CharField(max_length=100)
    option              = models.CharField(max_length=100)
    price               = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    order_item          = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='order_item')


class Order(models.Model):
    # category    = models.ManyToManyField(Category, related_name='order_category', null=True, blank=True)
    item        = models.ManyToManyField(OrderItem, related_name='order_items', blank=True, null=True)
    user        = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)    
    # item        = models.ForeignKey(MenuItem, on_delete=models.CASCADE, related_name='item', blank=True, null=True)
    Name        = models.CharField(max_length=250, null=False, blank=False)
    email       = models.CharField(max_length=250, null=True, blank=True)
    address     = models.CharField(max_length=500, null=True, blank=True)
    total       = models.DecimalField(decimal_places=2, max_digits=10, null=True, blank=True)
    quantity    = models.SmallIntegerField(null=True, blank=True, default=1)

    # def __str__(self):
    #         return f"Order for {self.Name}"

    
class SelectedOption(models.Model):
    choice      = models.ForeignKey(Choices, on_delete=models.CASCADE)
    option      = models.ForeignKey(Options, on_delete=models.CASCADE)
    order_item  = models.ForeignKey(OrderItem, on_delete=models.CASCADE, related_name='selected_options')

    
