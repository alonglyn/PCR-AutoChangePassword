import time
import pyautogui as pag
from core.data_help import notice_input

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

sel = notice_input(['不修改','修改'],'是否要修改默认密码')
if sel == 1:
    password = ''
    while True:
        password = input('输入自定义密码， 输入回车结束，使用随机密码直接回车\n').strip()
        if not password:
            break
        while True:
            a = input('密码是:%s\n, 确定使用直接输入回车， 否则输入N\n'%password).strip()
            if not a:
                confirm = True
                break
            else:
                confirm = False
                break
        if confirm:
            break

sel = notice_input(['不录制','录制'],'是否要录制添加邮件点')
if sel == 1:
    poss = test()
    with open('config.py','a') as f:
        f.write('\npassword = "%s"\n'%password)
        for i, pos in enumerate(poss):
            f.write('\npos%d = (%d, %d)\n'%(i+1,pos[0], pos[1]))
    print('完成配置到config.py文件中')