"""
User Login and Logout
=====================

"""
import logging

from imbi import base

LOGGER = logging.getLogger(__name__)


class LoginHandler(base.RequestHandler):

    def get(self, *args, **kwargs):
        self.render('login.html', error=self._error, username='',
                    next_arg=self.get_argument('next', None))

    async def post(self, *args, **kwargs):
        self.check_xsrf_cookie()
        username = self.get_body_argument('username')
        password = self.get_body_argument('password')
        if not await self.session.authenticate(username, password):
            LOGGER.debug('Session failed to authenticate')
            self.set_status(403)
            self.render('login.html',
                        error='Invalid Username or Password',
                        username=username,
                        next_arg=self.get_argument('next', None))
            return
        await self.session.save()
        self.redirect(self.get_argument('next', '/'))


class LogoutHandler(base.RequestHandler):

    async def get(self, *args, **kwargs):
        await self.session.clear()
        self._error = 'You have been logged out'
        self.redirect('/')
