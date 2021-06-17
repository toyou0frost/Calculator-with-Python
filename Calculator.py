from math import fabs, log, sqrt
from tkinter import *
from tkinter import ttk # tkinter의 확장모듈 GUI의 외형을 개선해줌
import logging # 코드 라인 출력
# 6~10 디버깅 모듈
logging.basicConfig(format='%(asctime)s,%(msecs)d %(levelname)-8s [%(filename)s:%(lineno)d] %(message)s',
    datefmt='%d-%m-%Y:%H:%M:%S',
    level=logging.DEBUG)

logger = logging.getLogger('log_1')

"""
버그 리스트 : 
1: - 연산을 진행할 때 +/- 버튼을 누르면 아무런 작동도 하지 않음 // Fixed
2: A--B일 때 = 버튼을 눌렀을 때 A - -B=Result 형태로 출력 // Fixed
3: formula의 값으로 * 대신 X가 들어가서 계산이 안되는 현상 // Fixed
4: -연산과 +/- 연산이 서로 충돌하는 현상 //Fixed
5: 수식이 없을때 +/- 버튼이 작동하지 않는 현상 //Fixed
6: 수식이 있을 때 +/- 버튼을 누르면 X-1 가 연산이 된 후 나와야 하는데 그대로 출력하는 현상 
7: eval 함수가 소수점 계산을 정확하게 하지 못하는 현상 //Fixed
8: funcnumM함수 다른 연산자와 충돌 다수 //delete
9: 소숫점 입력 이후 +/- 버튼을 누를 경우 소숫점 이후의 수만 -되는 현상 
10: 특정 상황에서 +/- 버튼을 누르면 정상적으로 동작하지 않고 왼쪽 상단에 -가 출력되는 현상

버그 발생 이유 :
1: - 와  +/- 두 연산에 차이를 주지 않아 발생한 현상 // -에는 공백문자를 주어 해결
2: 공백 제거 없이 oupPutData 값에 formula를 집어넣어 발생한 현상 // 공백 제거 함수를 생성해 해결
3: eval 함수에서 * 연산자를 X로 집어넣어 발생한 현상 // 연산하기 전에 X 를 *로 변경하여 해결
4: 공백을 지우지 않고 연산자를 추가하는 바람에 발생한 현상 // 숫자 입력과 연산자 입력을 나눠 해결
5: splice값이 예상히지 못한 값으로 들어와 발생 한 현상 // funcnumM 의 elif문에서 not을 빼주어 해결 
6: 5번 버그를 해결하는 과정에서 발생 funcnumM의 elif 문에서 not을 뺀 이후 발생
7: eval 함수 자체의 문제로 추정 // 소수 5번째 자리에서 반올림 해주는 형식으로 해결
8: 기초부터 잘못된 알고리즘 사용에 의한 문제로 추정 // getX함수로 픽스 예정
8-1 : getX_m 함수를 생성하여 해결 +/-버튼이 눌리면 괄호를 사용하여 구별

버그가 있는 기능:
1: +/- // Fixed
2: - // Fixed

디버깅 코드:
    print("formula =",formula,logger.debug(""))
    print("outPutData =",outPutData,logger.debug(""))
    print("strtmp =",strtmp,logger.debug(""))
    print("inttmp =",inttmp,logger.debug(""))

"""

tk = Tk()

data = []
formula = ""
outPutData = ""
isSymbol = False
splice = 0
lastInputData = ""
keyvalue = ""

tk.title("계산기")
tk.geometry("350x500")

value = StringVar(tk, value="")
num = ttk.Entry(tk, textvariable = value, width=30)
num.grid(row = 0, columnspan = 4)

def keyPressed(event):
    global keyvalue
    if(event.char == ""):
        keyvalue = "C"
    else :
        keyvalue = event.char
    insertNum(keyvalue)

def resultReturn(event):
    insertNum("=")

frame = Frame(tk, width=0, height=0)
frame.bind("<Key>", keyPressed) 
frame.bind("<Return>", resultReturn)
frame.place(x=0, y=0)

frame.focus_set()



