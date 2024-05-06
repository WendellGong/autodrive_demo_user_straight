import os
import sys
print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import time
import json
from socket_config import *
from vehicleControl import *
import config
import math
from utils import get_line_error,PID
sceneInfoOutputGap = config.sceneInfoOutputGap

turn_pid_obj = PID(kp=1.8, motion_kp=2.5, kd=25)
speed_pid_obj = PID(kp=0.8, motion_kp=0.4, kd=5)
pathlistx = []
pathlisty = []
base_speed = 10

def algorithm(apiList:APIList, vehicleControl1:vehicleControlAPI):
    control_velocity = 0
    control_steer = 0
    global turn_pid_obj
    global speed_pid_obj
    global base_speed
    global pathlistx
    global pathlisty
    endflag = False
    
    # 计算主车速度
    car_velx = apiList.DataGnssAPI()['velX']
    car_vely = apiList.DataGnssAPI()['velY']
    main_car_speed = pow(car_velx**2+car_vely**2+0.00001, 0.5)
    main_car_speed = math.sqrt(pow(car_velx, 2) + pow(car_vely, 2))


    # 根据道路线得打角值
    road_line_info = apiList.RoadLineListAPI()
    car_posx = apiList.DataGnssAPI()['posX']
    car_posy = apiList.DataGnssAPI()['posY']
    car_pos = (car_posx,  car_posy)
    error = get_line_error(car_pos, road_line_info)
    steering = turn_pid_obj.update(error)
    print("steering: ", steering)

    # 根据前方道路障碍物有无计算速度
    ObstacleEntryList = apiList.ObstacleEntryListAPI()

    if len(ObstacleEntryList) >= 0:
        # print(ObstacleEntryList)
        dis_error = math.sqrt(pow(car_posx - ObstacleEntryList[0]["posX"], 2) +
                              pow(car_posy - ObstacleEntryList[0]["posY"] - 4, 2))

        if dis_error < 0.6:
            endflag = True
        else:
            print(print(car_posx - ObstacleEntryList[0]["posX"], car_posy - ObstacleEntryList[0]["posY"]))
            print(dis_error)
        #print(dis_error)
        base_speed = speed_pid_obj.update(dis_error) * 0.5
        # print(base_speed)

    #print(ObstacleEntryList)

    speed = base_speed

    if abs(steering) >= 0.2:
        speed = base_speed*0.7

    if main_car_speed >= speed * 0.6:
        vehicleControl1.brake = 9
        vehicleControl1.throttle = 0
    else:
        if main_car_speed <= 6:
            vehicleControl1.brake = 0
            vehicleControl1.throttle = 1
        print("main_car_speed:", main_car_speed)

    if endflag:
        vehicleControl1.brake = 0.1
        vehicleControl1.throttle = 0
    else:
        pathlistx.append(car_posx)
        pathlisty.append(car_posy)

    vehicleControl1.pathlistx = pathlistx
    vehicleControl1.pathlisty = pathlisty

    vehicleControl1.steering = steering

    control_dict_demo = json_encoder(vehicleControl1)
    control_dict_demo = json.dumps(control_dict_demo)
    # print("speed:",main_car_speed)
    # print("throttle:",vehicleControl1.throttle,"steering:",vehicleControl1.steering)
    return control_dict_demo

def main():
    loop_counter = 0
    vehicleControl1 = vehicleControlAPI(0, 0, 0)  # 控制初始化
    socketServer = SocketServer()
    socketServer.socket_connect()

    while True:
        dataState, apiList = socketServer.socket_launch()

        if dataState and loop_counter == 0:
            socketServer.socket_respond()

        elif dataState and apiList.messageState() and loop_counter != 0:
            if (loop_counter>=2):
                control_dict_demo = algorithm(apiList, vehicleControl1)
                socketServer.socket_send(control_dict_demo)
        loop_counter += 1


if __name__ == "__main__":
    main()

