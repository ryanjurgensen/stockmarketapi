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
import urllib, time, json, webapp2
from google.appengine.ext.webapp import util
from google.appengine.api import memcache
from google.appengine.ext import deferred
from tasks import pull_stocks
    
class MainPage(webapp2.RequestHandler):
    def get(self):
        output = memcache.get("whole_nyse")
        if not output:
            output = pull_stocks()
            
        self.response.headers['Content-Type'] = 'application/json'
        self.response.out.write(json.dumps(output, sort_keys=True, indent=4))
        
app = webapp2.WSGIApplication([('/', MainPage)],debug=True)