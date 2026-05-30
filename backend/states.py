import collections

# Словари состояний пользователей
user_states = {}
player_states = {}

# Защита от спама (Rate Limiter)
user_last_messages = collections.defaultdict(lambda: collections.deque(maxlen=3))