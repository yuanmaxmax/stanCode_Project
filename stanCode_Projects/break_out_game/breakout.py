"""
stanCode Breakout Project
Adapted from Eric Roberts's Breakout by
Sonja Johnson-Yu, Kylie Jue, Nick Bowman,
and Jerry Liao

This extension have a loading page, eight
type of special treasures, maximum 5 lives
and record the score

When receive bullets (Rocket Icon), user
can fire at brick by click the mouse
"""

from campy.gui.events.timer import pause
from campy.gui.ginteractors import GButton
from campy.graphics.gobjects import GLabel
from campy.graphics.gwindow import Region
from breakoutgraphics import BreakoutGraphics, Treasure

FRAME_RATE = 1000 / 120  # 120 frames per second.
NUM_LIVES = 3            # Initial lives
MAX_NUM_LIVES = 5        # Maximum lives in game
graphics = BreakoutGraphics()   # Game window
frame_rate = FRAME_RATE  # In game frame rate
lives = NUM_LIVES        # Initial in game lives
heart = []               # Initial in game lives heart visualization
score = 0                # Initial in game score
life_label = GLabel(f'lives: {lives}')                  # Initial life label
bullet_label = GLabel(f'bullets: {graphics.bullets}')   # Initial bullet number label
score_label = GLabel(f'score: {score}')                 # Initial score label
button = GButton('Start Game')                          # Initial start game button
# button1 = GButton('Introduction')


def main():
    global lives, heart, life_label, button

    # Initialize start game button

    graphics.window.add_to_region(button, Region.SOUTH)
    button.add_click_handler(start)
    # graphics.window.add_to_region(button1, Region.SOUTH)
    # button.add_click_handler(introduction)

    # Add lives label
    for i in range(lives):
        heart.append(Treasure(2))
    life_label.font = 'Times New Roman-20-Bold'
    graphics.window.add(life_label, 0, graphics.window.height)
    for i in range(lives):
        graphics.window.add(heart[i], i * heart[i].width + life_label.width, graphics.window.height - heart[i].height)

    # Add bullets label
    bullet_label.font = 'Times New Roman-20-Bold'
    graphics.window.add(bullet_label, graphics.window.width - bullet_label.width-10, graphics.window.height)

    # Add score label
    score_label.font = 'Times New Roman-20-Bold'
    graphics.window.add(score_label, 0, score_label.height+5)

    # Add animation loop here!
    while True:
        while graphics.state and lives > 0 and len(graphics.brick):

            # update label
            life_label.text = f'lives: {lives}'
            bullet_label.text = f'bullets: {graphics.bullets}'
            score_label.text = f'scores: {score}'

            # object move
            for i in range(len(graphics.ball)):
                graphics.ball[i].moving()
            for i in range(len(graphics.treasure)):
                graphics.treasure[i].moving()
            for i in range(len(graphics.bullet)):
                graphics.bullet[i].moving()

            # treasure interactive function
            remove = []
            for i in range(len(graphics.treasure)):
                if graphics.treasure[i].y + graphics.treasure[i].height > graphics.window.height:
                    graphics.window.remove(graphics.treasure[i])
                    remove.append(i)
                if treasure_collide(i):
                    special(graphics.treasure[i].types)
                    graphics.window.remove(graphics.treasure[i])
                    remove.append(i)
            if len(remove):
                object_remove(remove, graphics.treasure)

            # bullet interactive function
            remove = []
            for i in range(len(graphics.bullet)):
                if graphics.bullet[i].y < 0:
                    graphics.window.remove(graphics.bullet[i])
                    remove.append(i)
                else:
                    if bullet_hit(i):
                        remove.append(i)
            object_remove(remove, graphics.bullet)

            # ball collide and bounce
            remove = []
            for i in range(len(graphics.ball)):
                if graphics.ball[i].x < 0 or (graphics.ball[i].x + graphics.ball[i].width) > graphics.window.width:
                    graphics.ball[i].x_bounce()
                if graphics.ball[i].y < 0:
                    graphics.ball[i].y_bounce()
                elif (graphics.ball[i].y + graphics.ball[i].height) > graphics.window.height:
                    remove.append(i)
                else:
                    collide = ball_collide(i)
                    if collide and not (graphics.ball[i].y > graphics.window.height/2 and graphics.ball[i].dy < 0):
                        graphics.ball[i].y_bounce()
            if len(remove):
                for i in range(len(remove)):
                    object_remove(remove, graphics.ball)

            # Died when ball go out
            if len(graphics.ball) == 0:
                lives -= 1
                graphics.window.remove(heart[-1])
                life_label.text = f'lives: {lives}'
                del heart[-1]
                graphics.reset()

            # Game Over when no lives left
            if lives <= 0:
                lose = GLabel('Game Over')
                lose.font = 'Times New Roman-40-Bold'
                lose.color = 'red'
                graphics.window.add(lose, graphics.window.width / 2 - lose.width / 2,
                                    graphics.window.height / 2 + lose.height)
            pause(frame_rate)
        # Win when no brick left
        if not len(graphics.brick):
            win = GLabel('You Win')
            win.font = 'Times New Roman-40-Bold'
            win.color = 'red'
            for i in range(len(graphics.ball)):
                graphics.window.remove(graphics.ball[i])
            for i in range(len(graphics.treasure)):
                graphics.window.remove(graphics.treasure[i])
            graphics.window.add(win, graphics.window.width/2 - win.width/2, graphics.window.height/2 + win.height)
            break
        pause(10)


