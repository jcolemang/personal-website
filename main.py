#!/usr/bin/env python2

import webapp2
import os
from jinja2 import Environment, FileSystemLoader

template_path = os.path.join(os.path.dirname(__file__), 'templates')

jinja_env = Environment(loader=FileSystemLoader([template_path]))


class BaseHandler(webapp2.RequestHandler):

    def get(self):
        template = self.get_template()
        values = self.get_values()
        self.response.write(template.render(values))

    def get_template(self):
        raise RuntimeError('Must override get_template()')

    def get_values(self):
        return {'path': self.request.path}


class MainHandler(BaseHandler):
    def get_template(self):
        return jinja_env.get_template('home.html')


class BlogDirectoryHandler(BaseHandler):
    def get_template(self):
        return jinja_env.get_template('blog-directory.html')


class BlogPostHandler(BaseHandler):
    def get(self, post_name):
        template = self.get_template(post_name)
        self.response.write(template.render({}))

    def get_template(self, post_name):
        directory = 'blog-posts/' + post_name + '.html'
        return jinja_env.get_template(directory)


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogDirectoryHandler),
    ('/blog/(\w+)', BlogPostHandler),
], debug=True)
