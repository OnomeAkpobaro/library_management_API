# Generated by Django 5.1.4 on 2025-01-26 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('author', models.CharField(max_length=100)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Science Fiction', 'Science Fiction'), ('Fantasy', 'Fantasy'), ('Mystery', 'Mystery'), ('Horror', 'Horror'), ('Romance', 'Romance'), ('Western', 'Western'), ('Thriller', 'Thriller'), ('Dystopian', 'Dystopian'), ('Memoir', 'Memoir'), ('Biography', 'Biography'), ('Self-Help', 'Self-Help'), ('Cookbook', 'Cookbook'), ('Poetry', 'Poetry'), ('History', 'History'), ('Science', 'Science'), ('Math', 'Math'), ('Art', 'Art'), ('Music', 'Music'), ('Film', 'Film'), ('Travel', 'Travel'), ('Sports', 'Sports'), ('Health', 'Health'), ('Crafts', 'Crafts'), ('Other', 'Other')], max_length=100)),
                ('publication_date', models.DateField()),
                ('avalability', models.CharField(choices=[('Available', 'Available'), ('Checked Out', 'Checked Out'), ('Lost', 'Lost'), ('Damaged', 'Damaged')], max_length=100)),
                ('edition', models.CharField(max_length=100)),
                ('summary', models.TextField()),
            ],
            options={
                'verbose_name_plural': 'Books',
                'ordering': ['title'],
            },
        ),
    ]
