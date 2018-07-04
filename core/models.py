from django.db import models
from django.utils import timezone
from django.contrib.postgres import fields as pg_fields

from lead_management.users.models import User


TARGET_TYPES = (
    ("HP", "Happiness Program"),
    ("AMP", "Advance Meditation Program"),
    ("DSN", "Dynamism For Self And Nation"),
    ("SSY2", "Sri Sri Yoga Level 2"),
    ("SSY1", "Sri Sri Yoga Level 1"),
    ("VTP", "Volunteer Training Program"),
    ("HPY", "Happiness Program for Youth"),
    ("YES+", "Youth Empowerment and Skills Workshop"),
    ("MY", "Medha Yoga"),
    ("PY", "Pragna Yoga"),
    ("AE", "Art Excel"),
)

LEAD_STATUS_CHOICES = (
    ('INTR', 'Interested'),
    ('PEND', 'Filled the form, payment pending'),
    ('PART', 'Part Payment'),
    ('NI', 'Not Interested'),
    ('NC', 'Next Course'),
    ('AOL', 'Already in AOL'),
    ('PAID', 'Paid'),
    ('DROP', 'Drop Out'),
    ('NOSO', 'No Show'),
    ('COMP', 'Completed'),
)


class Target(models.Model):
    """
    This contains Target(Course) related information
    """
    target_type = models.CharField(max_length=4, choices=TARGET_TYPES, default='HP')
    start_date = models.DateTimeField(db_index=True)
    end_date = models.DateTimeField()
    # Ids of the Users who are Owners/Admins for this Target
    admins = pg_fields.ArrayField(models.IntegerField(), db_index=True)
    # Ids of the Users who are Volunteers for this Target
    volunteers = pg_fields.ArrayField(models.IntegerField(), db_index=True)
    total_leads = models.IntegerField(default=0)
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)


class Lead(models.Model):
    """
    This contains Lead(Participant) related information
    """
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    target = models.ForeignKey(Target, on_delete=models.PROTECT)
    email = pg_fields.CIEmailField(max_length=100)
    history = pg_fields.ArrayField(
        pg_fields.CITextField()
    )
    lead_status = models.CharField(max_length=3, choices=LEAD_STATUS_CHOICES, default='INTR')
    target_type = models.CharField(max_length=4, choices=TARGET_TYPES, default='HP')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
