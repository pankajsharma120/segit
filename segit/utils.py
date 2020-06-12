import hashlib
from random import randint


def get_or_none(model, *args, **kwargs):
    try:
        return model.objects.get(*args, **kwargs)
    except model.DoesNotExist:
        return None


def get_state_string():
    hash_object = hashlib.sha256(str(randint(0,9999)).encode("utf-8"))
    txnid = hash_object.hexdigest().lower()[0:32]
    return txnid
