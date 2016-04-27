# from vtk import vtkSphereSource, vtkPolyDataMapper, vtkActor, vtkRenderer, vtkRenderWindow, vtkWindowToImageFilter, vtkGraphicsFactory, vtkPNGWriter, vtkRenderWindowInteractor
import vtk

from wizi_offscreen import VTKOffScreen, VTKCameraTrackBallInteractor

# graphics_factory = vtk.vtkGraphicsFactory()
# graphics_factory.SetOffScreenOnlyMode(1)
# graphics_factory.SetUseMesaClasses(1)

coneSource = vtk.vtkConeSource()
coneSource.SetResolution(10)

# mask=vtk.vtkMaskPoints()
# mask.SetInputConnection(coneSource.GetOutputPort())
# mask.SetOnRatio(10)
# mask.RandomModeOn()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(coneSource.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)

iren = VTKCameraTrackBallInteractor(renderWindow)
iren.start()





# renderWindow.SetOffScreenRendering(1)
# renderWindow.Render()
cam = renderer.GetActiveCamera()
vp = cam.GetViewUp()
vplane = cam.GetViewPlaneNormal()
pos = cam.GetPosition()




# iren = vtk.vtkRenderWindowInteractor()
# istyle = vtk.vtkInteractorStyleTrackballCamera()
# iren.SetInteractorStyle(istyle)
# iren.SetRenderWindow(renderWindow)
# iren.Initialize()
# iren.Start()

# renderer.SetBackground(1,1,1)

 
# renderWindow.Render()

# renderWindow.SetAlphaBitPlanes(1)


 
# def reset_all():
# 	cam.SetViewUp(vup)
# 	dump()

# def reset():
# 	vup=cam.GetViewUp()
# 	cam.SetViewUp(-vup[2], vup[0], vup[1])
# 	dump()

# def rotate_x(angle):
# 	cam.OrthogonalizeViewUp()
# 	cam.Azimuth(angle)
# 	dump()

# def rotate_y(angle):
# 	cam.OrthogonalizeViewUp()
# 	cam.Elevation(angle)
# 	dump()

# def dump():
# 	windowToImageFilter = vtk.vtkWindowToImageFilter()
# 	writer = vtk.vtkPNGWriter()
# 	# renderWindow.Render()
# 	windowToImageFilter.SetInput(renderWindow)
# 	windowToImageFilter.SetMagnification(3)
# 	# windowToImageFilter.SetInputBufferTypeToRGBA()
# 	writer.SetFileName("cone.png")
# 	writer.SetInputConnection(windowToImageFilter.GetOutputPort())

# 	windowToImageFilter.Update()
# 	writer.Update()
# 	writer.Write()
