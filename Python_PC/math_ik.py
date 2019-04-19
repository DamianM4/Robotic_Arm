from math import sin, cos, asin, acos, sqrt, tan, atan, pi

class math:
    def position(self, x4=1, y4=1, measure=()):
        l1 = measure[0]
        l2 = measure[1]
        l3 = measure[2]
        h = measure[3]
        y4 -= h #in regard to given y4 value, without this end of effector
        #is too high
        x1 = 0
        y1 = 0
        #vertical position of effector    
        x3 = x4
        y3 = y4 + l3

        c = sqrt(x3*x3+y3*y3)

        fi1bis = acos((l1*l1+c*c-l2*l2)/(2*l1*c))
        fi2bis = acos((l1*l1+l2*l2-c*c)/(2*l1*l2))
        fi3bis = acos((l2*l2+c*c-l1*l1)/(2*l2*c))

        fi1prim = atan(y3/x3)

        fi3prim = pi/2. - fi1prim

        fi1 = fi1prim + fi1bis
        fi2 = -(pi - fi2bis)
        fi3 = -(pi - fi3bis - fi3prim)

        x2 = l1*cos(fi1)
        y2 = l1*sin(fi1)
        #adding base height
        y1 += h
        y2 += h
        y3 += h
        y4 += h

        coordinates = [x1, y1, x2, y2, x3, y3, x4, y4]
        return coordinates

    def position_angles(self, x4=1, y4=1, measure=()):
        l1 = measure[0]
        l2 = measure[1]
        l3 = measure[2]
        h = measure[3]
        y4 -= h #in regard to given y4 value, without this end of effector
        #is too high
        x1 = 0
        y1 = 0
        #vertical position of effector    
        x3 = x4
        y3 = y4 + l3

        c = sqrt(x3*x3+y3*y3)

        fi1bis = acos((l1*l1+c*c-l2*l2)/(2*l1*c))
        fi2bis = acos((l1*l1+l2*l2-c*c)/(2*l1*l2))
        fi3bis = acos((l2*l2+c*c-l1*l1)/(2*l2*c))

        fi1prim = atan(y3/x3)

        fi3prim = pi/2. - fi1prim

        fi1 = fi1prim + fi1bis
        fi2 = -(pi - fi2bis)
        fi3 = -(pi - fi3bis - fi3prim)
        angles = [fi1,fi2,fi3]
        for i in range(len(angles)):
            angles[i] = 180*angles[i]/pi
        return angles