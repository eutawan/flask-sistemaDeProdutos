import uuid

def is_uuid(value):
    try:
        uuid_obj = uuid.UUID(value, version=4)
        return str(uuid_obj) == value
    except ValueError:
        return False
    
def generate_uuid():
    return str(uuid.uuid4())