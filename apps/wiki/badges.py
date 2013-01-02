from django.conf import settings
from django.db.models import Sum
from django.db.models.signals import post_save

from .models import (Document, Revision)

import badger
import badger.utils
from badger.utils import get_badge, award_badge, get_progress
from badger.models import Badge, Award, Progress
from badger.signals import badge_was_awarded


def update_badges(overwrite=False):
    badges = [
        dict(slug="welcome",
             title="Welcome to MDN",
             description="You are a new user on MDN!"),
    ]
    return badger.utils.update_badges(badges, overwrite)


def register_signals():
    pass
