import pytest

from tests.fixtures.fixture_data import N_TEST_POSTS, N_POSTS_LIMIT

pytestmark = [
    pytest.mark.django_db,
]


def test_all_unpublished(
        user_client, unpublished_posts_with_published_locations,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'Ensure that if the project has no published posts, no posts are '
        'shown on the homepage.'
    )


def test_mixed_published(
        user_client, posts_with_published_locations,
        unpublished_posts_with_published_locations,
        main_page_post_list_context_key
):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    n_expected = len(posts_with_published_locations)
    assert len(context_post_list) == n_expected, (
        'Ensure that the homepage context key '
        f'`{main_page_post_list_context_key}` contains only published posts '
        'with a published category and a publication date in the past.'
    )
    assert all(x.is_published for x in context_post_list), (
        'Ensure that the homepage context key '
        f'`{main_page_post_list_context_key}` contains only published posts.'
    )


@pytest.mark.parametrize('key', [
    'title',
    ('category', 'title'),
    ('category', 'slug'),
    ('location', 'name')
])
def test_check_context_keys(
        key,
        user_client,
        posts_with_published_locations, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    html = response.content.decode('utf-8')
    if isinstance(key, tuple):
        key_1, key_2 = key
        assert getattr(getattr(context_post_list[0], key_1), key_2) in html, (
            f'The homepage does not use the `{key_1}.{key_2}` attribute value.'
        )
    else:
        assert getattr(context_post_list[0], key) in html, (
            f'The homepage does not use the post attribute value `{key}`.'
        )


def test_category_unpublished(
        user_client, posts_with_unpublished_category,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'If a category is unpublished, its posts must not appear on the '
        'homepage.'
    )


def test_pub_date_later_today(
        user_client, posts_with_future_date, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == 0, (
        'If a post publication date is in the future, it must not appear on '
        'the homepage.'
    )


def test_posts_with_published_location(
        user_client, posts_with_published_locations,
        main_page_post_list_context_key
):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert all(x.location for x in context_post_list), (
        'Ensure that posts marked with a location include the `location` key '
        'and its value in the homepage context.'
    )


def test_posts_with_unpublished_locations(
        user_client,
        posts_with_unpublished_locations, main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == N_TEST_POSTS, (
        'Ensure that the homepage context also includes posts whose location '
        'is unpublished.'
    )


def test_many_posts_on_main_page(
        user_client, many_posts_with_published_locations,
        main_page_post_list_context_key):
    response = user_client.get('/')
    context_post_list = response.context.get(main_page_post_list_context_key)
    assert len(context_post_list) == N_POSTS_LIMIT, (
        f'Ensure that only the latest {N_POSTS_LIMIT} posts are displayed on '
        'the homepage.'
    )
