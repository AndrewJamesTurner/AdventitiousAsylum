import pygame


# SImple render queue - add stuff during update and call flush at the end
class RenderQueue:
    def __init__(self):
        self.queue = []

    def add(self, location, image, scale=(1, 1), z_index=1):
        self.queue.append({'loc': location, 'im': image, 'scale': scale, 'z': z_index})

    def flush(self, screen, camera_position = (0, 0), background=(255, 255, 255)):

        screen_box = screen.get_rect()

        # Adjust item locations
        for item in self.queue:
            item['loc'] = (item['loc'][0] - camera_position[0], item['loc'][1] - camera_position[1])
            item['item_rect'] = pygame.Rect(item['loc'], item['im'].get_size())

        # Filter offscreen items
        self.queue = [x for x in self.queue if screen_box.colliderect(x['item_rect'])]

        # Sort by z depth
        self.queue.sort(key=lambda x: x['z'])

        screen.fill(background)
        for item in self.queue:
            if item['scale'] is not (1, 1):  # Scale if necessary
                item['im'] = pygame.transform.scale(item['im'], (item['im'].get_width() * item['scale'][0], item['im'].get_height() * item['scale'][1]))

            # Draw the image
            screen.blit(item['im'], item['loc'])

        # Remove everything from the queue
        self.queue.clear()
