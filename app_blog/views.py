from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from django.utils import timezone

# Create your views here.
def home(request):
    posts = Post.objects
    return render(request, 'home.html', {'posts': posts})

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
    