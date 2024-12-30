from base.animator import Animator

class MoveGenerally(Animator):
    def __init__(self,glowing_circle):
        super().__init__()
        self.glowing_circle = glowing_circle
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


        self.glowing_circle.set_circle_center_x(c_x)
        self.x = c_x
        return False

    def next_animation(self) -> "Animator":
        return None

    def reset(self):
        self.x = -1
        return

class MoveRight_1(Animator):
    def __init__(self,glowing_circle,velocity = 1.0):
        super().__init__()
        self.glowing_circle = glowing_circle
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


        self.glowing_circle.set_circle_center_x(c_x)
        self.x = c_x
        return finish

    def next_animation(self) -> "Animator":
        return MoveLeft_1(self.glowing_circle,0.5)

    def reset(self):
        self.x = -1
        return

class MoveLeft_1(Animator):
    def __init__(self, glowing_circle,velocity = 1.0):
        super().__init__()
        self.glowing_circle = glowing_circle
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



        self.glowing_circle.set_circle_center_x(c_x)
        self.x = c_x
        return finish

    def next_animation(self) -> "Animator":
        return MoveRight_1(self.glowing_circle,0.25)

    def reset(self):
        self.x = 1
        return

