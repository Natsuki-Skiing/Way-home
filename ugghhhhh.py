import random
class RogueLikeRoom:
    def __init__(self, x, y, w, h):
        self.x = x  # top-left x
        self.y = y  # top-left y
        self.w = w
        self.h = h
        self.center = (x + w // 2, y + h // 2)

class RogueMap:
    def __init__(self, width=80, height=25, grid_size=(3, 3), room_min=6, room_max=10):
        self.width = width
        self.height = height
        self.grid_cols, self.grid_rows = grid_size
        self.room_min = room_min
        self.room_max = room_max
        self.map = [[' ' for _ in range(width)] for _ in range(height)]
        self.rooms = []
        self.generate_rooms()
        self.connect_rooms()

    def draw_room(self, room):
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                if y == room.y or y == room.y + room.h - 1:
                    self.map[y][x] = '-' if room.x < x < room.x + room.w - 1 else '+'
                elif room.x == x or x == room.x + room.w - 1:
                    self.map[y][x] = '|'
                else:
                    self.map[y][x] = '.'

    def draw_corridor(self, x1, y1, x2, y2):
        if random.choice([True, False]):
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.map[y1][x] == ' ':
                    self.map[y1][x] = '#'
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.map[y][x2] == ' ':
                    self.map[y][x2] = '#'
        else:
            for y in range(min(y1, y2), max(y1, y2) + 1):
                if self.map[y][x1] == ' ':
                    self.map[y][x1] = '#'
            for x in range(min(x1, x2), max(x1, x2) + 1):
                if self.map[y2][x] == ' ':
                    self.map[y2][x] = '#'

    def generate_rooms(self):
        cell_w = self.width // self.grid_cols
        cell_h = self.height // self.grid_rows

        for row in range(self.grid_rows):
            for col in range(self.grid_cols):
                if random.random() < 0.85:  # 85% chance to place a room
                    w = random.randint(self.room_min, min(cell_w - 2, self.room_max))
                    h = random.randint(self.room_min, min(cell_h - 2, self.room_max))
                    x = col * cell_w + random.randint(1, cell_w - w - 1)
                    y = row * cell_h + random.randint(1, cell_h - h - 1)
                    room = RogueLikeRoom(x, y, w, h)
                    self.rooms.append(room)
                    self.draw_room(room)

    def connect_rooms(self):
        for i in range(1, len(self.rooms)):
            x1, y1 = self.rooms[i - 1].center
            x2, y2 = self.rooms[i].center
            self.draw_corridor(x1, y1, x2, y2)

    def render(self):
        return '\n'.join(''.join(row) for row in self.map)

# Generate map in Rogue style
rogue_map = RogueMap(width=80, height=25, grid_size=(3, 3))
print(rogue_map.render())
