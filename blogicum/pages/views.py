from django.shortcuts import render


def about(request):
    """Страница О проекте."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Страница Наши правила."""
    template = 'pages/rules.html'
    return render(request, template)
