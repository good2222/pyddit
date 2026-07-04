from django.conf import settings
from django.db import models

class Announcement(models.Model):
    CATEGORY_CHOICES = [
        ('Important', 'Важное'),
        ('General', 'Общее'),
        ('Event', 'Событие'),
        ('Academic', 'Учеба'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    content = models.TextField(verbose_name="Содержание")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='General', 
        verbose_name="Категория"
    )
    author_name = models.CharField(max_length=100, default="Администратор", verbose_name="Автор")
    likes = models.IntegerField(default=0, verbose_name="Рейтинг (лайки)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Объявление"
        verbose_name_plural = "Объявления"


class Comment(models.Model):
    announcement = models.ForeignKey(
        Announcement, 
        on_delete=models.CASCADE, 
        related_name='comments', 
        verbose_name="Объявление"
    )
    author_name = models.CharField(max_length=100, default="Пользователь", verbose_name="Автор")
    content = models.TextField(verbose_name="Текст комментария")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"Комментарий от {self.author_name} к '{self.announcement.title}'"

    class Meta:
        ordering = ['created_at']
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"

class Survey(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок")
    description = models.TextField(verbose_name="Описание")
    questions_per_page = models.PositiveIntegerField(default=1, verbose_name="Вопросов на страницу")
    is_active = models.BooleanField(default=True, verbose_name="Активно")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Опрос'
        verbose_name_plural = 'Опросы'


class Question(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='questions',
        verbose_name="Опрос"
    )
    text = models.CharField(max_length=200, verbose_name="Вопрос")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Choice(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='choices',
        verbose_name="Вопрос"
    )
    text = models.CharField(max_length=200, verbose_name="Вариант ответа")
    is_correct = models.BooleanField(default=False, verbose_name="Правильний")
    votes = models.IntegerField(default=0, verbose_name="Голоси")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")

    def __str__(self):
        return self.text

    class Meta:
        ordering = ['order', 'id']
        verbose_name = 'Вариант ответа'
        verbose_name_plural = 'Варианты ответов'


class SurveySubmission(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Опрос'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='survey_submissions',
        verbose_name='Пользователь'
    )
    completed_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата завершения')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        unique_together = [('survey', 'user')]
        ordering = ['-completed_at']
        verbose_name = 'Отправка опроса'
        verbose_name_plural = 'Отправки опросов'

    def __str__(self):
        return f'{self.user} -> {self.survey}'


class SurveyAnswer(models.Model):
    submission = models.ForeignKey(
        SurveySubmission,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Отправка'
    )
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Вопрос'
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='answers',
        verbose_name='Выбор'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата ответа')

    class Meta:
        verbose_name = 'Ответ пользователя'
        verbose_name_plural = 'Ответы пользователей'

    def __str__(self):
        return f'{self.question.text} -> {self.choice.text}'


class Response(models.Model):
    survey = models.ForeignKey(
        Survey,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name="Опрос"
    )
    choice = models.ForeignKey(
        Choice,
        on_delete=models.CASCADE,
        related_name='responses',
        verbose_name="Выбор"
    )
    user_identifier = models.CharField(max_length=100, default="anonymous", verbose_name="Пользователь")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата ответа")

    def __str__(self):
        return f"{self.user_identifier} - {self.choice.text}" 

