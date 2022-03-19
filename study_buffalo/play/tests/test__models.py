"""Tests for the Models module of the Play app."""
from os.path import exists

import pytest

from django.utils import timezone

from play import models


pytestmark = pytest.mark.django_db


def test__category__minimal_creation():
    """Tests minimal Category model creation."""
    category_count = models.Category.objects.count()

    models.Category.objects.create(category='Category 1')

    assert models.Category.objects.count() == category_count + 1


def test__category__category__max_length():
    """Confirms category field's max length in Category model."""
    max_length = models.Category._meta.get_field('category').max_length

    assert max_length == 100


def test__category__str():
    """Tests for expected output of the Category __str__ method."""
    category = models.Category.objects.create(category='Category 1')

    assert str(category) == 'Category 1'


def test__play_page__minimal_creation(play_page):
    """Tests minimal PlayPage model creation."""
    page_count = models.PlayPage.objects.count()

    models.PlayPage.objects.create(
        title='Title 1',
        date=timezone.now(),
        category=play_page.category,
        release_date=timezone.now()
    )

    assert models.PlayPage.objects.count() == page_count + 1


def test__play_page__title__max_length():
    """Confirms title field's max length in PlayPage model."""
    max_length = models.PlayPage._meta.get_field('title').max_length

    assert max_length == 256


def test__play_page__str(play_page):
    """Tests for expected output of the PlayPage __str__ method."""
    page = models.PlayPage.objects.create(
        title='Title 1',
        date='2000-01-01',
        category=play_page.category,
        release_date=timezone.now()
    )

    assert str(page) == '2000-01-01 - Title 1'


def test__play_page__get_absolute_url(play_page):
    """Tests for expected output of the PlayPage get_absolute_url method."""
    assert play_page.get_absolute_url() == f'/play/{play_page.pk}/'


def test__play_page__previous_page(play_page):
    """Tests for expected output of PlayPage previous_page method."""
    # Create new model to ensure PK > 1
    page = models.PlayPage.objects.create(
        title='Title 1',
        date='2000-01-01',
        category=play_page.category,
        release_date=timezone.now()
    )
    assert page.previous_page() == page.pk - 1


def test__play_page__previous_page__first(play_page):
    """Tests handling of PlayPage previous_page method with first entry."""
    # Hold reference to category
    category = play_page.category

    # Delete any existing models
    models.PlayPage.objects.all().delete()

    # Create a pk = 1 instance
    page = models.PlayPage.objects.create(
        pk=1,
        title='Title 1',
        date='2000-01-01',
        category=category,
        release_date=timezone.now()
    )

    assert page.previous_page() is None


def test__play_page__next_page(play_page):
    """Tests for expected output of PlayPage next_page method."""
    # Set play_page date to allow triggering next_page method
    play_page.release_date = '2000-01-01T00:00:00Z'
    play_page.save()

    # Create new model to ensure there is a next page
    models.PlayPage.objects.create(
        title='NEXT PAGE',
        date=timezone.now(),
        category=play_page.category,
        release_date='1999-01-01T00:00:00Z',
    )

    # Confirm the next page PK is the expected model
    next_page = models.PlayPage.objects.get(pk=play_page.next_page())
    assert next_page.title == 'NEXT PAGE'


def test__play_page__next_page__last(play_page):
    """Tests handling of PlayPage next_page method with last entry."""
    # Hold reference to category
    category = play_page.category

    # Delete any existing models
    models.PlayPage.objects.all().delete()

    # Create new model that will be equivalent to last page
    page = models.PlayPage.objects.create(
        pk=1,
        title='Title 1',
        date=timezone.now(),
        category=category,
        release_date='2000-01-02T00:00:00Z',
    )

    assert page.next_page() is None


