import vtk
import wizi

coneSource = vtk.vtkConeSource()
coneSource.SetResolution(10)

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(coneSource.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(actor)

renderWindow = vtk.vtkRenderWindow()

# this is just a workaround or a hack - Later it has to be corrected . On connection open get the browser window size
renderWindow.SetSize(1366,659)
renderWindow.AddRenderer(renderer)

iren = wizi.VTKCameraTrackBallInteractor(renderWindow)
server = wizi.WiziServer(iren)
server.start()