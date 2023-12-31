# Generated by Django 4.1.7 on 2023-03-11 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_menuitem_menu_id'),
        ('orders', '0011_rename_item_orderitem_selectedoption'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='selectedoption',
            name='order_item',
        ),
        migrations.AddField(
            model_name='selectedoption',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='selected_options', to='orders.order'),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='order',
            name='item',
        ),
        migrations.AddField(
            model_name='order',
            name='item',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='item', to='product.menuitem'),
        ),
    ]
