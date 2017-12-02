import pygame


class RenderItem:
    def __init__(self, loc=(0, 0), image=None, scale=(1, 1), z=1):
        self.loc = loc
        self.image = image
        self.scale = scale
        self.z = z


# Simple render queue - add stuff during update and call flush at the end
class RenderQueue:
    def __init__(self):
        self.queue = []

    def add(self, location, image, scale=(1, 1), z_index=1):
        self.queue.append(RenderItem(location, image.convert_alpha(), scale, z_index))

    def flush(self, screen, scale=(1, 1), camera_position=(0, 0), background=(255, 255, 255)):

        # Adjust item locations
        for item in self.queue:
            item.loc = ((item.loc[0] - camera_position[0]) * scale[0],
                        (item.loc[1] - camera_position[1]) * scale[1])
            item.item_rect = pygame.Rect(item.loc, item.image.get_size())

        screen_box = screen.get_rect()

        # Filter offscreen items
        self.queue = [x for x in self.queue if screen_box.colliderect(x.item_rect)]

        # Sort by z depth
        self.queue.sort(key=lambda x: x.z)

        screen.fill(background)
        for item in self.queue:
            if item.scale is not (1, 1):  # Scale if necessary
                item.image = pygame.transform.scale(item.image, ( int(item.image.get_width() * item.scale[0] * scale[0]), int(item.image.get_height() * item.scale[1] * scale[1])))

            # Draw the image
            screen.blit(item.image, item.loc)

        # Remove everything from the queue
        self.queue.clear()
