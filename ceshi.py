import os

from django.db.models import Count

if __name__ == '__main__':
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bbs.settings")
    import django
    django.setup()
    from blog.models import Article, User, Category, Tag

    # a1 =Article.objects.first().comment_set.all()
    # print(a1)
    user =User.objects.filter(username='dxd').first()
    blog = user.blog
    # ret = Category.objects.filter(blog=blog)#dxdblog下所有的文章分类
    # res =ret[0].article_set.all()#该分类下所有的文章
    # res = ret.annotate(a = Count('article'))
    # ret = Category.objects.filter(blog=blog).annotate(c = Count('article')).values('title','c')
    # tag_list = Tag.objects.filter(blog=blog).annotate(c=Count('article')).values('tag_name', 'c')
    # #归档的一个list
    # time_list = Article.objects.filter(user=user).extra(select={'archive_ym':'date_format(create_time,"%%Y-%%m")'}).values('archive_ym').annotate(c = Count('id')).values('archive_ym','c')
    # print(time_list)
    #
