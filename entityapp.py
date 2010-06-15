import getentities
import datetime
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from render import render

try:
    from simplejson import json
except ImportError:
    try:
        import django.utils.simplejson as json
    except ImportError:
        import json

class JinjaRequestHandler(webapp.RequestHandler):
    def render(self, tmplname, context, mimetype='text/html'):
        self.response.headers['Content-Type'] = mimetype
        self.response.out.write(render(tmplname, context))

class MainPage(JinjaRequestHandler):
    def get(self):
        self.render("index.html", {})

class UrlPage(JinjaRequestHandler):
    def get(self):
        url = self.request.get('url', '')
        if not url.startswith('http'):
            url = 'http://' + url
        context = {}
        if url is not None:
            try:
                entities = getentities.get_entities(url)
            except getentities.DownloadError, e:
                context['error'] = "Couldn't download external resource: %s" % str(e)
                entities = dict(entities=[], categories=[])
            context.update(dict(url=url.encode('utf8'),
                                entities=entities.get('entities'),
                                categories=entities.get('categories'),
                               ))
        self.render("url.html", context)

class RefPage(JinjaRequestHandler):
    def get(self):
        ref = self.request.get('ref', '')
        context = dict(ref=ref,
                       name=self.request.get('name', None))
        try:
            refs = getentities.get_entity_references(ref)
        except getentities.DownloadError, e:
            context['error'] = "Couldn't download external resource: %s" % str(e)
            refs = []
        context['refs'] = refs
        self.render("ref.html", context)

class EntitiesPage(webapp.RequestHandler):
    def get(self):
        url=self.request.get('url')
        if not url.startswith('http'):
            url = 'http://' + url
        try:
            entities = getentities.get_entities(url)
        except getentities.DownloadError, e:
            entities = {'error': 'Download Error: %s.  Try reloading' % str(e)}
            self.response.set_status(400)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(entities))

class EntityPage(webapp.RequestHandler):
    def get(self):
        url=self.request.get('ref')
        try:
            refs = getentities.get_entity_references(url)
        except getentities.DownloadError, e:
            refs = {'error': 'Download Error: %s.  Try reloading' % str(e)}
            self.response.set_status(400)
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(refs))

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/url', UrlPage),
                                      ('/ref', RefPage),
                                      ('/entities', EntitiesPage),
                                      ('/entity', EntityPage),
                                      ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
