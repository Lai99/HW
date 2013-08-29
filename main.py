import webapp2
import jinja2
import os
import re
import hw2_1
import hw2_2

from google.appengine.ext import db

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
#HW3
#####################
def blog_key(name='default'):
    return db.Key.from_path('blogs', name)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p = self) 
        
class BlogFrontHandler(BaseHandler):
    def get(self):
        posts = db.GqlQuery("SELECT * FROM Post ORDER BY created DESC LIMIT 10")
        self.render('front.html', posts = posts)

    def post(self):
        self.redirect("/hw3/newpost.html")
        
class PostPageHandler(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id),parent=blog_key())
        post = db.get(key)

        if not post:
            self.error(404)
            return
        
        self.render('permalink.html', post = post)

class NewPostHandler(BaseHandler):
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(parent=blog_key(), subject=subject,content=content)
            p.put()
            self.redirect('/hw3/%s' % str(p.key().id()))
        else:
            error = "empty!"
            self.render("newpost.html", subject=subject, content=content, error=error)

#####################        

#HW2        
#####################    
class Rot13Handler(BaseHandler):
    def get(self):
        self.render('rot13-form.html')
                                
    def post(self):
        rot = ''
        text = self.request.get('text')
        if text:
#            rot = text.encode('rot13')
            rot = hw2_1.rot13(text)
            rot = hw2_1.escape_html(rot)
        self.render('rot13-form.html', text = rot)

class SignUpHandler(BaseHandler):
    def get(self):
        self.render('signup-form.html')

    def post(self):
        error = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = {'username':username, 'email':email}

        if not hw2_2.valid_username(username):
            params['error_username'] = "That's not a valid username."
            error = True
        if not hw2_2.valid_password(password):
            params['error_password'] = "That wasn't a valid password."
            error = True
        elif password != verify:
            params['error_verify'] = "Your passwords didn't match."
            error = True

        if not hw2_2.valid_email(email):
            params['error_email'] = "That's not a valid email."
            error = True
            
        if error:
            self.render('signup-form.html', **params)
        else:
            self.redirect('/hw2_2/welcome?username=' + username)
      
class Welcome(BaseHandler):    
    def get(self):
        username = self.request.get('username')
        if hw2_2.valid_username(username):
            self.render('welcome.html',username = username)
        else:
            self.redirect('/hw2_2')
#####################

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/hw2_1',Rot13Handler),
    ('/hw2_2',SignUpHandler),
    ('/hw2_2/welcome',Welcome),
    ('/hw3/?',BlogFrontHandler),
    ('/hw3/newpost',NewPostHandler),
    ('/hw3/([0-9]+)',PostPageHandler),
], debug=True)


