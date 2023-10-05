import os

usernames["wikidata"]["wikidata"] = os.environ["WIKIDATA_BOT_USERNAME"]

password_file = "user-password.py"

# Throttle read requests (in seconds) - starts at minthrottle, but can increase
# up to maxthrottle when the server is under load
minthrottle = 0
maxthrottle = 60

# Slow down the robot such that it never makes a second page edit within
# 'put_throttle' seconds.
put_throttle = int(os.environ.get("WIKIDATA_PUT_THROTTLE", "1.0"))

# If a delay is larger than 'noisysleep' seconds, it is logged on the screen.
noisysleep = 1.0

# Defer bot edits during periods of database server lag. For details, see
# https://www.mediawiki.org/wiki/Manual:Maxlag_parameter
maxlag = 5
