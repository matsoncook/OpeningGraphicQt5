from abc import ABC, abstractmethod

class Animator(ABC):
    def __init__(self):
        self.current_time_ms = 0
        self.previous_time_ms = 0
        self.elapsed_time_ms = 0

    def update(self, current_time_ms) -> bool:
        if self.previous_time_ms == 0:
            self.previous_time_ms = current_time_ms
            return False
        self.current_time_ms = current_time_ms
        self.elapsed_time_ms = self.current_time_ms - self.previous_time_ms
        finish = self.do_update( self.elapsed_time_ms / 1000 )
        self.previous_time_ms = current_time_ms
        return finish

    @abstractmethod
    def do_update(self,elapsed_time):
        return False

    @abstractmethod
    def next_animation(self)-> "Animator":
        return None

    @abstractmethod
    def reset(self):
        return


