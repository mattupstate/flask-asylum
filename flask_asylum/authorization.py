# -*- coding: utf-8 -*-
"""
    flask_asylum.authorization
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Stock authorization policies
"""

from datetime import timedelta

from flask import g
from itsdangerous import TimedJSONWebSignatureSerializer


class AuthorizationPolicy(object):
      """An object representing an authorization policy.
      """

      def permits(self, identity, permission, context=None):
          """Return `True` if the identity is allowed the permission in the current context,
          else return `False`.
          """
          raise NotImplementedError

      def authorized_userid(self, identity):
          """Return the unique identifier of the user as described by the identity or `None` if no
          user exists related to the identity.
          """
          raise NotImplementedError


class MultiAuthorizationPolicy(AuthorizationPolicy):

    def __init__(self, policies):
        self._policies = policies or []

    def permits(self, identity, permission, context=None):
        for policy in self._policies:
            if policy.permits(context, identity, permission):
                return True
        return False

    def authorized_userid(self, identity):
        for policy in self._policies:
            userid = policy.authorized_userid(identity)
            if userid:
                return userid