def insertNum(funcNum):
    frame.focus_set()
    global formula, outPutData, isSymbol, lastInputData
    tmp = ""
    check = True
    splice_1 = ""
    splice_2 = ""
    tmpformula = ""
    x = ""
    if(endSwithIsdigit() or formula.endswith(")")):
        check = True
    else:
        check = False
    if(paraIsdigit(funcNum)):
        check = True
    if(check):
        if(funcNum == "="): # 연산 완료 
            isSymbol = True
            DeleteSpaceFO()
            dataAdd()
            formula = formula.replace("X", "*")
            print("formula =",formula,logger.debug(""))
            outPutData += "=" + str(round(eval(formula), 5))
            outPutData = outPutData.replace("XX","^")
            entryDelete()
            entryInsert()
            formula = str(eval(formula))
        elif(funcNum == "*"): # X 입력시 출력 형태를 *로 나오는 것을 X로 변환
            lastInputData = funcNum
            isSymbol = True
            formula += funcNum
            DeleteSpaceFO()
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "+" or funcNum == "-" or funcNum == "/" or funcNum == "%"):
            lastInputData = funcNum
            isSymbol = True
            DeleteSpaceFO()
            if(funcNum == "-"):
                formula += " "+funcNum+" "
            else:
                formula += funcNum
            print("formula =",formula,logger.debug(""))
            DeleteSpaceO()
            print("formula =",formula,logger.debug(""))
            print("outPutData =",outPutData,logger.debug(""))
            dataAdd()
            print("formula =",formula,logger.debug(""))
            print("outPutData =",outPutData,logger.debug(""))
            entryDelete()
            print("outPutData =",outPutData,logger.debug(""))
            entryInsert()
        elif(funcNum.isdigit()):
            print("formula =",formula,logger.debug(""))
            formula += funcNum
            DeleteSpaceO()
            dataAdd()
            entryDelete()
            entryInsert()
        # elif(funcNum == "m"): # +/- 버튼
        #     print("formula =",formula,logger.debug(""))
        #     funcnumM()
        #     print("formula =",formula,logger.debug(""))
        #     print("isSymbol =",isSymbol,logger.debug(""))
        #     if(isSymbol):
        #         dataAdd()
        #     else:
        #         dataAdd_m(splice)
        #         formula = outPutData
        #     DeleteSpaceO()
        #     entryDelete()
        #     entryInsert()
        elif(funcNum == "E"):
            DeleteSpaceFO()
            if(isSymbol):
                for i in range(0, len(formula)):
                    tmp += str(formula[i])
                    if(arithmetic(tmp)):
                        splice_1 = i + 1
                        splice_2 = i - 1
                if(not(str(formula[splice_2]).isdigit())):
                    formula = str(tmp[0:splice_2+1])
                else:
                    formula = str(tmp[0:splice_1])
                dataAdd()
                entryDelete()
                entryInsert()
            else:
                formula = ""
                dataAdd()
                entryDelete()
                entryInsert()
        elif(funcNum == "C"):
            formula = ""
            dataAdd()
            entryDelete()
            entryInsert()
            isSymbol = False
        elif(funcNum == "B"):
            for i in range(0, len(formula) -1):
                tmpformula += formula[i]
            formula = tmpformula
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "."):
            formula += funcNum
            DeleteSpaceFO()
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "d"): # 1/X
            lastInputData = funcNum
            x = getX()
            print("x",getX(),logger.debug(""))
            formula += "1/" + x
            DeleteSpaceO()
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "^"): # X^2
            lastInputData = funcNum
            x = getX()
            formula += x+"**2"
            DeleteSpaceO()
            dataAdd()
            print("outPutData =",outPutData,logger.debug(""))
            outPutData = outPutData.replace("XX","^")
            entryDelete()
            entryInsert()
        elif(funcNum == "r"): # root
            lastInputData = funcNum
            x = getX()
            print("x",sqrt(int(x)),logger.debug(""))
            formula += str(round(sqrt(int(x)),5))
            DeleteSpaceO()
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "m"): # +/-
            x = getX_m()
            print("x",x,logger.debug(""))
            x = int(x) * -1
            formula += "("+str(x)+")"
            DeleteSpaceO()
            dataAdd()
            entryDelete()
            entryInsert()
        else:
            return



def arithmetic(funcNum): # 사칙연산 검사 사칙연산 == TRUE 사칙연산 != FALSE
    if(funcNum.endswith("*") == True or funcNum.endswith("/") == True or funcNum.endswith("-") == True or funcNum.endswith("+") == True):
        return True
    else:
        return False

def entryDelete(): # Entry 데이터 삭제
    num.delete(0, "end")

def entryInsert(): # Entry 에 outPutData 출력
    print("outPutData =",outPutData,logger.debug(""))
    num.insert("end",outPutData)

def dataAdd():  # outPutData에 수식 입력
    global outPutData, formula
    outPutData = ""
    tmpData = ""
    for i in range(0, len(formula)):
        if(formula[i] == "*"):
            outPutData += "X"
            tmpData += "X"
        elif(formula[i] != " "):
            print("formula =",formula[i],logger.debug(""))
            outPutData += formula[i]
            tmpData += formula[i]
        else:
            tmpData += " "

    #print("outPutData =",outPutData,"122")
    print("formula =",formula,logger.debug(""))
    print("outPutData =",outPutData,logger.debug(""))
    formula = tmpData
    #print("formula =",formula,"124")

