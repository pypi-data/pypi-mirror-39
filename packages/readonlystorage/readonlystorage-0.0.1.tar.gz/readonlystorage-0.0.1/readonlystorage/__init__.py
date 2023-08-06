import ZODB.POSException
import ZODB.interfaces
import zope.interface


class ReadOnlyStorage:
    def __init__(self, storage):
        self.storage = storage
        if ZODB.interfaces.IBlobStorage.providedBy(storage):
            self.loadBlob = storage.loadBlob
            self.temporaryDirectory = storage.temporaryDirectory
            if hasattr(storage, "openCommittedBlobFile"):
                self.openCommittedBlobFile = storage.openCommittedBlobFile

            zope.interface.alsoProvides(self, ZODB.interfaces.IBlobStorage)

    def getName(self):
        return "%s readonly" % (self.storage.getName())

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.getName())

    def __len__(self):
        return len(self.storage)

    def close(self, *args, **kwargs):
        self.storage.close(*args, **kwargs)

    def getSize(self, *args, **kwargs):
        return self.storage.getSize(*args, **kwargs)

    def history(self, *args, **kwargs):
        self.storage.history(*args, **kwargs)

    def isReadOnly(self):
        return True

    def getTid(self, *args, **kwargs):
        return self.storage.gitTid(*args, **kwargs)

    def lastTransaction(self, *args, **kwargs):
        return self.storage.lastTransaction(*args, **kwargs)

    def load(self, *args, **kwargs):
        return self.storage.load(*args, **kwargs)

    def loadBefore(self, *args, **kwargs):
        return self.storage.loadBefore(*args, **kwargs)

    def loadSerial(self, oid, serial):
        raise ZODB.POSException.POSKeyError(oid)

    def new_oid(self):
        raise ZODB.POSException.ReadOnlyError()

    def pack(self, pack_time, referencesf):
        raise ZODB.POSException.ReadOnlyError()

    def registerDB(self, *args, **kwargs):
        pass

    def sortKey(self, *args, **kwargs):
        return self.storage.sortKey(*args, **kwargs)

    def store(self, oid, serial, data, version, transaction):
        raise ZODB.POSException.StorageTransactionError(self, transaction)

    def storeBlob(self, oid, oldserial, data, blobfilename, version, transaction):
        raise ZODB.POSException.StorageTransactionError(self, transaction)

    def tpc_abort(self, transaction):
        pass

    def tpc_begin(self, transaction):
        raise ZODB.POSException.ReadOnlyError()

    def tpc_finish(self, transaction, func=lambda: None):
        raise ZODB.POSException.StorageTransactionError(self, transaction)

    def tpc_transaction(self):
        return None

    def tpc_vote(self, transaction):
        raise ZODB.POSException.StorageTransactionError(self, transaction)
