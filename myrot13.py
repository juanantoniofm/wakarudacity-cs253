
import webapp2
import cgi


rot13code = '''
<!DOCTYPE html>
<html>
  <head>
    <title>Unit 2 Rot 13</title>
  </head>

  <body>
    <h2>Enter some text to ROT13:</h2>
    <form method="post">
      <textarea name="text" style="height: 100px; width: 400px;">%(input)s</textarea>
      <br>
      <input type="submit">
    </form>
  </body>

</html>
'''

def escape_html(s):
    return cgi.escape(s, quote = True)

class Rot13Handler(webapp2.RequestHandler):
    def write_rot(self,text):
        self.response.out.write(rot13code % {"input": text})
        
    def rot13(self,text):
        return escape_html(text.encode('rot13'));
    
    def get(self):
        self.write_rot(self.request.get('text') );
        
    def post(self):
        self.write_rot(self.rot13(self.request.get('text')));
