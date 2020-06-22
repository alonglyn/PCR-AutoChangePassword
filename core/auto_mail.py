import pyautogui as pag
import time
import pandas as pd
from config import *
from core.data_help import addCol

class WinMouseKeyBorad():
    def __init__(self):
        self.width = pag.size().width
        self.height = pag.size().height
        print(pag.size())
    
    def rel_pos(self, rx, ry):
        return int(self.width * rx), int(self.height * ry)

    def add_one(self, address, password, time_delay):
        pag.moveTo(pos1) # 填添加邮件的点
        pag.sleep(0.2)
        pag.click()
        time.sleep(0.5)
        pag.typewrite(address)
        time.sleep(0.2)
        pag.press('tab')
        time.sleep(0.5)
        pag.typewrite(password)
        pag.moveTo(pos2) # 填登录的点
        pag.click()
        time.sleep(time_delay)
        pag.moveTo(pos3) # 填x掉小窗口的点
        pag.click()

def auto_add_mail(df, time_delay = 1):
    wmkb = WinMouseKeyBorad()
    addCol(df,'added')
    for i in df.index:
        if df.loc[i,'added'] == 0:
            wmkb.add_one(df.loc[i,'mail_add'], df.loc[i, 'mail_pwd'], time_delay)
            df.loc[i,'added'] = 1
def test():
    print('尽快将鼠标放在邮箱界面的添加邮箱 处 停止15s,会自动点击 \
        然后放在登录按钮上15s,会自动点击\
        然后放在关闭按钮上15s,会自动点击')
    sz = pag.size()
    times = 0
    d = dict()
    ret = []
        # print(pag.position())
    try:
        cp = 0
        while True:
            pos = pag.position()
            # print(pos.x,',', pos.y)
            if pos in d.keys():
                d[pos] += 1
            else:
                d[pos] = 1
            if d[pos] >= 15:
                ret.append((pos.x,pos.y))
                d[pos] = -20
                cp += 1
                
                pag.click()
                if cp == 1:
                    time.sleep(0.1)
                    pag.typewrite('test@163.com')
                    time.sleep(0.1)
                    pag.press('tab')
                    time.sleep(0.1)
                    pag.typewrite('testtest')
                
            if cp >= 3:
                break
            time.sleep(1)
            times+=1
            
    except (KeyboardInterrupt,Exception) as e:
        print(e)
        print('发生错误输出停留时间最长的三个坐标， 请重新运行')
        kvs = list(d.items())
        kvs.sort(key = lambda x:x[1])
        kvs.reverse()
        for kv in kvs[:3]:
            ret.append(kv[0].x,kv[0].y)
    finally:
        return ret



# pyautogui.size()            #返回屏幕宽高像素数的元组
#                             #例如，如果屏幕分辨率为1920*1080，那么左上角的坐标为（0,0）,
#                             #右下角的坐标是（1919,1079）
# pyautogui.position()    

# pyautogui.moveTo(x,y[,duration = t])  # 将鼠标移动到屏幕指定位置，
#                                       #x,y是目标位置的横纵坐标，duration指定鼠标光标移动到目标位置
#                                       #所需要的秒数，t可以为整数或浮点数，省略duration参数表示
#                                       #立即将光标移动到指定位置（在PyAutoGUI函数中，所有的duration
#                                       #关键字参数都是可选的）
#                                       #Attention：所有传入x,y坐标的地方，都可以用坐标x,y
#                                       #的元组或列表替代，(x,y)/[x,y]

# pyautogui.moveRel(x,y[,duration = t]) #相对于当前位置移动光标，
#                                       #这里的x,y不再是目标位置的坐标，而是偏移量，
#                                       #如，pyautogui.moveRel(100,0,duration=0.25)
#                                       #表示光标相对于当前所在位置向右移动100个像素

# pyautogui.mouseDown()   #按下鼠标按键（左键）

# pyautogui.mouseUp()     #释放鼠标按键（左键）

# pyautogui.click()       #向计算机发送虚拟的鼠标点击(click()函数只是前面两个函数调用的方便封装)
#                         #默认在当前光标位置，使用鼠标左键点击

# pyautogui.click([x,y,button='left/right/middle'])  #在(x,y)处点击鼠标左键、右键、中键
#                                                    #但不推荐使用这种方法，下面这种方法效果更好
#                                                    #pyautogui.moveTo(x,y,duration=t)
#                                                    #pyautogui.click()
# pyautogui.doubleClick() #双击鼠标左键

# pyautogui.rightClick()  #单击鼠标右键

# pyautogui.middleClick() #单击鼠标中键


# pyautogui.dragTo(x,y[,duration=t)      #将鼠标拖动到指定位置
#                                        #x,y：x坐标，y坐标

# pyautogui.dragRel(x,y[,duration=t])    #将鼠标拖动到相对当前位置的位置
#                                        #x,y：水平移动，垂直移动

# pyautogui.scroll()         #控制窗口上下滚动（滚动发生在鼠标的当前位置）
#                            #正数表示向上滚动，负数表示向下滚动，
#                            #滚动单位的大小需要具体尝试

# #eg
# sleep(2)
# click()
# moveTo((1418,12),duration=2)
# click()
# moveTo([1392,47],duration=1)
# click()
# typewrite('https://wwww.baidu.com')
# typewrite(['enter'])

# pyautogui.typewrite([键盘键字符串])      #除了单个字符串，还可以向typewrite()函数传递键字符串的列表
#                                          #如 pyautogui.typewrite(['a','b','left','left','X','Y'])
#                                          #按'a'键，'b'键，然后按左箭头两次，然后按'X'和'Y'
#                                          #输出结果为XYab

# pyautogui.keyDown()        #根据传入的键字符串，向计算机发送虚拟的按键（按下）

# pyautogui.keyUp()          #根据传入的键字符串，向计算机发送虚拟的释放（释放）

# pyautogui.press()          #前面两个函数的封装，模拟完整的击键（按下并释放）