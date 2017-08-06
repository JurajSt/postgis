class Point(object):
    def __init__(self, x, y, z=0):
        """Defines x, y and z variables"""
        self.X = x
        self.Y = y
        self.Z = z

    def getX(self):
        return self.X
    def getY(self):
        return self.Y
    def getZ(self):
        return self.Z
    pass
