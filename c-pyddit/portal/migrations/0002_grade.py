from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Grade',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('student_name', models.CharField(max_length=100, verbose_name='Имя студента')),
                ('author_name', models.CharField(max_length=100, verbose_name='Автор оценки')),
                ('total_score', models.IntegerField(default=1, verbose_name='Общая оценка (0-12)')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
                'ordering': ['-total_score', '-created_at'],
            },
        ),
    ]
