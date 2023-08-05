# -*- coding: utf-8 -*-
# Copyright 2011 webapp3 AUTHORS.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
webapp3_extras.appengine.auth.models
====================================

Auth related models.
"""
import time

try:
    from ndb import model
except ImportError:  # pragma: no cover
    from google.appengine.ext.ndb import model

from webapp3_extras import auth
from webapp3_extras import security


class User(model.Expando):
    """Stores user authentication credentials or authorization ids."""

    #: The model used to ensure uniqueness.
    unique_model = Unique
    #: The model used to store tokens.
    token_model = UserToken

    created = model.DateTimeProperty(auto_now_add=True)
    updated = model.DateTimeProperty(auto_now=True)
    # ID for third party authentication, e.g. 'google:username'. UNIQUE.
    auth_ids = model.StringProperty(repeated=True)
    # Hashed password. Not required because third party authentication
    # doesn't use password.
    password = model.StringProperty()

    def get_id(self):
        """Returns this user's unique ID, which can be an integer or string."""
        return self._key.id()

    def add_auth_id(self, auth_id):
        """A helper method to add additional auth ids to a User

        :param auth_id:
            String representing a unique id for the user. Examples:

            - own:username
            - google:username
        :returns:
            A tuple (boolean, info). The boolean indicates if the user
            was saved. If creation succeeds, ``info`` is the user entity;
            otherwise it is a list of duplicated unique properties that
            caused creation to fail.
        """
        self.auth_ids.append(auth_id)
        unique = '%s.auth_id:%s' % (self.__class__.__name__, auth_id)
        ok = self.unique_model.create(unique)
        if ok:
            self.put()
            return True, self
        else:
            return False, ['auth_id']

    @classmethod
    def get_by_auth_id(cls, auth_id):
        """Returns a user object based on a auth_id.

        :param auth_id:
            String representing a unique id for the user. Examples:

            - own:username
            - google:username
        :returns:
            A user object.
        """
        return cls.query(cls.auth_ids == auth_id).get()

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
        token_key = cls.token_model.get_key(user_id, 'auth', token)
        user_key = model.Key(cls, user_id)
        # Use get_multi() to save a RPC call.
        valid_token, user = model.get_multi([token_key, user_key])
        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            return user, timestamp

        return None, None

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
        user = cls.get_by_auth_id(auth_id)
        if not user:
            raise auth.InvalidAuthIdError()

        if not security.check_password_hash(password, user.password):
            raise auth.InvalidPasswordError()

        return user

    @classmethod
    def validate_token(cls, user_id, subject, token):
        """Checks for existence of a token, given user_id, subject and token.

        :param user_id:
            User unique ID.
        :param subject:
            The subject of the key. Examples:

            - 'auth'
            - 'signup'
        :param token:
            The token string to be validated.
        :returns:
            A :class:`UserToken` or None if the token does not exist.
        """
        return cls.token_model.get(user=user_id, subject=subject,
                                   token=token)

    @classmethod
    def create_auth_token(cls, user_id):
        """Creates a new authorization token for a given user ID.

        :param user_id:
            User unique ID.
        :returns:
            A string with the authorization token.
        """
        return cls.token_model.create(user_id, 'auth').token

    @classmethod
    def validate_auth_token(cls, user_id, token):
        return cls.validate_token(user_id, 'auth', token)

    @classmethod
    def delete_auth_token(cls, user_id, token):
        """Deletes a given authorization token.

        :param user_id:
            User unique ID.
        :param token:
            A string with the authorization token.
        """
        cls.token_model.get_key(user_id, 'auth', token).delete()

    @classmethod
    def create_signup_token(cls, user_id):
        entity = cls.token_model.create(user_id, 'signup')
        return entity.token

    @classmethod
    def validate_signup_token(cls, user_id, token):
        return cls.validate_token(user_id, 'signup', token)

    @classmethod
    def delete_signup_token(cls, user_id, token):
        cls.token_model.get_key(user_id, 'signup', token).delete()

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
        assert user_values.get('password') is None, \
            'Use password_raw instead of password to create new users.'

        assert not isinstance(auth_id, list), \
            'Creating a user with multiple auth_ids is not allowed, ' \
            'please provide a single auth_id.'

        if 'password_raw' in user_values:
            user_values['password'] = security.generate_password_hash(
                user_values.pop('password_raw'), length=12)

        user_values['auth_ids'] = [auth_id]
        user = cls(**user_values)

        # Set up unique properties.
        uniques = [('%s.auth_id:%s' % (cls.__name__, auth_id), 'auth_id')]
        if unique_properties:
            for name in unique_properties:
                key = '%s.%s:%s' % (cls.__name__, name, user_values[name])
                uniques.append((key, name))

        ok, existing = cls.unique_model.create_multi(k for k, v in uniques)
        if ok:
            user.put()
            return True, user
        else:
            properties = [v for k, v in uniques if k in existing]
            return False, properties

