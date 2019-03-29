from django.db.models import Count
from django.urls import reverse
from blog.reg_forms import RegForm
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.views import View
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired
from django.contrib.auth import authenticate, login, logout
from blog.models import User, Article, Category, Tag, ArticleUpDown, Comment, ArticleDetail
from bbs import settings
from utls.common import send_active_mail
import logging
## 生成一个logger实例，专门用来记录日志
logger = logging.getLogger(__name__)

# Create your views here.
class RegisterView(View):
    def get(self, request):
        '''显示注册页'''
        form_obj = RegForm()
        return render(request, 'register.html', {"form_obj": form_obj})

    def post(self, request):
        form_obj = RegForm(request.POST)
        if form_obj.is_valid():
            form_obj.cleaned_data.pop('re_password')
            photo_img = request.FILES.get('photo')
            user = User.objects.create_user(**form_obj.cleaned_data, photo=photo_img)
            User.objects.filter(id=user.id).update(is_active=False)
            token = user.generate_active_token()
            send_active_mail(username=form_obj.cleaned_data.get('username'),
                             receiver=form_obj.cleaned_data.get('email'), token=token)
            return render(request, 'login.html')
        else:
            return render(request, 'register.html', {'errmsg': form_obj.errors})


class ActiveView(View):
    def get(self, request, token):
        '''
        激活用户账号
        :param request:
        :param token:对字符串{'confirm':self.id}
        :return:
        '''
        try:
            # 要激活的用户id
            s = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
            info = s.loads(token)
            user_id = info['confirm']
        except SignatureExpired:
            return HttpResponse('激活链接已过期')
        User.objects.filter(id=user_id).update(is_active=True)
        return redirect('/login/')


class LoginView(View):
    '''登录函数'''

    def get(self, request):
        return render(request, 'login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')
        if not all([username, password]):
            return render(request, 'login.html', {'errmsg': '账号密码不能为空'})
        user = authenticate(username=username, password=password)
        if user is None:
            return render(request, 'login.html', {'errmsg': '账号或密码不正确'})
        if not user.is_active:
            return render(request, 'login.html', {'errmsg': '账号没激活,请先激活后在登录'})
        login(request, user)
        return redirect('/index/')


class IndexVie(View):
    '''首页视图函数'''

    def get(self, request):
        article_list = Article.objects.all()
        return render(request, 'index.html', {'article_list': article_list})


class LogoutVie(View):

    def get(self, request):
        # 由Django用户认证系统完成：会清理cookie
        # 和session,request参数中有user对象
        logout(request)
        return redirect('/index/')


class HomeView(View):
    '''个人博客'''

    def get(self, request, username,*args):
        '''
        :param request:
        :param username: 对应的用户跳转对应的个人首页
        :return:
            {'blog':blog,'article_list':article_list,'category_list':category_list}
            'blog'用户对应的博客
            'article_lis':通过用户得到用户对应的文章
            'category_list:根据blog得到文章的分类,反查询该类下文章的数目category.article_set.all().count()
        '''
        logger.debug("home视图获取到用户名:{}".format(username))
        # 去UserInfo表里把用户对象取出来
        user = User.objects.filter(username=username).first()
        if not user:
            logger.warning("又有人访问不存在页面了...")
            return HttpResponse("404")
        # 如果用户存在需要将TA写的所有文章找出来
        blog = user.blog
        if not args:
            logger.debug("args没有接收到参数，默认走的是用户的个人博客页面！")
            # 我的文章列表
            article_list = Article.objects.filter(user=user)
            # 我的文章分类及每个分类下文章数
            # 将我的文章按照我的分类分组，并统计出每个分类下面的文章数
            # category_list = models.Category.objects.filter(blog=blog)
            # category_list = models.Category.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
            # # [{'title': '技术', 'c': 2}, {'title': '生活', 'c': 1}, {'title': 'LOL', 'c': 1}]
            # # 统计当前站点下有哪一些标签，并且按标签统计出文章数
            # tag_list = models.Tag.objects.filter(blog=blog).annotate(c=Count("article")).values("title", "c")
            #
            # # 按日期归档
            # archive_list = models.Article.objects.filter(user=user).extra(
            #     select={"archive_ym": "date_format(create_time,'%%Y-%%m')"}
            # ).values("archive_ym").annotate(c=Count("nid")).values("archive_ym", "c")
        else:
            logger.debug(args)
            logger.debug("------------------------------")
            # 表示按照文章的分类或tag或日期归档来查询
            # args = ("category", "技术")
            # article_list = models.Article.objects.filter(user=user).filter(category__title="技术")
            if args[0] == "category":
                article_list = Article.objects.filter(user=user).filter(article_category__title=args[1])
            elif args[0] == "tag":
                article_list = Article.objects.filter(user=user).filter(tags__tag_name=args[1])
            else:
                # 按照日期归档
                try:
                    year, month = args[1].split("-")
                    print(year,month)
                    logger.debug("分割得到参数year:{}, month:{}".format(year, month))
                    # logger_s10.info("得到年和月的参数啦！！！！")
                    logger.debug("************************")
                    article_list = Article.objects.filter(user=user).filter(create_time__month=month)

                except Exception as e:
                    logger.warning("请求访问的日期归档格式不正确！！！")
                    logger.warning((str(e)))
                    return HttpResponse("404")
        return render(request, "home.html", {
            "username": username,
            "blog": blog,
            "article_list": article_list,
        })


