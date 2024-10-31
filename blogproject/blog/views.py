from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, View, FormView, TemplateView, UpdateView, DeleteView
from .models import *
import datetime
from .forms import *
from django.shortcuts import get_object_or_404
from django.contrib.auth import  login, logout, authenticate
from django.urls import reverse_lazy
# Create your views here.

def creatingpost(request):
    if request.POST:
        print(request.POST)
        user_id = get_user(request).id
        user = User.objects.get(id=user_id)
        post = CreatePost(request.POST)
        if post.is_valid():
            postrelease = post.save(commit=False)
            postrelease.Author = user
            postrelease.save()
            for i in request.FILES.getlist('PREVIEW_PICTURE'):
                Images.objects.create(image = i, blog=postrelease)
        return redirect('mainpage')
    usercr = request.user
    timenow = datetime.datetime.now()
    formcr = CreatePost()
    data = {
        'formcr': formcr,
        'data': timenow,
        'Author': usercr
    }

    return render(request, 'blogmain/post/createpost.html', data)


def Main(request):
    timenow = datetime.datetime.now()
    replyform = ReplyForm()
    formcreate = CreatePost()
    CForm = CommentForm()
    blogpost = list(Blogpost.objects.all().order_by('-data')[:7])
    for i in blogpost:
        likes = LikeOnBlogpost.objects.filter(blog = i).count()
        if likes > 0:
            blogpost.remove(i)
            blogpost.insert(0, i)
    blog_data = []
    for i in blogpost:
        comms_data = []
        imgs = None
        if Images.objects.filter(blog = i).count() > 0:
            imgs = Images.objects.filter(blog = i)
        blog = Blogpost.objects.get(id = i.id)
        usericon = Userbet.objects.get(User = blog.Author)
        comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            replsdata = []
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
            }
            if likesc > 0:
                comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)

        blogpost_data = {
            'user': usericon,
            'blog': blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    title = 'Главная'
    data = {
        'data': timenow,
        'usericon': usericon,
        'replyform': replyform,
        'formcr': formcreate,
        'form': CForm,
        'blogs': blog_data,
        'title': title
    }
    return render(request, 'blogmain/main.html', data)
    
def Create_comment(request):
    if request.POST.get('blog'):
        blog = Blogpost.objects.get(id = int(request.POST['blog']))
        user_id = get_user(request).id
        user = User.objects.get(id=user_id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.Author = user
            comment.Blog = blog
            comment.save()
        return redirect(request.POST['red'])
    
    elif request.POST.get('comment'):
        comment = Comment_on_post.objects.get(id = int(request.POST['comment']))
        user_id = get_user(request).id
        user = User.objects.get(id=user_id)
        userbet = Userbet.objects.get(User = user)
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.Author = userbet
            reply.comment = comment
            reply.save()        
        return redirect(request.POST['red'])
    
class Register(FormView):
    form_class = registrationuser
    template_name = 'reglog/register.html'
    success_url = reverse_lazy("login")
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    

def loginin(request):
    if request.POST:
       usernamep = request.POST['username']
       passwordp = request.POST['password']
       userauth = authenticate(request, username=usernamep, password=passwordp)
       if userauth is not None:
           login(request, user=userauth)
           return redirect('mainpage')
    print(request.user)   
    return render(request, 'reglog/login.html')

def log_out(request):
    logout(request)
    return redirect('mainpage')

#class UpdatePost(UpdateView):
   # model = Blogpost, Images
    #template_name = 'blogmain/post/update.html'
    #form_class = CreatePost

   # def get(self, request, *args, **kwargs):
    #    post = Blogpost.objects.get(id = kwargs['pk'])
    #    imgs = None
    #    if Images.objects.filter(blog = post).count() > 0: 
    #        imgs = Images.objects.filter(blog = post)
    #    data = {
    #    'image': imgs
    #    }
    #    return render(request, 'blogmain/post/update.html' , data)
       
def Updatepost(request, pk):
    if request.POST:
        post = Blogpost.objects.get(id = request.POST["id"])
        post.data = datetime.datetime.now()
        post.title = request.POST["title"]
        post.desc = request.POST["desc"]
        post.save()
        print(request.FILES.getlist('image'))
        if request.FILES.getlist('image'):
            img = Images.objects.filter(blog = post)
            img.delete()
            for i in request.FILES.getlist('image'):
                print(i)
                Images.objects.create(image = i, blog = post)
        return redirect('mainpage')
        
    post = Blogpost.objects.get(id = pk)
    imgs = None
    if Images.objects.filter(blog = post).count() > 0:
        imgs = list(Images.objects.filter(blog = post.id))
    data = {
        'blog': post,
        'image': imgs
    }
    return render(request, 'blogmain/post/update.html', data)



class DeletePost(DeleteView):
    success_url = '/' 
    model = Blogpost
    template_name = 'blogmain/post/delete.html'


def showprofile(request, pk):
    timenow = datetime.datetime.now()
    replyform = ReplyForm()
    userid = pk
    user = User.objects.get(id=userid)
    userwithicon = Userbet.objects.get(User = user)
    print(userwithicon.iconuser)
    formcreate = CreatePost()
    CForm = CommentForm()
    blogpost = list(Blogpost.objects.filter(Author = user).order_by('-data')[:7])
    blog_data = []
    for a in blogpost:
        likes = LikeOnBlogpost.objects.filter(blog = a).count()
        if likes > 0:
            blogpost.remove(a)
            blogpost.insert(0, a)
    for i in blogpost:
        comms_data = []
        imgs = None
        if Images.objects.filter(blog = i).count() > 0:
            imgs = Images.objects.filter(blog = i)
        comms = Comment_on_post.objects.filter(Blog = i).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
                }
            if likesc > 0:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)

        blogpost_data = {
            'blog': i,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
            }
        blog_data.append(blogpost_data)

    title = 'Главная'
    data = {
            'data': timenow,
            'replyform': replyform,
            'formcr': formcreate,
            'user': userwithicon,
            'form': CForm,
            'blogs': blog_data,
            'title': title
    }
    return render(request, 'profile/profile.html', data)

