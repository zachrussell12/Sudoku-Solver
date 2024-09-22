import cv2
from PIL import Image, ImageTk

class Camera_Puzzle:

    def __init__ (self):
        pass

    def getCameraFeed(self, webcamFeed):

        vc = cv2.VideoCapture(0)

        _, frame = vc.read() 
        
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 
        
        captured_image = Image.fromarray(opencv_image) 
        
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        
        webcamFeed.photo_image = photo_image 
        
        webcamFeed.configure(image=photo_image) 
        
        webcamFeed.after(10, self.getCameraFeed)