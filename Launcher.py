from tkinter import *
from game import run_game

# Initialize TK
def main():
	root = Tk()
	root.geometry("300x230")
	root.title("Elevators V4 - Rohan Dawar")
	root.protocol("WM_DELETE_WINDOW", root.destroy)
	lbl = Label(root, text="Rohan's Elevators V4")
	lbl.grid(row=0,column=0)

	floorFrame = LabelFrame(root, text="Number of Floors:")
	floorFrame.grid(row=1,column=0)

	floorOptions = range(3,13)
	floorVar = IntVar()
	floorVar.set(floorOptions[0])
	drop = OptionMenu(floorFrame, floorVar, *floorOptions)
	drop.pack()

	liftsFrame = LabelFrame(root, text="Number of Lifts:")
	liftsFrame.grid(row=2,column=0)

	liftsOptions = range(2,7)
	liftsVar = IntVar()
	liftsVar.set(liftsOptions[0])
	drop = OptionMenu(liftsFrame, liftsVar, *liftsOptions)
	drop.pack()

	b = Button(root, text="Start Game", padx=100, command=lambda: run_game(root,floorVar.get(),liftsVar.get()))
	b.grid(row=3,column=0, pady=20, padx=12)
	q = Button(root, text="Exit", command=root.quit, padx=100)
	q.grid(row=4,column=0)
	root.mainloop()

# Run
if __name__ == '__main__': main()