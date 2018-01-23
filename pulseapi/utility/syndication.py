"""
Provide RSS and Atom feeds for Pulse.
"""
from django.contrib.syndication.views import Feed
from django.utils.feedgenerator import Atom1Feed

from pulseapi import settings
from pulseapi.entries.models import Entry


# The creator(s) name can be found in the `OrderedCreatorRecord` class from the `creators` models.
def get_entry_creators(entry):
    # Since `creators` is an optional field and can be empty, we return the publisher name instead.
    if not entry.related_creators.all():
        return entry.published_by.name
    else:
        return ', '.join(
            creator_record.creator.creator_name
            for creator_record
            in entry.related_creators.all()
        )


# RSS feed for latest entries
class RSSFeedLatestFromPulse(Feed):
    title = "Latest from Mozilla Pulse"
    link = "{frontend_url}/latest".format(frontend_url=settings.PULSE_FRONTEND_HOSTNAME)
    description = "Subscribe to get the latest entries from Mozilla Pulse."

    def items(self):
        return Entry.objects.order_by('-created')

    def item_author_name(self, entry):
        return get_entry_creators(entry)

    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return entry.description

    def item_link(self, entry):
        return entry.frontend_entry_url()


# RSS feed for featured entries
class RSSFeedFeaturedFromPulse(Feed):
    title = "Latest from Mozilla Pulse"
    link = "{frontend_url}/featured".format(frontend_url=settings.PULSE_FRONTEND_HOSTNAME)
    description = "Subscribe to get the latest featured entries from Mozilla Pulse."

    def items(self):
        return Entry.objects.filter(featured=True).order_by('-created')

    def item_author_name(self, entry):
        return get_entry_creators(entry)

    def item_title(self, entry):
        return entry.title

    def item_description(self, entry):
        return entry.description

    def item_link(self, entry):
        return entry.frontend_entry_url()


# Atom feed for latest entries
class AtomFeedLatestFromPulse(RSSFeedLatestFromPulse):
    feed_type = Atom1Feed
    subtitle = RSSFeedLatestFromPulse.description


# Atom feed for featured entries
class AtomFeedFeaturedFromPulse(RSSFeedFeaturedFromPulse):
    feed_type = Atom1Feed
    subtitle = RSSFeedLatestFromPulse.description
