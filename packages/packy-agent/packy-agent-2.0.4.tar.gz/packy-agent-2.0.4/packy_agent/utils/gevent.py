from collections import defaultdict

from gevent.lock import RLock


database_locks = defaultdict(RLock)
