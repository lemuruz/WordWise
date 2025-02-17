# Generated by Django 5.1.4 on 2025-02-01 15:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('wordbank', '0002_wordbank_unique_word'),
    ]

    operations = [
        migrations.CreateModel(
            name='flashCardDeck',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('words', models.ManyToManyField(to='wordbank.wordbank')),
            ],
        ),
    ]
