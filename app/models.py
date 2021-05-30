from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db.models import CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver

from app.managers import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=CASCADE)
    nickname = models.CharField(max_length=16)
    avatar = models.ImageField(default="static/img/ava.jpg")
    rating = models.IntegerField(default=0)
    objects = ProfileManager()

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профиль'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Tag(models.Model):
    text = models.CharField(max_length=16)
    objects = TagManager()

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = 'Теги'
        verbose_name_plural = 'Теги'


class Like(models.Model):
    GRADE = [(1, 'like'), (-1, 'dislike')]

    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    rating = models.IntegerField(choices=GRADE)
    content_type = models.ForeignKey(ContentType, default=None, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_id = GenericForeignKey()
    objects = LikeManager()

    class Meta:
        verbose_name = 'Лайки'
        verbose_name_plural = 'Лайки'


class Question(models.Model):
    author = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=64)
    text = models.CharField(max_length=1024)
    date = models.DateTimeField(auto_now_add=True)
    tag = models.ManyToManyField(Tag, related_name='questions', blank=True)
    vote = GenericRelation(Like, related_query_name='questions')
    rating = models.IntegerField(default=0, null=False)
    objects = QuestionManager()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вопросы'
        verbose_name_plural = 'Вопросы'


class Answer(models.Model):
    body = models.CharField(max_length=256, null=False)
    author = models.ForeignKey(User, null=False, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now_add=True)
    question = models.ForeignKey(Question, null=False, on_delete=CASCADE, related_name='answers')
    vote = GenericRelation(Like, related_query_name='questions')
    rating = models.IntegerField(default=0, null=False)
    objects = AnswerManager()

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'Ответы'
        verbose_name_plural = 'Ответы'
