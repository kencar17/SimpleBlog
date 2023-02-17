# Generated by Django 4.1.5 on 2023-02-17 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0002_user_display_name_alter_user_bio"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="facebook_link",
            field=models.URLField(
                blank=True, help_text="Facebook Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="instagram_link",
            field=models.URLField(
                blank=True,
                help_text="Instagram Social Link.",
                max_length=250,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="linkedin_link",
            field=models.URLField(
                blank=True, help_text="LinkedIn Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="snapchat_link",
            field=models.URLField(
                blank=True, help_text="Snapchat Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="tiktok_link",
            field=models.URLField(
                blank=True, help_text="Tiktok Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="twitch_link",
            field=models.URLField(
                blank=True, help_text="Twitch Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="twitter_link",
            field=models.URLField(
                blank=True, help_text="Twitter Social Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="website_link",
            field=models.URLField(
                blank=True, help_text="Website Link.", max_length=250, null=True
            ),
        ),
        migrations.AlterField(
            model_name="account",
            name="youtube_link",
            field=models.URLField(
                blank=True, help_text="Youtube Social Link.", max_length=250, null=True
            ),
        ),
    ]
