import tkinter

window = tkinter.Tk()
window.title("Rock Paper Scissors - Socket edition")
label = tkinter.Label(window, text = "Welcome to DataCamp's Tutorial on Tkinter!").pack()

button_widget = tkinter.Button(window,text="Start")
button_widget.pack()
tkinter.mainloop()


# window.mainloop()