# Latex-Figure-Integration
This project is a template for integrating Latex (specifically Overleaf) with python code for creating figures. The strength of the repository is to combine multiple subfigures into a combined, fully customizeable figure, which can automatically get sent to your Latex directory, meaning that you don't have to pause your writing for manually copying and pasting subfigures.

Personally, I used this technique for writing my master thesis, which has saved me an immense amount of time. I would therefore like to stretch that I think **It is completely worth it to spend one or two full day(s) on getting this setup working for you, that time will be repayed by the time this saves!** With that, I would also put a disclaimer that I simply got this working for myself, but have not set out to build a fully functional plug-and-play repository for general use. With that out of the way, let's get into the specifics of how to get this thing working for you!

## Prerequisities
To work with this repository, you need the following things:
- A Windows system
- An overleaf account that has access to the Dropbox or Git synchronization feature
- A github or dropbox account
- Inkscape, an image editor
- UV package manager for python (makes everything 1000x simpler...)

## Install guide
Start by making sure to download all the required software and validate that all is working. After that, clone this repository onto your local device and start up a new brach (or fork) with your own name **Please do not edit the `main` branch!!**

On your own branch, you will need to edit a few things. First of all, let's set up your virtual environment. This is easily done with the UV package manager that you have installed! Simply open a terminal (`ctrl+shift+~` in VS Codes). In principle, you should be able to simply run

` uv sync `

This should trigger UV to start downloading the dependencies as indicated in the `pyproject.toml` file, it should also create a virtual environment for you to work in! After this, we can start editing specific files to get the project working on your desktop! Start by going to the *src/general/data_handling.py* file, at the top you will find one system specific variable: `PATH_TO_OVERLEAF`. In this example, I use Overleaf's synchronization feature with Dropbox to get the figures from this repository into my Overleaf. To this end, you should supply your system path to that local Dropbox account. If you use Overleaf's integrated synchronization with Git, you can omit this variable and the corresponding export command!

## How to use
This repository combines a few services, the general workflow is as follows:
1. Use **Jupyter Notebooks** in python to edit and create each subfigure of each figure that you want to make. An example of how to create these subfigures is given in *notebooks/figure1.ipynb*. I would advise making a separate Jupyter Notebook for each "combined figure" that you want to make! After making the figure, you can save it with the custom `save_figure()` function. This function will save a .svg file containing the subfigure in the corresponding subfolder of the "subfigures" folder. Repeatedly running this function simply updates this file, such that you can keep updating your subfigures as much as you want! The global variables from the *src/general/plotting.py* file will help you to make each figure the exact size you want, while keeping things like linestyles of fits, data colors and fontsizes consistent throughout your entire project!
2. Once you have created all required subfigures for your combined figure, it is time to use *Inkscape* to combine them. Start by opening Inkscape and creating a new document (third tab). This will start you off with a blank A4 page. For the sizes in the plots to make sense, it is crucial to **set the document width** to 157.42mm, you can do this through *File > Document Properties > Width*. Once you have done this and if you've used the `COL` and `COL_DUB` variables for the width of your subfigures, you should now *never adjust the sizes of your subfigures in Inkscape!*. Moreover, you now also never have to adjust the size of your figures in overleaf anymore! You can import the SVGs of your subfigures by going to *File > Import* (or `CTRL+I`). Navigate to the subfigures folder and select the subfigure that you would like to import. You will get a popup, where you should select the option that links the file location to the Inkscape file. To confirm, go to *Edit > Preferences > Imported images*. Make sure that the `SVG import" option is set to "link" and the box to automatically reload images is ticked. You can test if your setup worked by changing the subfigure you just imported in the Jupyter Notebook and observing it changing in Inkscape after a few seconds! Using Inkscape, you can now form all kinds of diagrams and arrows around your graphs and if you don't change the size of your subfigures, you will not need to change anything if you want a simple color change!
3. Once your sufficiently satisfied with the figure in Inkscape, it is time to **export it to your Overleaf**. You can do this through python and *don't have to manually push the export buttons!*. On the bottom of the example notebook of "figure1", there is a single cell that performs the export. By running the `update_combined_figure()` function with the correct figure number, Inkscape will start to export your creation into a few locations:
    1. A .png file will be exported to the corresponding subfolder in the *figures* folder.
    2. A .pdf file will be exported to this same subfolder
    3. A .pdf file will be uploaded in the folder of your Overleaf synchronized Dropbox (or you will use Git).
In principle you should now have your updated .pdf file of your figure in Overleaf (with Dropbox it takes 5-10 seconds). Note that you do not need to have Inkscape opened or active in order to do this, meaning that small adjustments to the subfigures can be made without opening Inkscape!
4. Whether through Dropbox or Git, your Overleaf should now be synchronized to get the exported image files. You can simply start **writing in Overleaf** (or any other Latex editor) now and quickly update figures by making the small adjustments and running the `update_combined_figure()` function when they are ready!

## Disclaimer
As I mentioned, I do not expect this project to already be a complete work with fully functional features. Please let me know if things are not working out for you, especially if there are fundamental issues with the code or setup! You can always reach me through timo.dolne@gmail.com or by leaving a comment in the Github page! If you have ideas for improvements or changes then also let me know, as I'm more than happy to let the base repository get better and stronger as time goes on.

Good luck!