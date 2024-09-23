import cv2
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import sv_ttk

#Local Classes
from image_processer import Image_Processer
from capture_camera_puzzle import Camera_Puzzle
from solve_agent import Solve_Agent

root = tk.Tk()
root.title("Sudoku Solver")
root.geometry("")

def openGUI():

    cell_vars = [[tk.StringVar() for _ in range(9)] for _ in range(9)]

    def clear_and_restart():
        for children in root.winfo_children():
            children.destroy()

        openGUI()

    def get_puzzle_from_image():

        file = filedialog.askopenfile("r", filetypes=[('JPG File', "*jpg")], title="Select puzzle image...")

        introContainer.destroy()

        sudokuContainer = ttk.Frame(root)
        sudokuContainer.pack(side='top', fill=tk.BOTH, anchor="center", padx=25, pady=25)

        loadingLabel = ttk.Label(sudokuContainer, text="Reading...", anchor="center", font=('Arial', 16))
        loadingLabel.pack(side='top', fill=tk.BOTH, anchor="center")

        loadingSpinner = ttk.Progressbar(sudokuContainer, orient="horizontal", length = 200, mode="determinate", takefocus=True, maximum=81)
        loadingSpinner.pack(side='top', fill=tk.X, anchor="center", padx=10, pady=15)
        
        image_preprocesser = Image_Processer(loadingSpinner, root)
        image_path = file.name 
        grid = image_preprocesser.extract_digits_from_grid(image_path=image_path)
        
        loadingLabel.destroy()
        #print("Extracted Grid:\n", grid)

        #sudokuContainer.config(relief="solid", borderwidth=4)

        root.update()
        
        for i in range(9):
            for j in range(9):

                cell_value = grid[i][j]

                if cell_value == '':
                    cell_value = "."
                #print(f"Entering value for cell ({i},{j}): {cell_value}")
                
                cell_vars[i][j] = cell_value

                sudoku_cell = ttk.Label(sudokuContainer, text=cell_value, width=3, anchor="center", font=('Arial', 24), relief="solid", borderwidth=4, border=4)
                sudoku_cell.grid(row=i, column=j, ipadx=5, ipady=10)

        #for child in sudokuContainer.winfo_children():
        #    print(child.cget("text"))

        #i = 2
        #j = 4

        #sudokuContainer.winfo_children()[(i*9)+j].configure(text="H")

        buttonContainer= ttk.Frame(root)
        buttonContainer.pack(side='top', fill=tk.Y, anchor='center')

        backButton = ttk.Button(buttonContainer, text="Back", command=clear_and_restart)
        backButton.pack(side='left', fill=tk.BOTH, anchor='center', padx=15, pady=15)

        confirmButton = ttk.Button(buttonContainer, text="Confirm", command=lambda: solve(sudokuContainer, confirmButton))
        confirmButton.pack(side='right', fill=tk.BOTH, anchor='center', padx=15, pady=15)

    def open_manual_puzzle():

        introContainer.destroy()
        sudokuContainer = ttk.Frame(root)
        sudokuContainer.pack(side='top', fill=tk.BOTH, anchor="center", padx=25, pady=25)
        
        for i in range(9):
            for j in range(9):

                #print(f"Entering value for cell ({i},{j}): {cell_value}")

                sudoku_cell = ttk.Entry(sudokuContainer, textvariable=cell_vars[i][j], width=3, font=('Arial', 24))
                sudoku_cell.grid(row=i, column=j, ipadx=5, ipady=10)

        submitButton = ttk.Button(root, text="Submit", command=lambda: show_puzzle(sudokuContainer, submitButton))
        submitButton.pack(side='top', fill=tk.BOTH, anchor="center", padx=25, pady=15)

    def show_puzzle(sudokuContainer, button):

        button.destroy()

        for child in sudokuContainer.winfo_children():
            child.destroy()

        for i in range(9):
            for j in range(9):

                cell_value = cell_vars[i][j].get()

                if cell_value == '':
                    cell_value = "_"
                #print(f"Entering value for cell ({i},{j}): {cell_value}")e

                sudoku_cell = ttk.Label(sudokuContainer, text=cell_value, width=3, anchor="center", font=('Arial', 24), relief="solid", borderwidth=4, border=4)
                sudoku_cell.grid(row=i, column=j, ipadx=5, ipady=10)

        buttonContainer= ttk.Frame(root)
        buttonContainer.pack(side='top', fill=tk.Y, anchor='center')

        backButton = ttk.Button(buttonContainer, text="Back", command=clear_and_restart)
        backButton.pack(side='left', fill=tk.BOTH, anchor='center', padx=15, pady=15)

        confirmButton = ttk.Button(buttonContainer, text="Confirm", command=lambda: solve(sudokuContainer, confirmButton))
        confirmButton.pack(side='right', fill=tk.BOTH, anchor='center', padx=15, pady=15)

    def get_puzzle_from_camera(camera_feed):

        introContainer.destroy()

        camera_puzzle = Camera_Puzzle()

        camera_puzzle.getCameraFeed(webcamFeed=camera_feed, on_puzzle_found_callback=on_puzzle_found)

        #camera_feed.destroy()

    def on_puzzle_found(puzzle):

        webcamFeed.destroy()

        sudokuContainer = ttk.Frame(root)
        sudokuContainer.pack(side='top', fill=tk.BOTH, anchor="center", padx=25, pady=25)

        loadingLabel = ttk.Label(sudokuContainer, text="Reading...", anchor="center", font=('Arial', 16))
        loadingLabel.pack(side='top', fill=tk.BOTH, anchor="center")

        loadingSpinner = ttk.Progressbar(sudokuContainer, orient="horizontal", length = 200, mode="determinate", takefocus=True, maximum=81)
        loadingSpinner.pack(side='top', fill=tk.X, anchor="center", padx=10, pady=15)
        
        image_preprocesser = Image_Processer(loadingSpinner, root)
        grid = image_preprocesser.extract_digits_from_grid(raw_image=puzzle)
        
        loadingLabel.destroy()
        #print("Extracted Grid:\n", grid)

        #sudokuContainer.config(relief="solid", borderwidth=4)
        
        for i in range(9):
            for j in range(9):

                cell_value = grid[i][j]

                if cell_value == '':
                    cell_value = "."
                
                cell_vars[i][j] = cell_value

                sudoku_cell = ttk.Label(sudokuContainer, text=cell_value, width=3, anchor="center", font=('Arial', 24), relief="solid", borderwidth=4, border=4)
                sudoku_cell.grid(row=i, column=j, ipadx=5, ipady=10)

        buttonContainer= ttk.Frame(root)
        buttonContainer.pack(side='top', fill=tk.Y, anchor='center')

        backButton = ttk.Button(buttonContainer, text="Back", command=clear_and_restart)
        backButton.pack(side='left', fill=tk.BOTH, anchor='center', padx=15, pady=15)

        confirmButton = ttk.Button(buttonContainer, text="Confirm", command=lambda: solve(sudokuContainer, confirmButton))
        confirmButton.pack(side='right', fill=tk.BOTH, anchor='center', padx=15, pady=15)
        
        root.update()

    def solve(sudokuContainer, confirmButton):

        confirmButton.destroy()

        solving_agent = Solve_Agent()

        solving_agent.solve_puzzle(cell_vars, sudokuContainer, root)



    introContainer = ttk.Frame(root)
    introContainer.pack(side='top', fill=tk.Y, anchor="center")

    labelTop = ttk.Label(introContainer, text="Welcome to the Sudoku Solver. \nPlease choose one of the choices below:", anchor='center')
    labelTop.pack(side='top', anchor='center', fill=tk.BOTH, padx="10px", pady="15px")

    buttonContainer = ttk.Frame(introContainer)
    buttonContainer.pack(side='top', anchor='center', fill=tk.X)

    webcamFeed = tk.Label(root)
    webcamFeed.pack(side='top', anchor='center', fill=tk.BOTH, padx="2px", pady="2px")

    uploadImageButton = ttk.Button(buttonContainer, text="Upload Puzzle Image", command=get_puzzle_from_image)
    uploadImageButton.pack(side='top', anchor='center', fill=tk.BOTH, padx="2px", pady="2px")

    photoButton = ttk.Button(buttonContainer, text="Show Puzzle on Camera", command=lambda: get_puzzle_from_camera(webcamFeed))
    photoButton.pack(side='top', anchor='center', fill=tk.BOTH, padx="2px", pady="2px")

    manualInputButton = ttk.Button(buttonContainer, text="Manually Input Puzzle", command=open_manual_puzzle)
    manualInputButton.pack(side='top', anchor='center', fill=tk.BOTH, padx="2px", pady="2px")

    sv_ttk.set_theme("dark", root)

    root.mainloop()



def main():

    #print(tf.__version__)

    openGUI()

    #image_preprocesser = Image_Processer()
    #image_path = "test.jpg" 
    #text = image_preprocesser.extract_text(image_path)
    #print("Extracted Text:\n", text)


if __name__ == "__main__":
    main()
