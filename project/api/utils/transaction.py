from sqlalchemy.util.compat import contextmanager

from project import print_flush, db


@contextmanager
def transaction():
    try:
        yield
        print_flush("Transaction started...")
        db.session.commit()
        print_flush("Transaction committed")
    except Exception:
        print_flush("Error in transaction")
        db.session.rollback()
        print_flush("Rollback the transaction")
        db.session.close()
        raise
