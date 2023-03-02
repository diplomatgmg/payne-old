from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView

from .form import CreateCommentForm, CreatePostForm
from .models import Post, Comment
from ..users.models import CustomUser


class PostListView(ListView):
    template_name = 'blog/blog_list.html'
    model = Post
    paginate_by = 3
    paginate_orphans = 2


class PostView(DetailView, FormView):
    template_name = 'blog/blog_details.html'
    model = Post
    form_class = CreateCommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = Comment.objects.filter(to_post=self.object)
        context['articles'] = Post.objects.filter(author=self.object.author)
        context['most_popular'] = Post.objects.most_popular()
        return context

    def get_success_url(self):
        return self.request.META['HTTP_REFERER']

    def form_valid(self, form):
        user = self.request.user
        to_post = self.model.objects.get(id=self.kwargs['pk'])
        content = form.cleaned_data['comment']
        Comment.objects.create(user=user, to_post=to_post, content=content)
        user.add_comment()
        return HttpResponseRedirect(self.get_success_url())

    def get(self, *args, **kwargs):
        Post.objects.get(id=self.kwargs['pk']).add_view()
        return super().get(*args, **kwargs)


def delete_comment(request, id_comment, id_author):
    comment = Comment.objects.filter(id=id_comment, user=request.user).last()
    if comment:
        comment.delete()
        CustomUser.objects.get(id=id_author).remove_comment()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


class CreatePost(CreateView):
    template_name = 'blog/blog_create.html'
    model = Post
    form_class = CreatePostForm
    success_url = reverse_lazy('post-list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


def delete_post(request, id_post):
    post = Post.objects.filter(id=id_post, author=request.user).last()
    if post:
        post.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])

