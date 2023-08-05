import asyncio
import logging
import transaction
import ZODB, ZODB.FileStorage
from BTrees import OOBTree
from opsdroid.database import Database

_LOGGER = logging.getLogger(__name__)


class ZODBDatabase(Database):

    async def connect(self, opsdroid=None):
        _LOGGER.debug("Connecting ZODB")
        filepath = self.config.get("database", "opsdroid.fs")
        self.storage = ZODB.FileStorage.FileStorage(filepath)
        self.db = ZODB.DB(self.storage)
        self.connection = self.db.open()
        self.root = self.connection.root
        if not hasattr(self.root, "memory"):
            with transaction.manager:
                self.root.memory = OOBTree.OOBTree()
        self.memory = self.root.memory
        _LOGGER.info("ZODB database connected")

    async def put(self, key, value):
        with transaction.manager:
            self.memory[key] = value
        return True

    async def get(self, key):
        with transaction.manager:
            result = self.memory.get(key)
        return result
