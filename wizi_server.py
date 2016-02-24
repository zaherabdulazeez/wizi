try:
	import tornado
except ImportError:
	raise RuntimeError("wizi requires tornado")

import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.websocket
import socket

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', title='Visualization')

class WSHandler(tornado.websocket.WebSocketHandler):
	def open(self):
		print "new connection"
	
	def on_message(self,message):
		print message
	
	def on_close(self):
		print "connection closed"
		
class Application(tornado.web.Application):
	def __init__(self):
		handlers = [
		(r'/',IndexHandler),
		(r'/ws',WSHandler)
		]
		settings = {
		'template_path' : 'templates',
		'static_path' : 'static'
		}
		debug = True
		tornado.web.Application.__init__(self,handlers,debug,**settings)

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	myIP = socket.gethostbyname(socket.gethostname())
	print "tornado server started at %s" % myIP
	tornado.ioloop.IOLoop.instance().start()