from math import fabs, log
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
5: 수식이 없을때 +/- 버튼이 작동하지 않는 현상

버그 발생 이유 :
1: - 와  +/- 두 연산에 차이를 주지 않아 발생한 현상 // -에는 공백문자를 주어 해결
2: 공백 제거 없이 oupPutData 값에 formula를 집어넣어 발생한 현상 // 공백 제거 함수를 생성해 해결
3: eval 함수에서 * 연산자를 X로 집어넣어 발생한 현상 // 연산하기 전에 X 를 *로 변경하여 해결
4: 공백을 지우지 않고 연산자를 추가하는 바람에 발생한 현상 // 숫자 입력과 연산자 입력을 나눠 해결
5: 모르겠음

버그가 있는 기능:
1: +/-
2: -

미구현 기능:
1: %
2: 1/X
3: X^2
4: root
5: .

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
    tmpformula = ""
    if(endSwithIsdigit()):
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
            outPutData += "=" + str(eval(formula))
            entryDelete()
            entryInsert()
            formula = str(eval(formula))
        elif(funcNum == "*"): # X 입력시 출력 형태를 *로 나오는 것을 X로 변환
            isSymbol = True
            formula += funcNum
            DeleteSpaceO()
            dataAdd()
            entryDelete()
            entryInsert()
        elif(funcNum == "+" or funcNum == "-" or funcNum == "/"):
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
        elif(funcNum == "m"): # +/- 버튼
            print("formula =",formula,logger.debug(""))
            funcnumM()
            if(isSymbol):
                print("??")
                dataAdd()
            else:
                dataAdd_m(splice)
                formula = outPutData
            DeleteSpaceO()
            entryDelete()
            entryInsert()
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
        #elif(funcNum == "."):
            

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
        #print(strtmp)
        if(formula[i] == " "):
            strtmp = ""
            splice -= 1
            continue
        elif((not(ord(formula[i]) >= ord("0") and ord(formula[i]) <= ord("9") or ord(formula[i]) == ord("-")))):
            strtmp = ""
            splice = i + 1
    if(splice == default):
        formula += "*-1"
        # print("formula =",formula,"168")
        # print("isSymbol =",isSymbol,"169")
        # print("outPutData =",outPutData,"170")
        return
    print("strtmp =",strtmp,logger.debug(""))
    inttmp = (int(strtmp) * -1)
    print("inttmp =",inttmp,logger.debug(""))
    strtmp = str(inttmp)
    print("strtmp =",strtmp,logger.debug(""))
    print("splice =",splice,logger.debug(""))
    dataAdd()
    formula = formula[0:splice]
    formula += strtmp
    # print("formula =",formula,"175")

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
