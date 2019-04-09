##数据输入部分去除
##PWM输出部分注释
##增加数据接收和数据解算
##双进程暂时去除

##库引入部分
from socket import *
import time
#from picamera import PiCamera
#import picamera.array
import numpy as np, cv2, sys
import multiprocess as mp
import random,pygame
from pygame.locals import *
import threading
#try:
#    import RPi.GPIO as GPIO
#except RuntimeError:
#    print("引入错误")
##库引入部分 END

##数据接收线程函数
RECV_DATA = 'FromPC+0+0+0+0+0+0+0+0+0+0+0+0+B'

def recv(sock, BUFSIZ):
    while True:
        try:
            global RECV_DATA
            RECV_DATA = sock.recv(BUFSIZ).decode()
        except OSError:
            return  # find it was close, then close it
##数据接收线程函数 END 

##服务器端连接状态
HOST = "47.103.39.180"
POST = 7890
ADDR = (HOST,POST)
client = socket(AF_INET,SOCK_STREAM)
client.connect(ADDR)
threadrev = threading.Thread(target = recv , args = (client, 1024))
threadrev.start()
##服务器端连接状态 END #无数据传输时无影响







##占空比范围限制函数
def Limit_PWM(A):
    if (A < 0):
        A = 0
    elif (A > 99):
        A = 99;
    return A
##占空比范围限制函数 END

             
##数据键入、解算、发送进程函数
def motionControl(enable):

    ##Pygame显示初始化
    key_flag = False
    pygame.init()
    screen = pygame.display.set_mode((400,400))
    pygame.display.set_caption("挖掘机控制平台")
    font1 = pygame.font.Font(None, 24)
    font2 = pygame.font.Font(None, 200)
    white = 255,255,255
    yellow = 255,255,0
    color = 125,100,210
    #指示变量：
    def print_text(font, x, y, text, color=(255,255,255)):
        imgText = font.render(text, True, color)
        screen.blit(imgText, (x,y))
    ##Pygame显示初始化 END
        
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

    

    ##初始化GPIO 对应引脚见：https://blog.csdn.net/qq21497936/article/details/79758560
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(4, GPIO.OUT)
    #GPIO.setup(14, GPIO.OUT)
    #GPIO.setup(17, GPIO.OUT)
    #GPIO.setup(18, GPIO.OUT)
    #GPIO.setup(22, GPIO.OUT)
    #GPIO.setup(23, GPIO.OUT)
    #GPIO.setup(9, GPIO.OUT)
    #GPIO.setup(25, GPIO.OUT)
    #GPIO.setup(11, GPIO.OUT)
    #GPIO.setup(8, GPIO.OUT)
    #GPIO.setup(6, GPIO.OUT)
    #GPIO.setup(12, GPIO.OUT)
    #Motor_A_0 = GPIO.PWM(4,1000)
    #Motor_A_1 = GPIO.PWM(14,1000)
    #Motor_B_0 = GPIO.PWM(17,1000)
    #Motor_B_1 = GPIO.PWM(18,1000)
    #Motor_C_0 = GPIO.PWM(22,1000)
    #Motor_C_1 = GPIO.PWM(23,1000)
    #Motor_D_0 = GPIO.PWM(9,1000)
    #Motor_D_1 = GPIO.PWM(25,1000)
    #Motor_E_0 = GPIO.PWM(11,1000)
    #Motor_E_1 = GPIO.PWM(8,1000)
    #Motor_F_0 = GPIO.PWM(6,1000)
    #Motor_F_1 = GPIO.PWM(12,1000) 

    #Motor_A_0.start(0)
    #Motor_A_1.start(0)
    #Motor_B_0.start(0)
    #Motor_B_1.start(0)
    #Motor_C_0.start(0)
    #Motor_C_1.start(0)
    #Motor_D_0.start(0)
    #Motor_D_1.start(0)
    #Motor_E_0.start(0)
    #Motor_E_1.start(0)
    #Motor_F_0.start(0)
    #Motor_F_1.start(0) 

    ##进程中主循环
    while enable.value == 1:
        ##定时发生
        current = time.clock() - clock_start
        if (current > 0.1):
            ##接收到的数据解算，输出到PWM占空比
            global RECV_DATA
            data_tmp = RECV_DATA[0:42]
            #print("recv:",data_tmp)
            if data_tmp :
                Decoded_data = data_tmp.split('+')[0:13]
                if len(Decoded_data)>12 :
                  print(Decoded_data[1],'+',Decoded_data[2],'+',Decoded_data[3],'+',Decoded_data[4],'+',)
                  PWM_A_0 = int(Decoded_data[1])
                  PWM_A_1 = int(Decoded_data[2])
                  PWM_B_0 = int(Decoded_data[3])
                  PWM_B_1 = int(Decoded_data[4])
                  PWM_C_0 = int(Decoded_data[5])
                  PWM_C_1 = int(Decoded_data[6])
                  PWM_D_0 = int(Decoded_data[7])
                  PWM_D_1 = int(Decoded_data[8])
                  PWM_E_0 = int(Decoded_data[9])
                  PWM_E_1 = int(Decoded_data[10])
                  PWM_F_0 = int(Decoded_data[11])
                  PWM_F_1 = int(Decoded_data[12])
            #Motor_A_0.ChangeDutyCycle(PWM_A_0)
            #Motor_A_1.ChangeDutyCycle(PWM_A_1)
            #Motor_B_0.ChangeDutyCycle(PWM_B_0)
            #Motor_B_1.ChangeDutyCycle(PWM_B_1)
            #Motor_C_0.ChangeDutyCycle(PWM_C_0)
            #Motor_C_1.ChangeDutyCycle(PWM_C_1)
            #Motor_D_0.ChangeDutyCycle(PWM_D_0)
            #Motor_D_1.ChangeDutyCycle(PWM_D_1)
            #Motor_E_0.ChangeDutyCycle(PWM_E_0)
            #Motor_E_1.ChangeDutyCycle(PWM_E_1)
            #Motor_F_0.ChangeDutyCycle(PWM_F_0)
            #Motor_F_1.ChangeDutyCycle(PWM_F_1)

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
	#更新
        pygame.display.update()
        ##电机控制进程主循环结束


#graph diaplay ##在这里面进行视频数据发送!
def displayImage(enable):
    if 0:
        print('0')
        
    #print("img OK")
    #camera = PiCamera()
    #output = picamera.array.PiRGBArray(camera)
    #camera.resolution = (400, 400) # 图像大小
    #camera.framerate=30 # 帧
    #for frame in camera.capture_continuous(output, format="bgr", use_video_port=True):
    #    img = output.array
    #    if img is not None:
    #        cv2.imshow('Tracking', img)
    #        cv2.waitKey(1)
    #    output.truncate(0)
    #    if enable.value == 0:
    #    	break
        
    #print('Quit displayImage')
    #cv2.destroyAllWindows()
    #camera.close()

##主函数
def main():
        enable = mp.Value('i', 0)
    #while True:
        enable.value = 1
        motionControl(enable)
        #判断是否开始
        #sign = input("请输入控制命令：")
        #print('sign = {}'.format(sign))
        #if sign == '1':#bytes([0x01])
        #    print('Program Begin!')
        #    enable.value = 1
        #    mp.Process(target=motionControl, args=(enable,)).start()
        #    mp.Process(target=displayImage, args=(enable,)).start()
            
        #elif sign == '2':
        #    print('Program Stop!')
        #    enable.value = 0

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
        #camera.close()

