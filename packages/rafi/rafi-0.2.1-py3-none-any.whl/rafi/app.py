import logging
import re
from collections import defaultdict


class App(object):
    def __init__(self, app_name):
        self.app_name = app_name
        self.log = logging.getLogger(self.app_name)
        self.routes = defaultdict(dict)
        self.request = None

    def route(self, path, methods=["GET"]):
        def decorator(f):
            self._add_route(path, methods, f)
            return f

        return decorator

    def _add_route(self, path, methods, view_func):
        methods = set(item.upper() for item in methods)
        regex = re.compile(
            re.escape(path).replace("<", "(?P<").replace(">", ">[^/]+)")
        )
        for method in methods:
            if method in self.routes[regex]:
                raise ValueError(
                    "Duplicate method '%s' detected for route '%s'.",
                    method,
                    path,
                )
            self.routes[regex][method] = view_func

    def __call__(self, request):
        # fix for empty paths
        path = "/" if not request.path else request.path
        for regex in self.routes.keys():
            match = re.fullmatch(regex, path)
            if match is None:
                continue
            if request.method not in self.routes[regex]:
                return "", 405

            self.request = request
            res = self.routes[regex][request.method](**match.groupdict())
            if isinstance(res, tuple):
                return res
            return res, 200

        return "", 404
