from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.views.generic import CreateView
from django.contrib.auth import get_user_model, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserPasswordChangeForm
from .models import Announcement, Comment
from django.http import HttpResponseForbidden

def get_current_role(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return 'Admin'
        if request.user.groups.filter(name='Moderator').exists():
            return 'Moderator'
        return 'User'
    return request.session.get('role', 'User')


def home_view(request):
    role = get_current_role(request)
    
    if not Announcement.objects.exists():
        Announcement.objects.create(
            title="Запуск группового репозитория c/pyddit",
            content="Приветствуем всех разработчиков! Этот портал спроектирован в стиле Reddit для координации работы над общим проектом. Вы можете переключаться между модулями в левом сайдбаре и тестировать функционал публикаций.",
            category="Important",
            author_name="Егор (Lead Dev)"
        )
        Announcement.objects.create(
            title="Код-ревью пул-реквестов по Django до пятницы",
            content="Напоминание для команды бэкенда: необходимо отправить все ветки на код-ревью в основную ветку main. Слияние (merge) без ревью заблокировано.",
            category="Academic",
            author_name="DevOps"
        )
        Announcement.objects.create(
            title="Предстоящий хакатон команды",
            content="В субботу в 12:00 собираемся для проведения спринта по интеграции всех модулей. Подготовьте ваши локальные БД и API-эндпоинты.",
            category="Event",
            author_name="Разработчик"
        )

    announcements = Announcement.objects.all()[:3]

    mock_forum_posts = [
        {"title": "Как настроить Docker для Django и PostgreSQL?", "author": "dev_ninja", "replies": 12, "votes": 25},
        {"title": "Оптимизация SQL-запросов (select_related vs prefetch_related)", "author": "django_guru", "replies": 5, "votes": 14},
        {"title": "Проблемы с CORS при интеграции фронтенда на React", "author": "frontend_dev", "replies": 8, "votes": 9},
    ]

    mock_grades = [
        {"student": "Developer A", "average": 11.2, "grades_count": 15},
        {"student": "Developer B", "average": 10.5, "grades_count": 12},
        {"student": "Developer C", "average": 9.8, "grades_count": 18},
    ]

    mock_events = [
        {"title": "Спринт по слиянию веток (Git Merge)", "date": "16.06.2026", "time": "14:00", "place": "Ауд. 305"},
        {"title": "Демонстрация рабочего прототипа", "date": "18.06.2026", "time": "11:00", "place": "Zoom"},
    ]

    mock_polls = [
        {"question": "Какую базу данных использовать для продакшена?", "votes": 42},
        {"question": "Согласование времени дейли-митинга", "votes": 31},
    ]

    mock_votings = [
        {"title": "Архитектурный выбор: SPA на React или Django Templates?", "status": "Активно"},
        {"title": "Выбор хостинга для развертывания проекта", "status": "Завершено"},
    ]

    mock_materials = [
        {"name": "Шпаргалка по оптимизации Django ORM.pdf", "type": "pdf", "size": "1.2 MB"},
        {"name": "Полезное руководство по паттернам проектирования", "type": "link", "url": "https://refactoring.guru"},
    ]

    mock_portfolio = [
        {"title": "clumsy - Утилита для симуляции сетевых задержек", "author": "Егор"},
        {"title": "Парсер расписания занятий на Python", "author": "Dev"},
    ]

    mock_gallery = [
        {"title": "Рабочий процесс в команде", "type": "photo", "url": "https://picsum.photos/id/1/300/200"},
        {"title": "Скриншот архитектурной схемы проекта", "type": "photo", "url": "https://picsum.photos/id/10/300/200"},
    ]

    context = {
        'role': role,
        'announcements': announcements,
        'forum_posts': mock_forum_posts,
        'grades': mock_grades,
        'events': mock_events,
        'polls': mock_polls,
        'votings': mock_votings,
        'materials': mock_materials,
        'portfolio': mock_portfolio,
        'gallery': mock_gallery,
    }
    return render(request, 'portal/home.html', context)


def set_role(request, role):
    if role in ['Admin', 'Moderator', 'User']:
        request.session['role'] = role
        messages.success(request, f"Роль изменена на: {role}")
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def ensure_moderator_group():
    group, _ = Group.objects.get_or_create(name='Moderator')
    return group

@user_passes_test(lambda u: u.is_superuser, login_url='login')
def manage_moderators(request):
    User = get_user_model()
    group = ensure_moderator_group()
    users = User.objects.all().order_by('username')

    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        action = request.POST.get('action')
        if user_id and action:
            target = get_object_or_404(User, pk=user_id)
            if action == 'grant':
                group.user_set.add(target)
                messages.success(request, f'Пользователь {target.username} получил роль модератора.')
            elif action == 'revoke':
                group.user_set.remove(target)
                messages.success(request, f'Роль модератора снята с пользователя {target.username}.')
            return redirect('manage_moderators')

    context = {
        'role': get_current_role(request),
        'users': users,
        'group': group,
    }
    return render(request, 'portal/role_management.html', context)


def announcements_list(request):
    role = get_current_role(request)
    announcements = Announcement.objects.all()
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        author_name = request.POST.get('author_name', f"Разработчик ({role})")

        if not title or not content:
            messages.error(request, "Заголовок и содержание не могут быть пустыми!")
        else:
            Announcement.objects.create(
                title=title,
                content=content,
                category=category,
                author_name=author_name
            )
            messages.success(request, "Объявление успешно создано!")
            return redirect('announcements_list')

    context = {
        'role': role,
        'announcements': announcements,
    }
    return render(request, 'portal/announcements_list.html', context)


def announcement_detail(request, pk):
    role = get_current_role(request)
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == "POST":
        author_name = request.POST.get('author_name', f"Пользователь ({role})")
        content = request.POST.get('content')
        
        if not content:
            messages.error(request, "Комментарий не может быть пустым!")
        else:
            Comment.objects.create(
                announcement=announcement,
                author_name=author_name,
                content=content
            )
            messages.success(request, "Комментарий добавлен!")
            return redirect('announcement_detail', pk=pk)

    comments = announcement.comments.all()
    context = {
        'role': role,
        'announcement': announcement,
        'comments': comments,
    }
    return render(request, 'portal/announcement_detail.html', context)


def announcement_edit(request, pk):
    role = get_current_role(request)
    announcement = get_object_or_404(Announcement, pk=pk)
    
    if request.method == "POST":
        title = request.POST.get('title')
        content = request.POST.get('content')
        category = request.POST.get('category')
        
        if not title or not content:
            messages.error(request, "Заголовок и содержание не могут быть пустыми!")
        else:
            announcement.title = title
            announcement.content = content
            announcement.category = category
            announcement.save()
            messages.success(request, "Объявление обновлено!")
            return redirect('announcements_list')
            
    context = {
        'role': role,
        'announcement': announcement,
    }
    return render(request, 'portal/announcement_edit.html', context)


def announcement_delete(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    announcement.delete()
    messages.success(request, "Объявление удалено!")
    return redirect('announcements_list')


def announcement_like(request, pk):
    announcement = get_object_or_404(Announcement, pk=pk)
    direction = request.GET.get('dir', 'up')
    
    if direction == 'up':
        announcement.likes += 1
    elif direction == 'down':
        announcement.likes -= 1
        
    announcement.save()
    return redirect(request.META.get('HTTP_REFERER', 'home'))


def mock_section(request, section_name):
    role = get_current_role(request)
    
    sections_info = {
        'forum': {
            'title': 'Форум разработчиков',
            'author': 'Разработчик',
            'task': 'Создать форум, ветки обсуждения, темы, список тем, отправку сообщений.',
            'instructions': 'Создать модели `Topic` и `Message` в приложении форума. Шаблоны разместить в папке `templates/forum/`.'
        },
        'auth': {
            'title': 'Аутентификация и права доступа',
            'author': 'Разработчик',
            'task': 'Страницы входа, регистрации, изменения профиля, смена почты и пароля, отображение ролей.',
            'instructions': 'Настроить работу со стандартной моделью User. Интегрировать сессии Django.'
        },
        'diary': {
            'title': 'Электронный трекер тасков (дневник)',
            'author': 'Разработчик',
            'task': 'Трекер оценок от 0 до 12, рейтинг участников, формы добавления оценок, редактирование и удаление.',
            'instructions': 'Создать модель `Grade` для оценок выполнения задач бэкенда и фронтенда.'
        },
        'events': {
            'title': 'События и календарь спринтов',
            'author': 'Разработчик',
            'task': 'Список событий, календарь, детальное описание события, создание и управление событиями.',
            'instructions': 'Создать модель `Event` с датой, временем, местом проведения и автором.'
        },
        'polls': {
            'title': 'Опросы по архитектуре',
            'author': 'Разработчик',
            'task': 'Многостраничные опросы, варианты ответов, сохранение последнего результата.',
            'instructions': 'Создать модели `Poll`, `Question` и `UserResponse`.'
        },
        'votings': {
            'title': 'Принятие решений (голосования)',
            'author': 'Разработчик',
            'task': 'Список голосований, выбор вариантов, отображение результатов для команды.',
            'instructions': 'Создать модель `Voting` и `Choice` с привязкой к голосам пользователей.'
        },
        'materials': {
            'title': 'Техническая документация (материалы)',
            'author': 'Разработчик',
            'task': 'Списки полезных файлов, ссылок, картинок, встроенный видеоплеер.',
            'instructions': 'Создать модель `Material` с FileField/URLField.'
        },
        'portfolio': {
            'title': 'Портфолио проектов',
            'author': 'Разработчик',
            'task': 'Отображение лучших проектов команды: название, описание, скриншот, файлы и ссылки.',
            'instructions': 'Создать модель `Project` и ограничить редактирование проектов только их авторами.'
        },
        'gallery': {
            'title': 'Фото и видео отчеты',
            'author': 'Разработчик',
            'task': 'Фото и видео отчеты разработчиков с обязательной премодерацией.',
            'instructions': 'Добавить поле `is_approved = models.BooleanField(default=False)` в модель галереи.'
        }
    }
    
    info = sections_info.get(section_name, {
        'title': 'Раздел портала',
        'author': 'Разработчик',
        'task': 'Разработка модуля портала.',
        'instructions': 'Сюда необходимо подключить модуль Django.'
    })
    
    context = {
        'role': role,
        'section_name': section_name,
        'info': info
    }
    return render(request, 'portal/mock_section.html', context)

@login_required(login_url='login')
def profile_view(request):
    context = {
        'role': get_current_role(request),
    }
    return render(request, 'portal/profile.html', context)

@login_required(login_url='login')
def profile_edit(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлен.')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    context = {
        'role': get_current_role(request),
        'form': form,
    }
    return render(request, 'portal/profile_edit.html', context)

@login_required(login_url='login')
def profile_password_change(request):
    if request.method == 'POST':
        form = UserPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Пароль успешно изменен.')
            return redirect('profile')
    else:
        form = UserPasswordChangeForm(request.user)

    context = {
        'role': get_current_role(request),
        'form': form,
    }
    return render(request, 'portal/password_change.html', context)

class UserRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'portal/register.html'
    success_url = reverse_lazy('login')

class UserLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'portal/login.html'
    redirect_authenticated_user = True


def logout_view(request):
    """Log out the user and redirect to home. Accepts GET and POST."""
    logout(request)
    return redirect('home')



#comment
