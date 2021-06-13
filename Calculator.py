from math import fabs
from tkinter import *
from tkinter import ttk # tkinter의 확장모듈 GUI의 외형을 개선해줌


tk = Tk()

data = []
formula = ""
outPutData = ""
isSymbol = False

tk.title("계산기")
tk.geometry("320x500")


value = StringVar(tk, value="")
num = ttk.Entry(tk, textvariable = value)
num.grid(row = 0, columnspan = 3)

def insertNum(funcNum):
    global formula, outPutData, isSymbol
    tmp = ""
    check = True
    splice_1 = ""
    splice_2 = ""
    if(endSwithIsdigit()):
        check = True
    else:
        check = False
    if(paraIsdigit(funcNum)):
        check = True
    if(check):
        if(funcNum == "="): # 연산 완료 
            isSymbol = True
            dataAdd()
            outPutData += "=" + str(eval(formula))
            entryDelete()
            entryInsert()
            formula = str(eval(formula))
        elif(funcNum == "*"): # X 입력시 출력 형태를 *로 나오는 것을 X로 변환
            isSymbol = True
            formula += funcNum
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "+" or funcNum == "-" or funcNum == "/" or funcNum.isdigit()):
            #isSymbol = True
            formula += funcNum
            num.insert("end", funcNum)
        elif(funcNum == "m"): # +/- 버튼 
            funcnumM()
            if(isSymbol):
                dataAdd()
            else:
                dataAdd_m()
                formula = outPutData
            entryDelete()
            entryInsert()
        elif(funcNum == "E"):
            if(isSymbol):
                for i in range(0, len(formula)):
                    tmp += str(formula[i])
                    if(arithmetic(tmp)):
                        splice_1 = i + 1
                        splice_2 = i - 1
                if(not(str(formula[splice_2]).isdigit())):
                    print("splice_2 =",splice_2,"68")
                    print("formula =",formula,"69")
                    formula = str(tmp[0:splice_2+1])
                    print("formula =",formula,"71")
                else:
                    print("splice_2 =",splice_2,"85")
                    print("formula =",formula,"86")
                    formula = str(tmp[0:splice_1])
                dataAdd()
                entryDelete()
                entryInsert()
            else:
                formula = ""
                dataAdd()
                entryDelete()
                entryInsert()
        #elif(funcNum == "."):
            

def arithmetic(funcNum): # 사칙연산 검사 사칙연산 == TRUE 사칙연산 != FALSE
    if(funcNum.endswith("*") == True or funcNum.endswith("/") == True or funcNum.endswith("-") == True or funcNum.endswith("+") == True):
        return True
    else:
        return False

def entryDelete(): # Entry 데이터 삭제
    num.delete(0, "end")

def entryInsert(): # Entry 에 outPutData 출력
    num.insert("end",outPutData)

def dataAdd():  # outPutData에 수식 입력
    global outPutData
    outPutData = ""
    for i in range(0, len(formula)):
        if(formula[i] == "*"):
            outPutData += "X"
        else:
            outPutData += formula[i]

def dataAdd_m():    # outPutData에 수식을 입력하는데 +/- 버튼을 누를 경우 *-1을 하는식으로 계산하기 때문에 수식에 *-1 이 그대로 들어가는 경우를 방지
    global outPutData
    outPutData = str(eval(formula))

def endSwithIsdigit(): #숫자 == TRUE 숫자 != FALSE
    global formula
    returnBool = True
    if(formula == ""):
        return False
    for i in range(0, len(formula)):
        if(ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9")):
            returnBool = True
        else:
            returnBool = False
            #tk.title(formula)
    #print(returnBool)
    return returnBool

def paraIsdigit(funcNum):
    if(ord(funcNum) >= ord("0") and ord(funcNum) <= ord("9")):
        return True
    else:
        return False

def funcnumM():
    global formula
    #print(formula+"???")
    strtmp = ""
    inttmp = 0
    splice = len(formula)
    default = splice
    for i in range(0, len(formula)):
        strtmp += formula[i]
        #print(strtmp)
        if(not(ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9") or ord(formula[i]) == ord("-"))):
            strtmp = ""
            splice = i + 1
    inttmp = (int(strtmp) * -1)
    strtmp = str(inttmp)
    if(splice == default):
        formula += "*-1"
        return
    dataAdd()
    formula = formula[0:splice]
    formula += strtmp





btn0 = ttk.Button(tk, text = "0", command = lambda:insertNum("0"))
btn0.grid(row = 7, column = 1)
btn1 = ttk.Button(tk, text = "1", command = lambda:insertNum("1"))
btn1.grid(row = 6, column = 0)
btn2 = ttk.Button(tk, text = "2", command = lambda:insertNum("2"))
btn2.grid(row = 6, column = 1)
btn3 = ttk.Button(tk, text = "3", command = lambda:insertNum("3"))
btn3.grid(row = 6, column = 2)
btn4 = ttk.Button(tk, text = "4", command = lambda:insertNum("4"))
btn4.grid(row = 5, column = 0)
btn5 = ttk.Button(tk, text = "5", command = lambda:insertNum("5"))
btn5.grid(row = 5, column = 1)
btn6 = ttk.Button(tk, text = "6", command = lambda:insertNum("6"))
btn6.grid(row = 5, column = 2)
btn7 = ttk.Button(tk, text = "7", command = lambda:insertNum("7"))
btn7.grid(row = 4, column = 0)
btn8 = ttk.Button(tk, text = "8", command = lambda:insertNum("8"))
btn8.grid(row = 4, column = 1)
btn9 = ttk.Button(tk, text = "9", command = lambda:insertNum("9"))
btn9.grid(row = 4, column = 2)
btn10 = ttk.Button(tk, text = "%", command = lambda:insertNum("%"))
btn10.grid(row = 1, column = 0)
btn11 = ttk.Button(tk, text = "CE", command = lambda:insertNum("E")) # CE 현재 수 초기화
btn11.grid(row = 1, column = 1)
btn12 = ttk.Button(tk, text = "C", command = lambda:insertNum("C")) # c 수식 전체 초기화
btn12.grid(row = 1, column = 2)
btn13 = ttk.Button(tk, text = "Backspace", command = lambda:insertNum("B")) # Backspace
btn13.grid(row = 1, column = 3)
btn14 = ttk.Button(tk, text = "1/x", command = lambda:insertNum("d")) # 1/x
btn14.grid(row = 2, column = 0)
btn15 = ttk.Button(tk, text = "x^2", command = lambda:insertNum("^")) # x^2
btn15.grid(row = 2, column = 1)
btn16 = ttk.Button(tk, text = "root", command = lambda:insertNum("r")) # root
btn16.grid(row = 2, column = 2)
btn17 = ttk.Button(tk, text = "/", command = lambda:insertNum("/"))
btn17.grid(row = 2, column = 3)
btn18 = ttk.Button(tk, text = "X", command = lambda:insertNum("*"))
btn18.grid(row = 4, column = 3)
btn19 = ttk.Button(tk, text = "-", command = lambda:insertNum("-"))
btn19.grid(row = 5, column = 3)
btn20 = ttk.Button(tk, text = "+", command = lambda:insertNum("+"))
btn20.grid(row = 6, column = 3)
btn21 = ttk.Button(tk, text = "=", command = lambda:insertNum("="))
btn21.grid(row = 7, column = 3)
btn22 = ttk.Button(tk, text = "+/-", command = lambda:insertNum("m")) #+/-
btn22.grid(row = 7, column = 0)
btn23 = ttk.Button(tk, text = ".", command = lambda:insertNum("."))
btn23.grid(row = 7, column = 2)
tk.mainloop()
