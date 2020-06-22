import time
from io import BytesIO
from PIL import Image
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from core.data_help import generate_mail


# class MyException(BaseException):
#     def __init__(self, msg):
#         self.msg = msg
 
#     def __str__(self):
#         return self.msg

class LoginException(Exception):
    def __init__(self, msg='密码错误'):
        self.msg = msg
 
    def __str__(self):
        return self.msg

class NoMailException(Exception):
    def __init__(self, msg='没有可用邮箱了'):
        self.msg = msg
 
    def __str__(self):
        return self.msg


class WebDriverHelp():
    def __init__(self):
        super().__init__()
    def wait_for(self,a,b,max_times = 6):
        '''超时重试，默认6次'''
        times = 0
        while True:
            times+=1
            try:
                ret = self.single(a,b)
            except Exception as e:
                print(e)
                print('重试',times,'次')
                if times > max_times:
                    raise TimeoutException('多次等待超时')
            else:
                return ret

    def wait_for_class(self, e, cls,max_times = 60):
        '''检查已存在元素是否具有某属性, 默认2min'''
        times = 0
        while cls not in e.get_attribute('class').split():
            times+=1
            if times > max_times:
                raise TimeoutException('邮件无法发送等错误')
            if times % 5 == 0:
                print('等待验证码或其他',times,'s')
            time.sleep(1)

    def wait_for_visible(self, e, mode = True, max_times = 10):
        '''检查元素是否可见，每秒1次， 默认10s'''
        times = 0
        while True:
            times += 1
            res = e.is_displayed()
            # print(res)
            if bool(res) == mode:
                break
            # print(times)
            if times > max_times:
                raise TimeoutException('可见等待超时')
            time.sleep(1)

    def wait_for_text(self, e,max_times = 60):
        '''等待元素出现文本, 返回改文本， 超时则抛出异常'''
        times = 0
        while True:
            times+=1
            msg = e.text
            if msg:
                return msg
            if times % 5 == 0:
                print('等待文本',times,'s')
            if times >= max_times:
                raise TimeoutException('等待文本超时')
            time.sleep(1)

    def single(self,b,c):
        return self.wait.until(EC.presence_of_element_located((b, c)),'等待元素超时')
    def multi(self,b,c):
        return self.wait.until(EC.presence_of_all_elements_located((b, c)),'等待元素超时')
        
    def trans_handle(self):
        self.browser.switch_to_window(self.handle)


    def isElementPresent(self, by, value):
        """
        用来判断元素标签是否存在，
        """
        try:
            element = self.single(by, value)
        # 原文是except NoSuchElementException, e:
        except Exception as e:
            # 发生了NoSuchElementException异常，说明页面中未找到该元素，返回False
            return False
        else:
            # 没有发生异常，表示在页面中找到了该元素，返回True
            return True
