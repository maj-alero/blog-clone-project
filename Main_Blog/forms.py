from django import forms
from Main_Blog.models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'titleTextInput', 'placeholder': 'Enter title'}),
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea ContentTextArea', 'placeholder': 'Enter text'}),
            
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea ',}),
        }
        