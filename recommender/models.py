import hashlib, random, sys
from django.db import models
from . import constants


def create_session_hash():
    hash = hashlib.sha1()
    hash.update(str(random.randint(0, sys.maxsize)).encode('utf-8'))
    return hash.hexdigest()


class UserProfile(models.Model):
    YES_OR_NO = (
        "Yes",
        "No",
    )

    gender_choices = (
        (constants.MALE, "Male"),
        (constants.FEMALE, "Female"),
    )

    test_indication_choices = (
        (constants.ABD, "Abroad"),
        (constants.CWC, "Contact with confirmed"),
        (constants.OTH, "Other"),
    )

    # page session info
    user_id = models.CharField(max_length=40, unique=True)
    stage = models.CharField(max_length=10, default=constants.STAGE_1)
    # stage 1 fields
    age = models.PositiveIntegerField()
    # stage 2 fields
    gender = models.CharField(choices=gender_choices, max_length=10, default=constants.MALE)
    # stage 3 fields
    cough = models.BooleanField(default=False)
    # stage 4 fields
    breath_shortness = models.BooleanField(default=False)
    # stage 5 fields
    fever = models.BooleanField(default=False)
    # stage 6 fields
    sore_throat = models.BooleanField(default=False)
    # stage 7 fields
    headache = models.BooleanField(default=False)
    # stage 8 fields
    test_indication = models.CharField(choices=test_indication_choices, max_length=50, default=constants.OTH)

    # outcome from predictor
    outcome = models.CharField(max_length=8)

    # operational
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    hidden_fields = ['stage']
    required_fields = ['age', 'sex', 'test_indication']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.user_id:
            while True:
                user_id = create_session_hash()
                if UserProfile.objects.filter(user_id=user_id).count() == 0:
                    self.user_id = user_id
                    break

    def __str__(self):
        return self.outcome

    @staticmethod
    def get_fields_by_stage(stage):
        fields = ['stage']  # Must always be present
        if stage == constants.STAGE_1:
            fields.extend(['age'])
        elif stage == constants.STAGE_2:
            fields.extend(['gender'])
        elif stage == constants.STAGE_3:
            fields.extend(['cough'])
        elif stage == constants.STAGE_4:
            fields.extend(['breath_shortness'])
        elif stage == constants.STAGE_5:
            fields.extend(['fever'])
        elif stage == constants.STAGE_6:
            fields.extend(['sore_throat'])
        elif stage == constants.STAGE_7:
            fields.extend(['headache'])
        elif stage == constants.STAGE_8:
            fields.extend(['test_indication'])
        return fields