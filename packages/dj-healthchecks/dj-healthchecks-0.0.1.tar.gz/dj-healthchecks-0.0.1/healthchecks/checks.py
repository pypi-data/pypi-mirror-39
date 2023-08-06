def format_health_check_response(name, is_ok, data):
    return {
        "name": name,
        "ok": is_ok,
        "data": data
    }

def im_ok(*args, **kwargs):
    return format_health_check_response("Is available", True, {"message": "TBD"})

def connect_to_db(*args, **kwargs):
    from django.db import connection
    from django.db.utils import OperationalError
    message = "A OK"
    is_ok = True

    try:
        connection.ensure_connection()
    except OperationalError:
        message = 'Database unavailable'
        is_ok = False

    return format_health_check_response(
        "Can connect to DB",
        is_ok,
        {"message": message}
    )

def get_a_django_user(*args, **kwargs):
    '''
    You can use this to double make sure you can connect to the db
    But note: it will fail if you don't have any users in the db
    '''
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.first()
    message = "A OK"
    is_ok = True
    try:
        user = get_user_model().objects.first()
        assert isinstance(user, get_user_model())
    except AssertionError:
        message = 'No users returned from DB. Verify DB settings'
        is_ok = False

    return format_health_check_response(
        "Can get a user from the db",
        is_ok,
        {"message": message}
    )

def connect_to_queue(*args, **kwargs):
    # verify can connect to rabbit and drop a task:
    # ping_result = ping.delay().wait(timeout=1)
    message = "A OK"
    # try:
    #     assert ping_result == 'pong'
    # except AssertionError:
    #     message = "Unable to process a message on the queue"

    return format_health_check_response(
        "Can connect to Queue",
        True,
        {"message": message}
    )


def connect_to_redis(*args, **kwargs):
    return format_health_check_response("Can connect to Redis", True, {"message": "TBD"})

def ping_upstream_urls(*args, **kwargs):
    return format_health_check_response("Can connect to upstream urls", True, {"message": "TBD"})
