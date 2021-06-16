from tkinter import *

tmp = ""

def keyPressed(event):
    global tmp
    if(event == " "):
        print("aa")
    else:
        tmp = event.char
        print(tmp)

def tmpFunc(e):
    print("asdasd")

root = Tk()

frame = Frame(root, width=350, height=500)
frame.bind("<Key>", keyPressed) 
frame.bind("<Return>", tmpFunc)
frame.bind("<Return>", tmpFunc)
frame.place(x=0, y=0)

# 키보드 포커를 갖게 한다
frame.focus_set()

root.mainloop()