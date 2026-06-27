from django.db import models 
from django.contrib.auth.models import User

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

class Grade(models.Model):
    student_name = models.CharField(max_length=100, verbose_name="Имя студента")
    author_name = models.CharField(max_length=100, verbose_name="Автор оценки")
    total_score = models.IntegerField(default=1, verbose_name="Общая оценка (0-12)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    last_vote_date = models.DateField(null=True, blank=True, verbose_name="Последний голос (дата)")

    def __str__(self):
        return f"{self.student_name}: {self.total_score}/12"
    
    def like(self):
        if self.total_score < 12:
            self.total_score += 1
            self.save()
    
    def dislike(self):
        if self.total_score > 0:
            self.total_score -= 1
            self.save()

    class Meta:
        ordering = ['-total_score', '-created_at']
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"