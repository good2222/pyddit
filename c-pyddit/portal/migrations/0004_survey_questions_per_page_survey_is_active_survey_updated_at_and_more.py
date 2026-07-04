from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_choice_is_correct_choice_votes_response'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='survey',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Активно'),
        ),
        migrations.AddField(
            model_name='survey',
            name='questions_per_page',
            field=models.PositiveIntegerField(default=1, verbose_name='Вопросов на страницу'),
        ),
        migrations.AddField(
            model_name='survey',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Дата обновления'),
        ),
        migrations.AddField(
            model_name='choice',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.AddField(
            model_name='question',
            name='order',
            field=models.PositiveIntegerField(default=0, verbose_name='Порядок'),
        ),
        migrations.CreateModel(
            name='SurveySubmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('survey', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submissions', to='portal.survey', verbose_name='Опрос')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='survey_submissions', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Отправка опроса',
                'verbose_name_plural': 'Отправки опросов',
                'ordering': ['-completed_at'],
            },
        ),
        migrations.CreateModel(
            name='SurveyAnswer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')),
                ('choice', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='portal.choice', verbose_name='Выбор')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='portal.question', verbose_name='Вопрос')),
                ('submission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='answers', to='portal.surveysubmission', verbose_name='Отправка')),
            ],
            options={
                'verbose_name': 'Ответ пользователя',
                'verbose_name_plural': 'Ответы пользователей',
            },
        ),
        migrations.AlterUniqueTogether(
            name='surveysubmission',
            unique_together={('survey', 'user')},
        ),
    ]
