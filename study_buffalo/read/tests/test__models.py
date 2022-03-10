"""Tests for the Models module of the Read app."""
import pytest

from django.utils import timezone

from read import models


pytestmark = pytest.mark.django_db


def test__publication__minimal_creation():
    """Tests minimal Publication model creation."""
    publication_count = models.Publication.objects.count()

    models.Publication.objects.create(
        title='Publication 1',
        description='Description 1',
        date_published=timezone.now(),
    )

    assert models.Publication.objects.count() == publication_count + 1


def test__publication__title__max_length():
    """Confirms title field's max length in Publication model."""
    max_length = models.Publication._meta.get_field('title').max_length

    assert max_length == 100


def test__publication__description__max_length():
    """Confirms description field's max length in Publication model."""
    max_length = models.Publication._meta.get_field('description').max_length

    assert max_length == 256


def test__publication__str():
    """Tests for expected output of the Publication __str__ method."""
    publication = models.Publication.objects.create(
        title='Publication 1',
        description='Description 1',
        date_published='2000-01-01',
    )

    assert str(publication) == '2000-01-01 - Publication 1'


def test__publication__get_absolute_url(read_publication):
    """Tests for expected output of the Publication get_absolute_url method."""
    assert read_publication.get_absolute_url() == f'/read/{read_publication.pk}/'


def test__html_publication__minimal_creation(read_publication):
    """Tests minimal HTMLPublication model creation."""
    html_count = models.HTMLPublication.objects.count()

    models.HTMLPublication.objects.create(
        publication=read_publication,
        html='1',
    )

    assert models.HTMLPublication.objects.count() == html_count + 1


def test__html_publication__str(read_publication):
    """Tests for expected output of the HTMLPublication __str__ method."""
    html = models.HTMLPublication.objects.create(
        publication=read_publication,
        html='1',
    )

    assert str(html) == f'HTML for {read_publication}'


def test__document_publication__minimal_creation(read_document_publication):
    """Tests minimal DocumentPublication model creation."""
    doc_count = models.DocumentPublication.objects.count()

    models.DocumentPublication.objects.create(
        publication=read_document_publication.publication,
        document=read_document_publication.document
    )

    assert models.DocumentPublication.objects.count() == doc_count + 1


def test__document_publication__str(read_document_publication):
    """Tests for expected output of the DocumentPublication __str__ method."""
    doc = models.DocumentPublication.objects.create(
        publication=read_document_publication.publication,
        document=read_document_publication.document
    )

    assert str(doc) == f'Document for {read_document_publication.publication}'
