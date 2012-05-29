# udacity.com cs253. Unit 3 Homework, build a blog.
# wakaru44 at gmail

import os
import webapp2
import jinja2
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)


def render_str(template, **params):
    """ taken from udacity.com 
    """
    t = jinja_env.get_template(template)
    return t.render(params)
    
error="where the hell"

# Blog things from the solutions :S
#########################################

def blog_key(name = "default"):
    return db.Key.from_path('blogs', name)


class Post(db.Model):
    subject = db.StringProperty(required= True)
    content = db.TextProperty(required= True)
    created = db.DateTimeProperty(auto_now_add = True)
    last_modified = db.DateTimeProperty(auto_now = True)
    
    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str("post.html", p=self)
    

class MyHandler(webapp2.RequestHandler):
        
    def write(self, *a, **kw):
        """ taken from udacity.com 
        """
        self.response.out.write(*a, **kw)
        
    def render_str(self, template, **params):
        """ taken from udacity.com 
        """
        return render_str(template, **params)
        
    def render ( self , template, **kw):
        """ taken from udacity.com 
        """
        self.write(self.render_str(template, **kw))
        
    
class BlogFront(MyHandler):
    """ lists the 10 first entries in the blog """
    def get(self):
        posts = db.GqlQuery("select * from Post order by created desc limit 10")
        self.render('front.html', posts = posts, texto = help(posts[0]) )
        self.write(dir(posts[0]))
        #self.write("mola---------")
        #self.write(posts[0].content)
        
class PostHandler(MyHandler):
    """ manages the permalinks to the posts """
    def get(self, post_id):
        """ get the url, make an id, look for it, and show the article
        """
        key = db.Key.from_path('Post', int(post_id), parent=blog_key())
        post = db.get(key)
        
        if not post:
            #self.render("front.html", error= "No hemos encontrado el post")
            self.error(404)
            return

        #self.render("post.html", p = post, post_id=post.key().id(), texto = post.content )
        self.render("permalink.html", p = post)

               
class NewPostHandler(MyHandler):
    """ offers input to make a new post. Requires subject and text"""
    def get(self):
        self.render("newpost.html")

    def post(self):
        subject=self.request.get('subject')
        content=self.request.get('content')
        
        if content=="" and subject=="":
            errmsg="Hay que poner contenido y un titulo o asunto"
        elif subject=="" or subject == "Titulo del post":
            errmsg="Hay que poner un titulo"
        elif content=="" or content=="Nuevo post":
            errmsg="Hay que poner contenido"
        else:
            errmsg=""
            
        if errmsg=="":
            p= Post(parent = blog_key(), subject=subject,content=content )
            p.put()
            self.redirect('/unit3/blog/%s' % str( 
                                                 p.key().id() ))
        else:
            self.render("newpost.html", subject = subject, content = content, error = error)

        