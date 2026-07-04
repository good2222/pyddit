from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_grade'),
    ]

    operations = [
        migrations.AddField(
            model_name='grade',
            name='last_vote_date',
            field=models.DateField(blank=True, null=True, verbose_name='Последний голос (дата)'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='total_score',
            field=models.IntegerField(default=1, verbose_name='Общая оценка (0-12)'),
        ),
    ]
