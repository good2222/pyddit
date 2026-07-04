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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return self.title


class Question(models.Model):
    survey = models.ForeignKey(
        Survey, 
        on_delete=models.CASCADE, 
        related_name='questions', 
        verbose_name="Опрос"
    )
    text = models.CharField(max_length=200, verbose_name="Вопрос")

    def __str__(self):
        return self.text



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

    def __str__(self):
        return self.text


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

