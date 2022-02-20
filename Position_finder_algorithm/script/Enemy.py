"""
实体类
"""
import PositionFinderAlgorithm as position_finder_solution ## 导入包

class enemy:
    x = 1.0
    y = 1.0
    velocity = 1.0
    direction = 1.0
    image_radius = 1.0
    attack_radius = 1.0
    uid:str
    destination_x = 1.0
    destination_y = 1.0
    speed = 1.0

    def __init__(self):
        self.y = 0
        self.x = 0
        self.uid = ""
        self.direction = 0
        self.attack_radius = 0
        self.image_radius = 0
        self.destination_x = 0
        self.destination_y = 0
        self.speed = 0

    def get_destination(self,_x:float,_y:float):
        self.destination_x = _x
        self.destination_y = _y

class Postion_finder_algorithm:

    def __init__(self):
        self.boss = enemy()
        self.players = []
        self.ask_in_angle = 1
        self.le_boss_angle = float
        self.ri_boss_angle = float

    def position_finder(self,x: float, y: float, image_radius: float, attack_radius: float, speed: float, uid: str):
        self.add_player(x,y,image_radius,attack_radius,speed,uid)
        ret_x,ret_y = self.solution.find_position(x,y,0,image_radius,attack_radius,speed,uid,self.ask_in_angle,self.le_boss_angle,self.ri_boss_angle)

        if(ret_x < -100 or ret_x > 100):
            ret_x = x
            ret_y = y

        if(ret_y < -100 or ret_y > 100):
            ret_x = x
            ret_y = y

        return ret_x,ret_y

    def position_boss_reset(self,x: float, y: float, image_radius: float, uid: str,ask_in_angle:int,
                            le_boss_angle: float, ri_boss_angle: float):
        """
        重置boss的位置，并且之前的player全部清空
        :return:
        """
        self.le_boss_angle = le_boss_angle
        self.ri_boss_angle = ri_boss_angle
        self.boss.x = x
        self.boss.y = y
        self.boss.image_radius = image_radius
        self.boss.uid = uid
        self.ask_in_angle = ask_in_angle
        self.solution = position_finder_solution.position_finder_algorithm(self.boss.x,
                                                                           self.boss.y,0,self.boss.image_radius,self.boss.attack_radius,self.boss.speed,self.boss.uid)
        ## 导入的是x，y，朝向，自身半径，攻击半径，速度，uid
        ## find_position导入的是 x,y,朝向，自身半径，攻击半径，速度，uid，左边角度，右边角度
        self.players.clear()

    def add_obstacle(self,x:float,y:float,image_radius:float,attack_radius:str,speed:float,uid:str):
        self.solution.add_obstacle(
            x,y,0,image_radius,attack_radius,speed,uid
        )

    def add_player(self,x: float, y: float, image_radius: float, attack_radius: float, speed: float, uid: str):
        new_player = enemy()
        new_player.x = x
        new_player.y = y
        new_player.image_radius = image_radius
        new_player.attack_radius = attack_radius
        new_player.speed = speed
        new_player.uid = uid

        self.players.append(new_player)

    def delete_player_uid(self,uid:str):
        ##删除函数
        pos = 0
        flag = 0
        return_list = list

        for player in self.players:
            if player.uid == uid:
                flag = 1
                break
            pos += 1

        if flag == 1:
            self.players = self.players[:pos] + self.players[pos + 1:]
        else: pos = len(self.players) + 15

        return pos


if __name__ == '__main__':
    new_player = enemy()
    new_player.uid = "fda"

    test = Postion_finder_algorithm()
    test.players.append(new_player)


