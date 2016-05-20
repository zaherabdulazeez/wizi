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
import json

from tornado.options import define, options

define("port", default=8000, help="run on the given port", type=int)

class IndexHandler(tornado.web.RequestHandler):
	def get(self):
		self.render('index.html', title='Wizi Visualization')


class WSHandler(tornado.websocket.WebSocketHandler):
	def initialize(self,iren):
		self.iren = iren
		print "OK Zaher"
		self.observer = Observer(self.iren)

	def open(self):
		print "new connection OK Zaher"
		img = pngtobase64()
		self.write_message(img)

	def on_message(self,message):
		msg = json.loads(message)
		print msg
		azimuth = msg['azimuth']
		elevation = msg['elevation']
		img = self.observer.rotated_img(azimuth,elevation)
		self.write_message(img)
		# print msg
	
	def on_close(self):
		print "connection closed"

		
class Application(tornado.web.Application):
	def __init__(self,iren):
		handlers = [
		(r'/',IndexHandler),
		(r'/ws',WSHandler,dict(iren=iren))
		]
		settings = {
		'template_path' : 'templates',
		'static_path' : 'static'
		}
		debug = True
		tornado.web.Application.__init__(self,handlers,debug,**settings)


class WiziServer(object):
	"""Instantiate this class with an wizi interactor object(aka iren).
	"""
	def __init__(self,iren):
		self.iren = iren
		self.iren.start()		

	def start(self,port=8000):
		app = Application(self.iren)
		http_server = tornado.httpserver.HTTPServer(app)
		http_server.listen(options.port)
		myIP = socket.gethostbyname(socket.gethostname())
		print "tornado server started at %s" % myIP
		tornado.ioloop.IOLoop.instance().start()


class Observer(object):
	""" WSHandler instantiates this class and ask it to keep an eye on the iren"""
	def __init__(self,iren):
		self.iren = iren

	def rotated_img(self, azimuth,elevation):
		#ignore small angles of rotation in any direction. prevent unnecessary rotation
		if abs(azimuth) <= 5:
			self.iren.rotate_y(elevation)
		if abs(elevation) <= 5:
			self.iren.rotate_x(azimuth)
		else:
			self.iren.rotate_x(azimuth)
			self.iren.rotate_y(elevation)

		tmp = pngtobase64()
		return tmp

#method that converts the png file to base 64
def pngtobase64(fname='wizi.png'):
	with open(fname, 'rb') as imagefile:
		image_str = base64.b64encode(imagefile.read())
		img = "data:image/png;base64,"+ image_str
	return img

if __name__ == '__main__':
	tornado.options.parse_command_line()
	app = Application()
	http_server = tornado.httpserver.HTTPServer(app)
	http_server.listen(options.port, address="10.196.26.145")
	myIP = socket.gethostbyname(socket.gethostname())
	print "tornado server started at %s" % myIP
	tornado.ioloop.IOLoop.instance().start()