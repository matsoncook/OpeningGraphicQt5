from typing import List

from base.animator import Animator


class BaseObject:
    def __init__(self, name):
        self.name = name
        self.animator_list: List[Animator] = []
        self.children: List["BaseObject"] = []

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
    def init_gl(self):
        pass

    def init(self):
        self.init_gl()
        for base_object in self.children:
            base_object.init()



class GroupObject(BaseObject):
    def __init__(self,name):
        super().__init__(name)


