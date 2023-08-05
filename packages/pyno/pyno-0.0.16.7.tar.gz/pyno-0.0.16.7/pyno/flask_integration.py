""" This file defines an object that defines methods to ease integration with Flask"""

def bond(l, name):
    'Utility function used to easily bind a name to a function'
    l.__name__ = name
    return l

class FlaskInterface:
    def __call__(self, **kwargs): # pragma: no cover
        if hasattr(self, 'kwargs'):
            self.kwargs.update(kwargs)
        def page_caller(environ, start_response, **kwargs):
            """ When called a TreeNode object will act like a WSGI application.
            This way they can be passed directly as output in for instance Flask apps, and served using the wsgi
            reference implementation easily """
            start_response('200 OK', [('Content-type', 'text/HTML charset=utf-8')])
            return [str(self)]
        return page_caller

    def attach(self, app, route):
        app.route(route)(bond(self, route))
