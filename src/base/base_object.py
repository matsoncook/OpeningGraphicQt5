from typing import List

import numpy as np

from base.animator import Animator
from shaders import Shaders


class BaseObject:
    def __init__(self, name):
        self.name = name
        self.animator_list: List[Animator] = []
        self.children: List["BaseObject"] = []
        self.translate = (0,0,0)
        self.world_matrix = np.eye(4)

    def update(self,time_ms):

        for animator in self.animator_list:
            finish = animator.update(time_ms)
            if finish:
                self.animator_list.remove(animator)
                if animator.next_animation() is not None:
                    self.animator_list.append(animator.next_animation())
                    animator.next_animation().reset()

        for base_object in self.children:
            base_object.update(time_ms)

    def add_animator(self, animator: Animator):
        self.animator_list.append(animator)

    def add_child(self, base_object:"BaseObject"):
        self.children.append(base_object)

    #override this to do initialisation
    def init_gl(self,shaders: Shaders):
        pass

    # override this to do resize
    def resize_gl(self,w,h):
        pass

    # override this to paint
    def paint_gl(self,context):
        pass

    def init(self,shaders: Shaders):
        self.init_gl(shaders)
        for base_object in self.children:
            base_object.init(shaders)

    def paint_prepare(self):
        pass

    def paint(self,context):
        self.paint_prepare()
        self.paint_gl(context)
        for base_object in self.children:
            base_object.paint(context)

    def resize(self,w,h):
        self.resize_gl(w,h)
        for base_object in self.children:
            base_object.resize(w,h)

    def set_position(self, x, y, z=0.0):

        self.world_matrix[3, 0] = x
        self.world_matrix[3, 1] = y
        self.world_matrix[3, 2] = z

    def move_position(self, x=0.0, y=0.0, z=0.0):

        self.world_matrix[3, 0] += x
        self.world_matrix[3, 1] += y
        self.world_matrix[3, 2] += z

class GroupObject(BaseObject):
    def __init__(self,name):
        super().__init__(name)


