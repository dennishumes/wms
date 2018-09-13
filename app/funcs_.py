from app import db
from models import Bin

from sqlalchemy.exc import InvalidRequestError, IntegrityError, SQLAlchemyError


class Dot_(dict):
     # Usage: arr = Map(dict)
     # keyvalue = arr.key
    def __init__(self, *args, **kwargs):
        super(Dot_, self).__init__(*args, **kwargs)
        for arg in args:
            if isinstance(arg, dict):
                for k, v in arg.iteritems():
                    self[k] = v

        if kwargs:
            for k, v in kwargs.iteritems():
                self[k] = v

    def __getattr__(self, attr):
        return self.get(attr)

    def __setattr__(self, key, value):
        self.__setitem__(key, value)

    def __setitem__(self, key, value):
        super(Dot_, self).__setitem__(key, value)
        self.__dict__.update({key: value})

    def __delattr__(self, item):
        self.__delitem__(item)

    def __delitem__(self, key):
        super(Dot_, self).__delitem__(key)
        del self.__dict__[key]


def db_bulk_insert(db_obj):
    error = None
    return_obj = 0
    if len(db_obj) > 0:
        db_sess = db.session

        db_sess.bulk_save_objects(db_obj, return_defaults=True)
        for obj_ in db_obj:
            assert obj_.id is not None

        try:
            db_sess.commit()
        except SQLAlchemyError, e:
            db_sess.rollback()
            db_sess.flush() # for resetting non-commited .add()
            error = e
        finally:
            db_sess.flush() 
            db_sess.close() 

        if error:
            return_obj = "%s"%error
        
    else:
        return_obj = "No entry to process!"

    return return_obj

def addMultiBins(form,wh):
    bins_ = []
    bins = form.name.data.split(",")
    error = 0
    if bins:
        for bin_ in bins:
            isBin = Bin.query.filter_by(name=bin_).first()
            if isBin is None;
                abin = Bin(name=bin_,depth=form.depth.data,warehouse_id=wh)
                bins_.append(abin)

        error = db_bulk_insert(bins_)


    return error