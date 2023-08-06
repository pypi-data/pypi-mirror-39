# coding: utf-8

import ZODB
import ZODB.POSException
import ZODB.DemoStorage
import readonlystorage
import pytest


class TestReadOnlyStorage:
    def test(self):
        rw_storage = ZODB.DemoStorage.DemoStorage()
        rw_db = ZODB.DB(rw_storage)
        ro_storage = readonlystorage.ReadOnlyStorage(rw_storage)
        ro_db = ZODB.DB(ro_storage)

        rw_conn = rw_db.open()
        rw_conn.root()["foo"] = "bar"
        rw_conn.transaction_manager.commit()
        rw_conn.close()

        ro_conn = ro_db.open()
        assert "bar" == ro_conn.root()["foo"]
        with pytest.raises(ZODB.POSException.ReadOnlyError):
            ro_conn.root()["foo"] = "anything"
            ro_conn.transaction_manager.commit()
        ro_conn.close()
