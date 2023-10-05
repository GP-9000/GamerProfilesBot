import pywikibot
import os
import re
from datetime import datetime, UTC
from urllib.parse import quote_plus as urlencode
from pymongo import MongoClient


def get_database():
    db_url = os.environ.get("DB_URL", "mongodb://localhost/gamerprofiles")
    if os.environ.get("DB_PASSWORD") and os.environ.get("DB_USER"):
        # if env db password and user is set, use them in the url for the db url
        db_url = db_url.replace(
            "://", "://%s:%s@" % (os.environ["DB_USER"], os.environ["DB_PASSWORD"])
        )
    client = MongoClient(db_url)
    return client.get_database()


def get_url_friendly_name(name=""):
    without_extras = re.sub(r"[^a-z0-9]", "-", name, flags=re.IGNORECASE)
    without_double_dashes = re.sub(r"-{2,}", "-", without_extras)
    without_leading_or_trailing_dashes = re.sub(r"(^-)|(-$)", "", without_double_dashes)
    return urlencode(without_leading_or_trailing_dashes)


def main():
    db = get_database()
    games_collection = db["games"]

    site = pywikibot.Site("wikidata:wikidata")
    repo = site.data_repository()

    games_to_update = games_collection.find(
        {
            "source": "wikidata",
            "sourceId": {"$exists": True},
            "gpIdAddedToWikidata": {"$exists": False},
        },
        {
            "sourceId": 1,
            "shortId": 1,
            "name": 1,
        },
    ).limit(int(os.environ.get("GAME_LIMIT", "10")))

    updated_games = []
    for item in games_to_update:
        wikidata_id = item.get("sourceId")
        wikidata_url = "https://www.wikidata.org/wiki/%s" % wikidata_id
        name = item.get("name")
        short_id = item.get("shortId")
        game_url = "https://gamerprofiles.com/game/%s/%s" % (
            short_id,
            get_url_friendly_name(name),
        )
        print("%s => %s" % (wikidata_url, game_url))

        item = pywikibot.ItemPage(repo, wikidata_id)
        existing_claims = item.get().get("claims")
        if not item.botMayEdit():
            print("Skipping %s because it cannot be edited by bots" % wikidata_id)
            continue
        if "P12001" in existing_claims:
            print(
                "Skipping %s because it already has a GamerProfiles game ID"
                % wikidata_id
            )
            continue
        try:
            claim = pywikibot.Claim(repo, "P12001")  # GamerProfiles game ID
            claim.setTarget(short_id)
            reference = pywikibot.Claim(repo, "P854")  # reference URL
            reference.setTarget(game_url)
            claim.addSource(reference, summary="Adding source URL")
            item.addClaim(claim, summary="Adding GamerProfiles game ID")
            updated_games.append(wikidata_id)
        except Exception as e:
            print("Error adding claims: %s" % e)

    games_collection.update_many(
        {"source": "wikidata", "sourceId": {"$in": updated_games}},
        {"$set": {"gpIdAddedToWikidata": datetime.now(tz=UTC)}},
    )
    print("Updated %d games" % len(updated_games))


if __name__ == "__main__":
    main()
