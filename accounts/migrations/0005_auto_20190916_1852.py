# Generated by Django 2.2.4 on 2019-09-16 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20190916_1851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='crack_level',
            field=models.IntegerField(choices=[(1, '基礎学習完了'), (2, '簡単なポートフォリオの作成'), (3, 'サービスを公開'), (4, '転職活動中・職探し真っ最中'), (5, 'すでにプログラマーとして活動中')], default=1),
        ),
    ]
