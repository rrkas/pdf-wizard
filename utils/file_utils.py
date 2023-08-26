import datetime, uuid


def get_file_name():
    now = datetime.datetime.now()
    return f"{now.year:04d}{now.month:02d}{now.day:02d}_{uuid.uuid4().hex}"
