# Sudoku Solver!

### Overview

This weekend project was a challenge I took on to strengthen my knowledge in AI, machine learning, and image recognition. The project was broken up into multiple stages and utilized multiple different technologies to accomplish.

### Video Demo

https://github.com/user-attachments/assets/de547165-30a8-4269-99c9-b45172f19932

### Technologies and Methodologies Leveraged

#### OpenCV

OpenCV was utilized for the following tasks in this project:
- Reading in webcam data to display in the GUI
- Extracting sudoku grid from the webcam data or uploaded images using contour identification
- Cropping and de-skewing puzzles extracted from the webcam.
- Pre-processing sudoku grid images so they can be read by the ML model

#### Ensemble Classifier using CNN Models

A custom group of 10 Convolutional Neural Network (CNN) models were created in Google Colab to do the number classification for the sudoku grids submitted by the user. The model was trained over 1000 epochs with a batch size of 128 using an early stop mechanism with a patience of 20 watching the validation accuracy of the model. Each model had the following architecture:

![Architecture of the CNN model using in the ensemble classifier](./media/model-architecture.jpg)

Each models was trained using an original dataset of approximately 1,081 images of digits ranging from 1-9 and blank spaces from 7 different online puzzles. Additional data was augmented from the 1,081 original images using various transformations including zooms, horizontal shifts, vertical shifts, shears, and brightness fluctuations. The original dataset plus the augmented data resulted in a total dataset size of approximately 21,620 images for each model to be trained on.

Each model was then downloaded locally and used in the project. Using OpenCV, each cell in the sudoku grid was given to the models one by one and each model produced a prediction. After each model made a prediction on one cell, their predictions were averaged out and finalized.

#### Backtracking (DFS Search)

After reading the digits in the sudoku puzzle and where the blank spaces were, the information was compiled into a 2D array and passed to the solving agent. This agent used a simple backtracking method to solve the puzzle. A basic step-by-step of what the agent does is described below:

1. Find first (or next) empty cell and figure out all possible moves in that cell
2. If any valid moves, add those possible puzzle states to the node stack
3. Pop the last added puzzle state off the stack and make it the current state
4. Check goal state, is it solved? If not, repeat.

This essentially means the agent is running through all possible combinations of moves for the puzzle to solve it. It is able to solve "easy", "medium", and "hard" puzzles in under a minute. It only starts to struggle when attempting even harder difficulties on some sites like "evil", "extreme", and "excruciating". Nevertheless this method is a proven way to solve the puzzle eventually. I would like to explore more efficient options in the future though.

### Challenges Encountered and Overcame

#### Digit Recognition

I originally wanted to use the Pytesseract modele to perform OCR to extract the digits from the sudoku grids. After trying to read the puzzle as a whole, trying to read each cell individually, and a range of different image pre-processing techniques and combinations I ultimately came to the conclusion that it wasn't working as I had hoped. At its best, I was able to read puzzles from one site reliably (albeit very slowly as well), but I wanted this project to be able to read in any sudoku puzzle that was given to it. That meant it needed to be able to handle different sized numbers, different fonts, and different line thicknesses. I came to the conclusion that the best way to perform the digit recognition would be to train my own Convolutional Neural Network model.

#### Training the CNN Model

Constructing the model and its training data was not hard to do initially. I already had experience creating machine learning models for other tasks like my hybrid CNN-LSTM [here.](https://github.com/zachrussell12/Hybrid-CNN-LSTM-Time-Series-Forecasting) The model was performing well on the training data but it was severly underperforming on the validation data. Since the original model I made was clearly overfitting, I made a litany of changes that ultimately improved the validation accuracy to 100%. The changes to the model included:
- Adding a second CNN layer to the model
- Adding dropout after both CNN/Batch Normalization layers (this significantly helped boost validation accuracy)
- Adjusting the hyperparameters of the model (optimizer, learning rate, # of CNN filters, kernel size, dropout percentage)

A portion of these changes were done with the help of the Keras Tuner. This helped me programatically hone in on the best hyperparameters for the model instead of aimlessly trying different combinations. Even after all these changes though, the model was still performing with about an 88% accuracy. At this point in the process I only had about 500 images of digits + blank spaces for my dataset. I believed there was no further improvement that could be made of the model so I turned to making a larger dataset and tweaking the input images. The following changes were made to the dataset:
- Changed the size of the images from a shape of 98 x 98 to a shape of 128 x 128
- Pre-processed the images the same way they would be processed by my OpenCV code in the solver so the digits were uniform to the model
- Added approximately 581 photos to the dataset
- Augmented the original 1,081 images to create a larger dataset of over 20,000

Once the dataset for the model grew to over 20,000, the model became much getter at recognizing the different digits and achieved a validation accuracy of 100%.

####  Further Improving Digit Recognition by the CNN Model

Although the model achieved a strong validation accuracy, when it was finally implemented into the sudoku solver it was still struggling. With each puzzle it was given, it was routinely getting at least 1 to 2 digits wrong. Even though the model achieved a validation accuracy of 100% in real-world scenarios it was failing to recognize some of them. To further improve the sudoku solvers ability to read the puzzles, I turned to implementing an ensemble classifier to recognize the digits in the puzzle. This would allow multiple models each to have a say in the prediction instead of giving the entire decision to just one model.

To create the ensemble of models, 10 different models were each trained one after the other (no bagging or boosting them) and saved to my local environment. From there, each model was loaded and used in predicting each cell in a puzzle. A cell is extracted from the grid, each model makes its prediction, all the predictions are averaged out, and the final prediction is put forth.

Using an ensemble of models instead of a single model for classification improved the sudoku solvers ability to read digits completely. It can now read almost any puzzle it is given from a screenshot or webcam so long as it is of good quality (well-lit, in focus).


### Future Improvements

- Optimize and increase speed to read puzzles
- Try different method for solving sudoku puzzles to speed up solving time
- Leverage PyAutoGUI to find a sudoku puzzle on the user's screen and extract it from there so the user no longer needs to upload a screenshot of a puzzle
- Improve digit recognition further
- Improve OpenCV puzzle recognition
- Error Handling
- Metrics related to the puzzle solving
