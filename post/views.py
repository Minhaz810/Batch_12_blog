from django.shortcuts import render,redirect
from post.models import Post,Category,Comment
from django.db.models import Q
from post.forms import CommentForm,PostCreationForm

# Create your views here.
def post_list_view(request):
    try:
        query = request.GET.get('query','')
        category_id = request.GET.get('category_id','')
        status = request.GET.get('status','')

        posts = Post.objects.select_related('category','author')

        if category_id:
            posts = posts.filter(category__id=category_id)
        if status:
            posts = posts.filter(status=status)
        if query:
            posts = posts.filter(
                Q(title__icontains = query) |
                Q(content__icontains = query) |
                Q(author__username__icontains =query)
            )
        post_summary_list =[]
        all_categories = Category.objects.all()
        status_choices = Post.STATUS_CHOICES
        for post in posts:
            post_summary_list.append({
                    "id":post.id,
                    "title":post.title,
                    "content":post.content[:100],
                    "category":post.category,
                    "created_at":post.created_at
                }
            )


        return render(
            request=request,
            template_name="post_list.html",
            context={
                "post_summary":post_summary_list,
                "categories":all_categories,
                "status_choices":status_choices
            }
        ) 

    except Exception as e:
        return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )

def post_detail_view(request,pk):
    try:
        post = Post.objects.get(id=pk)
        parent_comments = post.comments.filter(parent__isnull=True)
        form = CommentForm()
        if request.method == "POST" and request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                comment.author = request.user
                parent_id = request.POST.get('parent_id')
                if parent_id:
                    comment.parent = Comment.objects.get(id=parent_id)
                comment.save()
                return redirect('post_detail',pk=post.id)
        return render(
            request=request,
            template_name='post_detail.html',
            context={
                'post':post,
                "parent_comments":parent_comments,
                'form':form
            }
        )
    except Exception as e:
         return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )

def post_create_view(request):
    try:
        form = PostCreationForm()
        if request.method == "POST":
            form = PostCreationForm(request.POST)
            category_id = request.POST.get('category')
            category = Category.objects.get(id=category_id)
            
            if form.is_valid():
                post = Post(
                    title=request.POST.get('title'),
                    content=request.POST.get('content'),
                    category = category,
                    author = request.user
                )
                post.save()
                return redirect('post_list')

        return render(
            request=request,
            template_name='post_creation.html',
            context={'form':form}
        )

    except Exception as e:
         return render(
            request=request,
            template_name='error.html',
            context={'error':e}
        )