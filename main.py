#!/usr/bin/env python2

import webapp2
import os
import logging
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

    def page_not_found(self):
        self.response.write("<h1>Page not found</h1>")


class NotFoundHandler(BaseHandler):
    pass


class MainHandler(BaseHandler):
    def get_template(self):
        return jinja_env.get_template('home.html')


class BlogDirectoryHandler(BaseHandler):
    def get_template(self):
        return jinja_env.get_template('blog-directory.html')


class BlogPostHandler(BaseHandler):
    def get(self, post_name):
        post_name = post_name.lower()
        try:
            template = self.get_template(post_name)
            self.response.write(template.render({}))
        except:
            logging.error('Error getting post:' + post_name)
            self.page_not_found()

    def get_template(self, post_name):
        directory = 'blog-posts/' + post_name + '.html'
        template = jinja_env.get_template(directory)
        return template


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/blog', BlogDirectoryHandler),
    ('/blog/(\w+)', BlogPostHandler),
], debug=True)
