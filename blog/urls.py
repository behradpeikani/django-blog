from django.urls import path, re_path
from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.ArticlesList.as_view(), name='articles_list'),
    re_path(r'detail/(?P<slug>[-\w]+)/', views.ArticleDetail.as_view(), name='articles_detail'),
    path('add/', views.AddArticle.as_view(), name='add_article'),
    re_path(r'edit/(?P<slug>[-\w]+)/', views.EditArticle.as_view(), name='edit_article'),
    re_path(r'delete/(?P<slug>[-\w]+)/', views.DeleteArticle.as_view(), name='delete_article'),
    path('search/', views.SearchList.as_view(), name='search'),
    re_path(r'search/page/(?P<slug>[-\w]+)/', views.SearchList.as_view(), name='search-list'),
    re_path(r'tag/(?P<slug>[-\w]+)/', views.TagView.as_view(), name='tag_view'),
]
