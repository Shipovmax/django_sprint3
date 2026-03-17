from http import HTTPStatus

import pytest
from django.apps import apps
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer as _mixer

try:
    from blog.models import Category, Location, Post  # noqa:F401
except ImportError:
    raise AssertionError(
        'Define the `Post`, `Category`, and `Location` models '
        'in the `blog` application.'
    )
except RuntimeError:
    registered_apps = set(app.name for app in apps.get_app_configs())
    need_apps = {'blog': 'blog', 'pages': 'pages'}
    if not set(need_apps.values()).intersection(registered_apps):
        need_apps = {
            'blog': 'blog.apps.BlogConfig', 'pages': 'pages.apps.PagesConfig'}

    for need_app_name, need_app_conf_name in need_apps.items():
        if need_app_conf_name not in registered_apps:
            raise AssertionError(
                f'Ensure the `{need_app_name}` application is registered.'
            )

pytest_plugins = [
    'fixtures.fixture_data'
]


@pytest.fixture
def mixer():
    return _mixer


@pytest.fixture
def user(mixer):
    User = get_user_model()
    return mixer.blend(User)


@pytest.fixture
def user_client(user, client):
    client.force_login(user)
    return client


@pytest.fixture
def post_context_key(user_client, post_with_published_location):
    check_post_page_msg = (
        'Ensure the post page exists and is rendered as required.'
    )
    try:
        post_response = user_client.get(
            f'/posts/{post_with_published_location.id}/')
    except Exception:
        raise AssertionError(check_post_page_msg)
    assert post_response.status_code == HTTPStatus.OK, check_post_page_msg
    post_key = None
    for key, val in dict(post_response.context).items():
        if isinstance(val, Post):
            post_key = key
            break
    assert post_key, (
        'Ensure the post page context includes a post object.'
    )
    return post_key


def get_post_list_context_key(
        user_client, page_url, page_load_err_msg, key_missing_msg):
    try:
        post_response = user_client.get(page_url)
    except Exception:
        raise AssertionError(page_load_err_msg)
    assert post_response.status_code == HTTPStatus.OK, page_load_err_msg
    post_list_key = None
    for key, val in dict(post_response.context).items():
        try:
            assert isinstance(iter(val).__next__(), Post)
            post_list_key = key
            break
        except Exception:
            pass
    assert post_list_key, key_missing_msg
    return post_list_key


@pytest.fixture
def main_page_post_list_context_key(mixer, user_client):
    temp_category = mixer.blend('blog.Category', is_published=True)
    temp_location = mixer.blend('blog.Location', is_published=True)
    temp_post = mixer.blend('blog.Post', is_published=True,
                            location=temp_location, category=temp_category)
    page_load_err_msg = (
        'Ensure the homepage exists and is rendered as required.'
    )
    key_missing_msg = (
        'Ensure that if there is at least one published post with a '
        'published category and a publication date in the past, the homepage '
        'context contains a non-empty post list.'
    )
    try:
        result = get_post_list_context_key(
            user_client, '/', page_load_err_msg, key_missing_msg)
    except Exception as e:
        raise AssertionError(str(e)) from e
    finally:
        temp_post.delete()
        temp_location.delete()
        temp_category.delete()
    return result


@pytest.fixture
def category_page_post_list_context_key(mixer, user_client):
    temp_category = mixer.blend('blog.Category', is_published=True)
    temp_location = mixer.blend('blog.Location', is_published=True)
    temp_post = mixer.blend(
        'blog.Post', is_published=True,
        category=temp_category, location=temp_location)
    page_load_err_msg = (
        'Ensure the category page exists and is rendered as required when the '
        'category exists and is published.'
    )
    key_missing_msg = (
        'Ensure that if there is at least one published post with a '
        'published category and a publication date in the past, the category '
        'page context contains a non-empty post list.'
    )
    try:
        result = get_post_list_context_key(
            user_client, f'/category/{temp_category.slug}/',
            page_load_err_msg, key_missing_msg)
    except Exception as e:
        raise AssertionError(str(e)) from e
    finally:
        temp_post.delete()
        temp_location.delete()
        temp_category.delete()
    return result


class _TestModelAttrs:

    @property
    def model(self):
        raise NotImplementedError(
            'Override this property in the inherited test class.')

    def get_parameter_display_name(self, param):
        return param

    def test_model_attrs(self, field, type, params):
        model_name = self.model.__name__
        assert hasattr(self.model, field), (
            f'Define the `{field}` attribute in the `{model_name}` model.')
        model_field = self.model._meta.get_field(field)
        assert isinstance(model_field, type), (
            f'Ensure the `{field}` attribute in the `{model_name}` model '
            f'uses the `{type}` type.'
        )
        for param, value_param in params.items():
            display_name = self.get_parameter_display_name(param)
            assert param in model_field.__dict__, (
                f'Configure the `{display_name}` parameter for the '
                f'`{field}` attribute in the `{model_name}` model.'
            )
            assert model_field.__dict__.get(param) == value_param, (
                f'Ensure the `{display_name}` parameter for the `{field}` '
                f'attribute in the `{model_name}` model matches the '
                'specification.'
            )
