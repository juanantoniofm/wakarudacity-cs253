#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import webapp2
import string
import re
import cgi

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

form = '''
<form method="post">
    What is your birthday?
    <br>

    <label> Month
        <input type="text" name="month" value="%(month)s">
    </label>
    
    <label> Day
        <input type="text" name="day" value="%(day)s">
    </label>
    
    <label> Year
        <input type="text" name="year" value="%(year)s">
    </label>
    <div style="color: red">%(error)s</div>
    <br>
    <br>
    <input type="submit">
</form>
'''

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

months = ['January', 
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

month_abbvs = dict((m[:3].lower(), m) for m in months)

def valid_month(month):
    if month:
        short_month = month[:3].lower()
        return month_abbvs.get(short_month)

def valid_day(day):
    if day and day.isdigit():
        day = int(day)
        if day in range(1,32):
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year in range(1900,2021):
            return year
            
class MainHandler(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form %{"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(self.request.get('month'))
        day = valid_day(self.request.get('day'))
        year = valid_year(self.request.get('year'))

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend.",
                            user_month, user_day, user_year)
        else:
            self.redirect('/thanks')

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")
        
class Rot13Handler(webapp2.RequestHandler):
    def write_rot(self,text):
        self.response.out.write(rot13code % {"input": text})
        
    def rot13(self,text):
        return text;
    
    def get(self):
        self.write_rot(self.request.get('text') );
        
    def post(self):
        self.write_rot(self.rot13(self.request.get('text')));
        
app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/thanks', ThanksHandler),
                               ('/unit2/rot13', Rot13Handler)
                               ], 
                               debug=True)
