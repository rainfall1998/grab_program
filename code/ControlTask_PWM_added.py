#encoding=utf-8
import sys,random,time,pygame
from pygame.locals import *

try:
    import RPi.GPIO as GPIO
except RuntimeError:
    print("引入错误")



##Python3
##不太会写Python了
##键位设置：
'''
W -- 前进
S -- 后退
A -- 左转
D -- 右转
Q -- 云台左旋
E -- 云台右旋
U -- 臂根上摆
I -- 臂根下摆
J -- 臂茎上摆
K -- 臂茎下摆
M -- 臂叶上摆
, -- 臂叶下摆
↑ -- 加速
↓ -- 减速
'''
##所有状态可以叠加，即可以同时按下不同的按键来使所有动作同时进行（相矛盾的操作除外）


#指示变量：
CM_forward_back_dir = 0    ##底盘前后指示，0为停止，1为前进，2为后退
CM_forward_back_speed  = 40##底盘前后速度,0-99
CM_left_right_dir = 0      ##底盘左右指示，0为停止，1为左转，2为右转
CM_left_right_speed = 40   ##底盘转向速度,0-99
GM_rotate_dir = 0          ##云台旋转指示，0为停止，1为左旋，2为右旋
GM_rotate_speed = 40        ##云台旋转速度,0-99
ARM_root_dir = 0           ##臂根上下指示，0为停止，1为上摆，2为下摆
ARM_root_speed = 40         ##臂根上下速度,0-99
ARM_stem_dir = 0           ##臂茎上下指示，0为停止，1为上摆，2为下摆
ARM_stem_speed = 40         ##臂茎上下速度,0-99
ARM_leaf_dir = 0           ##臂叶上下指示，0为停止，1为上摆，2为下摆
ARM_leaf_speed = 40         ##臂叶上下速度,0-99

##输出占空比：
PWM_A_0 = 0        ##PWM范围为0-99(暂定)   
PWM_A_1 = 0        ##A:底盘左侧电机 B:底盘右侧电机 C:云台电机 D:臂根电机 E:臂茎电机 F:臂叶电机
PWM_B_0 = 0
PWM_B_1 = 0
PWM_C_0 = 0
PWM_C_1 = 0
PWM_D_0 = 0
PWM_D_1 = 0
PWM_E_0 = 0
PWM_E_1 = 0
PWM_F_0 = 0
PWM_F_1 = 0

##用于计时函数
current = 0
clock_start = 0

##用于按键调速
last_key_up = 0
last_key_down = 0



def print_text(font, x, y, text, color=(255,255,255)):
    imgText = font.render(text, True, color)
    screen.blit(imgText, (x,y))
    

#主程序
pygame.init()
screen = pygame.display.set_mode((600,500))
pygame.display.set_caption("挖掘机控制平台")
font1 = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 200)
white = 255,255,255
yellow = 255,255,0
color = 125,100,210

