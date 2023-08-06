import logging
import os

from entity.models import Person
from rest_framework.renderers import JSONRenderer
from slugify import slugify
from tracker.serializers import PersonSerializer
from tracker.utils.aws import defaults, get_bucket
from celery import shared_task

logger = logging.getLogger("tasks")

OUTPUT_PATH = "election-results/2020/candidate-tracker/"


@shared_task(acks_late=True)
def bake_candidate(pk):
    print(pk)
    person = Person.objects.get(pk=pk)

    print("hi task")
    try:
        person.candidacies.get(
            race__cycle__slug="2020", race__office__slug="president"
        )
    except:
        return

    print("still running")

    data = PersonSerializer(person).data
    json_string = JSONRenderer().render(data)
    key = os.path.join(OUTPUT_PATH, slugify(person.full_name), "data.json")
    bucket = get_bucket()
    bucket.put_object(
        Key=key,
        ACL=defaults.ACL,
        Body=json_string,
        CacheControl=defaults.CACHE_HEADER,
        ContentType="application/json",
    )

    logger.info("Published {} to AWS".format(key))
