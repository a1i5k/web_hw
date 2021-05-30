from random import randint

from django.core.management.base import BaseCommand
from faker import Faker

from app.models import *


class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        for i in range(11):
            tag_text = set()
            while len(tag_text) != 999:
                tag_text.add(Faker().word() + str(randint(0, 1000)) + str(i))
                print(11 - i, ' ', len(tag_text))
            tags = []
            for k in tag_text:
                tags.append(Tag(text=k))
            Tag.objects.bulk_create(tags)

        for i in range(100000):
            obj = Question.objects.get(pk=randint(2, 10000))
            Like.objects.create(
                user=User.objects.get(pk=randint(2, 10000)),
                content_type=ContentType.objects.get_for_model(obj),
                rating=1,
                object_id=obj.id
            )
            print(i)

        for i in range(100000):
            obj = Answer.objects.get(pk=randint(2, 10000))
            Like.objects.create(
                user=User.objects.get(pk=randint(2, 10000)),
                content_type=ContentType.objects.get_for_model(obj),
                rating=1,
                object_id=obj.id
            )
            print(i)

        for i in range(10001):
            User.objects.create(username=Faker().simple_profile()['username'] + Faker().pystr()[:10],
                                email=Faker().email(),
                                password=Faker().name())
            print(i)

        for i in range(100001):
            Question.objects.create(
                author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                title=Faker().paragraph(nb_sentences=1),
                text=Faker().text,
                date=Faker().date,
                rating=randint(-100, 100),
            )
            print(i)

        for i in range(1000001):
            Answer.objects.create(body=Faker().text,
                                  author=User.objects.get(pk=randint(User.objects.first().id, User.objects.last().id)),
                                  date=Faker().date,
                                  question=Question.objects.get(
                                      pk=randint(Question.objects.first().id, Question.objects.last().id)),
                                  rating=randint(-100, 100),
                                  )
            print(i)