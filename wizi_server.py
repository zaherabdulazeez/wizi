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
import base64

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', title='Wizi Visualization')

class WSHandler(tornado.websocket.WebSocketHandler):
	
	def open(self):
		print "new connection"
		img = pngtobase64()
		self.write_message(img)

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


class WiziServer(object):
	"""Instantiate this class with an wizi interactor object.
	"""
	def __init__(self,iren):
		self.iren = iren
		self.iren.start()		

	def start(self,port=8000):
		app = Application()
		http_server = tornado.httpserver.HTTPServer(app)
		http_server.listen(options.port)
		myIP = socket.gethostbyname(socket.gethostname())
		print "tornado server started at %s" % myIP
		tornado.ioloop.IOLoop.instance().start()

def pngtobase64(fname='wizi.png'):
	with open(fname, 'rb') as imagefile:
		image_str = base64.b64encode(imagefile.read())
	return image_str

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port)
	myIP = socket.gethostbyname(socket.gethostname())
	print "tornado server started at %s" % myIP
	tornado.ioloop.IOLoop.instance().start()