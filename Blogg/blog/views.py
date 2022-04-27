from django.shortcuts import get_object_or_404, render, get_list_or_404 , HttpResponseRedirect, redirect
from blog.models import *
from django.core.paginator import PageNotAnInteger, EmptyPage, Paginator
from django.db.models import Q
from blog.forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    context = dict()
    post_list = Post.objects.all()
    query = request.GET.get('q')
    if query:
        post_list = Post.objects.filter(
            Q(title__icontains=query) 
        )
        print()
    context['posts']=post_list
    context['post_list']=Post.objects.distinct()
    context['category']=Category.objects.all()
    return render(request, 'index.html', context)

def about(request):
    return render(request, "about.html")

def blog(request):
    context = dict()
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 3)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context['posts']=posts
    return render(request, "blog.html", context)

def contact(request):
    return render(request, "contact.html")

def post(request,slug):
    post = get_list_or_404(Post, id = slug)
    form = CommentForm(request.POST or None)

    if form.is_valid():
        comment = form.save(commit=False)
        comment.post=post
        comment.save()
        return HttpResponseRedirect("index.html")

    context = {
        'post':post,
        'form':form,
    }
    return render(request, "post-details.html", context)

def add_comment_to_post(request,pk):
    post = Post.get_object_or_404(Post, pk=pk)

    if request.POST == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post=post
            comment.save()
            return redirect('detail', pk=post.pk)
    else:
        form= CommentForm()
    return render(request, 'forms.html', {'form':form})

@login_required
def comment_approved(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.approve()
    return redirect('detail', pk = comment.post.pk)

@login_required
def comment_remove(request,pk):
    comment = get_object_or_404(Comments, pk=pk)
    comment.delete()
    return redirect('detail', pk = comment.post.pk)


def category_show(request,category_slug):
    context = dict()
    context['category'] = get_object_or_404(
        Category, slug=category_slug
    )

    context['items']= Post.objects.filter(
        category=context['category']
    )
    return render(request, 'category.html',context)