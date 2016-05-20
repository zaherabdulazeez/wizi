"""This module implements offscreen renderers for wizi for different applications"""

import vtk

class VTKOffScreen(object):
	"""wizi base class that takes and renderwindow object at the end of VTK pipeline and renders it offline.Renderwindow preferably 
	should not have an interactor attached to it as wizi implements its own interaction"""
	
	def __init__(self, renderwindow):
		self.RenderWindow = renderwindow
		self.Renderer = self.get_renderer()
		self.image_count = 0

	def get_renderer(self):
		rens = self.RenderWindow.GetRenderers()
		ren = rens.GetFirstRenderer()
		return ren

	def render_offscreen(self):
		self.RenderWindow.SetOffScreenRendering(1)
		self.RenderWindow.Render()
	
	def dump_view(self,file_name):
		windowToImageFilter = vtk.vtkWindowToImageFilter()
		writer = vtk.vtkPNGWriter()

		windowToImageFilter.SetInput(self.RenderWindow)
		# windowToImageFilter.SetMagnification(3)
		writer.SetFileName(file_name)
		writer.SetInputConnection(windowToImageFilter.GetOutputPort())

		windowToImageFilter.Update()
		writer.Update()
		writer.Write()
		self.image_count +=1

	
class VTKTrackBallCameraInteractor(VTKOffScreen):
	"""wizi vtk track ball interactor class that interacts with the offscreen render window.
	Instantiate this with a vtk render window
	"""
	def  __init__(self,renderwindow):
		VTKOffScreen.__init__(self,renderwindow)
		self.camera = self.get_camera()

	def start(self):
		self.render_offscreen()
		self.reset_camera()
		self.dump_view("wizi.png")

	def get_camera(self):
		camera = self.Renderer.GetActiveCamera()
		return camera

	def reset_camera(self):
		self.Renderer.ResetCamera()
		self.dump_view("wizi.png")

	def rotate_x(self,angle):
		self.camera.OrthogonalizeViewUp()
		self.camera.Azimuth(-angle)
		self.dump_view("wizi.png")
		
	def rotate_y(self,angle):
		self.camera.OrthogonalizeViewUp()
		self.camera.Elevation(-angle)
		self.dump_view("wizi.png")

	def resize(self,x,y):
		# to be fixed for opengl errors
		self.RenderWindow.SetSize(x,y)
		# self.RenderWindow.Render()
		self.dump_view("wizi.png")