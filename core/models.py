from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify


def slug_generator(title):
    new_slug = slugify(title)
    return new_slug[:100]


class AdvUser(AbstractUser):
    avatar = models.ImageField('photo', upload_to='avatar_img', null=True, blank=True)
    birthday = models.DateField(null=True, blank=True)
    info = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.username


class Question(models.Model):
    question = models.CharField(max_length=250)
    choise_1 = models.CharField(max_length=100)
    choise_2 = models.CharField(max_length=100)
    choise_3 = models.CharField(max_length=100)
    choise_4 = models.CharField(max_length=100)
    answer = models.CharField(max_length=100)
    test = models.ForeignKey('core.Test', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.question


class Test(models.Model):
    user = models.ManyToManyField(AdvUser, through='Examination')
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=100, blank=True, unique=True)
    description = models.TextField(default='', blank=True)
    question_quantity = models.PositiveSmallIntegerField(default=5)
    author = models.CharField(max_length=50, default='admin')
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    is_active = models.BooleanField(default=True)
    attempts_counter = models.PositiveSmallIntegerField(default=0)
    comment = GenericRelation('comment')

    def get_absolute_url(self):
        return reverse('test_detail', kwargs={'test_slug_name': self.slug})

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = slug_generator(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Examination(models.Model):
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)
    test = models.ForeignKey(Test, on_delete=models.CASCADE)
    correct_answer_counter = models.PositiveSmallIntegerField(default=0)
    result = models.DecimalField(max_digits=5, decimal_places=2, default=-1)


class Comment(models.Model):
    author = models.ForeignKey('core.AdvUser', on_delete=models.SET_NULL, null=True)
    text = models.TextField(default='', blank=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveSmallIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')


class TestSortModel(models.Model):
    sort_by = models.CharField(max_length=10, default='title', null=True, blank=True, choices=(
        ('title', 'Title'),
        ('-created', 'Date +'),
        ('created', 'Date -'),
        ('attempts_counter', 'rating'),
    ))
