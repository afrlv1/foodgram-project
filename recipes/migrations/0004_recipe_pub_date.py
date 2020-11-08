# Generated by Django 3.1.1 on 2020-09-04 11:10

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("recipes", "0003_auto_20200904_1046"),
    ]

    operations = [
        migrations.AddField(
            model_name="recipe",
            name="pub_date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=django.utils.timezone.now,
                verbose_name="Дата публикации",
            ),
            preserve_default=False,
        ),
    ]