def dataAdd_m(splice):    # outPutData에 수식을 입력하는데 +/- 버튼을 누를 경우 *-1을 하는식으로 계산하기 때문에 수식에 *-1 이 그대로 들어가는 경우를 방지
    global outPutData,formula
    # tmp1 = ""
    formula = str(eval(formula))
    outPutData = formula
    # print("formula =",formula,logger.debug(""))
    #  print("splice =",splice,"125")
    # tmp1 = formula[splice:splice + 4]
    # formula = formula[0 : splice]
    # print("tmp1 =",tmp1,logger.debug(""))
    #  print("formula =",formula,"131")
    # formula += " "+str(eval(int(tmp1)))
    #  print("formula =",formula,"133")
    # outPutData = formula
    # print("outPutData =",outPutData,"135")

def endSwithIsdigit(): # 마지막숫자 == TRUE 마지막숫자 != FALSE
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

def funcnumM(): # 버그덩어리
    global formula, splice
    #print(formula+"???")
    strtmp = ""
    inttmp = 0
    splice = len(formula)
    default = splice
    print("formula =",formula,logger.debug(""))
    for i in range(0, len(formula)):
        strtmp += formula[i]
        if(formula[i] == " "):
            strtmp = ""
            splice -= 1
            continue
        elif(((ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9") or ord(formula[i]) == ord("-")))):
            strtmp = ""
            splice = i + 1
    if(splice == default):
        print(logger.debug(""))
        formula += "*-1"
        return
    print("strtmp =",strtmp,logger.debug(""))
    inttmp = (int(strtmp) * -1)
    print("inttmp =",inttmp,logger.debug(""))
    if(lastInputData == "-"):
        strtmp = " "+str(inttmp)
    else:
        strtmp = str(inttmp)
    print("strtmp =",strtmp,logger.debug(""))
    print("splice =",splice,logger.debug(""))
    #dataAdd()
    formula = formula[0:splice]
    formula += strtmp

def DeleteSpaceO(): # Code08_04 참고 문자열의 공백 삭제 (only outPutData)
    global formula,outPutData
    tmp = ""
    for i in range(0, len(formula)):
        if(formula[i] != " "):
            tmp += formula[i]
    outPutData = tmp
    #print("outPutData =",outPutData,"222")
    #print("formula =",formula,"223")
    # print("issybol =", isSymbol,"224")

def DeleteSpaceFO(): # Code08_04 참고 문자열의 공백 삭제 (formula, outPutData)
    global formula,outPutData
    tmp = ""
    for i in range(0, len(formula)):
        if(formula[i] != " "):
            tmp += formula[i]
    outPutData = tmp
    formula = outPutData
    # print("issybol =", isSymbol,"197")

def isSpace(): # 문자열의 공백여부 확인
    tmp = ""
    for i in range(0, len(formula)):
        if(formula[i] != " "):
            tmp += formula[i]
    if(formula == tmp):
        return False
    else :
        return True

def getX():
    global formula
    reverseStr = ""
    forwardStr = ""
    splice = 0
    for i in range(len(formula) - 1, -1, -1):
        if(formula[i] == " " or (not(ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9")))):
            print("i",i,logger.debug(""))
            splice = i + 1
            break;
        else :
            reverseStr += formula[i]
    for i in range(len(reverseStr) - 1, -1, -1):
        print("x",reverseStr,logger.debug(""))
        forwardStr += reverseStr[i]
    print("x",forwardStr,logger.debug(""))
    formula = formula[0:splice]
    return forwardStr

def getX_m():
    global formula
    reverseStr = ""
    forwardStr = ""
    splice = 0
    isPare = False
    if(formula.endswith(")")):
        isPare = True
    for i in range(len(formula) - 1, -1, -1):
        if(isPare):
            if(formula[i] == "("):
                splice = i
                break
            else:
                if(formula[i] == ")"):
                    continue
                reverseStr += formula[i]
        else :
            if(formula[i] == " " or (not(ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9") and formula[i] == "."))):
                print("i",i,logger.debug(""))
                splice = i + 1
                break
            else :
                reverseStr += formula[i]
    for i in range(len(reverseStr) - 1, -1, -1):
        print("x",reverseStr,logger.debug(""))
        forwardStr += reverseStr[i]
    print("x",forwardStr,logger.debug(""))
    formula = formula[0:splice]
    print("formula",formula,logger.debug(""))
    return forwardStr

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
