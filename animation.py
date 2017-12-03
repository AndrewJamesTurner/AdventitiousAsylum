from pygame import Surface, Rect, SRCALPHA


class Animation:
    def __init__(self, repeats=False, sprite_sheet=None, frame_width=None):
        self.repeats = repeats

        self.frames = []
        self.frameNo = 0

        if sprite_sheet is not None:
            x = 0
            frame_height = sprite_sheet.get_width()

            while x < sprite_sheet.get_width():
                frame = Surface((frame_width, frame_height), flags=SRCALPHA)
                frame.blit(sprite_sheet, (0, 0), Rect(x, 0, frame_width, frame_height))
                self.add_frame(frame)
                x += frame_width

    def add_frame(self, image):
        self.frames.append(image)

    def step(self):
        self.frameNo += 1
        if self.repeats:
            self.frameNo %= len(self.frames)
        else:
            self.frameNo = min(len(self.frames)-1, self.frameNo+1)

        return self.on_last_frame()

    def on_last_frame(self):
        return self.frameNo == len(self.frames)-1

    def get_current_frame(self):
        return self.frames[self.frameNo]