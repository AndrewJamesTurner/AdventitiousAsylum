from math import sqrt


def binomial(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke.
    See http://stackoverflow.com/questions/3025162/statistics-combinations-in-python
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1
        return ntok // ktok
    else:
        return 0


class MovementPath:
    def __init__(self, start_x, start_y, duration, points):
        self.start_x = start_x
        self.start_y = start_y
        self.x = start_x
        self.y = start_y
        self.duration = duration
        self.points = points
        self.progress = 0
        if self.points[0] is not (0, 0):
            self.points = [(0, 0)] + self.points

    def step(self, dt):
        self.progress = min(self.progress + dt, self.duration)

        t = self.progress/self.duration
        one_minus_t = 1-t

        x = 0
        y = 0
        n = len(self.points)
        for i in range(1, n+1):
            bino = binomial(n, i)
            coeff = bino * (one_minus_t ** (n-i)) * (t**i)

            print("Progress: {0}     T: {1}     n: {3}     i: {2}     bin: {4}".format(self.progress, t, i, n, bino))

            x += coeff * self.points[i-1][0]
            y += coeff * self.points[i-1][1]

        self.x = self.start_x + x
        self.y = self.start_y + y

    def get_position(self):
        return self.x, self.y

    def is_done(self):
        return self.progress >= self.duration
