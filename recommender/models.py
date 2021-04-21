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


    bool_choices = (
        (constants.NO, 'NO'),
        (constants.YES, 'YES'),
    )


    # page session info
    user_id = models.CharField(max_length=40, unique=True)
    stage = models.CharField(max_length=10, default=constants.STAGE_1)
    # stage 1 fields
    What_is_your_age = models.PositiveIntegerField()
    # stage 2 fields
    What_is_your_gender = models.CharField(choices=gender_choices, max_length=10, default=constants.MALE)
    # stage 3 fields
    #cough = models.BooleanField(default=False)
    Do_you_have_cough = models.CharField(choices=bool_choices, max_length=10, default=constants.NO)
    # stage 4 fields
    #breath_shortness = models.BooleanField(default=False)
    Are_you_experiencing_breath_shortness = models.CharField(choices=bool_choices, max_length=10, default=constants.NO)
    # stage 5 fields
    #fever = models.BooleanField(default=False)
    Are_you_running_a_fever = models.CharField(choices=bool_choices, max_length=10, default=constants.NO)
    # stage 6 fields
    #sore_throat = models.BooleanField(default=False)
    Do_you_have_a_sore_throat = models.CharField(choices=bool_choices, max_length=10, default=constants.NO)
    # stage 7 fields
    #headache = models.BooleanField(default=False)
    Do_you_have_a_headache = models.CharField(choices=bool_choices, max_length=10, default=constants.NO)
    # stage 8 fields
    Have_you_been_overseas_in_the_last_14_days = models.CharField(choices=bool_choices, max_length=50, default=constants.NO)
    # stage 9 fields
    Have_you_been_in_contact_with_someone_with_COVID_19 = models.CharField(choices=bool_choices, max_length=50, default=constants.NO)
    #vaccine = models.CharField(choices=vaccine, max_length=50, default=constants.YES)
    # outcome from predictor
    outcome = models.CharField(max_length=8)

    # operational
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    hidden_fields = ['stage']
    required_fields = ['What_is_your_age', 'sex', 'Have_you_been_overseas_in_the_last_14_days','Have_you_been_in_contact_with_someone_with_COVID-19']

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
            fields.extend(['What_is_your_age'])
        elif stage == constants.STAGE_2:
            fields.extend(['What_is_your_gender'])
        elif stage == constants.STAGE_3:
            fields.extend(['Do_you_have_cough'])
        elif stage == constants.STAGE_4:
            fields.extend(['Are_you_experiencing_breath_shortness'])
        elif stage == constants.STAGE_5:
            fields.extend(['Are_you_running_a_fever'])
        elif stage == constants.STAGE_6:
            fields.extend(['Do_you_have_a_sore_throat'])
        elif stage == constants.STAGE_7:
            fields.extend(['Do_you_have_a_headache'])
        elif stage == constants.STAGE_8:
            fields.extend(['Have_you_been_overseas_in_the_last_14_days'])
        elif stage == constants.STAGE_9:
            fields.extend(['Have_you_been_in_contact_with_someone_with_COVID_19'])
        return fields