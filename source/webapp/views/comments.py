from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView, View

from webapp.forms import CommentForm
from webapp.forms.like_comment import CommentLikeForm
from webapp.models import Article, Comment


class CreateCommentView(LoginRequiredMixin, CreateView):
    template_name = "comments/create_comment.html"
    form_class = CommentForm

    # def form_valid(self, form):
    #     article = get_object_or_404(Article, pk=self.kwargs['pk'])
    #     form.instance.article = article
    #     return super().form_valid(form)

    def form_valid(self, form):
        article = get_object_or_404(Article, pk=self.kwargs['pk'])
        comment = form.save(commit=False)
        comment.article = article
        comment.author = self.request.user
        comment.save()
        return redirect(article.get_absolute_url())

    # def get_success_url(self):
    #     return reverse("webapp:article_detail", kwargs={"pk": self.object.article.pk})


class UpdateCommentView(UpdateView):
    template_name = "comments/update_comment.html"
    form_class = CommentForm
    model = Comment

    def get_success_url(self):
        return reverse("webapp:article_detail", kwargs={"pk": self.object.article.pk})


class DeleteCommentView(DeleteView):
    queryset = Comment.objects.all()

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.delete()
        return redirect("webapp:article_detail", pk=self.object.article.pk)


class CommentLikeView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        form = CommentLikeForm(request.POST)
        if form.is_valid():
            comment_id = form.cleaned_data.get('comment_id')
            comment = get_object_or_404(Comment, id=comment_id)

            if request.user not in comment.liked_by.all():
                comment.liked_by.add(request.user)
                comment.likes_count += 1
            else:
                comment.liked_by.remove(request.user)
                comment.likes_count -= 1
            comment.save()

        return redirect('webapp:article_detail', pk=comment.article.id)
