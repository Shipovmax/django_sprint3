from django.shortcuts import render


def about(request):
    """Render the About page."""
    template = 'pages/about.html'
    return render(request, template)


def rules(request):
    """Render the Rules page."""
    template = 'pages/rules.html'
    return render(request, template)
