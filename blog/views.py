from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import BlogPost


class BlogPostListView(ListView):
    """ Список записей"""
    model = BlogPost
    template_name = 'blog/blogpost_list.html'
    context_object_name = 'posts'

    def get_queryset(self):
        """Фильтруем только опубликованные статьи и сортируем по дате создания"""
        return BlogPost.objects.filter(is_published=True).order_by('-created_at')


class BlogPostDetailView(DetailView):
    """ Детальная страница"""
    model = BlogPost
    template_name = 'blog/blogpost_detail.html'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        """Увеличиваем счетчик просмотров при каждом открытии статьи"""
        obj = super().get_object(queryset)
        obj.views_count += 1
        obj.save()
        return obj


class BlogPostCreateView(CreateView):
    """ Создание записи"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']
    success_url = reverse_lazy('blog:post_list')


class BlogPostUpdateView(UpdateView):
    """ Редактирование записи"""
    model = BlogPost
    template_name = 'blog/blogpost_form.html'
    fields = ['title', 'content', 'preview', 'is_published']

    def get_success_url(self):
        """После редактирования перенаправляем на страницу статьи"""
        return reverse_lazy('blog:post_detail', kwargs={'pk': self.object.pk})


class BlogPostDeleteView(DeleteView):
    """ Удаление записи"""
    model = BlogPost
    template_name = 'blog/blogpost_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')