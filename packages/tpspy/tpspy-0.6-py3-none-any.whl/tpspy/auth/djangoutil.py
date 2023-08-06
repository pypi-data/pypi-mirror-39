# -*- coding: utf-8 -*-

try:
    from urllib.request import quote
    from urllib.parse import urljoin
except ImportError:
    from urllib import quote
    from urlparse import urljoin
from django.shortcuts import redirect
from django.conf import settings
from django.http import JsonResponse

from .authutil import AuthUtil


class TpsAuthMiddleware(object):
    def __init__(self, get_response=None):
        self.get_response = get_response

        self.sys_id = getattr(settings, 'TPS_SYS_ID', None)
        if not self.sys_id:
            raise ValueError("MUST set: TPS_SYS_ID in settings.py")

        self.secret = getattr(settings, 'TPS_SYS_SECRET', None)
        if not self.secret:
            raise ValueError("MUST set: TPS_SYS_SECRET in settings.py")

        self.tps_login_url = getattr(settings, 'TPS_LOGIN_URL', None)
        if not self.tps_login_url:
            raise ValueError("MUST set: TPS_LOGIN_URL in settings.py")

        self.tps_check_token_url = getattr(settings, 'TPS_CHECK_TOKEN_URL', None)
        if not self.tps_check_token_url:
            raise ValueError("MUST set: TPS_CHECK_TOKEN_URL in settings.py")

        self.auth = AuthUtil()
        self.auth.set_secret(secret=self.secret)

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.
        response = None
        if hasattr(self, 'process_request'):
            response = self.process_request(request)
        if not response:
            response = self.get_response(request)
        if hasattr(self, 'process_response'):
            response = self.process_response(request, response)
        return response

    def process_view(self, request, view, *args, **kwargs):
        user_agent = request.META.get("HTTP_USER_AGENT", None)
        if request.is_ajax():
            # 如果是 API 请求, 需要跳转到 refer 页面
            redirect_uri = request.META.get('HTTP_REFERER', "")
        else:
            redirect_uri = request.build_absolute_uri(request.get_full_path())

        # 无需鉴权
        if getattr(view, 'tps_auth_exempt', False):
            print("TpsAuthMiddleware.process_view, auth_exempt, uri: ", redirect_uri)
            return None

        token = request.GET.get("token", None)
        if token is None:
            token = request.META.get("HTTP_TOKEN", None) or request.COOKIES.get("token")

        ok, user_or_msg = self.auth.check_token(token)
        if ok:
            print("TpsAuthMiddleware.process_view, user: %s, token: %s" % (user_or_msg, token))
            setattr(view, "user", user_or_msg)
        else:
            print("TpsAuthMiddleware.process_view, token is invalid, will login again, token: %s" % token)
            login_url = urljoin(self.tps_login_url, "?sys_id=%s&redirect_uri=%s&check_uri=%s&user_agent=%s" %
                                (quote(self.sys_id), quote(redirect_uri), quote(self.tps_check_token_url), quote(user_agent)))
            print("TpsAuthMiddleware.process_view, login_url: %s" % login_url)

            # see: https://github.com/axios/axios/issues/932
            # AJAX 请求会返回包含 location 的 JSON, 由 js 代码执行具体的跳转
            if request.is_ajax():
                resp = JsonResponse(dict(location=login_url, status="ok", msg="need login..."))
                resp.status_code = 401
                return resp
            else:
                return redirect(login_url)


def deco_auth_exempt(func):
    """
    对无需进行 TPS 鉴权的 view, 使用这个 decorator

    对于 class-based view, 请参考:

    urls.py
    -------
    url('^somePath$', deco_auth_exempt(views.SomeView.as_view())),

    请注意上面的方式是不能区分 GET/POST/DELETE ...
    """

    # 对 view 函数添加属性 tps_auth_exempt, 标记不需要鉴权
    func.tps_auth_exempt = True
    return func
