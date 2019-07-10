from django.conf import settings
from django.db import models

from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from taggit.managers import TaggableManager


class Article(models.Model):
    DRAFT = "D"
    PUBLISHED = "P"
    STATUS = (
        (DRAFT, ("Draft")),
        (PUBLISHED,("Published")),
    )

    user = models.ForeignKey(
            settings.AUTH_USER_MODEL,
            null=True,
            related_name="author",
            on_delete=models.SET_NULL
                )
    '''image = models.ImageField(
            _('Featured image'), upload_to='articles_pictures/%Y/%m/%d/')
    )'''
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255, null=False, unique=True)
    slug = models.SlugField(max_length=80, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS, default=DRAFT)
    content = MarkdownxField()
    edited = models.BooleanField(default=False)
    tags = TaggableManager()
    #objects = ArticleQuerySet.as

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.title}",
                                to_lower=True, max_length=80)
        super().save(*args, **kwargs)

    def get_markdown(self):
        return markdownify(self.content)
