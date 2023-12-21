# Generated by Django 4.1.7 on 2023-03-11 23:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_remove_selectedoption_order_item_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectedoption',
            name='order',
        ),
        migrations.AddField(
            model_name='selectedoption',
            name='order_item',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='selected_options', to='orders.orderitem'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ManyToManyField(blank=True, null=True, related_name='order_items', to='orders.orderitem'),
        ),
    ]
