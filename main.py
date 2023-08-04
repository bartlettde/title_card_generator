# Import the required libraries
from tkinter import *
from PIL import ImageGrab
import cv2
import os, random

# Create an instance of tkinter frame or window
win=Tk()

# Set the size of the window
win.geometry("600x600")

# Create a list of the created lines during the design stage
linesCoord = []
linesDrawn = []

# Variable to track whether the user has clicked once or twice
click_num=0

# These variables track the first point for each line placed by the user
x1 = None
y1 = None

# This variable tracks the the last line drawn to the canvas, for the line visualition
oldLine = None

# This variable determines the folder in which the images will be saved
outputFolder = "output/"

# Set the required colours
backgroundColour = "black"
textColour = "white"


def draw_line(event):

   global click_num # tracks whether the click was the start of a line, or the end of a line
   global x1,y1 # if clicked before, these are the X and Y coordinates
   global linesCoord # The list of user drawn lines, tracked for the animation step
   global linesDrawn

   if click_num==0:
      x1=event.x
      y1=event.y
      click_num=1
   else:
      x2=event.x
      y2=event.y

   # Draw the line in the given co-ordinates
   try:
      line = canvas.create_line(x1,y1,x2,y2, fill=textColour, width=1)
      linesDrawn.append(line)
      linesCoord.append([x1, y1, x2, y2])
      click_num = 0
      canvas.update()
   except:
      pass


def visualiseLine(event):

   global x1, y1 # the position of the line start point
   global oldLine # the line drawn in the previous frame

   currentx, currenty = event.x, event.y # Finding the current position of the cursor

   # Only visualising the line if the user has already clicked once
   if click_num == 1:
      if oldLine == None:
         # This is the users first time clicking in the canvas
         oldLine = canvas.create_line(x1, y1, currentx, currenty, fill=textColour, width=1)
      else:
         canvas.delete(oldLine) # Remove the old line
         oldLine = canvas.create_line(x1, y1, currentx, currenty, fill=textColour, width=1) # add the new line

   canvas.update()


def undo(event):
   global linesCoord
   global click_num
   global oldLine

   if click_num == 1:
      pass
   else:
      try:
         canvas.delete(linesDrawn[-1])
         canvas.delete(oldLine)
         canvas.update()
         linesDrawn.pop()
         linesCoord.pop()
      except:
         pass

   
def animate(event):

   global linesCoord # the list of lines created by the user
   global canvas

   totalFrames = 50 # Change this variable to increase the number of frames that will be created

   currentFrame = 0 # indexing variable

   while currentFrame < totalFrames:
      print("PROGRESS: Frame " + str(currentFrame) + " / Frame " + str(totalFrames))
      for l in linesCoord:
         # for each line the user drew
         numLines = 0 # Another indexing variable
         # Creating the random lines around the user drawn lines. 
         while numLines < 5:
            canvas.create_line(l[0] + random.randint(-3, 3),l[1] + random.randint(-3, 3),l[2] + random.randint(-3, 3),l[3] + random.randint(-3, 3), fill=textColour, width=1)
            numLines += 1

      # Canvas must be updated here, otherwise the screen shot is taken before the lines are drawn
      canvas.update()

      # call function that captures the screen
      screenCapture(canvas, currentFrame)

      # Remove all the lines, before looping
      canvas.delete("all")
      currentFrame += 1

   createVideo()
   # Close the window once all frames have been created
   canvas.quit()
    
    
def screenCapture(canvas, currentFrame):
    # get the position of the top left of the window
    # extra pixels are added here to account for the mac frame around the canvas.
    x=canvas.winfo_rootx() + 15
    y=canvas.winfo_rooty() + 70
    # Find the position of the bottom right of the window
    # Again offsets have been added here to account for the mac frame around the canvas
    x1= x + (canvas.winfo_reqwidth() * 2) - 25
    y1= y + (canvas.winfo_reqheight() * 2) - 75
    # Capture image and save to user specified location
    ImageGrab.grab().crop((x,y,x1,y1)).save(outputFolder + "test" + str(currentFrame) + ".png")


def createVideo():
   video_name = outputFolder + 'video.mp4'

   images = [img for img in os.listdir(outputFolder) if img.endswith(".png")]
   frame = cv2.imread(os.path.join(outputFolder, images[0]))
   height, width, layers = frame.shape

   video = cv2.VideoWriter(video_name, cv2.VideoWriter_fourcc(*'mp4v'), 5, (width,height))

   for image in images:
      video.write(cv2.imread(os.path.join(outputFolder, image)))

   cv2.destroyAllWindows()
   video.release()


# Create a canvas widget
canvas=Canvas(win, width=600, height=600, background=backgroundColour)
canvas.grid(row=0, column=0)

# These call the functions defined above when specific events happen
canvas.bind('<Button-1>', draw_line)
win.bind('<Motion>', visualiseLine)
win.bind("<space>", animate)
win.bind('<BackSpace>', undo)

win.mainloop()