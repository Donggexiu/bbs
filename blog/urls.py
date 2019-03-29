from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from blog import views

urlpatterns = [
    url(r'add_article/',views.AddArticleView.as_view(),name='add_article'),
    url(r'up_down/',views.up_down),
    url(r"comment/", views.comment),
    url(r"comment_tree/(\d+)/", views.comment_tree),
    url(r'(\w+)/(tag|category|archive)/(.+)/', views.HomeView.as_view()),  # home(request, username, tag, 'python')
    url(r'(\w+)/article/(\d+)$', views.ArticleDetailView.as_view()),
    url(r'(\w+)',views.HomeView.as_view()),#这个放在第一个,会匹配到所有的url
]