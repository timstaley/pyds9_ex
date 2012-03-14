
pyds9_ex
======================

A lightweight wrapper class and associated functions, 
adding extended functionality and ease of use to the pyds9 package. 

---------------------------------------------------------------------

The main aims are: 
 - To provide python bindings for common actions, in order to avoid frequent use of error prone ``ds9.set(some_command_string)``, etc.
 - To make complex interactions with multiple frames more streamlined.

Prerequisites: ds9, xpa, pyds9

Note that this mini-project is very much in the alpha stage - essentially I threw it together during an afternoon, and I'm currently adding functionality as and when I need it. As such, there is not yet any packaging or testing, let alone suggestion of reliability. 
*(Note a quick and dirty method of installation is to symlink the ds9_ex folder from ~/.local/python2.7/site-packages )*


I've decided to publish the code anyway as 
 - It might attract the attention of collaborators / perhaps this sort of functionality could be integrated into the original pyds9 package.
 - It might save somebody some time by functioning as a template.
 - I'm trying to move towards a practice of 'publish everything when possible' , and this seemed like a good place to start.

I'm also quietly pleased with the ``@per_frame`` function decorator. 
This takes a function and produces a duplicate version
that will apply the action to all frames, bound with the prefix ``all_``,
so for example

    ``foo.zoom_to(4) # zoom active frame to 4x``

becomes: 

    ``foo.all_zoom_to(4) # zoom all frames to 4x``

This is particularly useful when say, panning around filtered and original versions of an image, in tandem. (And saves on code duplication!)


Comments and collaborators very welcome!

