from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

from webapp.models import BaseModel

statuses = [("new", "Новая"), ("moderated", "Модерированная"), ("deleted", "Удаленная")]


class Article(BaseModel):
    title = models.CharField(max_length=50, null=False, blank=False, verbose_name="Название")
    content = models.TextField(null=False, blank=False, verbose_name="Контент")
    status = models.CharField(max_length=20, choices=statuses, verbose_name="Статус", default=statuses[0][0])
    likes_count = models.PositiveIntegerField(default=0)
    liked_by = models.ManyToManyField(get_user_model(), related_name='liked_articles', blank=True)

    author = models.ForeignKey(
        get_user_model(),
        related_name="articles",
        on_delete=models.SET_DEFAULT,
        default=1
    )

    tags = models.ManyToManyField(
        "webapp.Tag",
        related_name="articles",
        verbose_name="Теги",
        blank=True,
        through='webapp.ArticleTag',
        through_fields=("article", "tag"),
    )

    def get_absolute_url(self):
        return reverse("webapp:article_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return f"{self.pk}. {self.title}: {self.author}"

    class Meta:
        db_table = "articles"
        verbose_name = "Статья"
        verbose_name_plural = "Статьи"
        permissions = [("change_article_status", "менять статус статье")]
