import os
from pywikibot.login import BotPassword

(
    os.environ["WIKIDATA_BOT_USERNAME"],
    BotPassword(os.environ["WIKIDATA_BOT_SUFFIX"], os.environ["WIKIDATA_BOT_PASSWORD"]),
)
