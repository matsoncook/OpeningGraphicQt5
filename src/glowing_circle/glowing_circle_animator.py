from base.animator import Animator
from base.base_object import BaseObject


class MoveGenerally(Animator):
    def __init__(self,base_bject: BaseObject, the_lambda):
        super().__init__()
        self.base_bject = base_bject
        self.the_lambda = the_lambda
        self.velocity = 1
        self.direction = 1
        self.x = -1
        self.reset()

    def do_update(self, elapsed_time_secs):
        distance_elapse = self.velocity * elapsed_time_secs

        #c_x = self.glowing_circle.circle_center[0]
        c_x = self.x

        c_x += distance_elapse * self.direction

        if c_x >= 1.0 or c_x <= -1.0:
            self.direction *= -1

        c_x += (0.01 * self.direction)



        self.x = c_x
        return False

    def next_animation(self) -> "Animator":
        return None

    def reset(self):
        self.x = -1
        return

class MoveRight_1(Animator):
    def __init__(self,base_object: BaseObject,velocity = 1.0):
        super().__init__()
        self.base_object = base_object
        self.velocity = velocity
        self.direction = 1
        self.x = -1
        self.reset()

    def do_update(self, elapsed_time_secs):
        finish = False
        distance_elapse = self.velocity * elapsed_time_secs

        #c_x = self.glowing_circle.circle_center[0]
        c_x = self.x

        c_x += distance_elapse * self.direction

        if c_x >= 1.0 or c_x <= -1.0:
            self.direction *= -1
            finish = True

        #c_x += (0.01 * self.direction)


        self.base_object.set_position(c_x, self.base_object.world_matrix[3,1])
        self.x = c_x
        return finish

    def next_animation(self) -> "Animator":
        return MoveLeft_1(self.base_object,0.5)

    def reset(self):
        self.x = -1
        return

class MoveLeft_1(Animator):
    def __init__(self, base_object: BaseObject,velocity = 1.0):
        super().__init__()
        self.base_object = base_object
        self.velocity = velocity
        self.direction = -1
        self.x = 1
        self.reset()

    def do_update(self, elapsed_time_secs):
        finish  = False
        distance_elapse = self.velocity * elapsed_time_secs

        # c_x = self.glowing_circle.circle_center[0]
        c_x = self.x

        c_x += distance_elapse * self.direction

        if c_x >= 1.0 or c_x <= -1.0:
            self.direction *= -1
            finish = True

        direction_y = self.base_object.world_matrix[3,1]
        if direction_y >= 0:
            direction_y = 1.0
        else:
            direction_y = -1.0

        self.base_object.set_position(c_x, self.base_object.world_matrix[3,1]+( 0.003 * direction_y ))
        self.x = c_x
        return finish

    def next_animation(self) -> "Animator":
        return MoveRight_1(self.base_object,0.25)

    def reset(self):
        self.x = 1
        return

