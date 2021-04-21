# Generated by Django 3.1.7 on 2021-04-18 13:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recommender', '0007_auto_20210418_1527'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userprofile',
            old_name='age',
            new_name='What_is_your_age',
        ),
        migrations.RenameField(
            model_name='userprofile',
            old_name='gender',
            new_name='What_is_your_gender',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='breath_shortness',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cough',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='fever',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='headache',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='sore_throat',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='test_indication',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Are_you_experiencing_breath_shortness',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Are_you_running_a_fever',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Do_you_have_a_headache',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Do_you_have_a_sore_throat',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Do_you_have_cough',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Have_you_been_in_contact_with_someone_with_COVID_19',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=50),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='Have_you_been_overseas_in_the_last_14_days',
            field=models.CharField(choices=[('NO', 'NO'), ('YES', 'YES')], default='NO', max_length=50),
        ),
    ]