from pygame import Surface, Rect


class Animation:
    def __init__(self, repeats=False, sprite_sheet=None, frame_width=None):
        self.repeats = repeats

        if sprite_sheet is None:
            self.frames = []
            self.frameNo = 0
        else:
            x = 0
            frame_height = sprite_sheet.get_width()

            while x < sprite_sheet.width:
                frame = Surface((frame_width, frame_height))
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