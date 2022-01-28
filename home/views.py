from django.contrib.auth import models
from django.urls.base import reverse_lazy
from home.models import Blog, Comment, IpModel
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.http import HttpResponse, request
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import Edit_blog, CommentForm
from django.urls import reverse
from django.views.generic import CreateView
def index(request):
    blog = Blog.objects.all()
    allblogs = []
    catprods= Blog.objects.values('category', 'id')
    cats= {item["category"] for item in catprods}
    for cat in cats:
        bl = Blog.objects.filter(category=cat)
        allblogs.append(bl)
    params = {'blogs': allblogs}
    return render(request, 'index.html', params)

def about(request):
    return HttpResponse("Lvda ghe i am at About")

def registerUser(request):
    if request.method == "POST":
        fname = request.POST.get('firstname')
        lname = request.POST.get('lastname')
        uname = request.POST.get('username')
        email = request.POST.get('email')
        passw = request.POST.get('password')

        if User.objects.filter(username = uname).exists():
            messages.warning(request, 'Username already taken !')
            return redirect('register')

        elif User.objects.filter(email = email).exists():
            messages.warning(request, 'Email already taken !')
            return redirect('register')

        user = User.objects.create_user(first_name = fname, last_name = lname, username = uname, email = email, password = passw)
        user.save()
        messages.success(request, 'User has been registered succesfully !')
        return redirect('login')
    return render(request, 'register.html')

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'User has been Logged in succesfully !')
            return redirect('/')
        else:
            messages.warning(request, "sorry ! user is not registered")
            return redirect('register')
    return render(request, 'login.html')

def logoutUser(request):
    logout(request)
    messages.success(request, 'User has been Logged out succesfully !')
    return redirect('/')

def post_blog(request):
    if request.method == "POST":
        title = request.POST.get('title')
        category = request.POST.get('category')
        content = request.POST.get('content')
        blog = Blog(title=title, desc=content, user_id=request.user, category=category)
        if((title) == ""  and content == ""):
            messages.success(request, 'Please add conent and Title to your blog !')
            return redirect('post_blog')
        else:
            blog.save()
            messages.success(request, 'Blog added succesfully !')
            return redirect('post_blog')
    return render(request, "post_blog.html")

def displayblog(request, id):
    bl = Blog.objects.get(id=id)
    params = {'blog':bl}
    return render(request, "dispblog.html", params)

def deleteblog(request, id):
    bl = Blog.objects.get(id=id)
    bl.delete()
    messages.warning(request, 'Blog has been deleted !')
    return redirect('/')

def editblog(request, id):
    bl = Blog.objects.get(id=id)
    editblog = Edit_blog(instance=bl)
    if request.method == "POST":
        form = Edit_blog(request.POST, instance=bl)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog Edited succesfully !')
            return redirect('/')

    return render(request, "editblog.html", {'edit_blog':editblog})


def dashboard(request):
    blogs = Blog.objects.all()
    return render(request, 'dashboard.html', {'blogs':blogs})

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def postlike(request, pk):
    # blog_id = request.POST.get('blog_id')
    blog = Blog.objects.get(pk=pk)
    blogs = Blog.objects.all()
    ip = get_client_ip(request)
    liked = False
    if not IpModel.objects.filter(ip=ip).exists():
        IpModel.objects.create(ip=ip)
    if blog.likes.filter(ip = IpModel.objects.get(ip=ip)).exists():
        blog.likes.remove(IpModel.objects.get(ip=ip))
        liked = False

    else:
        blog.likes.add(IpModel.objects.get(ip=ip))
        liked = True
    return HttpResponseRedirect(reverse('display', args=[pk]), {'blog_posts': blogs, 'liked':liked})

class Addcomment(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "add_comnt.html"
    #fields = '__all__'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.blog_id = self.kwargs['id']
        return super().form_valid(form)

def search(request):
    query = request.POST.get('query')
    blogs = Blog.objects.filter(desc__contains = query)
    return render(request, "search_res.html", {'blogs':blogs, 'query':query})