def ball_collide(i):
    """
    This function will handle the ball collide interaction between brick and paddle
    :param i: (int) The index of the ball to interact
    :return: (Bool) If this ball collide with brick or paddle
    """
    global score
    collide = False
    for j in range(2):
        for k in range(2):
            object_get = graphics.window.get_object_at(graphics.ball[i].x + graphics.ball[i].width * j,
                                                       graphics.ball[i].y + graphics.ball[i].height * k)
            if object_get in graphics.brick:
                # brick lose life when being hit by ball
                index = graphics.brick.index(object_get)
                graphics.brick_collide(index)
                score += 1
                collide = True
            elif object_get is graphics.paddle:
                collide = True
    return collide


def object_remove(remove, objects):
    """
    Remove the objects from window
    :param remove: (int array) The index array to remove
    :param objects: (array) the array to remove some elements
    :return: None
    """
    for i in range(len(remove)):
        graphics.window.remove(objects[remove[i]-i])
        del objects[remove[i]-i]


def treasure_collide(index):
    """
    This function will handle the interaction between treasure and paddle
    :param index: (int) the index of the treasure
    :return: (Bool) if treasure collide paddle
    """
    for i in range(graphics.treasure[index].width//10):
        maybe_object = graphics.window.get_object_at(graphics.treasure[index].x + i*10,
                                                     graphics.treasure[index].y + graphics.treasure[index].height+1)
        if maybe_object is graphics.paddle:
            return True
    return False


def bullet_hit(bullet_i):
    """
    This function handles if a bullet hit brick
    :param bullet_i: (int) the index of the bullet
    :return: None
    """
    global score
    maybe_object = graphics.window.get_object_at(graphics.bullet[bullet_i].x + 2, graphics.bullet[bullet_i].y-1)
    if maybe_object in graphics.brick:
        index = graphics.brick.index(maybe_object)
        graphics.brick_collide(index)
        score += 1
        return True
    return False


def special(types):
    """
    This function handles the special events when a treasure being active (collide with paddle)
    :param types: (int) the types enum of treasure
    :return: None
    """
    global frame_rate, lives, heart
    if types == 0:
        graphics.add_bullets(20)
    elif types == 1:
        graphics.add_ball(graphics.paddle.x + graphics.paddle.width / 2, graphics.paddle.y)
    elif types == 2:
        if lives < MAX_NUM_LIVES:
            lives += 1
            heart.append(Treasure(2))
            graphics.window.add(heart[-1], (lives-1) * heart[0].width + life_label.width,
                                graphics.window.height - heart[0].height)
    elif types == 3:
        lives -= 1
        graphics.window.remove(heart[-1])
        del heart[-1]
    elif types == 4:
        frame_rate = int(0.5 * frame_rate)
    elif types == 5:
        frame_rate = int(2 * frame_rate)
    elif types == 6:
        graphics.paddle_decrease()
    elif types == 7:
        graphics.paddle_increase()


def start(e):
    """
    Start the game
    :param e: event handler
    :return: None
    """
    global button
    button.disable()
    graphics.start(e)

# TODO treasure introduction page
# def introduction(e):
#     w = GWindow(200, 500)


if __name__ == '__main__':
    main()
