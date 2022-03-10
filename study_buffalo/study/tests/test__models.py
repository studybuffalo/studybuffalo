"""Tests for the Models module of the Study app."""
import pytest

from django.utils import timezone

from study import models


pytestmark = pytest.mark.django_db


def test__guide__minimal_creation():
    """Tests minimal Guide model creation."""
    guide_count = models.Guide.objects.count()

    models.Guide.objects.create(
        title='Guide 1',
        short_description='Short 1',
        long_description='Long 1',
        date_original=timezone.now(),
        last_update=timezone.now(),
        permissions=None,
    )

    assert models.Guide.objects.count() == guide_count + 1


def test__guide__title__max_length():
    """Confirms title field's max length in Guide model."""
    max_length = models.Guide._meta.get_field('title').max_length

    assert max_length == 100


def test__guide__short_description__max_length():
    """Confirms short_description field's max length in Guide model."""
    max_length = models.Guide._meta.get_field('short_description').max_length

    assert max_length == 256


def test__guide__permissions__max_length():
    """Confirms permissions field's max length and defaults in Guide model."""
    max_length = models.Guide._meta.get_field('permissions').max_length

    assert max_length == 3


def test__guide__str():
    """Tests for expected output of the Guide __str__ method."""
    guide = models.Guide.objects.create(
        title='Guide 1',
        short_description='Short 1',
        long_description='Long 1',
        date_original=timezone.now(),
        last_update='2000-01-01',
        permissions=None,
    )

    assert str(guide) == 'Guide 1 (Updated 2000-01-01)'


def test__guide__get_absolute_url(study_guide):
    """Tests expected output of the Guide get_absolute_url method."""
    assert study_guide.get_absolute_url() == f'/study/{study_guide.pk}/'


def test__guide__has_bounty__false(study_guide):
    """Tests expected output of Guide has_bounty method when no bounty."""
    assert study_guide.has_bounty() is False


def test__guide__has_bounty__true(study_bounty):
    """Tests expected output of Guide has_bounty method when bounty."""
    assert study_bounty.study_guide.has_bounty() is True


def test__bounty__minimal_creation(study_guide):
    """Tests minimal Bounty model creation."""
    bounty_count = models.Bounty.objects.count()

    models.Bounty.objects.create(
        study_guide=study_guide,
        bounty_details='Bounty 1'
    )

    assert models.Bounty.objects.count() == bounty_count + 1


def test__bounty__bounty_status__max_length_default():
    """Confirms bounty_status field's max length and defaults in Bounty model."""
    max_length = models.Bounty._meta.get_field('bounty_status').max_length
    default = models.Bounty._meta.get_field('bounty_status').default

    assert max_length == 1
    assert default == 'o'


def test__bounty__bounty_amount__max_digits_default():
    """Confirms bounty_amount field's max digits and defaults in Bounty model."""
    max_digits = models.Bounty._meta.get_field('bounty_amount').max_digits
    default = models.Bounty._meta.get_field('bounty_amount').default

    assert max_digits == 6
    assert default == 0


def test__bounty__str(study_guide):
    """Tests for expected output of the Bounty __str__ method."""
    bounty = models.Bounty.objects.create(
        study_guide=study_guide,
        bounty_details='Bounty 1'
    )

    assert str(bounty) == f'$0 bounty on {study_guide}'


def test__bounty_assignment__minimal_creation(user, study_bounty):
    """Tests minimal BountyAssignment model creation."""
    assignment_count = models.BountyAssignment.objects.count()

    models.BountyAssignment.objects.create(
        bounty=study_bounty,
        assignment_status='i',
        assigned_user=user,
        proportion=1,
    )

    assert models.BountyAssignment.objects.count() == assignment_count + 1


def test__bounty_assignment__assignment_status__max_length():
    """Confirms assignment_status field's max length in BountyAssignment model."""
    max_length = models.BountyAssignment._meta.get_field('assignment_status').max_length

    assert max_length == 1


def test__bounty_assignment__proportion__max_digits_default():
    """Confirms proportion field's max digits and defaults in BountyAssignment model."""
    max_digits = models.BountyAssignment._meta.get_field('proportion').max_digits
    default = models.BountyAssignment._meta.get_field('proportion').default

    assert max_digits == 3
    assert default == 0


def test__bounty_assignment__str(user, study_bounty):
    """Tests for expected output of the BountyAssignment __str__ method."""
    assignment = models.BountyAssignment.objects.create(
        bounty=study_bounty,
        assignment_status='i',
        assigned_user=user,
        proportion=1,
    )

    assert str(assignment) == f'{study_bounty} assigned to {user}'


def test__html_guide__minimal_creation(study_guide):
    """Tests minimal HTMLGuide model creation."""
    html_count = models.HTMLGuide.objects.count()

    models.HTMLGuide.objects.create(
        study_guide=study_guide,
        html='1',
    )

    assert models.HTMLGuide.objects.count() == html_count + 1


def test__html_guide__str(study_guide):
    """Tests for expected output of the HTMLGuide __str__ method."""
    html = models.HTMLGuide.objects.create(
        study_guide=study_guide,
        html='1',
    )

    assert str(html) == f'HTML for {study_guide}'


def test__document_guide__minimal_creation(study_document_guide):
    """Tests minimal DocumentGuide model creation."""
    doc_count = models.DocumentGuide.objects.count()

    models.DocumentGuide.objects.create(
        study_guide=study_document_guide.study_guide,
        document=study_document_guide.document
    )

    assert models.DocumentGuide.objects.count() == doc_count + 1


def test__document_guide__str(study_document_guide):
    """Tests for expected output of the DocumentGuide __str__ method."""
    doc = models.DocumentGuide.objects.create(
        study_guide=study_document_guide.study_guide,
        document=study_document_guide.document
    )

    assert str(doc) == f'Document for {study_document_guide.study_guide}'
