Python Tool for Visualization on the Web
========================================

##Description

Wizi provides a interface for Visulization applications like [VTK](www.vtk.org) to visualize heavy data sets in a light-weight and fast manner on the web browser. 

Wizi makes it possible to deploy heavy visualizations on run heavy visualizations on a remote server or cluster and deploy them at a remote client withot heavy infrastructure cost at the client side. Wizi uses simple image delivery mechanism to achieve this.

##Supported Applications

 - VTK ( 6 >= )
 - More to be devloped

##Requirements

 - Python 2.7 (Not tested on Python 3)


##Usage

This example uses VTK with python. 

Assemble the VTK pipeline till the _vtkRenderWindow_ & plug it to the required wizi iteractor. 

**Important:** Do not connect the RenderWindow to _vtkRenderWindowInteractor_ as it creates a pop up window.

```python
import wizi
# asseble the vtk pipeline till the renderwindow.
# give the renderwindow to wizi's interactor

iren = wizi.VTKCameraTrackBallInteractor(renderwindow)
server = wizi.WiziServer(iren)
server.start() 
```
Open the visulization in the browser  

##For Development

1. Extend the functionality to Mayavi by writing modules. Practically - any 3D application's offscreen renderwindow and Camera can be used to write a module to extend wizi's functionality to the module. Look into wizi_offscreen.py.
2. VTKCameraTrackBallInteractor is just one way of interacting with the offscreen renderwindow. More ways of interacting with renderwindow.
3. Implement diffing and compression for image delivery for faster and light-weight visualization 

##Branches 

1. master
 ...*wizi web application
2. experiment_jupyter_comm
 ...*wizi on IPython notebook with ipykernel.comm Comm(In development)
3. notebook_with_ipywidgets
 ...*wizi on IPython notebook with ipywidgets(In development)
