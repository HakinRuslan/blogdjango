from django import template


from django.contrib.auth.models import User

from blog.models import Blogpost, LikeOnBlogpost, LikeOnComment, LikeOnReply

register = template.Library()


@register.simple_tag(takes_context = True)
def islike(context, blogid):
    request = context['request']
    try:
        bloglike = LikeOnBlogpost.objects.get(blog = blogid, userlike = request.user.id).like
    except:
        bloglike = False
    return bloglike

@register.simple_tag(takes_context = True)
def countLikes(context, blogid):
    request = context['request']
    return LikeOnBlogpost.objects.filter(blog = blogid, like = True).count()

@register.simple_tag(takes_context = True)
def postlikedid(context, blogid):
    request = context['request']
    return LikeOnBlogpost.objects.get(blog = blogid, userlike = request.user.id).id

@register.simple_tag(takes_context = True)
def commislike(context, commentid):
    request = context['request']
    try:
        commlike = LikeOnComment.objects.get(Comment = commentid, userlike = request.user.id).like
    except:
        commlike = False
    return commlike

@register.simple_tag(takes_context = True)
def countLikescomm(context, commentid):
    request = context['request']
    return LikeOnComment.objects.filter(Comment = commentid, like = True).count()


@register.simple_tag(takes_context = True)
def commlikedid(context, commentid):
    request = context['request']
    return LikeOnComment.objects.get(Comment = commentid, userlike = request.user.id).id


@register.simple_tag(takes_context = True)
def repislike(context, replyid):
    request = context['request']
    try:
        replike = LikeOnReply.objects.get(reply = replyid, userlike = request.user.id).like
    except:
        replike = False
    return replike

@register.simple_tag(takes_context = True)
def countLikesrep(context, replyid):
    request = context['request']
    return  LikeOnReply.objects.filter(reply = replyid, like = True).count()

@register.simple_tag(takes_context = True)
def replikedid(context, replyid):
    request = context['request']
    return LikeOnReply.objects.get(reply = replyid, userlike = request.user.id).id