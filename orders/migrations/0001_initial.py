# Generated by Django 4.1.7 on 2023-03-01 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('product', '0002_alter_choices_price'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=250)),
                ('email', models.CharField(blank=True, max_length=250, null=True)),
                ('address', models.CharField(blank=True, max_length=500, null=True)),
                ('quantity', models.SmallIntegerField(blank=True, default=1, null=True)),
                ('item', models.ManyToManyField(blank=True, null=True, related_name='item', to='product.menuitem')),
            ],
        ),
    ]