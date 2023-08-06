from contextlib import contextmanager
import logging
import threading
from typing import Any, Dict

import attr
from sqlalchemy import create_engine, event
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.pool import StaticPool
from sqlalchemy.schema import MetaData
from sqlalchemy_utils import force_auto_coercion

__all__ = ["Base", "Factory", "Session", "orm_session", "initialize_storage",
           "release_storage", "configure_storage", "get_secret_key"]

logger = logging.getLogger("chaosplatform")
Factory = sessionmaker(autocommit=False, autoflush=True)
Session = scoped_session(Factory)
_engines_lock = threading.Lock()
_engines = {}

# Ensure uniform naming across various providers, help migrations...
# see https://alembic.zzzcomputing.com/en/latest/naming.html
meta = MetaData(naming_convention={
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
})
Base = declarative_base(metadata=meta)
Base.query = Session.query_property()

# let sqlalchemy utils help us converting data in/out of the database
force_auto_coercion()


@attr.s
class RelationalStorage:
    engine: Engine = attr.ib(default=None)


def initialize_storage(config: Dict[str, Any]) -> RelationalStorage:
    """
    Initialize the storage.
    """
    engine = get_engine(config)
    return RelationalStorage(engine)


def configure_storage(storage: RelationalStorage):
    """
    Configure the underlying storage and create all tables.
    """
    engine = storage.engine
    meta = Base.metadata
    if not meta.is_bound():
        Factory.configure(bind=engine, autocommit=False, autoflush=True)
        Session.configure(bind=engine, autocommit=False, autoflush=True)
        meta.bind = engine
    meta.create_all(bind=engine)


def release_storage(storage: RelationalStorage):
    """
    Release the storage resources.
    """
    logger.info("Releasing relational database storage")
    Session.remove()
    Factory.close_all()
    storage.engine.dispose()


@contextmanager
def orm_session() -> Session:
    """
    Wrap a function so that it commits or rollbacks to/from the
    database when it returns.
    """
    try:
        yield Session
        Session.commit()
    except Exception:
        Session.rollback()
        raise
    finally:
        Session.close()


def get_secret_key() -> str:
    return "secret"


###############################################################################
# Internals
###############################################################################
def get_engine(config: Dict[str, Any]) -> Engine:
    """
    Get a SQLAlchemy engine for the connection URI in the configuration.

    The `config` mapping must contain the `db` key which maps to a dictionary.
    That dictionary must have at least the `uri` key, set to the connection
    string.

    ```
    config = {
        "db": {
            "uri": "sqlite:///:memory:"
            "debug": False
        }
    }
    ```

    When an engine was initialized for a given connection string, it is
    returned directly.
    """
    db_config = config.get("db")
    sa_debug = True if db_config.get("debug") else False
    conn_uri = db_config.get("uri")

    # in most cases, let SQLAlchemy pick the right connection pooling
    pool = None
    connect_args = None

    with _engines_lock:
        if conn_uri in _engines:
            logger.info("Relational database storage already initialized")
            return _engines[conn_uri]

        logger.info("Initializing relational database storage")
        # when running SQLite, we must enable this directive on each new
        # connexion made to the database to enable foreign key
        if conn_uri.startswith("sqlite"):
            pool = StaticPool
            connect_args = {
                "check_same_thread": False
            }

            @event.listens_for(Engine, "connect")
            def set_sqlite_pragma(dbapi_connection, connection_record):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()

        engine = create_engine(
            conn_uri, poolclass=pool, connect_args=connect_args, echo=sa_debug)
        _engines[conn_uri] = engine
        logger.info("Relational database setup")

    return engine
