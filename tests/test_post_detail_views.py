from http import HTTPStatus

import pytest

from blog.models import Post

pytestmark = [
    pytest.mark.django_db,
]


def test_posts_page_pk_published_location(
        user_client, post_with_published_location, post_context_key):
    response = user_client.get(f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Ensure that a published post with a published category and a past '
        'publication date is displayed on its detail page.'
    )
    context_post = response.context.get(post_context_key)
    assert context_post == post_with_published_location, (
        'Ensure that the `/posts/<int:pk>/` page context key '
        f'`{post_context_key}` contains the post whose `pk` matches the GET '
        'request parameter.'
    )


def test_posts_page_pk_unpublished_location(
        user_client, post_with_unpublished_location, post_context_key):
    response = user_client.get(f'/posts/{post_with_unpublished_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Ensure that a published post with a published category and a past '
        'publication date is still displayed on its detail page even if its '
        'location is unpublished.'
    )


def test_posts_page_pk_post_doesnt_exists(user_client):
    try:
        response = user_client.get('/posts/1/')
    except Post.DoesNotExist:
        raise AssertionError(
            'Ensure that requesting a non-existent post page does not raise '
            'an unhandled exception in the view.'
        )
    assert response.status_code != HTTPStatus.OK, (
        'Ensure that a non-existent post request does not return a detail '
        'page.'
    )


@pytest.mark.parametrize('key', [
    'title',
    'text',
    ('category', 'title'),
    ('category', 'slug'),
    ('location', 'name')
])
def test_posts_page_pk_check_context_keys(
        key, user_client, post_with_published_location,
        post_context_key
):
    response = user_client.get(
        f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Ensure that a post detail page exists and is rendered as required '
        'when the post is published, has a location, and its category is '
        'published.'
    )
    context_post = response.context.get(post_context_key)
    html = response.content.decode('utf-8')
    if isinstance(key, tuple):
        key_1, key_2 = key
        assert getattr(getattr(context_post, key_1), key_2) in html, (
            f'The post detail page does not use the `{key_1}.{key_2}` '
            'attribute value.'
        )
    else:
        attr_val = getattr(context_post, key)
        if key == 'text':
            if attr_val in html:
                return
            else:
                attr_val = attr_val.replace('\n', '<br>')
        assert attr_val in html, (
            f'The post detail page does not use the `{key}` attribute value.'
        )


def test_posts_page_pk_unpublished_post(user_client, unpublished_post):
    response = user_client.get(f'/posts/{unpublished_post.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Ensure that an unpublished post detail page returns HTTP 404.'
    )


def test_posts_page_pk_pub_date_later_today(
        user_client, post_with_future_date):
    response = user_client.get(f'/posts/{post_with_future_date.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Ensure that a post with a future publication date returns HTTP 404 '
        'on its detail page.'
    )


def test_posts_page_pk_category_unpublished(
        user_client,
        post_with_unpublished_category,
):
    response = user_client.get(f'/posts/{post_with_unpublished_category.id}/')
    assert response.status_code == HTTPStatus.NOT_FOUND, (
        'Ensure that a post assigned to an unpublished category returns HTTP '
        '404 on its detail page.'
    )


def test_posts_page_pk_post_with_published_location_and_category(
        user_client, post_with_published_location,
        post_context_key
):
    response = user_client.get(
        f'/posts/{post_with_published_location.id}/')
    assert response.status_code == HTTPStatus.OK, (
        'Ensure that if a post is published, has a location, and its category '
        'is published, its detail page exists and is rendered.'
    )
    context_post = response.context.get(post_context_key)
    assert context_post == post_with_published_location, (
        'Ensure that the post page context key '
        f'`{post_context_key}` contains the post object whose `pk` matches '
        'the GET request parameter.'
    )
