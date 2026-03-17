def test_blog_urls():
    try:
        from blog.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'An error occurred while importing `urlpatterns` from '
            f'`blog/urls.py`: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Ensure that `urlpatterns` is defined as a list.'
    )
    assert len(solution_urlpatterns) >= 3, (
        'Ensure that the root `urlpatterns` includes the routes from '
        '`blog/urls.py`.'
    )


def test_pages_urls():
    try:
        from pages.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'An error occurred while importing `urlpatterns` from '
            f'`pages/urls.py`: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Ensure that `urlpatterns` in `pages/urls.py` is defined as a list.'
    )
    assert len(solution_urlpatterns) >= 2, (
        'Ensure that the root `urlpatterns` includes the routes from '
        '`pages/urls.py`.'
    )


def test_blogicum_urls():
    try:
        from blogicum.urls import urlpatterns as solution_urlpatterns
    except Exception as e:
        raise AssertionError(
            'An error occurred while importing `urlpatterns` from '
            f'`blogicum/urls.py`: {e}'
        ) from e
    assert isinstance(solution_urlpatterns, list), (
        'Ensure that `urlpatterns` in `blogicum/urls.py` is defined as a list.'
    )
    assert len(solution_urlpatterns) >= 3, (
        'Ensure that the root `urlpatterns` includes the routes from '
        '`blogicum/urls.py`.'
    )
