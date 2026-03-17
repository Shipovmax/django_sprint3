import pytest
from django.db.models import (
    BooleanField, CharField, DateTimeField, ForeignKey, TextField)
from django.db.utils import IntegrityError

from blog.models import Post
from tests.conftest import _TestModelAttrs

pytestmark = [
    pytest.mark.django_db,
]


@pytest.mark.parametrize(('field', 'type', 'params'), [
    ('title', CharField, {'max_length': 256}),
    ('text', TextField, {}),
    ('pub_date', DateTimeField, {}),
    ('author', ForeignKey, {'null': False}),
    ('location', ForeignKey, {'null': True}),
    ('category', ForeignKey, {'null': True}),
    ('is_published', BooleanField, {'default': True}),
    ('created_at', DateTimeField, {'auto_now_add': True}),
])
class TestCategoryModelAttrs(_TestModelAttrs):

    @property
    def model(self):
        return Post


def test_author_on_delete(posts_with_author):
    author = posts_with_author[0].author
    try:
        author.delete()
    except IntegrityError:
        raise AssertionError(
            'Ensure that the `on_delete` value for the `author` field in the '
            '`Post` model matches the specification.'
        )
    assert not Post.objects.filter(author=author).exists(),  (
        'Ensure that the `on_delete` value for the `author` field in the '
        '`Post` model matches the specification.'
    )


def test_location_on_delete(posts_with_published_locations):
    location = posts_with_published_locations[0].location
    try:
        location.delete()
    except IntegrityError:
        raise AssertionError(
            'Ensure that the `on_delete` value for the `location` field in '
            'the `Post` model matches the specification.'
        )
    assert Post.objects.filter(location=location).exists(), (
        'Ensure that the `on_delete` value for the `location` field in the '
        '`Post` model matches the specification.'
    )
