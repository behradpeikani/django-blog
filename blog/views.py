from django.shortcuts import redirect, render, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from django.views.generic.detail import SingleObjectMixin
from .models import Article, Tag
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.text import slugify
from django.db.models import Q
from django.core.paginator import Paginator


# Create your views here.

class ArticlesList(ListView):
    template_name = 'blog/articles_list.html'
    queryset = Article.objects.published()
    context_object_name = 'articles_list'
    paginate_by = 9


class ArticleDetail(DetailView):
    template_name = 'blog/articles_detail.html'
    model = Article
    context_object_name = 'article'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


class AddArticle(LoginRequiredMixin, CreateView):
    model = Article
    fields = ('title', 'image', 'content', 'tag')
    template_name = 'blog/add_article.html'
    success_url = reverse_lazy('blog:articles_list')

    def form_valid(self, form):
        article = form.save(commit=False)
        form.instance.author = self.request.user
        article.slug = slugify(form.cleaned_data['title'])
        article.save()
        messages.success(self.request, 'مقاله شما با موفقیت ثبت شد.', 'success')
        return super().form_valid(form)


class EditArticle(LoginRequiredMixin, UpdateView):
    template_name = 'blog/edit_article.html'
    model = Article
    fields = ('title', 'content', 'tag')
    success_url = reverse_lazy('blog:articles_list')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class DeleteArticle(LoginRequiredMixin, DeleteView):
    template_name = 'blog/delete_article.html'
    model = Article
    success_url = reverse_lazy('blog:articles_list')

    def get_queryset(self):
        return self.model.objects.filter(author=self.request.user)


class SearchList(View):
    template_name = 'blog/search_list.html'

    def get(self, request, *args, **kwargs):
        search = self.request.GET.get('q')
        articles = Article.objects.published()
        result = articles.filter(Q(content__icontains=search) | Q(title__icontains=search))
        paginator = Paginator(result, 9)

        page_number = request.GET.get('page')
        result = paginator.get_page(page_number)

        return render(request, self.template_name, {"result": result, "search": search})


class TagView(ListView):
    template_name = 'blog/tag_view.html'
    model =Tag
    paginate_by = 9

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        slug = self.kwargs.get('slug')
        context["tag"] = get_object_or_404(Tag, slug=slug)
        return context
    
