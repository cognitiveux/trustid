import uuid


def generate_random_uuid():
    """
    Generates a random UUID as a 32-character hexadecimal string

        Returns:
            (str): The UUID
    """
    return uuid.uuid4().hex


def serialize_request(request):
    '''
    Serializes a django.http.request object to be passed as a parameter in tasks

    Args:
        request (django.http.request):
            The request object that will be serialized
    Returns:
        dict:
            The serialized dictionary
    '''
    username = None

    try:
        username = request.user.email
    except Exception as e:
        try:
            username = request.user.get_username()
        except Exception as e:
            username = None

    # Only the required properties for logging are serialized
    result = {
        'user': {
            'username': username,
            'id': request.user.id,
        },
        'data': request.data,
        'META': {
            'HTTP_X_FORWARDED_FOR': request.META.get('HTTP_X_FORWARDED_FOR'),
            'REMOTE_ADDR': request.META.get('REMOTE_ADDR'),
            'HTTP_USER_AGENT': request.META.get('HTTP_USER_AGENT'),
            'HTTP_AUTHORIZATION': request.META.get('HTTP_AUTHORIZATION'),
        },
    }
    return result


def request_details(request):
    '''
    Returns details for the request as a string. This is a helper function for logging.

    Args:
        request (rest_framework.request.Request):
            The request object

    Returns:
        <ip> <user> if possible else <ip>
    '''
    username = None

    if isinstance(request, dict):
        user = request.get('user')
        if user:
            username =  user.get('username')
        else:
            username = request['data'].get('username')
    else:
        try:
            username = request.user.email or request.data.get('email')
        except AttributeError as e:
            username = None

    if not username:
        username = 'anonymous'

    return get_ip_address(request)+" - "+username+" - "


def get_ip_address(request):
    '''Returns the client's IP address from the `request` META attribute

        Args:
            request (rest_framework.request.Request): The request object

        Returns:
            ip (str): Client's IP address
    '''
    ip = None

    if isinstance(request, dict):
        x_forwarded_for = request['META']['HTTP_X_FORWARDED_FOR']

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request['META']['REMOTE_ADDR']
    else:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')

        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')

    return ip
