from typing import List

from base.animator import Animator


class BaseObject:
    def __init__(self):
        self.animator_list: List[Animator] = []

    def update(self,time_ms):
        for animator in self.animator_list:
            finish = animator.update(time_ms)
            if finish:
                self.animator_list.remove(animator)
                if animator.next_animation() is not None:
                    self.animator_list.append(animator.next_animation())
                    animator.next_animation().reset()

    def add_animator(self, animator: Animator):
        self.animator_list.append(animator)