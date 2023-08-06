from rest_framework.renderers import JSONRenderer
from slugify import slugify
from tqdm import tqdm
from tracker.serializers import (
    PersonSerializer,
    PersonHomeSerializer,
    StoryFeedSerializer,
    EndorsementFeedSerializer,
    QuoteFeedSerializer,
    TweetFeedSerializer,
)
from tracker.utils.aws import defaults, get_bucket


def bake_candidate(candidate):
    data = PersonSerializer(candidate.person).data
    json_string = JSONRenderer().render(data)
    key = "election-results/2020/candidate-tracker/{}/data.json".format(
        slugify(candidate.person.full_name)
    )
    bucket = get_bucket()
    bucket.put_object(
        Key=key,
        ACL=defaults.ACL,
        Body=json_string,
        CacheControl=defaults.CACHE_HEADER,
        ContentType="application/json",
    )


def sort_feed_item(item):
    if item["identity"].startswith("quote"):
        return item["date"]

    if item["identity"].startswith("tweet"):
        return item["publish_date"]

    if item["identity"].startswith("endorsement"):
        return item["endorsement_date"]

    if item["identity"].startswith("story"):
        return item["publish_date"]


def bake_feed(candidates):
    feed_items = []
    print("Baking master feed")
    for candidate in tqdm(candidates):
        endorsements = EndorsementFeedSerializer(
            candidate.campaign.endorsements, many=True
        ).data
        stories = StoryFeedSerializer(candidate.stories, many=True).data
        quotes = QuoteFeedSerializer(candidate.quotes, many=True).data
        tweets = TweetFeedSerializer(candidate.tweets, many=True).data

        feed_items.extend(endorsements)
        feed_items.extend(stories)
        feed_items.extend(quotes)
        feed_items.extend(tweets)

    sorted_feed = sorted(feed_items, key=sort_feed_item, reverse=True)
    json_string = JSONRenderer().render(sorted_feed)
    key = "election-results/2020/candidate-tracker/feed.json"
    bucket = get_bucket()
    bucket.put_object(
        Key=key,
        ACL=defaults.ACL,
        Body=json_string,
        CacheControl=defaults.CACHE_HEADER,
        ContentType="application/json",
    )


def bake_homepage(candidates):
    people = []
    print("Baking homepage candidates")
    for candidate in tqdm(candidates):
        person = PersonHomeSerializer(candidate.person).data
        people.append(person)

    json_string = JSONRenderer().render(people)
    key = "election-results/2020/candidate-tracker/candidates.json"
    bucket = get_bucket()
    bucket.put_object(
        Key=key,
        ACL=defaults.ACL,
        Body=json_string,
        CacheControl=defaults.CACHE_HEADER,
        ContentType="application/json",
    )
