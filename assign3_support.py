import math
import json

# The following constants (ALL CAPS) may be useful to the student.
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 15

NUM_ROWS = 30
NUM_COLUMNS = 12
WIDTH = BLOCK_WIDTH * NUM_COLUMNS
HEIGHT = BLOCK_HEIGHT * NUM_ROWS - 5
PADDLE_HEIGHT = 10

TIME_STEP = 20  # 20 millisecs
BALL_INITIAL_X_SPEED = 1
BALL_INITIAL_Y_SPEED = -4

BALL_RADIUS = 5

EXTRA_BALLS = 2

# For task 2
PADDLE_STRETCH = 5
MAX_EXTRA_BALLS = 4

# used internally for deflection of ball off paddle - the surface of the paddle
# is treated as part of a circle of this radius
PADDLE_RADIUS = 50

def read_level_data(filename):
    """
    Read the levels or level data from filename

    read_level_data(str) -> dict
    """
    with open(filename, 'r') as f:
        return json.loads(f.read())


def sign(x):
    """
    Returns 0 if very close to 0, else 1 if x > 0, else -1 if x < -1

    sign(num) -> int
    """

    if abs(x) < 0.00000001:
        return 0
    elif x > 0:
        return 1
    else:
        return -1


class GridInfo(object):
    """
    Represents a grid.
    Facilitates conversion between (x, y) points and (row, column) pairs.
    """
    _block_width = BLOCK_WIDTH
    _block_height = BLOCK_HEIGHT

    def set_block_size(self, width=BLOCK_WIDTH, height=BLOCK_HEIGHT):
        """
        Sets the size of a block.

        GridInfo.set_block_side(GridInfo, int, int) -> None
        """
        self._block_width = width
        self._block_height = height

    def get_block_width(self):
        """
        Returns the block width.

        GridInfo.get_block_width(GridInfo) -> int
        """
        return self._block_width

    def get_block_height(self):
        """
        Returns the block height.

        GridInfo.get_block_height(GridInfo) -> int
        """
        return self._block_height

    def pos2rc(self, x, y):
        """
        Converts an (x, y) point to a (row, column) pair.

        GridInfo.pos2rc(GridInfo, num, num) -> (int, int)
        """
        return (math.floor(y / self._block_height) + 1,
                math.floor(x / self._block_width) + 1)

    def rc2rect(self, r, c):
        """
        Returns the upper left and lower right coordinates
        (as a list of 4 elements) of the rectangle forming the cell (r, c)

        GridInfo.rc2rect(GridInfo, int, int) -> list(int)
        """
        return [(c - 1) * self._block_width, (r - 1) * self._block_height,
                c * self._block_width, r * self._block_height]

    def rc_centre(self, row, column):
        """
        Returns the (x, y) centre point of the (row, column) pair

        GridInfo.rc_centre(GridInfo, int, int) -> (int, int)
        """
        return ((column - 1) * self._block_width + self._block_width // 2,
                (row - 1) * self._block_height + self._block_height // 2)


class CollisionHandler(object):
    """
    Handles collisions for a Model.
    Note: Only the __init__ and process_collisions methods are of interest to
    students doing task 1/2.
    """
    _radius = BALL_RADIUS
    _paddle_radius = PADDLE_RADIUS
    _grid_info = None
    _model = None

    def __init__(self, model):
        """
        Constructor

        CollisionHandler.__init__(CollisionHandler, Model)
        """
        self._model = model
        self._grid_info = GridInfo()

    def process_collisions(self):
        """
        Detect collisions within the model updating the ball position and speed.

        Returns a list of all (row, column) pairs that the ball collided with.

        CollisionHandler.process_collisions(CollisionHandler, Model)
                                                        -> list<(int, int)>
        """

        if self.paddle_interact():
            # the ball hits the paddle so no blocks are hit
            return []

        ball = Point()
        ball.xs, ball.ys = self._model.get_ball_speed()
        ball.x, ball.y = self._model.get_ball_position()

        xs_sign, ys_sign = sign(ball.xs), sign(ball.ys)

        # the cell containing the trailing corner of the ball
        row, column = self._grid_info.pos2rc(ball.x - xs_sign * self._radius,
                                             ball.y - ys_sign * self._radius)

        adj_cell, adj_block = Edges(), Edges()

        # the 3 adjacent cells "in the direction of travel"
        for key, (x, y) in ADJ_DIRS._items():
            adj_cell[key] = (row + y * ys_sign, column + x * xs_sign)

        # are there blocks in these 3 cells?
        for key in adj_block:
            adj_block[key] = self._model.is_block_at(adj_cell[key])

        if not any(adj_block._values()):  # no possible collisions
            self._model.step_ball()
            return []

        points = self.generate_ball_hazards(ball, adj_block)

        collide_block = self.test_adj_for_collisions(adj_block, points)

        x_time, y_time = points.diagonal.xt, points.diagonal.yt
        collide = self.collisions_to_reflection(adj_cell, collide_block, x_time,
                                                y_time)

        if not collide:
            self._model.step_ball()

        return collide

    def paddle_interact(self):
        """
        Processes any interaction between the ball and the paddle.

        Updates the ball position and speed, if the ball hits the paddle.
        The ball is set to have exited, if the ball has passed the paddle.

        Returns True iff the ball hits the paddle.

        CollisionHandler.paddle_interact(CollisionHandler, Model) -> bool
        """

        min_x, paddle_top, max_x, _ = self._model.get_paddle_box()

        ball_xs, ball_ys = self._model.get_ball_speed()
        ball_x, ball_y = self._model.get_ball_position()

        x1, y1 = ball_x + ball_xs, ball_y + ball_ys

        if y1 + self._radius <= paddle_top:  # still in play above paddle
            return False

        if x1 + self._radius < min_x or x1 - self._radius > max_x:  # sewer ball
            self._model.exit_ball()
            return False

        # ball still in play above paddle
        # will the ball also hit the wall at the same time?
        xs_sign, ys_sign = sign(ball_xs), sign(ball_ys)

        # the cell containing the ball centre
        r, c = self._grid_info.pos2rc(ball_x, ball_y)

        # If block exists in the adjacent column, ball will collide with wall
        if self._model.is_block_at((r, c + xs_sign)):
            p_x = ball_x + xs_sign * self._radius
            p_y = ball_y - ys_sign * self._radius
            p_xt, _ = self.times_to_cell_boundary(p_x, p_y, ball_xs, ball_ys,
                                                  self._grid_info.rc2rect(r, c))

            if p_xt <= 1:  # next to wall so bounce off wall and paddle
                ty = (paddle_top - (ball_y + self._radius)) / ball_ys
                self.do_reflect(p_xt, -1, ty, -1)

                return True

        # at this point the ball bounces off paddle and paddle not near wall
        self.do_paddle_reflect()

        return True

    def do_paddle_reflect(self):
        """
        Performs a reflection when a collision with the paddle has happened.

        Precondition: by next step, ball has collided with paddle.

        CollisionHandler.do_paddle_reflect(CollisionHandler, Model) -> None
        """

        ball_xs, ball_ys = self._model.get_ball_speed()
        ball_x, ball_y = self._model.get_ball_position()

        min_x, paddle_top, max_x, _ = self._model.get_paddle_box()

        ty = (paddle_top - (ball_y + self._radius)) / ball_ys

        x_offset = ball_x - (min_x + max_x) / 2
        ball_x += ball_xs * ty
        ball_y += ball_ys * ty

        ball_xs, ball_ys = self.paddle_bounce(ball_xs, ball_ys, x_offset)
        # print(ty, ball_x, ball_y, x_offset, ball_xs, ball_ys)

        if abs(ball_xs) < 0.0001:
            ball_xs = 0.0001
        if abs(ball_ys) < 0.5:
            ball_ys = -0.5

        ball_x += ball_xs * (1 - ty)
        ball_y += ball_ys * (1 - ty)

        self._model.set_ball_speed(ball_xs, ball_ys)
        self._model.set_ball_position(ball_x, ball_y)

    def do_reflect(self, x_time, x_sign, y_time, y_sign):
        """Performs a reflection when a collision has happened,
        such that in x_time, y_time time units the ball will hit
        an x and y boundaries respectively.

        The signs specify how the speeds change.

        Precondition: 0 <= x_time<= 1, 0 <= y_time <= 1
                      x_sign in [1, -1], y_sign in [1, -1]

        CollisionHandler.do_reflect(CollisionHandler, Model,
                                    float, int, float, int) -> None
        """

        ball_xs, ball_ys = self._model.get_ball_speed()
        ball_x, ball_y = self._model.get_ball_position()

        ball_x += x_time * ball_xs
        ball_xs *= x_sign

        ball_x += (1 - x_time) * ball_xs
        ball_y += y_time * ball_ys

        ball_ys *= y_sign
        ball_y += (1 - y_time) * ball_ys

        self._model.set_ball_speed(ball_xs, ball_ys)
        self._model.set_ball_position(ball_x, ball_y)

    def collisions_to_reflection(self, adj_cell, collisions, x_time, y_time):
        """
        Reflects ball off adjacent block cells, if there are any, according to
        the corresponding collisions flags, with x_time, y_time being the time
        until collision along the given axis.

        Returns a list of cells that the ball collided with.

        CollisionHandler.\
            collisions_to_reflection(CollisionHandler, Edge<(int, int)>,
                                     Edge<bool>, float, float) ->
                                                        list<(int, int)>
        """
        hits = [adj_cell[key] for key, value in collisions._items() if
                value]

        if not hits:
            return []

        x_reflect, y_reflect = -1, -1

        if collisions.row and collisions.column :
            # ball collides with both adjacent row and column blocks
            if adj_cell.diagonal in hits:
                hits.remove(adj_cell.diagonal)  # do not include diagonal block

        elif collisions.row:  # ball collides with adjacent row block
            x_reflect, x_time = 1, 1  # disable x reflection

        elif collisions.column:  # ball collides with adjacent column block
            y_reflect, y_time = 1, 1  # disable y reflection

        elif collisions.diagonal:
            if y_time < x_time <= 1:  # bounce off column
                y_reflect, y_time = 1, 1  # disable y reflection
            else:  # bounce off row
                x_reflect, x_time = 1, 1  # disable x reflection

        self.do_reflect(x_time, x_reflect, y_time, y_reflect)

        return hits

    @classmethod
    def test_adj_for_collisions(cls, adj_block, points):
        """
        Tests adjacent blocks for collisions, given an Edge set of points with
        times to collide with the respective edge boundary.

        Returns an Edge set with each edge type True iff a collision would occur
        on that edge.

        CollisionHandler.\
            test_adj_for_collisions(CollisionHandler, Edge<bool>, Edge<Point>)
                                                            -> Edge<bool>
        """
        collisions = Edges()

        collisions.column = adj_block.column and points.column.xt < 1 and \
                            points.column.xt <= points.column.yt
        collisions.row = adj_block.row and \
                         points.row.yt < 1 and points.row.yt <= points.row.xt
        collisions.diagonal = adj_block.diagonal and \
                              points.diagonal.xt < 1 and points.diagonal.yt <= 1

        return collisions

    def generate_ball_hazards(self, ball, adj_block):
        """
        Generates an Edge set of hazards points for a ball with adjacent blocks.
        A hazard point is None iff there is no corresponding adjacent block.

        CollisionHandler.generate_ball_hazards(
                            CollisionHandler, Edge<bool>, Point) -> list(int)
        """
        points = Edges()

        xs_sign, ys_sign = sign(ball.xs), sign(ball.ys)

        # the cell containing the trailing corner of the ball
        r, c = self._grid_info.pos2rc(ball.x - xs_sign * self._radius,
                                      ball.y - ys_sign * self._radius)
        rect = self._grid_info.rc2rect(r, c)

        for key, (xs_dir, ys_dir) in SPEED_DIRS._items():
            #if adj_block[key]:
                point = points[key] = Point()

                point.x = ball.x + xs_dir * xs_sign * self._radius
                point.y = ball.y + ys_dir * ys_sign * self._radius

                point.xt, point.yt = \
                    self.times_to_cell_boundary(point.x, point.y, ball.xs,
                                                ball.ys, rect)

        return points

    @classmethod
    def times_to_cell_boundary(cls, x_position, y_position, x_speed, y_speed,
                               boundary):
        """
        Calculates the time it would take for an object with given position and
        speed to reach a boundary in both x and y directions.

        CollisionHandler.\
            times_to_cell_boundary(CollisionHandler, int, int, float,
                                   float, (int, int, int, int))
                                                            -> (float, float)
        """
        xs_sign = sign(x_speed)
        ys_sign = sign(y_speed)

        x_time = (boundary[1 + xs_sign] - x_position) / x_speed
        y_time = (boundary[2 + ys_sign] - y_position) / y_speed

        return x_time, y_time

    def paddle_bounce(self, x_speed, y_speed, ball_position):
        """
        Calculates the xy-speed pair of the ball after bouncing off the paddle,
        given current xy-speed and position that the ball impacts the paddle.

        CollisionHandler.paddle_bounce(CollisionHandler, float, float, int)
                                                            -> (float, float)
        """
        beta = math.asin(ball_position / self._paddle_radius)
        s2b = math.sin(2 * beta)
        c2b = math.cos(2 * beta)
        return x_speed * c2b + y_speed * s2b, x_speed * s2b - y_speed * c2b

    def set_ball_radius(self, radius=BALL_RADIUS):
        """
        Sets the radius of the ball as used for collision detection.

        CollisionHandler.set_ball_radius(CollisionHandler, int) -> None
        """
        self._radius = radius

    def set_paddle_radius(self, radius=PADDLE_RADIUS):
        """
        Sets the radius of the paddle as used for paddle collision detection.

        CollisionHandler.set_paddle_radius(CollisionHandler, int) -> None
        """
        self._paddle_radius = radius

    def set_model(self, model):
        """
        Sets the model to use for processing collisions.

        CollisionHandler.set_model(CollisionHandler, Model) -> None
        """
        self._model = model

    def set_grid_info(self, grid_info):
        """
        Sets the grid info as used for collision detection.

        CollisionHandler.set_grid_info(CollisionHandler, GridInfo) -> None
        """
        self._grid_info = grid_info


# ###############################################################################
# THE REMAINING CODE IS USED INTERNALLY FOR COLLISION HANDLING AND IS NOT
# DIRECTLY RELEVANT TO THE STUDENT, HOWEVER THE STUDENT MAY USE IT IF THEY WISH
# ###############################################################################

class Record(object):
    """
    A struct like class that can be accessed and iterated over as a dictionary.
    """

    def __getitem__(self, name):
        """
        Returns the value of the attribute with the given name.

        Enables [] syntax: record[name]
        """
        return getattr(self, name)

    def __setitem__(self, name, value):
        """
        Sets the value of the attribute with given name to value.

        Enables [] syntax: record[name] = value
        """
        setattr(self, name, value)

    def __delitem__(self, name):
        """
        Deletes the attribute with the given name.
        Note: This will reset to class default if one was given.

        Enables [] syntax: del record[name]
        """
        delattr(self, name)

    def __iter__(self):
        """
        Returns a generator yielding attribute names for this record.

        Record.__iter__(Record) -> generator<str>
        """
        for name in dir(self):
            if name.startswith("_"):
                continue
            yield name

    def _items(self):
        """
        Returns a generator yielding attribute (name, value) pairs for this
        record.

        Record._items(Record) -> generator<(str, *)>
        """
        for name in dir(self):
            if name.startswith("_"):
                continue
            yield (name, getattr(self, name))

    def _values(self):
        """
        Returns a generator yielding attribute values for this record.

        Record._values(Record) -> generator<*>
        """
        for name in dir(self):
            if name.startswith("_"):
                continue
            yield getattr(self, name)


class Point(Record):
    """
    An (x, y) point in the grid, with speed & time to collide in each direction.
    """
    x = 0  # x position
    y = 0  # y position
    xt = 0  # x time
    yt = 0  # y time
    xs = 0  # x speed
    ys = 0  # y speed


class Edges(Record):
    """
    A map of values corresponding to collisions across row/column/diagonal edge.
    """
    row = None
    column = None
    diagonal = None


SPEED_DIRS = Edges()
SPEED_DIRS.column = (1, -1)
SPEED_DIRS.row = (-1, 1)
SPEED_DIRS.diagonal = (1, 1)

# ADJ_DIRS[i] == (SPEED_DIRS[i] + 1) / 2
# can be mapped as above, but explicitly defined for clarity in code
ADJ_DIRS = Edges()
ADJ_DIRS.column = (1, 0)
ADJ_DIRS.row = (0, 1)
ADJ_DIRS.diagonal = (1, 1)
