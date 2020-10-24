"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

The class for breakout_extension.py
"""
from campy.graphics.gwindow import GWindow
from campy.graphics.gobjects import GOval, GRect
from campy.graphics.gimage import GImage
from campy.gui.events.mouse import onmouseclicked, onmousemoved
from campy.gui.events.timer import pause
import random

BRICK_SPACING = 5      # Space between bricks (in pixels). This space is used for horizontal and vertical spacing.
BRICK_WIDTH = 40       # Height of a brick (in pixels).
BRICK_HEIGHT = 15      # Height of a brick (in pixels).
BRICK_ROWS = 10        # Number of rows of bricks.
BRICK_COLS = 10        # Number of columns of bricks.
BRICK_OFFSET = 50      # Vertical offset of the topmost brick from the window top (in pixels).
BALL_RADIUS = 10       # Radius of the ball (in pixels).
PADDLE_WIDTH = 75      # Width of the paddle (in pixels).
PADDLE_HEIGHT = 15     # Height of the paddle (in pixels).
PADDLE_OFFSET = 50     # Vertical offset of the paddle from the window bottom (in pixels).
BULLETS = 5            # Initial bullets

INITIAL_Y_SPEED = 7.0  # Initial vertical speed for the ball.
MAX_X_SPEED = 5      # Maximum initial horizontal speed for the ball.
BRICK_LIFE = {0: 'black',
              1: 'blue',
              2: 'green',
              3: 'orange',
              4: 'red'}     # The color of different brick life


class BreakoutGraphics:

    def __init__(self, ball_radius=BALL_RADIUS, paddle_width=PADDLE_WIDTH,
                 paddle_height=PADDLE_HEIGHT, paddle_offset=PADDLE_OFFSET,
                 brick_rows=BRICK_ROWS, brick_cols=BRICK_COLS,
                 brick_width=BRICK_WIDTH, brick_height=BRICK_HEIGHT,
                 brick_offset=BRICK_OFFSET, brick_spacing=BRICK_SPACING,
                 title='Breakout'):

        # Initialize variable
        self.state = 0
        self.ball_radius = ball_radius
        self.brick_width = brick_width
        self.__bullets = BULLETS
        self.__paddle_width = paddle_width
        self.__paddle_height = paddle_height
        color = 'black'

        # Create a graphical window, with some extra space.
        window_width = brick_cols * (brick_width + brick_spacing) - brick_spacing
        window_height = brick_offset + 3 * (brick_rows * (brick_height + brick_spacing) - brick_spacing)
        self.window = GWindow(width=window_width, height=window_height, title=title)

        # Loading Animation
        self.icon = GImage('icon/breakoutico.png')
        self.window.add(self.icon, (self.window.width-self.icon.width)/2, self.window.height/9)
        loading = GRect(30, 30)
        loading_width = 30
        loading.filled = True
        self.window.add(loading, 50, self.window.height/2)
        for i in range(11):
            self.window.remove(loading)
            loading_width += 30
            loading = GRect(loading_width, 30)
            loading.filled = True
            self.window.add(loading, 50, self.window.height*2/3)
            pause(200)
        # Loading Animation End

        # Create a paddle.
        paddle = GRect(paddle_width, paddle_height)
        paddle.filled = True
        paddle.fill_color = 'black'
        self.paddle = paddle
        self.paddle_height = self.window.height - paddle_offset
        self.window.add(paddle, (self.window.width - self.paddle.width)/2, self.paddle_height)

        # Center a filled ball in the graphical window.
        self.ball = []
        self.ball.append(Ball(ball_radius*2, ball_radius*2, dx=MAX_X_SPEED, dy=INITIAL_Y_SPEED))
        self.window.add(self.ball[0], (self.window.width/2 - ball_radius), (self.window.height/2 - ball_radius))

        # Create treasure array
        self.treasure = []
        self.bullet = []

        # Draw bricks and initial brick lives
        self.brick = []
        self.brick_live = []
        for i in range(0, brick_cols):
            for j in range(0, brick_rows):
                life = 1
                if j//2 == 0:
                    color = 'red'
                    life = 5
                elif j//2 == 1:
                    color = 'orange'
                    life = 4
                elif j//2 == 2:
                    color = 'yellow'
                    life = 3
                elif j//2 == 3:
                    color = 'green'
                    life = 2
                elif j//2 == 4:
                    color = 'blue'
                    life = 1
                self.brick.append(GRect(brick_width, brick_height))
                self.brick_live.append(life)
                self.brick[-1].filled = True
                self.brick[-1].fill_color = color
                self.brick[-1].color = color
                self.window.add(self.brick[-1], x=i*(brick_width+brick_spacing),
                                y=j*(brick_height+brick_spacing)+brick_offset)

        # Loading page end
        self.window.remove(loading)
        self.icon.move(0, 200)

    def start(self, e):
        """
        Start the game
        :param e: event
        :return: None
        """
        onmousemoved(self.paddle_move)
        onmouseclicked(self.click)
        self.window.remove(self.icon)

    def paddle_move(self, e):
        """
        The paddle will follow the mouse
        :param e: the mouse coordinate
        :return: None
        """
        if self.paddle.width/2 < e.x < self.window.width-self.paddle.width/2:
            self.paddle.x = e.x - self.paddle.width / 2
        elif e.x < self.paddle.width/2:
            self.paddle.x = 0
        else:
            self.paddle.x = self.window.width - self.paddle.width

    def click(self, e):
        """
        The event when mouse clicked (Start game of fire bullet)
        :param e: mouse event
        :return: None
        """
        if not self.state:
            self.state = 1
        elif self.bullets:
            self.bullet_fire(x=e.x)

    def reset(self):
        """
        Reset the game when lose ball
        :return: None
        """
        self.state = 0
        self.ball.append(Ball(self.ball_radius*2, self.ball_radius*2))
        self.window.add(self.ball[-1], self.window.width/2 - self.ball_radius, self.window.height/2 - self.ball_radius)
        for i in range(len(self.treasure)):
            self.window.remove(self.treasure[len(self.treasure)-i-1])
            del self.treasure[len(self.treasure)-i-1]
        if self.paddle.width != self.__paddle_width:
            self.window.remove(self.paddle)
            paddle = GRect(self.__paddle_width, self.__paddle_height)
            paddle.filled = True
            paddle.fill_color = 'black'
            self.paddle = paddle
            self.window.add(paddle, (self.window.width - self.paddle.width)/2, self.paddle_height)

    def if_collide(self, x, y):
        """
        Return if (x, y) have object
        :param x: x-coordinate
        :param y: y-coordinate
        :return: (Bool) If have object
        """
        maybe_object = self.window.get_object_at(x, y)
        if maybe_object is not None:
            return True
        else:
            return False

    def add_ball(self, x, y):
        """
        Add ball at (x, y)
        :param x: x-coordinate
        :param y: y-coordinate
        :return: None
        """
        self.ball.append(Ball(self.ball_radius*2, self.ball_radius*2))
        self.window.add(self.ball[-1], x, y)

    def add_treasure(self, types, brick_index):
        """
        Add treasure at brick center
        :param types: (int) the type of treasure
        :param brick_index: (int) the index of the brick where treasure being add
        :return: None
        """
        self.treasure.append(Treasure(types))
        self.window.add(self.treasure[-1], self.brick[brick_index].x + self.brick_width, self.brick[brick_index].y)

    def paddle_increase(self):
        """
        Double the width of paddle
        :return: None
        """
        x = self.paddle.x + self.paddle.width / 2
        self.window.remove(self.paddle)
        if self.paddle.width >= self.__paddle_width:
            paddle = GRect(self.__paddle_width * 2, self.__paddle_height)
        else:
            paddle = GRect(self.__paddle_width, self.__paddle_height)
        paddle.filled = True
        paddle.fill_color = 'black'
        self.paddle = paddle
        self.window.add(paddle, x - (self.paddle.width / 2), self.paddle_height)

    def paddle_decrease(self):
        """
        Decrease paddle width by 1/2
        :return: None
        """
        x = self.paddle.x + self.paddle.width / 2
        self.window.remove(self.paddle)
        if self.paddle.width <= self.__paddle_width:
            paddle = GRect(self.__paddle_width / 2, self.__paddle_height)
        else:
            paddle = GRect(self.__paddle_width, self.__paddle_height)
        paddle.filled = True
        paddle.fill_color = 'black'
        self.paddle = paddle
        self.window.add(paddle, x - (self.paddle.width / 2), self.paddle_height)

    def brick_collide(self, index):
        """
        Handles the brick related function when being hit
        :param index: (int) the brick index which being hit
        :return: None
        """
        self.brick_live[index] -= 1
        self.brick[index].fill_color = (BRICK_LIFE[self.brick_live[index]])
        self.brick[index].color = (BRICK_LIFE[self.brick_live[index]])
        if self.brick_live[index] <= 0:
            if_treasure = random.randint(0, 800)
            if if_treasure < 80:
                self.add_treasure(if_treasure % 8, index)
            self.brick_remove(index)

    def brick_remove(self, index):
        """
        Remove brick from window
        :param index: (int) the brick index to remove
        :return: None
        """
        self.window.remove(self.brick[index])
        del self.brick[index]
        del self.brick_live[index]

    def bullet_fire(self, x=0):
        """
        Fire the bullet
        :param x: the x-coordinate to fire the bullet
        :return: None
        """
        self.bullet.append(Bullet())
        self.window.add(self.bullet[-1], x, self.paddle_height)
        self.__bullets -= 1

    def add_bullets(self, number):
        """
        Add bullets storage
        :param number: (int) how many bullets to add
        :return:
        """
        self.__bullets += number

    @property
    def bullets(self):
        return self.__bullets


class Ball(GOval):
    def __init__(self, width=BALL_RADIUS*2, height=BALL_RADIUS*2, color='black', dx=MAX_X_SPEED, dy=INITIAL_Y_SPEED):
        super().__init__(width, height)
        self.filled = True
        self.fill_color = color
        self.color = color
        self.__dx = random.randint(1, dx)
        if random.random() > 0.5:
            self.__dx = -self.__dx
        self.__dy = dy

    @property
    def dy(self):
        return self.__dy

    def moving(self):
        super().move(self.__dx, self.__dy)

    def x_bounce(self):
        self.__dx = -self.__dx

    def y_bounce(self):
        self.__dy = -self.__dy


class Treasure(GImage):
    def __init__(self, types=1, dy=INITIAL_Y_SPEED/2):
        picture = {0: 'icon/rocket.png',
                   1: 'icon/ball.png',
                   2: 'icon/redheart.png',
                   3: 'icon/blackheart.png',
                   4: 'icon/quickclock.png',
                   5: 'icon/slowclock.png',
                   6: 'icon/shrink.jpg',
                   7: 'icon/expand.jpg'}
        super().__init__(picture[types])
        self.__dy = dy
        self.__types = types

    def moving(self):
        super().move(0, self.__dy)

    @property
    def types(self):
        return self.__types


class Bullet(GRect):
    def __init__(self, dy=INITIAL_Y_SPEED):
        super().__init__(5, 10)
        self.__dy = -dy
        self.filled = True

    def moving(self):
        super().move(0, self.__dy)
