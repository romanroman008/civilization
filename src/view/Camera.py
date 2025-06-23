


class Camera:
    def __init__(self, offset_x=0, offset_y=0, screen_width=800, screen_height=600, map_width=200, map_height=200, tile_size=10):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
        self.tile_size = tile_size
    def get_viewport(self):
        tile_w = self.screen_width //  self.tile_size
        tile_h = self.screen_height //  self.tile_size
        start_x = self.offset_x //  self.tile_size
        start_y = self.offset_y //  self.tile_size
        return start_x, start_y, tile_w, tile_h

    def move(self, dx: int, dy: int):

        new_offset_x = self.offset_x + dx *  self.tile_size
        new_offset_y = self.offset_y + dy *  self.tile_size

        max_offset_x = (self.map_width *  self.tile_size) - self.screen_width
        max_offset_y = (self.map_height *  self.tile_size) - self.screen_height

        self.offset_x = max(0, min(new_offset_x, max_offset_x))
        self.offset_y = max(0, min(new_offset_y, max_offset_y))