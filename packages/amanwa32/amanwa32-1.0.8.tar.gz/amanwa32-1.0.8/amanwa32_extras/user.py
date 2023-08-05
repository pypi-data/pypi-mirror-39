import jwt
from datetime import datetime, timedelta
from amanwa32_extras.dal import Simpledal

TOKEN_SECRET = 'secret'
EXPIRE_DAYS = 2
dalobj = Simpledal()

class User(object): #Reference base class

    def get_id(self):
        """Returns this user's unique ID, which can be an integer or string."""

    @classmethod
    def get_by_auth_token(cls, user_id, token):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """


    @classmethod
    def get_by_auth_password(cls, auth_id, password):
        """Returns a user object, validating password.

        :param auth_id:
            Authentication id.
        :param password:
            Password to be checked.
        :returns:
            A user object, if found and password matches.
        :raises:
            ``auth.InvalidAuthIdError`` or ``auth.InvalidPasswordError``.
        """

    @classmethod
    def create_auth_token(cls, user_id):
        """Creates a new authorization token for a given user ID.

        :param user_id:
            User unique ID.
        :returns:
            A string with the authorization token.
        """



    @classmethod
    def delete_auth_token(cls, user_id, token):
        """Deletes a given authorization token.

        :param user_id:
            User unique ID.
        :param token:
            A string with the authorization token.
        """

    @classmethod
    def create_user(cls, auth_id, unique_properties=None, **user_values):
         '''

         :param auth_id:
         :param unique_properties:
         :param user_values:
         :return:
         '''

class userinfo(object):
    '''
        stores user information
    '''
    def __init__(self, **kwargs):
        for k,v in kwargs.items():
            setattr(self, k, v)


def jwt_encode(user_id):
    timestamp = datetime.utcnow()
    exp = timestamp + timedelta(days=EXPIRE_DAYS)
    print(timestamp, exp)

    return jwt.encode({'user_id': user_id, 'timestamp': int(timestamp.timestamp()), 'exp': int(exp.timestamp())}, TOKEN_SECRET, algorithm='HS256')


class User1(User):

    def __init__(self, auth_id, **kwargs):
        allkeyvals = {'auth_id':auth_id}
        allkeyvals.update(**kwargs)
        self.ob = userinfo(**allkeyvals)


    def get_id(self):
        """Returns this user's unique ID, which can be an integer or string."""
        return self.ob.auth_id



    @classmethod
    def get_by_auth_token(cls, user_id, token):
        """Returns a user object based on a user ID and token.

        :param user_id:
            The user_id of the requesting user.
        :param token:
            The token string to be verified.
        :returns:
            A tuple ``(User, timestamp)``, with a user object and
            the token timestamp, or ``(None, None)`` if both were not found.
        """
        # decoded_jwt_json = jwt.decode(token, TOKEN_SECRET)
        try:
            decoded_jwt_json = jwt.decode(token, TOKEN_SECRET)
            # print(decoded_jwt_json)
            if decoded_jwt_json['user_id'] == user_id:
                return (dalobj.get('auth_id','nullid'), decoded_jwt_json['timestamp'])

        except Exception as e:
            # raise (e)
            return (None, None)

    @classmethod
    def get_by_auth_password(cls, auth_id, password):
        """Returns a user object, validating password.

        :param auth_id:
            Authentication id.
        :param password:
            Password to be checked.
        :returns:
            A user object, if found and password matches.
        :raises:
            ``auth.InvalidAuthIdError`` or ``auth.InvalidPasswordError``.
        """
        #TODO: password handling?? should this be implemented everytime? Third Party Authentication (TPA) won't need passwords.


    @classmethod
    def create_auth_token(cls, user_id):
        """Creates a new authorization token for a given user ID.

        :param user_id:
            User unique ID.
        :returns:
            A string with the authorization token.
        """

        auth_token = jwt_encode(user_id)

        return auth_token

    @classmethod
    def delete_auth_token(cls, user_id, token):
        """Deletes a given authorization token.

        :param user_id:
            User unique ID.
        :param token:
            A string with the authorization token.
        """
        #TODO: ? jwt doen't have an explicit deletion, workaournd to be decided


    @classmethod
    def create_user(cls, auth_id, unique_properties=None, **user_values):
        """Creates a new user.

        :param auth_id:
            A string that is unique to the user. Users may have multiple
            auth ids. Example auth ids:

            - own:username
            - own:email@example.com
            - google:username
            - yahoo:username

            The value of `auth_id` must be unique.
        :param unique_properties:
            Sequence of extra property names that must be unique.
        :param user_values:
            Keyword arguments to create a new user entity. Since the model is
            an ``Expando``, any provided custom properties will be saved.
            To hash a plain password, pass a keyword ``password_raw``.
        :returns:
            A tuple (boolean, info). The boolean indicates if the user
            was created. If creation succeeds, ``info`` is the user entity;
            otherwise it is a list of duplicated unique properties that
            caused creation to fail.
        """


        u = cls(auth_id=auth_id, **user_values)
        dalobj.insert(auth_id=u)
        return u