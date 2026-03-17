from http import HTTPStatus

import pytest
from pytest_django.asserts import assertTemplateUsed


@pytest.mark.parametrize('page', ('about', 'rules'))
@pytest.mark.django_db
def test_pageapp_views(user_client, page):
    response = user_client.get(f'/pages/{page}/')
    assert response.status_code == HTTPStatus.OK, (
        f'Ensure that the `/pages/{page}/` page exists and is rendered as '
        'required.'
    )
    try:
        assertTemplateUsed(response, f'pages/{page}.html')
    except AssertionError:
        raise AssertionError(
            f'Use the `pages/{page}.html` template for the `/pages/{page}/` '
            'page.'
        )
