import datetime
from functools import wraps
from logging import getLogger

from search.redis_client import RedisClient

logger = getLogger(__file__)


def checkpoint_timer(code):
    now = datetime.datetime.now()
    now_epoch = now.timestamp()
    r = RedisClient.get_instance()
    last_epoch = None
    try:
        last_epoch = float(r.get("chkt_last_epoch"))
    except:
        pass
    time = None
    if last_epoch:
        last_time = datetime.datetime.fromtimestamp(last_epoch)
        diff = now - last_time
        td = int(diff.total_seconds() * 1000)
    else:
        td = None
    if td:
        logger.info("CHKT {}, took {} ms".format(code, td))
    else:
        logger.info("CHKT {}".format(code))
    r.set("chkt_last_epoch", str(now_epoch))


def chkt(code):
    def func(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            checkpoint_timer("Initializing {}".format(code))
            r = f(*args, **kwargs) or None
            checkpoint_timer(code)
            return r

        return wrapped

    return func
