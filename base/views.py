from django.shortcuts import render, redirect   
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.mail import EmailMessage
from django.core.mail.backends import smtp

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Post
from .forms import PostForm,RegisterForm
from .filters import PostFilter
# Create your views here.

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user= form.save()
            auth_login(request, user)
            return redirect("home")
    context = {'form':form,}
    return render(request, 'base/register.html', context)

def login(request):
    context = {
    }
    return render(request, 'base/login.html', context)

def home(request): 
    posts = Post.objects.filter(active=True, featured=True)[0:3]
   


    context = {'posts':posts}
    return render(request, 'base/index.html', context) 

def post(request, slug):
    post = Post.objects.get(slug=slug)  
     
    context = {'post':post}
    return render(request, 'base/post.html', context)

def posts(request):
    posts = Post.objects.filter(active=True)
    myFilter = PostFilter(request.GET, queryset=posts)
    filtered_posts = myFilter.qs

    ordered_posts = filtered_posts.order_by('-created')


    paginator = Paginator(ordered_posts, 2)

    page = request.GET.get('page')

    try:
        paginated_posts = paginator.page(page)
    except PageNotAnInteger:
        paginated_posts = paginator.page(1)
    except EmptyPage:
        paginated_posts = paginator.page(paginator.num_pages)
    

    context = {'posts':paginated_posts,'myFilter':myFilter}
    return render(request, 'base/posts.html', context)
 
def profile(request):
    return render(request, 'base/profile.html') 
 
@login_required(login_url="home")
def createPost(request):
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form':form}
    return render(request, 'base/post_form.html', context)

@login_required(login_url="home")
def updatePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
        return redirect('posts')

    context = {'form':form}
    return render(request, 'base/post_form.html', context)


@login_required(login_url="home")
def deletePost(request,slug):
    post = Post.objects.get(slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('posts')
    context = {'item':post}
    return render(request, 'base/delete.html', context)


def sendEmail(request):

    if request.method == 'POST':

        template = render_to_string('base/email_template.html',{
            'name': request.POST['name'],
            'email': request.POST['email'],
            'message': request.POST['message'],
        })
        email = EmailMessage(
            request.POST['subject'],
            template,
            settings.EMAIL_HOST_USER,
            ['stevekamworor@gmail.com']
        )
        email.fail_silently=False
        email.send()

    return render(request, 'base/email_sent.html')
 