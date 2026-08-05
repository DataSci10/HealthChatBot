import pickle
import redis

from langchain_core.documents import Document
from langchain_core.stores import BaseStore


class RedisDocStore(BaseStore[str, Document]):

    def __init__(
        self,
        host="localhost",
        port=6379,
        db=0,
        prefix="docstore:"
    ):
        self.client = redis.Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=False,
        )
        self.prefix = prefix

    def _key(self, key: str):
        return f"{self.prefix}{key}"

    def mget(self, keys):
        docs = []

        for key in keys:
            value = self.client.get(self._key(key))

            if value is None:
                docs.append(None)
            else:
                docs.append(pickle.loads(value))

        return docs

    def mset(self, key_value_pairs):
        for key, value in key_value_pairs:
            self.client.set(
                self._key(key),
                pickle.dumps(value)
            )

    def mdelete(self, keys):
        if keys:
            self.client.delete(
                *[self._key(k) for k in keys]
            )

    def yield_keys(self, prefix=None):
        pattern = self.prefix

        if prefix:
            pattern += prefix

        pattern += "*"

        for key in self.client.scan_iter(pattern):
            yield key.decode().replace(self.prefix, "")