# Generated by Django 3.2.2 on 2021-05-21 08:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0004_answer_like_profile_question_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='body',
            field=models.CharField(max_length=256),
        ),
    ]