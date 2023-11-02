# 이것은 각 상태들을 객체로 구현한 것임.
import random

from pico2d import load_image
import game_framework

# state event check
# ( state event type, event value )


# bird Run Speed
# fill here

PIXEL_PER_METER = (10.0 / 0.3) # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0 # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# bird Action Speed
# fill here

TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 0.5 / TIME_PER_ACTION
FRAMES_PER_ACTION = 14


class Run:

    @staticmethod
    def enter(bird, e):
        bird.dir = 1

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        bird.frame_all = (bird.frame_all + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 14
        if bird.x < 50:
            bird.dir = 1
        elif bird.x > 1550:
            bird.dir = -1
        bird.frame = bird.frame_all % 5
        bird.action = 2 - int(bird.frame_all / 5)
        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_draw(int(bird.frame) * 183, int(bird.action) * 168, 183, 168, bird.x, bird.y, 80, 70)
        if bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, int(bird.action) * 168, 183, 168, 0, 'h', bird.x, bird.y, 80, 70)



class StateMachine:
    def __init__(self, bird):
        self.bird = bird
        self.cur_state = Run

    def start(self):
        self.cur_state.enter(self.bird, ('NONE', 0))

    def update(self):
        self.cur_state.do(self.bird)

    def handle_event(self, e):
        for check_event, next_state in self.transitions[self.cur_state].items():
            if check_event(e):
                self.cur_state.exit(self.bird, e)
                self.cur_state = next_state
                self.cur_state.enter(self.bird, e)
                return True

        return False

    def draw(self):
        self.cur_state.draw(self.bird)


class Bird:
    def __init__(self):
        self.x, self.y = random.randint(20, 1580), 500
        self.frame = 0
        self.frame_all = random.randint(0, 13)
        self.action = 3
        self.face_dir = 1
        self.dir = 0
        self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start()

    def update(self):
        self.state_machine.update()

    def handle_event(self, event):
        self.state_machine.handle_event(('INPUT', event))

    def draw(self):
        self.state_machine.draw()
