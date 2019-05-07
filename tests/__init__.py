from sqlalchemy import MetaData, ForeignKeyConstraint, Table
from sqlalchemy.engine import reflection
from sqlalchemy.sql.ddl import DropConstraint, DropTable

from dh_backend.models import db


def _db_drop_all_force(db):
    # From http://www.sqlalchemy.org/trac/wiki/UsageRecipes/DropEverything

    conn = db.engine.connect()

    # the transaction only applies if the DB supports
    # transactional DDL, i.e. Postgresql, MS SQL Server
    trans = conn.begin()

    inspector = reflection.Inspector.from_engine(db.engine)

    # gather all data first before dropping anything.
    # some DBs lock after things have been dropped in
    # a transaction.
    metadata = MetaData()

    tbs = []
    all_fks = []

    for table_name in inspector.get_table_names():
        fks = []
        for fk in inspector.get_foreign_keys(table_name):
            if not fk['name']:
                continue
            fks.append(
                ForeignKeyConstraint((), (), name=fk['name'])
                )
        t = Table(table_name,metadata,*fks)
        tbs.append(t)
        all_fks.extend(fks)

    for fkc in all_fks:
        conn.execute(DropConstraint(fkc))

    for table in tbs:
        conn.execute(DropTable(table))

    trans.commit()


def setup_db(app):
    """Method used to build a database"""
    db.app = app
    db.create_all()


def teardown_db():
    """Method used to destroy a database"""
    db.session.remove()
    _db_drop_all_force(db)
    db.session.bind.dispose()


def clean_db():
    """Clean all data, leaving schema as is
    Suitable to be run before each db-aware test. This is much faster than
    dropping whole schema an recreating from scratch.
    """
    for table in reversed(db.metadata.sorted_tables):
        db.session.execute(table.delete())
