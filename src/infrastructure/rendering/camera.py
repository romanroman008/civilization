


class Camera:
    def __init__(self,
                 offset_x=0,
                 offset_y=0,
                 screen_width=800,
                 screen_height=600,
                 map_width=200,
                 map_height=200,
                 tile_size=32):

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size

    def get_viewport(self):
        start_x = self.offset_x //  self.tile_size
        start_y = self.offset_y //  self.tile_size
        end_x = (self.offset_x + self.screen_width) // self.tile_size
        end_y = (self.offset_y + self.screen_height) // self.tile_size
        return start_x, end_x, start_y, end_y

    def move(self, dx: float, dy: float, speed: int = 50):

        new_offset_x = self.offset_x + dx *  speed
        new_offset_y = self.offset_y + dy *  speed

        max_offset_x = (self.map_width *  self.tile_size) - self.screen_width
        max_offset_y = (self.map_height *  self.tile_size) - self.screen_height

        self.offset_x = max(0.0, min(new_offset_x, max_offset_x))
        self.offset_y = max(0.0, min(new_offset_y, max_offset_y))