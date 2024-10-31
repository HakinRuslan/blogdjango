from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Userbet(models.Model):
    User = models.OneToOneField(User, on_delete=models.CASCADE)
    iconuser = models.ImageField('Иконка профиля', upload_to='blog/static/profile/profileimg', blank=True, null=True)

    def __str__(self):
        return f'{self.User} {self.iconuser}'

class Blogpost(models.Model):
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField('Название Поста', max_length=150)
    desc = models.TextField('Содержимое поста')
    data = models.DateTimeField('Дата публикации', auto_now=True)

    def __str__(self):
        return f'Пост от {self.Author}, {self.title}, Опубликован в {self.data}'
    

class Images(models.Model):
    blog = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    image = models.ImageField('Картинка', upload_to='blog/static/blogapp/blogimg' , blank=True, null=True)

    def __str__(self):
        return f'{self.blog}, {self.image}'

class Comment_on_post(models.Model):
    Author = models.ForeignKey(User, on_delete=models.CASCADE)
    Blog = models.ForeignKey(Blogpost, on_delete=models.CASCADE)
    desc = models.TextField('Содержимое комента')
    data = models.DateTimeField('Дата публикации комента', auto_now=True)

    def __str__(self):
        return f'Комент от {self.Author}, оставлен на {self.Blog.title} Опубликован в {self.data}'
    
class LikeOnBlogpost(models.Model):
    blog = models.ForeignKey(Blogpost, on_delete=models.SET_NULL, null=True, verbose_name='Блог который лайкнули')
    userlike = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Тот кто лайкнул отзыв')
    like = models.BooleanField('like', default=False)

    def __str__(self) -> str:
        return f'{self.userlike}: {self.blog} {self.like}'
    
class LikeOnComment(models.Model):
    Comment = models.ForeignKey(Comment_on_post, on_delete=models.SET_NULL, null=True, verbose_name='Блог который лайкнули')
    userlike = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Тот кто лайкнул отзыв')
    like = models.BooleanField('like', default=False)

    def __str__(self) -> str:
        return f'{self.userlike}: {self.Comment} {self.like}'
    

class ReplyOnComm(models.Model):
    Author = models.ForeignKey(Userbet, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment_on_post, on_delete=models.CASCADE)
    desc = models.TextField('Содержимое комента')
    data = models.DateTimeField('Дата публикации комента', auto_now=True)

    def __str__(self):
        return f'Ответил {self.Author}, на коментарий {self.comment}, ответил в {self.data}'
    

class LikeOnReply(models.Model):
    reply = models.ForeignKey(ReplyOnComm, on_delete=models.SET_NULL, null=True, verbose_name='Блог который лайкнули')
    userlike = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Тот кто лайкнул отзыв')
    like = models.BooleanField('like', default=False)

    def __str__(self) -> str:
        return f'{self.userlike}: {self.reply} {self.like}'
    
