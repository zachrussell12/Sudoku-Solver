import os
import cv2
import pytesseract
import numpy as np
from puzzle_extractor import PuzzleExtractor
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
from keras.models import load_model

model_paths = [r'cnn_model_0.keras', r'cnn_model_1.keras', r'cnn_model_2.keras', r'cnn_model_3.keras', r'cnn_model_4.keras', r'cnn_model_5.keras', r'cnn_model_6.keras', r'cnn_model_7.keras', r'cnn_model_8.keras', r'cnn_model_9.keras']

class Image_Processer:

    def __init__(self, progressBarWidget, rootWindow):
        pytesseract.pytesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        self.progressBar = progressBarWidget
        self.rootWindow = rootWindow
        self.models = [load_model(model_path) for model_path in model_paths]

    def ensemble_predict(self, input_image):
        predictions = np.zeros((11,))

        for model in self.models:
            preds = model.predict(input_image)[0]
            predictions += preds

        averaged_predictions = predictions / len(self.models)
        final_prediction = np.argmax(averaged_predictions)
        return final_prediction

    def preprocess_image(self, image):

        image = cv2.resize(image, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        _, binary_image = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

        kernel = np.ones((2, 2), np.uint8)
        thickened = cv2.dilate(binary_image, kernel, iterations=1)

        final_image = cv2.bitwise_not(thickened)

        return final_image

    def extract_digits_from_grid(self, image_path=None, raw_image=None):

        if image_path is not None:
            image = PuzzleExtractor().find_sudoku_grid(image_path)
        else:
            image = raw_image

        cleaned_image = self.preprocess_image(image)

        #cnn_model = load_model(r"cnn_model_100.keras", custom_objects={'BatchNormalization': BatchNormalization, 'Dropout': Dropout})

        cv2.imwrite("processed_image.jpg", cleaned_image)
        print("image processed")

        grid_size = 9
        h, w = cleaned_image.shape
        cell_h = h // grid_size
        cell_w = w // grid_size

        grid = [['0' for _ in range(grid_size)] for _ in range(grid_size)]
        
        padding = 18
        for i in range(grid_size):
            for j in range(grid_size):

                cell = cleaned_image[max(0, i*cell_h-padding):(i+1)*cell_h+padding, max(0, j*cell_w-padding):(j+1)*cell_w+padding]

                #cell_filename = os.path.join("cellimages/", f'{image_path.split("/")[4].replace(".jpg", "_")}cell_{i}_{j}.png')
                #cv2.imwrite(cell_filename, cell)

                cell = cv2.resize(cell, (128,128))
                cell = cell / 255.0

                cell = np.stack((cell,)*3, axis=-1)
                cell = np.reshape(cell, (1, 128, 128, 3))

                cell_text = self.ensemble_predict(cell)

                print(f"Prediction for location {i}, {j}: {cell_text}")
                
                if cell_text == 10:
                    cell_text = ""

                grid[i][j] = cell_text

                self.progressBar.step()
                self.rootWindow.update()

        self.progressBar.destroy()

        return grid
    

    def get_progress(self):
        return self.progress
