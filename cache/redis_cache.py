import redis
import hashlib

redis_client = redis.Redis(
    host="localhost",
    port=6379,
    decode_responses=True
)


def get_cache_key(question: str):

    return hashlib.md5(question.encode()).hexdigest()


def get_cached_answer(question):

    key = get_cache_key(question)

    return redis_client.get(key)


def cache_answer(question, answer, ttl=3600):

    key = get_cache_key(question)

    redis_client.setex(
        key,
        ttl,
        answer
    )