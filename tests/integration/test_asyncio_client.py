import pytest

from bson import CodecOptions
from pymongo import ReadPreference, WriteConcern
from pymongo.mongo_client import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from motor.motor_asyncio import AsyncIOMotorDatabase


@pytest.mark.asyncio
class TestAsyncioClient(object):

    async def test_database_named_delegate(self, asyncio_client):
        assert type(asyncio_client.delegate) == MongoClient
        assert type(asyncio_client['delegate']) == AsyncIOMotorDatabase

    async def test_connection_timeout(self, asyncio_client, event_loop):
        asyncio_client.io_loop = event_loop

        with pytest.raises(ServerSelectionTimeoutError):
                await asyncio_client.admin.command('ismaster')

    async def test_get_database(self,asyncio_client, event_loop):
        asyncio_client.io_loop = event_loop

        db_name = 'foo'
        codec_options = CodecOptions(tz_aware=True)
        write_concern = WriteConcern(w=2, j=True)
        database = asyncio_client.get_database(
            db_name, codec_options, ReadPreference.SECONDARY, write_concern)

        assert type(database) == AsyncIOMotorDatabase
        assert database.name == db_name
        assert database.codec_options == codec_options
        assert database.read_preference == ReadPreference.SECONDARY
        assert database.write_concern == write_concern
