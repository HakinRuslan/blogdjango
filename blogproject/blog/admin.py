from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Blogpost)
admin.site.register(Images)
admin.site.register(Comment_on_post)
admin.site.register(ReplyOnComm)
admin.site.register(LikeOnBlogpost)
admin.site.register(LikeOnComment)
admin.site.register(LikeOnReply)
admin.site.register(Userbet)