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
#Import the sub-aplications i've made
import myrot13
import mydates
import myblog

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")


class MainHandler(webapp2.RequestHandler):
    def get(self):
        pass

    def post(self):
        pass


app = webapp2.WSGIApplication([('/', mydates.DatesHandler),
                               ('/thanks', mydates.ThanksHandler),
                               ('/unit3/blog', myblog.BlogFront),
                               ('/unit3/blog/newpost', myblog.NewPostHandler),
                               ('/unit3/blog/([0-9]+)', myblog.PostHandler),
                               ('/unit2/rot13', myrot13.Rot13Handler)
                               ], 
                               debug=True)


