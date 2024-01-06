import redis
from app.settings import redis_host, redis_port, text_cache_ttl

storage = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)


def get_text_cache(session_id):
    key = get_key(session_id)
    return storage.get(key)


def set_text_cache(session_id, text):
    key = get_key(session_id)
    storage.set(key, text, ex=text_cache_ttl)


def get_key(session_id):
    return 'recognized-text-{session_id}'.format(session_id=session_id)