class SliderCrack():
    def __init__(self):
        pass

    # def show_img(self):
    #     """鼠标悬停,显示极验图片
    #     """
    #     div_element = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "gt_slider")))
    #     ActionChains(self.browser).move_to_element(div_element).perform()

    def get_screenshot(self):
        """
        获取网页截图
        :return: 截图对象
        """
        screenshot = self.browser.get_screenshot_as_png()
        screenshot = Image.open(BytesIO(screenshot))
        return screenshot
    
    def get_position(self):
        """获取图片所在标签的位置信息        
        Returns:返回截图区域信息, 类似于CSS中的位置描述
        """
        img = self.wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/div[2]/div[6]/div/div[1]/div[1]/div/a/div[1]/div/canvas[2]")))
        time.sleep(2)
        location = img.location
        size = img.size
        top, bottom, left, right = location['y'], location['y'] + size['height'], location['x'], location['x'] + size[
            'width']
        return (top, bottom, left, right)
    
    def get_image(self, name='captcha.png'):
        """根据位置信息,通过截图获取验证码图片
        :return: 图片对象
        """
        top, bottom, left, right = self.get_position()
        # print('验证码位置', top, bottom, left, right)
        screenshot = self.get_screenshot()
        captcha = screenshot.crop((left, top, right, bottom))
        captcha.save(name)
        return captcha

    def get_slider(self):
        """获取滑块
        :return: 滑块对象
        """
        slider = self.wait.until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[2]/div[2]/div[6]/div/div[1]/div[2]/div[2]")))
        return slider
    
    def get_gap(self, image1, image2):
        """通过对比像素点,获取缺口偏移量, 起始位置left设为58~70均可, 是为了正好跳过前面拖动的缺口位置, 从而找到后面的拼图缺口,计算大致偏移量,如果移动偏移量过于准确,会提示图片被怪兽吃掉了!
        :param image1: 不带缺口图片
        :param image2: 带缺口图片
        :return: 偏移量的大小
        """
        # print("Image Size:",image1.size)
        left = 65
        for i in range(left, image1.size[0]):
            for j in range(image1.size[1]):
                if not self.is_pixel_equal(image1, image2, i, j):
                    left = i
                    return left
        return left

    def is_pixel_equal(self, image1, image2, x, y):
        """
        判断两个像素是否相同
        :param image1: 图片1
        :param image2: 图片2
        :param x: 位置x
        :param y: 位置y
        :return: 像素是否相同(每个像素点的RGB值之差小于60,则认为它们相同)
        """
        # 取两个图片的像素点
        pixel1 = image1.load()[x, y]
        pixel2 = image2.load()[x, y]
        threshold = 58
        if abs(pixel1[0] - pixel2[0]) < threshold and abs(pixel1[1] - pixel2[1]) < threshold and abs(
                pixel1[2] - pixel2[2]) < threshold:
            return True
        else:
            return False
    
    def get_track(self, distance):
        """根据偏移量获取移动的轨迹列表,主要是模拟人的操作行为,先加速后减速,将每个次move的值用列表存起来,move的总和与偏移量相等
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 移动轨迹, 即每次移动的距离,为一个列表,总和等于偏移量
        track = []
        # 当前位移, 也即记录当前移动了多少距离
        current = 0
        # 减速阈值, 也即开始减速的位置,这里设置为偏移量的4/5处开始减速,可以更改
        mid = distance * 4 / 5
        # 计算用的时间间隔
        t = 0.3
        # 初始速度
        v = 0

        while current < distance:
            if current < mid:
                # 当前位移小于4/5的偏移量时,加速度为2
                a = 2
            else:
                # 当前位移大于4/5的偏移量时,加速度为-3
                a = -3
            # 初始速度v0
            v0 = v
            # 本次移动完成之后的速度v = v0 + at
            v = v0 + a * t
            # 本次移动距离x = v0t + 1/2 * a * t^2
            move = v0 * t + 1 / 2 * a * t * t
            # 当前位移, 这里都将move四舍五入取整
            current += round(move)
            # 将move的距离放入轨迹列表
            track.append(round(move))
            # print("轨迹列表:", track)

        return track
    
    def move_slider(self, slider, track):
        """根据轨迹列表,拖动滑块到缺口处
        :param slider: 滑块
        :param track: 轨迹
        """
        ActionChains(self.browser).click_and_hold(slider).perform()
        for x in track:
            ActionChains(self.browser).move_by_offset(xoffset=x, yoffset=0).perform()
        time.sleep(0.5)
        ActionChains(self.browser).release().perform()

    def run_slider(self):
        img_1 = self.get_image(name='img1.png')
        # 获取滑块对象
        slider = self.get_slider()
        #input()
        # 点击滑块对象,显示有缺口的验证码图片
        # slider.click()
        # 等待6秒, 让点击之后出现提示消失, 方便截图
        # time.sleep(6)
        # 获取有缺口的验证码截图,保存
        img_2 = self.get_image(name='img2.png')
        # 获取偏移量大小
        gap = self.get_gap(img_1, img_2)
        # print('偏移量:', gap)

        # 根据偏移量的值, 计算移动轨迹, 得到轨迹列表, 传入的偏移量可以适当修正, 比如gap-6
        track = self.get_track(gap-3)
        # print("轨迹列表:", track)
        self.move_slider(slider, track)


class BiliBili(SliderCrack, WebDriverHelp):
    def __init__(self,browser):
        super().__init__()
        self.url = 'https://passport.bilibili.com/login'
        self.browser = browser
        # self.browser.execute_script('window.open("%s");'%self.url)
        self.handle = self.browser.window_handles[-1]
        self.wait = WebDriverWait(self.browser,10)

    def set_mail_df(self, df):
        self.mail_df = df
        print(self.mail_df.head())


    def set_info(self,username,password,mail_add,new_password='qwerfdsa'):
        self.username = str(username)
        self.password = str(password)
        self.new_password = str(new_password)
        self.mail_add = str(mail_add)
        print(self.username, self.password,self.mail_add,self.new_password)


    def login(self):
        self.browser.get(self.url)
        username = self.single(By.ID, "login-username")
        password = self.single(By.ID, "login-passwd")
        username.send_keys(self.username)
        password.send_keys(self.password)
        btn_login = self.single(By.CLASS_NAME, "btn-login")
        time.sleep(0.5)
        btn_login.click()
        # input('登录')
        self.wait_for(By.ID,'reportFirst1')
    def logout(self):
        self.browser.get('https://account.bilibili.com/login?act=exit')

    def check_lock_IP(self):
        pass
        
    def re_apply_mail(self,times):
        if times >= 10:
            raise NoMailException('连续邮箱失败次数过多，请检查邮箱文件')
        
        index = generate_mail(self.mail_df)
        if index == -1:
            raise NoMailException('无可用邮箱了')
        print(self.mail_df.loc[index,'mail_add'])
        box = self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[1]/input')
        box.clear()
        box.send_keys(self.mail_df.loc[index,'mail_add'])
        time.sleep(0.5)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/button').click()
        shadow_panel = self.single(By.CSS_SELECTOR,'body > div.geetest_panel.geetest_wind')
        # 等待拼图验证码
        self.wait_for_visible(shadow_panel)
        # 拼图验证码结束
        self.wait_for_visible(shadow_panel,False,30)
        # 检查是否重复
        form_box = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[2]')
        msg = self.wait_for_text(form_box)
        print(msg)
        if msg == '发送成功':
            return index
        else:
            self.mail_df.loc[index,'used'] = 2
            # print(self.mail_df.loc[index])
            return self.re_apply_mail(times+1)

        # self.mail_df.loc[index,'used'] = 1


    def change_password(self):
        try:
            self.login()
        except Exception as e:
            print(e)
            raise LoginException('%s\n登录发生错误认为是密码错误，账号标记为不可用'%str(e))
        self.browser.get('https://passport.bilibili.com/account/security#/setpassword/mail/verify')
        # link_change_password = self.single(By.LINK_TEXT,'修改密码')
        time.sleep(0.5)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/button').click()
        step2 = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div[1]/div/div/div/a[2]')
        self.wait_for_class(step2,'active')
        # input('测试')
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[1]/div[1]/input').send_keys(self.new_password)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/input').send_keys(self.new_password)
        self.wait_for(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[4]/button').click()
        self.wait_for(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/img')


    def change_mail(self):
        try:
            self.login()
        except Exception as e:
            print(e)
            raise LoginException('%s\n登录发生错误认为是密码错误，账号标记为不可用'%str(e))
        self.browser.get('https://passport.bilibili.com/account/security#/bindmail/mail/verify')
        # link_change_password = self.single(By.LINK_TEXT,'修改密码')
        time.sleep(0.5)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[2]/div/div[2]/div/div[2]/div[1]/button').click()
        step2 = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div[1]/div/div/div/a[2]')
        self.wait_for_class(step2,'active')
        try:
            index = self.re_apply_mail(0)
        except NoMailException as nme:
            raise nme
        else:
            step3 = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div[1]/div/div/div/a[3]')
            self.wait_for_class(step3,'active')
            self.logout()
            # print('index_mail = ', index)
            return index



    def reset_password(self):
        self.browser.get('https://passport.bilibili.com/register/findpassword.html#/verify?gourl=https%3A%2F%2Fwww.bilibili.com%2F')
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[3]/div[1]/div[1]/input').send_keys(self.mail_add)
        time.sleep(0.8)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[3]/div[2]/button').click()
        #input()
        # self.run_slider()
        
        step2 = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div/div/a[2]')
        self.wait_for_class(step2,'active')
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[3]/div[1]/div[1]/input').send_keys(self.new_password)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[3]/div[2]/div[1]/input').send_keys(self.new_password)
        time.sleep(0.5)
        self.single(By.XPATH,'//*[@id="app"]/div[3]/div/div[3]/div[4]/div[1]/button').click()
        step3 = self.single(By.XPATH, '//*[@id="app"]/div[3]/div/div[2]/div/div/div/a[3]')
        self.wait_for_class(step3,'active')
        
    def check_login(self):
        try:
            self.login()
        except Exception as e:
            print(e)
            return False
        self.logout()
        return True