def showlikecomm(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    user = User.objects.get(id=pk)
    usericon = Userbet.objects.get(User = user)
    blog_data = []
    likescomment = list(LikeOnComment.objects.filter(userlike = user))
    idblog = []
    for l in likescomment:
        if l.Comment.Blog.id not in idblog:
            idblog.append(l.Comment.Blog.id)
    for ids in idblog:
        blog = Blogpost.objects.get(id = ids)
        likes = LikeOnBlogpost.objects.filter(blog = blog).count()
        if likes > 0:
            idblog.remove(ids)
            idblog.insert(0, ids)
    for i in idblog:
        comms_data = []
        imgs = None
        blog = Blogpost.objects.get(id = i)
        useric = Userbet.objects.get(User = blog.Author)
        if Images.objects.filter(blog = blog).count() > 0:
            imgs = Images.objects.filter(blog = blog)
        comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
                }
            if likesc > 0:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)

        blogpost_data = {
            'user': useric,
            'blog': blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    data = {
            'usericon': usericon,
            'form': CForm,
            'replyform': replyform,
            'blogs': blog_data,
        }
    return render(request, 'blogmain/main.html', data)

def showlikerep(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    user = User.objects.get(id=pk)
    usericon = Userbet.objects.get(User = user)
    blog_data = []
    likesreply = list(LikeOnReply.objects.filter(userlike = user))
    idblog = []
    for l in likesreply:
        if l.reply.comment.Blog.id not in idblog:
            idblog.append(l.reply.comment.Blog.id)
    for ids in idblog:
        blog = Blogpost.objects.get(id = ids)
        useric = Userbet.objects.get(User = blog.Author)
        likes = LikeOnBlogpost.objects.filter(blog = blog).count()
        if likes > 0:
            idblog.remove(ids)
            idblog.insert(0, ids)
    for i in idblog:
        comms_data = []
        imgs = None
        blog = Blogpost.objects.get(id = i)
        if Images.objects.filter(blog = blog).count() > 0:
            imgs = Images.objects.filter(blog = blog)
        comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
                }
            if likesc > 0:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)

        blogpost_data = {
            'user': useric,
            'blog': blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    data = {
        'usericon': usericon,
        'form': CForm,
        'replyform': replyform,
        'blogs': blog_data,
        }
    return render(request, 'blogmain/main.html', data)

def showcomms(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    user = User.objects.get(id=pk)
    usericon = Userbet.objects.get(User = user)
    blog_data = []
    idblog = []
    commsbyuser = Comment_on_post.objects.filter(Author = user)
    for i in commsbyuser:
        if i.Blog.id not in idblog:
            idblog.append(i.Blog.id)
            print(idblog)
    for a in idblog:
        blog = Blogpost.objects.get(id = a)
        likes = LikeOnBlogpost.objects.filter(blog = blog).count()
        if likes > 0:
            idblog.remove(a)
            idblog.insert(0, a)
    for i in idblog:
        comms_data = []
        blog = Blogpost.objects.get(id = i)
        useric = Userbet.objects.get(User = blog.Author)
        imgs = None
        if Images.objects.filter(blog = i).count() > 0:
            imgs = Images.objects.filter(blog = i)
        comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
            }
            if a.Author.id == user.id:
                if likesc > 0:
                    comms_data.insert(0, data_comms)
                else:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)
        blogpost_data = {
            'user': useric,
            'blog': blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    data = {
            'usericon': usericon,
            'form': CForm,
            'replyform': replyform,
            'blogs': blog_data,
        }
    return render(request, 'blogmain/main.html', data)


def showlike(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    user = User.objects.get(id=pk)
    usericon = Userbet.objects.get(User = user)
    blog_data = []
    likesblogs = list(LikeOnBlogpost.objects.filter(userlike = user))
    for a in likesblogs:
        likes = LikeOnBlogpost.objects.filter(blog = a.blog).count()
        print(likes)
        if likes > 1:
            likesblogs.remove(a)
            likesblogs.insert(0, a)
    for i in likesblogs:
        comms_data = []
        useric = Userbet.objects.get(User = i.blog.Author)
        imgs = None
        if Images.objects.filter(blog = i.blog).count() > 0:
            imgs = Images.objects.filter(blog = i.blog)
        comms = Comment_on_post.objects.filter(Blog = i.blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if likesr > 0:
                    replys.remove(r)
                    replys.insert(0, r)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
                }
            if likesc > 0:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)

        blogpost_data = {
            'user': useric,
            'blog': i.blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    data = {
            'usericon': usericon,
            'form': CForm,
            'replyform': replyform,
            'blogs': blog_data,
        }
    return render(request, 'blogmain/main.html', data)
        
def showreply(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    user = User.objects.get(id=pk)
    userbet = Userbet.objects.get(User = user)
    usericon = Userbet.objects.get(User = user)
    blog_data = []
    idblog = []
    reppsbyuser = ReplyOnComm.objects.filter(Author = userbet)
    for i in reppsbyuser:
        if i.comment.Blog.id not in idblog:
            idblog.append(i.comment.Blog.id)
            print(idblog)
    for a in idblog:
        blog = Blogpost.objects.get(id = a)
        likes = LikeOnBlogpost.objects.filter(blog = blog).count()
        if likes > 0:
            idblog.remove(a)
            idblog.insert(0, a)
    for i in idblog:
        comms_data = []
        blog = Blogpost.objects.get(id = i)
        useric = Userbet.objects.get(User = blog.Author)
        imgs = None
        if Images.objects.filter(blog = i).count() > 0:
            imgs = Images.objects.filter(blog = i)
        comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
        for a in comms:
            likesc = LikeOnComment.objects.filter(Comment = a).count()
            replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
            autcomm = Userbet.objects.get(User = a.Author)
            for r in replys:
                likesr = LikeOnReply.objects.filter(reply = r).count()
                if r.Author.id == user.id:
                    if likesr > 0:
                        replys.remove(r)
                        replys.insert(0, r)
                    else:
                        replys.remove(r)
                        replys.insert(1, r)
            print(replys)
            data_comms = {
                'user': autcomm,
                'comm': a, 
                'reply': replys[:1],
                'countrep': len(replys),
                'morereps': replys[1:],
                'havemorereps': len(replys) > 1
            }
            if likesc > 0:
                    comms_data.insert(0, data_comms)
            else:
                comms_data.append(data_comms)
        blogpost_data = {
            'user': useric,
            'blog': blog,
            'imgs': imgs,
            'comms': comms_data[:1],
            'countcomms': len(comms_data),
            'morecomms': comms_data[1:],
            'havemorecomms': len(comms_data) > 1
        }
        blog_data.append(blogpost_data)
    data = {
            'usericon': usericon,
            'form': CForm,
            'replyform': replyform,
            'blogs': blog_data,
        }
    return render(request, 'blogmain/main.html', data)

def addlike(request):
    if request.POST.get('blogids'):
        userid = request.user.id
        user = User.objects.get(id=userid)
        blogids = int(request.POST.get('blogids'))
        blog = Blogpost.objects.get(id = blogids)
        try:
            like = LikeOnBlogpost.objects.get(blog = blog, userlike = user)
        except:
            like = LikeOnBlogpost(blog = blog, like = True, userlike = user)
            like.save()
    elif request.POST.get('commentid'):
        userid = request.user.id
        user = User.objects.get(id=userid)
        commids = int(request.POST.get('commentid'))
        comm = Comment_on_post.objects.get(id = commids)
        try:
            like = LikeOnComment.objects.get(comment = comm, userlike = user)
        except:
            like = LikeOnComment(Comment = comm, like = True, userlike = user)
            like.save()
    elif request.POST.get('replyid'):
        userid = request.user.id
        user = User.objects.get(id=userid)
        replyids = int(request.POST.get('replyid'))
        reply = ReplyOnComm.objects.get(id = replyids)
        try:
            like = LikeOnReply.objects.get(reply = reply, userlike = user)
        except:
            like = LikeOnReply(reply = reply, like = True, userlike = user)
            like.save()

    return redirect(request.POST.get('in'))

def removelike(request):
    if request.POST.get('bloglikesid'):
        like = LikeOnBlogpost.objects.get(id = request.POST.get('bloglikesid'))
        like.delete()
    elif request.POST.get('commlikeid'):
        likeoncomm = LikeOnComment.objects.get(id = request.POST.get('commlikeid'))
        likeoncomm.delete()
    elif request.POST.get('replylikeid'):
        likerep = LikeOnReply.objects.get(id = request.POST.get('replylikeid'))
        likerep.delete()
    return redirect(request.POST.get('in'))


def showaboutpost(request, pk):
    replyform = ReplyForm()
    CForm = CommentForm()
    blog = Blogpost.objects.get(id = pk)
    useric = Userbet.objects.get(User = blog.Author)
    comms_data = []
    imgs = None
    if Images.objects.filter(blog = blog).count() > 0:
        imgs = Images.objects.filter(blog = blog)
    comms = Comment_on_post.objects.filter(Blog = blog).order_by('-data')
    for a in comms:
        comm = a
        likesc = LikeOnComment.objects.filter(Comment = a).count()
        replys = list(ReplyOnComm.objects.filter(comment = a).order_by('-data'))
        autcomm = Userbet.objects.get(User = a.Author)
        for r in replys:
            likesr = LikeOnReply.objects.filter(reply = r).count()
            if likesr > 0:
                replys.remove(r)
                replys.insert(0, r)
        data_comms = {
            'user': autcomm,
            'comm': comm, 
            'reply': replys[:1],
            'countrep': len(replys),
            'morereps': replys[1:],
            'havemorereps': len(replys) > 1
        }
        if likesc > 0:
            comms_data.insert(0, data_comms)
        else:
            comms_data.append(data_comms)
    blogpost_data = {
        'user': useric,
        'blog': blog,
        'imgs': imgs,
        'comms': comms_data[:1],
        'countcomms': len(comms_data),
        'morecomms': comms_data[1:],
        'havemorecomms': len(comms_data) > 1
        }
    data = {
        'replyform': replyform,
        'form': CForm,
        'blogs': blogpost_data,
    }
    return render(request, 'blogmain/post/aboutpost.html', data)