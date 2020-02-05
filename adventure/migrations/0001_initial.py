from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('cooldown', models.IntegerField(default=100)),
                ('vision_enabled', models.BooleanField(default=False)),
                ('can_mine', models.BooleanField(default=False)),
                ('catchup_enabled', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='DEFAULT TITLE', max_length=50)),
                ('description', models.CharField(default='DEFAULT DESCRIPTION', max_length=500)),
                ('coordinates', models.CharField(default='()', max_length=32)),
                ('n_to', models.IntegerField(blank=True, null=True)),
                ('s_to', models.IntegerField(blank=True, null=True)),
                ('e_to', models.IntegerField(blank=True, null=True)),
                ('w_to', models.IntegerField(blank=True, null=True)),
                ('elevation', models.IntegerField(default=0)),
                ('terrain', models.CharField(default='NORMAL', max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, null=True, unique=True)),
                ('active', models.BooleanField(default=True)),
                ('has_rename', models.BooleanField(default=False)),
                ('has_mined', models.BooleanField(default=False)),
                ('is_pm', models.BooleanField(default=False)),
                ('description', models.CharField(default=' looks like an ordinary person.', max_length=140)),
                ('currentRoom', models.IntegerField(default=0)),
                ('uuid', models.UUIDField(default=uuid.uuid4, unique=True)),
                ('cooldown', models.DateTimeField(auto_now_add=True)),
                ('gold', models.IntegerField(default=0)),
                ('strength', models.IntegerField(default=10)),
                ('speed', models.IntegerField(default=10)),
                ('bodywear', models.IntegerField(default=0)),
                ('footwear', models.IntegerField(default=0)),
                ('encumbrance', models.IntegerField(default=0)),
                ('can_fly', models.BooleanField(default=False)),
                ('can_dash', models.BooleanField(default=False)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Group')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='DEFAULT_ITEM', max_length=20)),
                ('description', models.CharField(default='DEFAULT DESCRIPTION', max_length=200)),
                ('weight', models.IntegerField(default=1)),
                ('aliases', models.CharField(default='', max_length=200)),
                ('value', models.IntegerField(default=1)),
                ('itemtype', models.CharField(default='DEFAULT', max_length=20)),
                ('attributes', models.CharField(default='{}', max_length=1000)),
                ('level', models.IntegerField(default=1)),
                ('exp', models.IntegerField(default=0)),
                ('group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Group')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Player')),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='adventure.Room')),
            ],
        ),
    ]
