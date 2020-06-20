from core.auto_mail import test

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

poss = test()

with open('config.py','a') as f:
    f.write('\npassword = "%s"\n'%password)
    for i, pos in enumerate(poss):
        f.write('\npos%d = (%d, %d)\n'%(i+1,pos[0], pos[1]))


print('完成配置到config.py文件中')