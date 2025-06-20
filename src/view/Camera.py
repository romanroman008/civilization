from config.constans import TILE_SIZE


class Camera:
    def __init__(self, offset_x=0, offset_y=0, screen_width=800, screen_height=600, map_width=200, map_height=200):
        self.offset_x = offset_x
        self.offset_y = offset_y
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.map_width = map_width
        self.map_height = map_height
    def get_viewport(self):
        tile_w = self.screen_width // TILE_SIZE
        tile_h = self.screen_height // TILE_SIZE
        start_x = self.offset_x // TILE_SIZE
        start_y = self.offset_y // TILE_SIZE
        return start_x, start_y, tile_w, tile_h

    def move(self, dx: int, dy: int):

        new_offset_x = self.offset_x + dx * TILE_SIZE
        new_offset_y = self.offset_y + dy * TILE_SIZE

        max_offset_x = (self.map_width * TILE_SIZE) - self.screen_width
        max_offset_y = (self.map_height * TILE_SIZE) - self.screen_height

        self.offset_x = max(0, min(new_offset_x, max_offset_x))
        self.offset_y = max(0, min(new_offset_y, max_offset_y))