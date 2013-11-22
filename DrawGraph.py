from Tkinter import *

class NoTuplePassedToDraw (Exception):
    pass

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DrawGraph:
    def __init__(self,top_window, values, times, width = 500, height = 500, row = 1, column = 1):
        if type(values) is not tuple: raise NoTuplePassedToDraw
        if type(times) is not tuple: raise NoTuplePassedToDraw
        self.times = times
        self.max_time_value = self.get_max_time_value_from_times()
        self.values = values
        self.min_value = 0
        self.max_value = 0

        canvas_width = self.max_time_value 
        canvas_height = height
        scroll_height = 15
        frame_width = width
        frame_height = canvas_height + scroll_height
        box_for_text_height = 10

        self.y_top = 1
        self.y_bottom = canvas_height - box_for_text_height
        self.x_left_border = 1 
        self.x_right_border = canvas_width 
        self.x_axis = self.y_bottom

        self.top_window = top_window

        self.setup_frame(frame_width, frame_height, row, column)
        self.setup_canvas(frame_width, canvas_width, canvas_height)
 
        self.set_min_max_values()
        self.set_values_rank()
        self.set_range_of_values()
        self.set_scale()
        self.set_x_axis_position()
        self.draw_x_axis_line()
        self.draw_y_axis_line()
        self.draw_graph()

    def get_max_time_value_from_times(self):
        max_time = 0
        for time in self.times:
            if time > max_time:
                max_time = time
        return max_time

    def setup_canvas(self, frame_width, canvas_width, canvas_height):
        self.scroll = Scrollbar (self.frame, orient=HORIZONTAL)
        self.board = Canvas (self.frame, width = frame_width, height = canvas_height)
        self.board['scrollregion'] = (0,0,canvas_width, canvas_height)
        self.board ['xscrollcommand'] = self.scroll.set
        self.scroll['command'] = self.board.xview
        self.board.grid(row = 0, column = 0, sticky = (N,E,W,S))
        self.scroll.grid(row = 1, column = 0, sticky = (E,W))
        
    def setup_frame(self, frame_width, frame_height, row, column):
        self.frame = Frame(self.top_window, width = frame_width, height = frame_height, bd = 1)
        self.frame.grid(row = 0, column = 0)
        self.frame.grid_propagate(False)

    def set_min_max_values(self):
        for v in self.values:
            if v > self.max_value: self.max_value = v
            elif v < self.min_value: self.min_value = v

    def set_values_rank(self):
        self.rank = 1
        tmp_value = self.max_value
        while tmp_value > 10:
            self.rank = self.rank * 10
            tmp_value = tmp_value / 10
            
    def set_range_of_values(self):
        self.range_of_values = self.max_value - self.min_value

    def set_scale(self):
        self.scale = float(10 * self.y_bottom / self.range_of_values) / 10

    def set_x_axis_position(self):
        if self.min_value < 0 and self.max_value > 0:
            self.x_axis = self.max_value * self.scale
        elif self.min_value < 0 and self.max_value <= 0:
            self.x_axis = 0

    def draw_x_axis_line(self):
        self.board.create_line(self.x_left_border, self.x_axis, self.x_right_border, self.x_axis)

    def draw_y_axis_line(self):
        self.board.create_line(self.x_left_border,self.y_top,self.x_left_border,self.y_bottom)

    def get_y_from_values(self, y):
        return self.x_axis-(self.values[y]*self.scale)

    def get_x_from_times(self, x):
        return self.times[x]

    def draw_graph(self):
        get_x_from_times = self.get_x_from_times
        get_y_from_values = self.get_y_from_values
 
        for i in range(1,len(self.values)):
            self.board.create_line(get_x_from_times(i-1), get_y_from_values(i-1), get_x_from_times(i), get_y_from_values(i))
            self.board.create_line(get_x_from_times(i), self.y_top, get_x_from_times(i), self.y_bottom, fill="grey")
            
            P = self.find_value_between_points(i) 
           #if P != 0:
           #    tmp_y = max(get_y_from_values(i-1), get_y_from_values(i))
           #    tmp_y = tmp_y - (tmp_y % self.rank)
           #    self.board.create_text(P.x, P.y, text = tmp_y, font = "arial 7")
        for time in range(0, self.max_time_value, 100):
            self.board.create_text(time, self.y_bottom + 5,  text = time, font = "arial 10")

    def find_value_between_points(self, i):
        get_y_from_values = self.get_y_from_values
        get_x_from_times = self.get_x_from_times
        if (get_y_from_values(i-1)/self.rank != get_y_from_values(i)/self.rank):
            A = Point(get_x_from_times(i-1), get_y_from_values(i-1))
            B = Point(get_x_from_times(i), get_y_from_values(i))
            print self.values[i-1]
            print self.values[i]
            print range(get_y_from_values(i-1), get_y_from_values(i))
            print range(0, self.max_value, self.rank)
            for tmp_y in filter(lambda l: l in range(int(get_y_from_values(i-1)), int(get_y_from_values(i))), range(0, self.max_value, self.rank)):
                print tmp_y
                C = Point(get_x_from_times(i-1), tmp_y)
                D = Point(get_x_from_times(i), tmp_y)
                self.board.create_line(A.x, A.y, B.x, B.y)
                self.board.create_line(C.x, C.y, D.x, D.y)
                x = ((B.x-A.x) * (D.x*C.y - D.y*C.x) - (D.x-C.x) * (B.x*A.y - B.y*A.x)) / ((B.y-A.y) * (D.x-C.x) - (D.y-C.y) * (B.x-A.x));
                y = ((D.y-C.y) * (B.x*A.y - B.y*A.x) - (B.y-A.y) * (D.x*C.y - D.y*C.x)) / ((D.y-C.y) * (B.x-A.x) - (B.y-A.y) * (D.x-C.x));
                self.board.create_text(x, y, text = tmp_y, font = "arial 7")
        else:
            return 0

if __name__ == "__main__":
    top_window = Tk()
    tuple_of_numbers = (0,1,4,9,16,25,36,49,64,81,100,81,64,49,36,25,16,9,4,1)
    tuple_of_times = (0,)
    for i in range(1,21):
        tuple_of_times = tuple_of_times + (tuple_of_times[-1]+10,)
    for i in range(21,101):
        tuple_of_times = tuple_of_times + (tuple_of_times[-1]+20,)
    #draw_graph = DrawGraph(top_window, tuple_of_numbers*5, tuple_of_times)
    draw_graph = DrawGraph(top_window, (0,25,36), (0,100, 200))
    draw_graph.top_window.mainloop()