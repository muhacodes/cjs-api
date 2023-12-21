from django.db import models

class Category(models.Model):
    id = models.AutoField(primary_key=True)
    imgUrl = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    categoryId = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    imgUrl = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class MenuItem(models.Model):
    # menu_id = models.CharField(max_length=50)
    menu_id         = models.ForeignKey(Menu, on_delete=models.CASCADE)
    title           = models.CharField(max_length=50)
    description     = models.CharField(max_length=200, null=True, blank=True)
    image_url       = models.URLField(max_length=200)
    price           = models.IntegerField()
    choices         = models.ManyToManyField('Choices', related_name='choices', null=True, blank=True)
    add_ons         = models.ManyToManyField('AddOn', related_name='addon', null=True, blank=True)
    featured        = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return f"{self.title} ({self.price})"


class Choices(models.Model):
	name 				= models.CharField(max_length=30)
	options				= models.ManyToManyField('Options', related_name='options')
	price 				= models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)

	def __str__(self):
		return self.name

class Options(models.Model):
    option = models.CharField(max_length=50)
    amount = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.option

class AddOn(models.Model):
    add_on = models.CharField(max_length=50)
    price = models.IntegerField(null=True, blank=True)