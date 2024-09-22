import cv2
import numpy as np

class PuzzleExtractor:
    
    def __init__(self):
        pass
    
    def find_sudoku_grid(self, image_path):

        image = cv2.imread(image_path)
        original_image = image.copy()

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        
        thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
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
            
            cropped_image = original_image[y:y+h, x:x+w]
            
            cv2.imwrite("sudoku_cropped.png", cropped_image)
            
            return cropped_image
        else:
            print("Grid not found.")
            return None