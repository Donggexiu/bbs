# Generated by Django 2.1.5 on 2019-03-10 12:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20190224_1853'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='article_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Category'),
        ),
    ]