class ArticleDetailView(View):
    '''文章详情'''

    def get(self, request, username, pk):
        '''

        :param request:
        :param pk: 访问文章的主键id
        :return:
        '''
        user = User.objects.filter(username=username).first()
        if not user:
            data = {'errmsg': '该用户不存在,请核对后再试', 'code': 0}
            return HttpResponse(data)
        article_obj = Article.objects.filter(pk=pk).first()
        comment_list = Comment.objects.filter(article_id=pk)
        blog = user.blog
        return render(request, 'article_detail.html', {"username": username, "article": article_obj, "blog": blog,'comment_list':comment_list})

from django.db.models import F
import json
def up_down(request):
    print(request.POST)
    #获取文章对应id
    article_id=request.POST.get('article_id')
    #获取是点赞还是踩
    is_up=json.loads(request.POST.get('is_up'))
    user=request.user
    response={"state":True}
    print("is_up",is_up)
    try:
        #
        ArticleUpDown.objects.create(user=user,article_id=article_id,is_up=is_up)
        Article.objects.filter(pk=article_id).update(up_count=F("up_count")+1)

    except Exception as e:
        response["state"]=False
        response["fisrt_action"]=ArticleUpDown.objects.filter(user=user,article_id=article_id).first().is_up

    return JsonResponse(response)

def comment(request):

    print(request.POST)

    pid=request.POST.get("pid")
    article_id=request.POST.get("article_id")
    content=request.POST.get("content")
    user_pk=request.user.pk
    response={}
    if not pid:  #根评论
        comment_obj=Comment.objects.create(article_id=article_id,user_id=user_pk,contenrt=content)
    else:
        comment_obj=Comment.objects.create(article_id=article_id,user_id=user_pk,contenrt=content,parent_comment_id=pid)



    response["create_time"]=comment_obj.create_time.strftime("%Y-%m-%d")
    response["content"]=comment_obj.contenrt
    response["username"]=comment_obj.user.username

    return JsonResponse(response)




def comment_tree(request,article_id):

    ret=list(Comment.objects.filter(article_id=article_id).values("pk","contenrt","parent_comment_id"))
    print(ret)
    return JsonResponse(ret,safe=False)



class AddArticleView(View):

    def get(self,request):
        return render(request,'add_article.html')


    def post(self,request):
        title = request.POST.get('title')
        article_content = request.POST.get('article_content')
        user = request.user
        from bs4 import BeautifulSoup
        bs = BeautifulSoup(article_content,'html.parser')
        desc = bs.text[0:150] + "..."
        #过滤非法字符
        for tag in bs.find_all():

            print(tag.name)

            if tag.name in ["script", "link"]:
                tag.decompose()

        article_obj = Article.objects.create(user=user,article_title=title,article_desc=desc,article_category='')
        ArticleDetail.objects.create(content=str(bs),article=article_obj)
        return HttpResponse('添加成功')
from bbs import settings
import os,json
def upload(request):
    print(request.FILES)
    obj  = request.FILES.get('upload_img')
    path = os.path.join(settings.MEDIA_ROOT,'add_article_img',obj.name)
    with open(path,'wb') as f:
        for line in obj:
            f.write(line)

    res = {
        "code":0,
        "url":"/media/add_article_img/"+obj.name
    }
    return HttpResponse(json.dumps(res))



