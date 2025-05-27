import orjson
import pkgutil

manifest = orjson.loads(pkgutil.get_data(__name__, "archipelago.json"))

LINKS_AWAKENING = manifest["game"]
WORLD_VERSION = manifest["world_version"]
BASE_ID = 10000000
DIRECTORY = "ladx_beta"
SUFFIX = ".apladxb"
