import webapp2
import jinja2
import os
import re
import hw2_1

template_dir = os.path.join(os.path.dirname(__file__), 'template')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

class MainHandler(BaseHandler):
    def get(self):
        self.render('main.html')
    
class Rot13Handler(BaseHandler):
    def get(self):
        self.render('rot13-form.html')
                                
    def post(self):
        rot13 = ''
        text = self.request.get('text')
        if text:
#            rot13 = text.encode('rot13')
            rot13 = rot13(text)
            rot13 = escape_html(rot13)
        self.render('rot13-form.html', text = rot13)  

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/hw2_1',Rot13Handler)
], debug=True)
