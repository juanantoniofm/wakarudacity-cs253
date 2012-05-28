# udacity.com cs253. Unit 3 Homework, build a blog.
# wakaru44 at gmail

import webapp2
from jinja2 import Template
from google.appengine.ext import db
 
frontTemplate = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>Wakarudacity CS253 Singalong Blog</title>
  </head>
  <body>
  {%- for post in post_list %}
    <h2>{{ post['subject']|escape }}{% if not loop.last %},{% endif %}</h2>
    <h4></h4>
    <p>{{ post['content']|escape }}{% if not loop.last %},{% endif %} </p>
  {%- endfor %}
  </body>
</html>
''')

newPostTemplate = Template(u'''\
<!DOCTYPE html>
<html>
  <head>
    <title>Wakarudacity CS253 Singalong Blog</title>
  </head>
  <body>
    <form method="post">
    <label> Asunto:
    <input type="text" value="{{ subject }}" name="subject" >
    </label>
    <br>
    
    <textarea name="content" style="height: 100px; width: 400px;">---{{ content }}</textarea>
    
    <input type="submit" id="submitbutton" >
    </form>
    <div id="error" style="color:red"> {{ error }} </div>
  </body>
</html>
''')


error="where the hell"

class Post(db.Model):
    subject = db.StringProperty(required= True)
    content = db.TextProperty(required= True)
    date = db.DateTimeProperty(auto_now_add = True)

class MyHandler(webapp2.RequestHandler):
    def render_front(self,posts):
        self.response.out.write(frontTemplate.render( posts ) )
        
    
class BlogHandler(MyHandler):
    """ lists the 10 first entries in the blog """
    def get(self):
        posts = db.GqlQuery("select * from Post order by date desc limit 10")
        # contents = db.GqlQuery("")
        # d={} TODO: como creo un diccionario de esto, elegantemente??
        for post in posts:
            self.response.out.write(post.subject)
            self.response.out.write(post.date)
            self.response.out.write(post.content)
        
        
        #self.render_front({'post_list':({'subject':"titulo primero",'content':"Lorem Ipsum"},{'subject':"titulo segundo",'content':"Lorem Ipsum sit amet"} ) })

    def post(self):
        pass
        # p = Post(subject="wwww",content="qqqq")
        # p.put()
        
       
class NewPostHandler(MyHandler):
    """ offers input to make a new post. Requires subject and text"""
    def get(self):
        self.response.out.write(newPostTemplate.render( subject="Titulo del post", content="Nuevo post" ) )

    def post(self):
        newsubject=self.request.get('subject')
        content=self.request.get('content')
        
        if content=="" and newsubject=="":
            errmsg="Hay que poner contenido y un titulo o asunto"
        elif newsubject=="":
            errmsg="Hay que poner un titulo"
        elif content=="":
            errmsg="Hay que poner contenido"
        else:
            errmsg=""
            
        if errmsg=="":
            p= Post(subject=newsubject,content=content )
            p.put()
        
        self.response.out.write( newPostTemplate.render({'subject':newsubject, 'content': content, 'error':errmsg}) )
        

class PostHandler(MyHandler):
    """ manages the permalinks to the posts """
    def get(self, postId):
        self.response.out.write(error)
        
        

    def post(self):
        pass

        