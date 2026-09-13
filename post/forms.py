from django.forms import ModelForm
from post.models import Post,Comment

class PostCreationForm(ModelForm):
    
    class Meta:
        model = Post
        fields = ['title','content','category']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body']