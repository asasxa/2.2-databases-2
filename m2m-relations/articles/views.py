from django.shortcuts import render
from .models import Article

def articles_list(request):
    articles = Article.objects.prefetch_related('scopes__tag').order_by('-published_at')
    return render(request, 'articles/news.html', {'object_list': articles})