def test__play_page__last_page(play_page):
    """Tests for expected output of PlayPage last_page method."""
    # Set play_page date to allow triggering last_page method
    play_page.release_date = '2000-01-01T00:00:00Z'
    play_page.save()

    # Create new model to ensure there is a next page
    models.PlayPage.objects.create(
        title='LAST PAGE',
        date=timezone.now(),
        category=play_page.category,
        release_date='1999-01-01T00:00:00Z',
    )

    # Confirm the last page PK is the expected model
    last_page = models.PlayPage.objects.get(pk=play_page.last_page())
    assert last_page.title == 'LAST PAGE'


def test__play_image__minimal_creation(play_image):
    """Tests minimal PlayImage model creation."""
    image_count = models.PlayImage.objects.count()

    models.PlayImage.objects.create(
        title='Image 1',
        original_image=play_image.original_image,
        alt_text='Alt 1',
        description='Description 1',
    )

    assert models.PlayImage.objects.count() == image_count + 1


def test__play_image__title__max_length():
    """Confirms title field's max length in PlayImage model."""
    max_length = models.PlayImage._meta.get_field('title').max_length

    assert max_length == 256


def test__play_image__type__max_length_default():
    """Confirms type field's max length and default in PlayImage model."""
    max_length = models.PlayImage._meta.get_field('type').max_length
    default = models.PlayImage._meta.get_field('type').default

    assert max_length == 1
    assert default == 'i'


def test__play_image__str(play_image):
    """Tests for expected output of the PlayImage __str__ method."""
    image = models.PlayImage.objects.create(
        title='Image 1',
        original_image=play_image.original_image,
        alt_text='Alt 1',
        description='Description 1',
    )

    assert str(image) == play_image.original_image.name


def test__play_image__save__small_image(play_image):
    """Tests for resized image when small image saved to PlayImage."""
    image = models.PlayImage.objects.create(
        title='Image 1',
        original_image=play_image.original_image,
        alt_text='Alt 1',
        description='Description 1',
    )

    assert image.resized_image.width == image.original_image.width
    assert image.resized_image.height == image.original_image.height


def test__play_image__save__large_image(play_image_large):
    """Tests for resized image when large image saved to PlayImage."""
    image = models.PlayImage.objects.create(
        title='Image 1',
        original_image=play_image_large.original_image,
        alt_text='Alt 1',
        description='Description 1',
    )

    assert image.resized_image.width == 800
    assert image.resized_image.height == 800


def test__play_audio__minimal_creation(play_audio):
    """Tests minimal PlayAudio model creation."""
    audio_count = models.PlayAudio.objects.count()

    models.PlayAudio.objects.create(
        title='Audio 1',
        audio=play_audio.audio,
        description='Description 1',
    )

    assert models.PlayAudio.objects.count() == audio_count + 1


def test__play_audio__title__max_length():
    """Confirms title field's max length in PlayAudio model."""
    max_length = models.PlayAudio._meta.get_field('title').max_length

    assert max_length == 256


def test__play_audio__type__max_length_default():
    """Confirms type field's max length and default in PlayAudio model."""
    max_length = models.PlayAudio._meta.get_field('type').max_length
    default = models.PlayAudio._meta.get_field('type').default

    assert max_length == 1
    assert default == 'a'


def test__play_audio__str(play_audio):
    """Tests for expected output of the PlayAudio __str__ method."""
    audio = models.PlayAudio.objects.create(
        title='Audio 1',
        audio=play_audio.audio,
        description='Description 1',
    )
    assert str(audio) == 'Audio 1'


def test__play_image_delete__fires_when_expected(play_image_large):
    """Confirms the post-delete signal fires when expected."""
    # Create image for testing
    image = models.PlayImage.objects.create(
        title='Image 1',
        original_image=play_image_large.original_image,
        alt_text='Alt 1',
        description='Description 1',
    )

    # Paths to image files
    original_image = image.original_image.path
    resized_image = image.resized_image.path

    # Delete image
    image.delete()

    # Confirm files no longer exist
    assert exists(original_image) is False
    assert exists(resized_image) is False
