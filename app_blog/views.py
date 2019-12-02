from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.utils import timezone
from django.contrib import auth  
from django.contrib.auth.models import User
from django.core.paginator import Paginator



# Create your views here.
def home(request):
    posts = Post.objects.all()
    paginator = Paginator(posts, 2)    #2는 2개씩 보여준다는 의미임 
    page = request.GET.get('page')      # 'page' value를 page를 넣는거임
    posts = paginator.get_page(page)    



    return render(request, 'home.html', {'posts': posts , 'posts':posts})

def detail(request,post_id):
    blog_detail = get_object_or_404(Post , pk=post_id)
    return render(request,'detail.html', {'post':blog_detail})

def new(request):
    return render(request,'new.html')

def create(request):
    new_blog=Post()
    new_blog.title = request.POST['title']
    new_blog.date = timezone.datetime.now()
    new_blog.body = request.POST['body']
    new_blog.save()
    return redirect('/app_blog/'+str(new_blog.id))

def edit(request,post_id):
    edit_blog = Post.objects.get(id=post_id)
    return render(request, 'edit.html',{'post':edit_blog})

def update(request, post_id):
    update_blog = Post.objects.get (id = post_id)
    update_blog.title = request.POST['title']
    update_blog.body = request.POST['body']
    update_blog.save()
    update_blog.date = timezone.datetime.now()       #이 부분 수정해본건데 자세히는 모르겠음 물어보기
    return redirect('home')

def delete(request, post_id):
    delete_blog = Post.objects.get(id=post_id)
    delete_blog.delete()
    return redirect('home')
    
def signup(request):
    if request.method == 'POST':  #method 무엇인지 물어보기 
        # User has info and wants an account now!
        if request.POST['password1'] == request.POST['password2']:   
            try:
                user = User.objects.get(username=request.POST['username'])
                return render(request, 'signup.html', {'error': 'Username has already been taken'})
            except User.DoesNotExist:
                user = User.objects.create_user(
                    request.POST['username'], password=request.POST['password1'])
                auth.login(request, user)   #로그인 상태를 유지시켜주는 함수임
               

                return redirect('login')
        else:
            return render(request, 'signup.html', {'error': 'Passwords must match'})
    else:
        # User wants to enter info
        return render(request, 'signup.html')
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:   #유저가 none 이 아니면은 로그인 조져라  그다음에 홈창으로 가주는거임
            auth.login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'username or password is incorrect.'})
    else:
        return render(request, 'login.html')

def logout(request):
    auth.logout(request)
    return render(request,'login.html')          #그냥 단순하게 로그아웃 상태가 해체된다