##初始化GPIO 对应引脚见：https://blog.csdn.net/qq21497936/article/details/79758560
GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(14, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(18, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(23, GPIO.OUT)
GPIO.setup(9, GPIO.OUT)
GPIO.setup(25, GPIO.OUT)
GPIO.setup(11, GPIO.OUT)
GPIO.setup(8, GPIO.OUT)
GPIO.setup(6, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
Motor_A_0 = GPIO.PWM(4,1000)
Motor_A_1 = GPIO.PWM(14,1000)
Motor_B_0 = GPIO.PWM(17,1000)
Motor_B_1 = GPIO.PWM(18,1000)
Motor_C_0 = GPIO.PWM(22,1000)
Motor_C_1 = GPIO.PWM(23,1000)
Motor_D_0 = GPIO.PWM(9,1000)
Motor_D_1 = GPIO.PWM(25,1000)
Motor_E_0 = GPIO.PWM(11,1000)
Motor_E_1 = GPIO.PWM(8,1000)
Motor_F_0 = GPIO.PWM(6,1000)
Motor_F_1 = GPIO.PWM(12,1000)

Motor_A_0.start(0)
Motor_A_1.start(0)
Motor_B_0.start(0)
Motor_B_1.start(0)
Motor_C_0.start(0)
Motor_C_1.start(0)
Motor_D_0.start(0)
Motor_D_1.start(0)
Motor_E_0.start(0)
Motor_E_1.start(0)
Motor_F_0.start(0)
Motor_F_1.start(0)

##GPIO初始化完毕

##占空比范围限制函数
def Limit_PWM(A):
    if (A < 0):
        A = 0
    elif (A > 99):
        A = 99;
    return A
## def Limit_PWM() FINISHED


#输出PWM占空比结算，依据
def CAL_to_PWM(CM_forward_back_dir,CM_forward_back_speed,CM_left_right_dir,CM_left_right_speed, \
               GM_rotate_dir,GM_rotate_speed,ARM_root_dir,ARM_root_speed,ARM_stem_dir,ARM_stem_speed, \
               ARM_leaf_dir,ARM_leaf_speed):
    ##底盘两个电机结算
    
    if (CM_forward_back_dir == 0 ):
        CM_PWM_LEFT = 0
        CM_PWM_RIGHT = 0
    elif (CM_forward_back_dir == 1):
        CM_PWM_LEFT = CM_forward_back_speed
        CM_PWM_RIGHT = CM_forward_back_speed
    elif (CM_forward_back_dir == 2):
        CM_PWM_LEFT = CM_forward_back_speed
        CM_PWM_RIGHT = CM_forward_back_speed
        
    if (CM_left_right_dir == 0 ):
        CM_PWM_LEFT = CM_PWM_LEFT
        CM_PWM_RIGHT = CM_PWM_RIGHT
    elif (CM_left_right_dir == 1 ):
        CM_PWM_LEFT = CM_PWM_LEFT + CM_left_right_speed/3
        CM_PWM_RIGHT = CM_PWM_RIGHT + CM_left_right_speed
    elif (CM_left_right_dir == 2):
        CM_PWM_LEFT = CM_PWM_LEFT + CM_left_right_speed
        CM_PWM_RIGHT = CM_PWM_RIGHT + CM_left_right_speed/3

    if (CM_forward_back_dir == 0 ):
        PWM_A_0 = CM_PWM_LEFT
        PWM_A_1 = 0
        PWM_B_0 = CM_PWM_RIGHT
        PWM_B_1 = 0
    elif (CM_forward_back_dir == 1):
        PWM_A_0 = CM_PWM_LEFT
        PWM_A_1 = 0
        PWM_B_0 = CM_PWM_RIGHT
        PWM_B_1 = 0
    elif (CM_forward_back_dir == 2):
        PWM_A_0 = 0
        PWM_A_1 = CM_PWM_LEFT
        PWM_B_0 = 0
        PWM_B_1 = CM_PWM_RIGHT
               
    #云台电机结算：
    if (GM_rotate_dir == 0 ):
        PWM_C_0 = 0
        PWM_C_1 = 0
    elif (GM_rotate_dir == 1):
        PWM_C_0 = GM_rotate_speed
        PWM_C_1 = 0
    elif (GM_rotate_dir == 2):
        PWM_C_0 = 0;
        PWM_C_1 = GM_rotate_speed
               
    #臂根电机结算：
    if (ARM_root_dir == 0 ):
        PWM_D_0 = 0
        PWM_D_1 = 0
    elif (ARM_root_dir == 1):
        PWM_D_0 = ARM_root_speed
        PWM_D_1 = 0
    elif (ARM_root_dir == 2):
        PWM_D_0 = 0
        PWM_D_1 = ARM_root_speed

    #臂茎电机结算：
    if (ARM_stem_dir == 0 ):
        PWM_E_0 = 0
        PWM_E_1 = 0
    elif (ARM_stem_dir == 1):
        PWM_E_0 = ARM_stem_speed
        PWM_E_1 = 0
    elif (ARM_stem_dir == 2):
        PWM_E_0 = 0
        PWM_E_1 = ARM_stem_speed

    #臂叶电机结算：
    if (ARM_leaf_dir == 0 ):
        PWM_F_0 = 0
        PWM_F_1 = 0
    elif (ARM_leaf_dir == 1):
        PWM_F_0 = ARM_leaf_speed
        PWM_F_1 = 0
    elif (ARM_leaf_dir == 2):
        PWM_F_0 = 0
        PWM_F_1 = ARM_leaf_speed

    ##对占空比进行限制
    PWM_A_0 = Limit_PWM(PWM_A_0)
    PWM_A_1 = Limit_PWM(PWM_A_1)
    PWM_B_0 = Limit_PWM(PWM_B_0)
    PWM_B_1 = Limit_PWM(PWM_B_1)
    PWM_C_0 = Limit_PWM(PWM_C_0)
    PWM_C_1 = Limit_PWM(PWM_C_1)
    PWM_D_0 = Limit_PWM(PWM_D_0)
    PWM_D_1 = Limit_PWM(PWM_D_1)
    PWM_E_0 = Limit_PWM(PWM_E_0)
    PWM_E_1 = Limit_PWM(PWM_E_1)
    PWM_F_0 = Limit_PWM(PWM_F_0)
    PWM_F_1 = Limit_PWM(PWM_F_1)
        
    
    return PWM_A_0,PWM_A_1,PWM_B_0,PWM_B_1,PWM_C_0,PWM_C_1, \
           PWM_D_0,PWM_D_1,PWM_E_0,PWM_E_1,PWM_F_0,PWM_F_1
##  def CAL_to_PWM() FINISHED             
    
    


#clock_start = 0
key_flag = False

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == KEYDOWN:
            key_flag = True
        elif event.type == KEYUP:
            key_flag = False
            

    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    if keys[K_RETURN]:
        0
        
    if keys[K_w]:
        CM_forward_back_dir = 1
    elif keys[K_s]:
        CM_forward_back_dir = 2
    else:
        CM_forward_back_dir = 0
        
    if keys[K_a]:
        CM_left_right_dir = 1
    elif keys[K_d]:
        CM_left_right_dir = 2
    else:
        CM_left_right_dir = 0
        
    if keys[K_q]:
        GM_rotate_dir = 1
    elif keys[K_e]:
        GM_rotate_dir = 2
    else:
        GM_rotate_dir = 0

    if keys[K_u]:
        ARM_root_dir = 1
    elif keys[K_i]:
        ARM_root_dir = 2
    else:
        ARM_root_dir = 0

    if keys[K_j]:
        ARM_stem_dir = 1
    elif keys[K_k]:
        ARM_stem_dir = 2
    else:
        ARM_stem_dir = 0

    if keys[K_m]:
        ARM_leaf_dir = 1
    elif keys[K_COMMA]:
        ARM_leaf_dir = 2
    else:
        ARM_leaf_dir = 0

    if (keys[K_UP]):
        if (last_key_up == 0):
            CM_forward_back_speed += 10
            last_key_up = 1
        if (CM_forward_back_speed > 70):
            CM_forward_back_speed = 70
    elif (keys[K_DOWN]):
        if (last_key_down == 0):
            CM_forward_back_speed -= 10
            last_key_down = 1
        if (CM_forward_back_speed < 0):
            CM_forward_back_speed = 0
    else:
        last_key_up = 0
        last_key_down = 0

        
    
        

    #数据结算
    PWM_A_0,PWM_A_1,PWM_B_0,PWM_B_1,PWM_C_0,PWM_C_1, \
    PWM_D_0,PWM_D_1,PWM_E_0,PWM_E_1,PWM_F_0,PWM_F_1 = \
    CAL_to_PWM(CM_forward_back_dir,CM_forward_back_speed,CM_left_right_dir,CM_left_right_speed, \
               GM_rotate_dir,GM_rotate_speed,ARM_root_dir,ARM_root_speed,ARM_stem_dir,ARM_stem_speed, \
               ARM_leaf_dir,ARM_leaf_speed)

    
    ##PWM对应输出
    current = time.clock() - clock_start
    if (current > 0.1):
        ##执行PWM改变命令，待封个函数
        Motor_A_0.ChangeDutyCycle(PWM_A_0)
        Motor_A_1.ChangeDutyCycle(PWM_A_1)
        Motor_B_0.ChangeDutyCycle(PWM_B_0)
        Motor_B_1.ChangeDutyCycle(PWM_B_1)
        Motor_C_0.ChangeDutyCycle(PWM_C_0)
        Motor_C_1.ChangeDutyCycle(PWM_C_1)
        Motor_D_0.ChangeDutyCycle(PWM_D_0)
        Motor_D_1.ChangeDutyCycle(PWM_D_1)
        Motor_E_0.ChangeDutyCycle(PWM_E_0)
        Motor_E_1.ChangeDutyCycle(PWM_E_1)
        Motor_F_0.ChangeDutyCycle(PWM_F_0)
        Motor_F_1.ChangeDutyCycle(PWM_F_1)

        clock_start = time.clock()

    ##PWM对应输出完毕
       
    

 
    #清屏
    screen.fill(color)
 
    print_text(font1, 0, 20, "NOW THE OUTPUT IS:")
    print_text(font1, 0, 40, "PWM_A_0:" + str(int(PWM_A_0)))
    print_text(font1, 0, 60, "PWM_A_1:" + str(int(PWM_A_1)))
    print_text(font1, 0, 80, "PWM_B_0:" + str(int(PWM_B_0)))
    print_text(font1, 0, 100, "PWM_B_1:" + str(int(PWM_B_1)))
    print_text(font1, 0, 120, "PWM_C_0:" + str(int(PWM_C_0)))
    print_text(font1, 0, 140, "PWM_C_1:" + str(int(PWM_C_1)))
    print_text(font1, 0, 160, "PWM_D_0:" + str(int(PWM_D_0)))
    print_text(font1, 0, 180, "PWM_D_1:" + str(int(PWM_D_1)))
    print_text(font1, 0, 200, "PWM_E_0:" + str(int(PWM_E_0)))
    print_text(font1, 0, 220, "PWM_E_1:" + str(int(PWM_E_1)))
    print_text(font1, 0, 240, "PWM_F_0:" + str(int(PWM_F_0)))
    print_text(font1, 0, 260, "PWM_F_1:" + str(int(PWM_F_1)))

    print_text(font1, 450, 40, "Speed:"+ str(int(CM_forward_back_speed)))
    

    
    




    
    #更新
    pygame.display.update()
