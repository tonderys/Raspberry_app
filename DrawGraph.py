from tkinter import *

class NoTuplePassedToDraw (Exception):
    pass

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class DrawGraph:
    min_value = 0
    max_value = 0
    def __init__(self,top_window, values, times, width = 500, height = 500, row = 1, column = 1, rowspan = 1, columnspan = 1):
        if type(values) is not tuple: raise NoTuplePassedToDraw
        if type(times) is not tuple: raise NoTuplePassedToDraw
        self.times = times
        self.max_time_value = self.times[-1]
        self.values = values

        self.set_min_max_values()
        self.set_values_rank()
        self.set_range_of_values()
        self.set_x_scale()

        canvas_width = self.max_time_value * self.x_scale 
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

        self.set_y_scale()
        self.set_x_axis_position()
        self.setup_frame(frame_width, frame_height, row, column, rowspan, columnspan)
        self.setup_canvas(frame_width, canvas_width, canvas_height)
 
        self.draw_x_axis_line()
        self.draw_y_axis_line()
        self.draw_graph()

    def setup_frame(self, frame_width, frame_height, row, column, rowspan, columnspan):
        self.frame = Frame(self.top_window, width = frame_width, height = frame_height, bd = 1)
        self.frame.grid(row = row, column = column, rowspan = rowspan, columnspan = columnspan)
        self.frame.grid_propagate(False)

    def setup_canvas(self, frame_width, canvas_width, canvas_height):
        self.scroll = Scrollbar (self.frame, orient=HORIZONTAL)
        self.board = Canvas (self.frame, width = frame_width, height = canvas_height)
        self.board['scrollregion'] = (0,0,canvas_width, canvas_height)
        self.board ['xscrollcommand'] = self.scroll.set
        self.scroll['command'] = self.board.xview
        self.board.grid(row = 0, column = 0, sticky = (N,E,W,S))
        self.scroll.grid(row = 1, column = 0, sticky = (E,W))
        
    def set_min_max_values(self):
        for v in self.values:
            if v > self.max_value: self.max_value = v
            elif v < self.min_value: self.min_value = v

    def set_values_rank(self):
        self.rank = 1
        tmp_value = self.max_value
        while tmp_value > 30:
            self.rank = self.rank * 10
            tmp_value = tmp_value / 10
            
    def set_range_of_values(self):
        self.range_of_values = self.max_value - self.min_value

    def set_y_scale(self):
        if self.range_of_values != 0:
            self.y_scale = float(10 * self.y_bottom / self.range_of_values) / 10
        else:
            self.y_scale = 1

    def set_x_scale(self):
        if len(self.times) > 1:
            self.x_scale = 10 / (self.times[1] - self.times[0])
        else:
            self.x_scale = 1

    def set_x_axis_position(self):
        if self.min_value < 0 and self.max_value > 0:
            self.x_axis = self.max_value * self.y_scale
        elif self.min_value < 0 and self.max_value <= 0:
            self.x_axis = 0

    def draw_x_axis_line(self):
        self.board.create_line(self.x_left_border, self.x_axis, self.x_right_border, self.x_axis)

    def draw_y_axis_line(self):
        self.board.create_line(self.x_left_border,self.y_top,self.x_left_border,self.y_bottom)

    def draw_graph(self):
        get_x_from_times = self.get_x_from_times
        get_y_from_values = self.get_y_from_values
        remembered_x = 0
 
        for i in range(1,len(self.values)):
            self.board.create_line(get_x_from_times(i-1), get_y_from_values(i-1), get_x_from_times(i), get_y_from_values(i))
            self.board.create_line(get_x_from_times(i), self.y_top, get_x_from_times(i), self.y_bottom, fill="grey")
            if int(self.values[i]/self.rank) != remembered_x:
                self.board.create_text(get_x_from_times(i), get_y_from_values(i), text = self.values[i], font = "arial 8")
                remembered_x = int(self.values[i]/self.rank)
            
        for time in range(0, int(self.max_time_value), 100):
            self.board.create_text(time, self.y_bottom + 5,  text = time, font = "arial 10")

    def get_y_from_values(self, y):
        return self.x_axis-(self.values[y]*self.y_scale)

    def get_x_from_times(self, x):
        return self.times[x]*self.x_scale

if __name__ == "__main__":
    top_window = Tk()
    tuple_of_numbers = (0,1,4,9,16,25,36,49,64,81,100,81,64,49,36,25,16,9,4,1)
    tuple_of_times = (0,)
    for i in range(1,21):
        tuple_of_times = tuple_of_times + (tuple_of_times[-1]+10,)
    for i in range(21,101):
        tuple_of_times = tuple_of_times + (tuple_of_times[-1]+20,)
    draw_graph = DrawGraph(top_window, tuple_of_numbers*5, tuple_of_times)
    #draw_graph = DrawGraph(top_window, (0,25,36), (0,100, 200))
    draw_graph.top_window.mainloop()
