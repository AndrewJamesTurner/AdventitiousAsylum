import pygame


# SImple render queue - add stuff during update and call flush at the end
class RenderQueue:
    def __init__(self):
        self.queue = []

    def add_item(self, location, image, scale=(1, 1), z_index=1):
        self.queue.append({'loc': location, 'im': image, 'scale': scale, 'z': z_index})

    def flush(self, screen, background=(255, 255, 255)):
        # Sort by z depth
        self.queue.sort(key=lambda x: x.z)

        screen.fill(background)
        for item in self.queue:
            if item.scale is not (1, 1): # Scale if necessary
                item.im = pygame.transform.scale(item.im, (item.im.get_width() * item.scale[0], item.im.get_height() * item.scale[1]))

            # Draw the image
            screen.blit(item.im, item.loc)

        # Remove everything from the queue
        self.queue.clear()

