import contextlib
import os
import time

import config
from vehicleControl import *
from socket_config import *

print(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sceneInfoOutputGap = config.sceneInfoOutputGap


def going_straight(apiList, vehicleControl1):
    """
    车辆直行指定距离后平稳刹车，刚好停在目标位置。
    :param apiList: 来自仿真环境的API数据。
    :param vehicleControl1: 车辆控制API对象。
    :param target_distance: 目标距离，单位为米，默认为 50 米。
    :return: 控制命令字典的JSON字符串。
    """

    target_distance = 50

    current_distance = apiList.DataGnssAPI()

    # 获取初始位置，避免重复获取
    if not hasattr(vehicleControl1, 'start_position_x') or not hasattr(vehicleControl1, 'start_position_y'):
        vehicleControl1.start_position_x = int(current_distance['posX'])
        vehicleControl1.start_position_y = int(current_distance['posY'])

    # 计算当前位置到目标位置的距离
    current_x = int(current_distance['posX'])
    current_y = int(current_distance['posY'])
    start_x = int(vehicleControl1.start_position_x)
    start_y = int(vehicleControl1.start_position_y)
    current_speed = apiList.DataMainVehilceAPI()['speed']
    print(f'current_speed: {current_speed}')

    # 使用整数差的绝对值来避免浮点数
    distance_x = abs(current_x - start_x)
    distance_y = abs(current_y - start_y)
    distance_to_target = (distance_x ** 2 + distance_y ** 2) ** 0.5
    print(f'distance_to_target: {distance_to_target}')

    # 油门控制逻辑还不清楚
    vehicleControl1.__throttleSet__(throttle=0.5, speed=15, keyboardModel=False)

    pre_brake = 4
    # 判断是否到达刹车开始位置
    # if distance_to_target + pre_brake >= 50:
    #     vehicleControl1.__brakeSet__(brake=1, speed=10, keyboardModel=False)
    #     vehicleControl1.__throttleSet__(throttle=0, speed=0, keyboardModel=False)
    #     print('开始刹车')
    # 编码控制指令
    control_command = json_encoder(vehicleControl1)
    return json.dumps(control_command)


def main():
    loop_counter = 0
    vehicleControl1 = vehicleControlAPI(0, 0, 0, 120)  # 控制初始化
    socketServer = SocketServer()
    socketServer.socket_connect()

    # 获取当前时间并格式化
    current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
    filename = f"debug_{current_time}.txt"

    with open(filename, "a", encoding="utf-8") as f:
        with contextlib.redirect_stdout(f):
            while True:
                dataState, apiList = socketServer.socket_launch()

                if dataState:
                    if apiList is not None:
                        if loop_counter % sceneInfoOutputGap == 1:
                            print("\n\nInfo begin:")
                            apiList.showAllState()
                            print("gear mode: ", vehicleControl1.gear)

                    if loop_counter == 0:
                        socketServer.socket_respond()

                    elif apiList.messageState() and loop_counter != 0:
                        # 调用直行算法函数，传入当前的apiList和vehicleControl对象
                        control_dict_demo = going_straight(apiList, vehicleControl1)

                        # 发送控制命令给仿真环境
                        socketServer.socket_send(control_dict_demo)

                loop_counter += 1


if __name__ == "__main__":
    main()
