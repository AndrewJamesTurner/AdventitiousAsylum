

# Values shared by every scene
shared_values = None


class SharedValues:

    distance_through_level = 0.5
    player = None
    orderly = None

    def reset(self):
        pass


def get_shared_values():

    global shared_values
    if shared_values is None:
        shared_values = SharedValues()
    return shared_values
