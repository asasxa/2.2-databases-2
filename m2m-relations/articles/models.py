from django.db import models
from django.core.exceptions import ValidationError


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Название раздела')

    class Meta:
        verbose_name = 'Раздел'
        verbose_name_plural = 'Разделы'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    text = models.TextField(verbose_name='Текст статьи')
    image = models.ImageField(upload_to='', blank=True, null=True, verbose_name='Изображение')
    published_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')

    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-published_at']

    def __str__(self):
        return self.title


class Scope(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='scopes', verbose_name='Статья')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='scopes', verbose_name='Раздел')
    is_main = models.BooleanField(default=False, verbose_name='Основной раздел')

    class Meta:
        verbose_name = 'Связь статьи с разделом'
        verbose_name_plural = 'Связи статей с разделами'
        ordering = ['-is_main', 'tag__name']

    def __str__(self):
        return f'{self.article.title} - {self.tag.name} (основной: {self.is_main})'

    def clean(self):
        if self.is_main:
            existing_main = Scope.objects.filter(article=self.article, is_main=True).exclude(id=self.id)
            if existing_main.exists():
                raise ValidationError('У статьи может быть только один основной раздел.')
