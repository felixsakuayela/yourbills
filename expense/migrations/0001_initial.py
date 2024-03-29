# Generated by Django 4.2.7 on 2023-11-11 23:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Expense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=48)),
                ('date_create', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('user_create', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Spent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date', models.DateTimeField()),
                ('type', models.CharField(choices=[('I', 'Individual'), ('C', 'Compartilhado')], max_length=1)),
                ('active', models.BooleanField(default=True)),
                ('expense', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.expense')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='spents', to=settings.AUTH_USER_MODEL)),
                ('users_shared', models.ManyToManyField(blank=True, related_name='share_request', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShareRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('P', 'Pending'), ('A', 'Approved'), ('R', 'Refused')], default='P', max_length=1)),
                ('spent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='expense.spent')),
                ('user_approving', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_received', to=settings.AUTH_USER_MODEL)),
                ('user_requesting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requests_made', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
