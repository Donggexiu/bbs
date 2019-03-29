from django.db import models
from bbs import settings
# Create your models here.
from django.contrib.auth.models import AbstractUser
from utls.models import BaseModel
from itsdangerous import TimedJSONWebSignatureSerializer


class User(AbstractUser, BaseModel):
    '''
    用户信息表
    '''
    photo = models.FileField(upload_to='photo/', default='photo/default.jpg', verbose_name='头像')
    blog = models.OneToOneField(to="Blog", on_delete=models.CASCADE, null=True)

    class Meta:
        db_table = 'user'

    def generate_active_token(self):
        '''生成激活令牌'''
        serializer = TimedJSONWebSignatureSerializer(settings.SECRET_KEY, 3600)
        token = serializer.dumps({'confirm': self.id})
        return token.decode()

    def __str__(self):
        return self.username


class Blog(BaseModel):
    """
    博客信息
    """
    title = models.CharField(max_length=64)  # 个人博客标题
    site = models.CharField(max_length=32, unique=True)  # 个人博客后缀
    theme = models.CharField(max_length=32)  # 博客主题

    class Meta:
        db_table = 'blog'

    def __str__(self):
        return self.title


class Category(BaseModel):
    '''
    个人博客分类表
    '''
    title = models.CharField(max_length=32, verbose_name='博客分类标题')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)

    class Meta:
        db_table = 'blog_category'
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Tag(BaseModel):
    '''标签
    '''
    tag_name = models.CharField(max_length=32, verbose_name='标签名')
    blog = models.ForeignKey('Blog', on_delete=models.CASCADE)

    class Meta:
        db_table = 'tag'
        verbose_name = '标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class Article(BaseModel):
    '''文章'''
    article_title = models.CharField(max_length=50, verbose_name='文章标题')
    article_desc = models.CharField(max_length=400, verbose_name='文章描述')

    # 评论数
    comment_count = models.IntegerField(verbose_name='评论数', default=0)
    # 点赞数
    up_count = models.IntegerField(verbose_name="点赞数", default=0)
    # 踩数
    down_count = models.IntegerField(verbose_name="踩数", default=0)
    article_category = models.ForeignKey('Category', on_delete=models.CASCADE,null=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag',  # 中介模型
                                  through='Article2Tag',
                                  through_fields=("article", "tag"), )  # 注意顺序

    class Meta:
        db_table = 'article'
        verbose_name = '文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.article_title


class Article2Tag(BaseModel):
    '''文章和标签的多对多标关系表'''
    article = models.ForeignKey(to="Article", on_delete=models.CASCADE)
    tag = models.ForeignKey(to="Tag", on_delete=models.CASCADE)

    class Meta:
        unique_together = (("article", "tag"),)
        verbose_name = "文章-标签"
        verbose_name_plural = verbose_name
    def __str__(self):
        return "{}-{}".format(self.article.article_title, self.tag.tag_name)


class ArticleDetail(BaseModel):
    '''文章详情表'''
    content = models.TextField()
    article = models.OneToOneField(to='Article', on_delete=models.CASCADE)

    class Meta:
        db_table = 'article_detail'
        verbose_name = "文章详情"
        verbose_name_plural = verbose_name


class ArticleUpDown(BaseModel):
    '''点赞表'''

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    article = models.ForeignKey('Article', on_delete=models.CASCADE)
    is_up = models.BooleanField(default=True, verbose_name='是否点赞')

    class Meta:
        db_table = ''
        unique_together = (("article", "user"),)
        verbose_name = "文章点赞"
        verbose_name_plural = verbose_name


class Comment(BaseModel):
    '''评论表'''
    article = models.ForeignKey('Article',on_delete=models.CASCADE)
    user =models.ForeignKey('User',on_delete=models.CASCADE)
    contenrt= models.CharField(max_length=255)#评论内容
    parent_comment =models.ForeignKey('self',on_delete=models.CASCADE,null=True,blank=True)#在admin后台可以为空
    class Meta:
        db_table ='comment'
        verbose_name = '评论'
        verbose_name_plural=verbose_name
    def __str__(self):
        return self.contenrt
