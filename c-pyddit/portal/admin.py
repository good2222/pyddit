from django.contrib import admin
from .models import Announcement, Comment, Survey, Question, Choice, SurveySubmission, SurveyAnswer


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author_name', 'created_at')
    list_filter = ('category', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'announcement', 'created_at')
    list_filter = ('created_at', 'announcement')
    search_fields = ('author_name', 'content')
    readonly_fields = ('created_at',)


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 2
    fields = ('text', 'is_correct', 'votes')


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1
    fields = ('text',)
    inlines = [ChoiceInline]


@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'questions_per_page', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'survey')
    list_filter = ('survey',)
    search_fields = ('text',)
    inlines = [ChoiceInline]


@admin.register(Choice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ('text', 'question', 'is_correct', 'votes')
    list_filter = ('question__survey', 'is_correct')
    search_fields = ('text',)


@admin.register(SurveySubmission)
class SurveySubmissionAdmin(admin.ModelAdmin):
    list_display = ('survey', 'user', 'completed_at', 'updated_at')
    list_filter = ('survey', 'completed_at')
    search_fields = ('user__username', 'survey__title')
    readonly_fields = ('completed_at', 'updated_at')


@admin.register(SurveyAnswer)
class SurveyAnswerAdmin(admin.ModelAdmin):
    list_display = ('submission', 'question', 'choice', 'created_at')
    list_filter = ('submission__survey', 'question')
    search_fields = ('question__text', 'choice__text')
    readonly_fields = ('created_at',)
