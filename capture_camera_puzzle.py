import cv2
from PIL import Image, ImageTk
import time
import numpy as np

class Camera_Puzzle:

    def __init__ (self):
        self.vc = None
        self.isGrid = 0
        self.puzzle_grid = None
        pass

    def order_corners(self, points):

        rect = np.zeros((4, 2), dtype="float32")

        s = points.sum(axis=1)
        rect[0] = points[np.argmin(s)]
        rect[2] = points[np.argmax(s)]

        diff = np.diff(points, axis=1)
        rect[1] = points[np.argmin(diff)]
        rect[3] = points[np.argmax(diff)]

        return rect
    
    def transform_rect(self, image, points):

        rect = self.order_corners(points)
        (topleft, topright, bottomright, bottomleft) = rect

        widthA = np.sqrt(((bottomright[0] - bottomleft[0]) ** 2) + ((bottomright[1] - bottomleft[1]) ** 2))
        widthB = np.sqrt(((topright[0] - topleft[0]) ** 2) + ((topright[1] - topleft[1]) ** 2))
        maxWidth = max(int(widthA), int(widthB))

        heightA = np.sqrt(((topright[0] - bottomright[0]) ** 2) + ((topright[1] - bottomright[1]) ** 2))
        heightB = np.sqrt(((topleft[0] - bottomleft[0]) ** 2) + ((topleft[1] - bottomleft[1]) ** 2))
        maxHeight = max(int(heightA), int(heightB))

        dest = np.array([[0,0], [maxWidth - 1, 0], [maxWidth - 1, maxHeight - 1], [0, maxHeight - 1]], dtype="float32")

        M = cv2.getPerspectiveTransform(rect, dest)
        warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))

        return warped
    
    def correct_skew(self, image, approx):
        if len(approx) == 4:
            
            approx = approx.reshape(4, 2)
            warped = self.transform_rect(image, approx)
            return warped
        else:
            return image


    def checkforPuzzle(self, image):
        found = False
        original_image = image.copy()
        cropped_image = image.copy()
        original_image = cv2.resize(original_image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(original_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        largest_contour = None
        max_area = 0
        for contour in contours:
            epsilon = 0.02 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) == 4:
                area = cv2.contourArea(contour)
                if area > max_area:
                    max_area = area
                    largest_contour = approx

        if largest_contour is not None:
            x, y, w, h = cv2.boundingRect(largest_contour)
            aspect_ratio = w / float(h)

            if 0.9 < aspect_ratio < 1.1 and max_area > 1000:

                cropped_image = self.correct_skew(original_image, largest_contour)
                cropped_image = cv2.addWeighted(cropped_image, 1, np.zeros(cropped_image.shape, cropped_image.dtype), 0, 75)


                cv2.rectangle(original_image, (x,y), (x+w, y+h), (124, 237, 43), 3)
                cv2.putText(original_image, "Sudoku Grid", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 1, (124, 237, 43), 2, cv2.LINE_AA)
                found = True
        
        return original_image, found, cropped_image

    def getCameraFeed(self, webcamFeed, on_puzzle_found_callback):

        if self.vc == None:
            self.vc = cv2.VideoCapture(0)

        if not self.vc.isOpened():
            print("Error: Webcam already in use.")
            return

        _, frame = self.vc.read() 

        if frame is None:
            print("Error: Failed to capture webcam feed")
            return
        
        opencv_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA) 

        puzzle_image, flag, cropped_Image = self.checkforPuzzle(opencv_image)
        
        captured_image = Image.fromarray(puzzle_image) 
        
        photo_image = ImageTk.PhotoImage(image=captured_image) 
        
        webcamFeed.imgtk = photo_image 
        
        webcamFeed.configure(image=photo_image) 

        if flag:
            self.isGrid += 1

        if self.isGrid >= 100:

            captured_image = Image.fromarray(cropped_Image) 
        
            photo_image = ImageTk.PhotoImage(image=captured_image) 

            self.puzzle_grid = cropped_Image
            
            webcamFeed.imgtk = photo_image 
            
            webcamFeed.configure(image=photo_image)  

            on_puzzle_found_callback(self.puzzle_grid)
        
            self.stopCamera()

        else:
            webcamFeed.after(20, self.getCameraFeed, webcamFeed, on_puzzle_found_callback)

    def stopCamera(self):
        if self.vc is not None:
            self.vc.release()
            self.vc = None