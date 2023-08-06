Readonly Storage
================

A simple read-only wrapper around a regular [ZODB](https://github.com/zopefoundation/ZODB) storage.

```python
import ZODB

# Let's set a read-write DemoStorage
rw_storage = ZODB.DemoStorage.DemoStorage()
rw_db = ZODB.DB(rw_storage)

# And now, let's set a ReadOnlyStorage around it.
ro_storage = readonlystorage.ReadOnlyStorage(rw_storage)
ro_db = ZODB.DB(ro_storage)

# Now, add some data
rw_conn = rw_db.open()
rw_conn.root()["foo"] = "bar"
rw_conn.transaction_manager.commit()
rw_conn.close()

# Read the data
ro_conn = ro_db.open()
assert "bar" == ro_conn.root()["foo"]

ro_conn.root()["foo"] = "anything"
ro_conn.transaction_manager.commit() # This one would emit a ZODB.POSException.ReadOnlyError!

ro_conn.close()
```
