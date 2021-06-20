from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from app.models import *

COUNT_THOUSAND_TAG = 11
COUNT_USER = 10001
COUNT_QUESTION = 100001
COUNT_TAG_IN_QUESTION = 5
COUNT_ANSWER = 1000001
COUNT_LIKE_QUESTION = 100001
COUNT_LIKE_ANSWER = 100001


class Command(BaseCommand):
    def handle(self, *args, **options):
        for i in range(COUNT_THOUSAND_TAG):
            tag_text = set()
            while len(tag_text) != 999:
                tag_text.add(Faker().word() + str(randint(1000, 2000)) + str(i))
                print(11 - i, ' ', len(tag_text))
            tags = []
            for k in tag_text:
                tags.append(Tag(text=k))
            Tag.objects.bulk_create(tags)

        for i in range(COUNT_USER):
            user = User.objects.create(username=Faker().simple_profile()['username'] + Faker().pystr()[:10],
                                       email=Faker().email(),
                                       password=Faker().name())
            user.profile.nickname = Faker().simple_profile()['username'] + Faker().pystr()[:10]
            user.save()
            print(i)

        for i in range(COUNT_QUESTION):
            question = Question.objects.create(
                author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                title=Faker().paragraph(nb_sentences=1),
                text=Faker().text,
                date=Faker().date,
                rating=randint(-100, 100)
            )
            tags = []
            for j in range(COUNT_TAG_IN_QUESTION):
                tags.append(Tag.objects.get(pk=randint(Tag.objects.first().id, Tag.objects.last().id)))
            question.tag.set(tags)
            print(i)

        for i in range(COUNT_ANSWER):
            Answer.objects.create(body=Faker().text,
                                  author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                                  date=Faker().date,
                                  question=Question.objects.get(
                                      pk=randint(Question.objects.first().id, Question.objects.last().id)),
                                  rating=randint(-100, 100),
                                  )
            print(i)

        for i in range(COUNT_LIKE_QUESTION):
            obj = Question.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))
            Like.objects.create(
                user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                content_type=ContentType.objects.get_for_model(obj),
                rating=1,
                object_id=obj.id
            )
            print(i)

        for i in range(COUNT_LIKE_ANSWER):
            obj = Answer.objects.get(pk=randint(User.objects.first().id, User.objects.last().id))
            Like.objects.create(
                user=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                content_type=ContentType.objects.get_for_model(obj),
                rating=1,
                object_id=obj.id
            )
            print(i)
