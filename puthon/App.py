import tkinter as tk

root = tk.Tk()
root.title("My First App")
root.geometry("300x200")

label = tk.Label(root, text="Hello, World!", font=("Arial", 16))
label.pack(pady=20)

def click_me():
    label.config(text="You clicked the button!")

button = tk.Button(root, text="Click Me", command=click_me)
button.pack()

root.mainloop()








