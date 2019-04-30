from math import sin, cos, asin, acos, sqrt, tan, atan, pi


class math:
    def position(self, fi1, fi2, measure=()):
        l1 = measure[0]
        l2 = measure[1]
        l3 = measure[2]
        h = measure[3]

        fi1 *= pi/180
        fi2 *= pi / 180

        x1 = 0
        y1 = 0

        x2 = l1*cos(fi1)
        y2 = l1*sin(fi1)

        x3 = l1*cos(fi1) + l2*cos(fi1-fi2)
        y3 = l1*sin(fi1) + l2*sin(fi1-fi2)

        x4 = x3
        y4 = y3 - l3

        # adding base height
        y1 += h
        y2 += h
        y3 += h
        y4 += h

        coordinates = [x1, y1, x2, y2, x3, y3, x4, y4]
        return coordinates

    def position_angles(self, fi1, fi2, measure=()):
        fi3prim = 90 - fi1 + fi2
        fi3 = 180 - fi3prim
        angles = [fi1, fi2, fi3]
        return angles
