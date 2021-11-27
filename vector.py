import math

class Vector(object):
    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple(coordinates)
            self.dimension = len(coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def add(self, v):
        coor = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(coor)

    def subtract(self, v):
        coor = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(coor)
            
    def scalar_mult(self, number):
        coor = [number*x for x in self.coordinates]
        return Vector(coor)

    def mag(self):
        coor = [pow(x,2) for x in self.coordinates]
        summ = 0
        for x in coor:
            summ += x
        return math.sqrt(summ)

    def dot(self, v):
        coor = sum([x*y for x,y in zip(self.coordinates, v.coordinates)])
        return coor

    def angle(self, v):
        dot = self.dot(v)
        self_mag = self.mag()
        v_mag = v.mag()
        denom = self_mag * v_mag
        num = dot / denom
        return math.acos(num), ((math.acos(num) * 180) / math.pi)

    def is_orth(self, v, tol=1e-10):
        return abs(self.dot(v)) < tol

    def is_parallel(self, v):
        return self.angle(v)[1] == 0 or self.angle(v)[1] == 180
    
    def orth(self, v):
        if self.is_orth(v):
            return "Orthogonal", self.dot(v)
        if self.is_parallel(v):
            return "Parallel", self.dot(v), self.angle(v)
        return "Neither", self.dot(v)
        

    def proj(self, v):
        proj = self.dot(v)
        proj /= v.mag() # = (V * Ub)

        proj /= v.mag()
        proj = v.scalar_mult(proj) # = (V/b * b)
        return proj

    def proj_par(self, v):
        return self.proj(v)
    
    def proj_perp(self, v):
        return self.subtract(self.proj(v))

    def cross(self, v):
        cross = []
        cross.append((v.coordinates[2] * self.coordinates[1]) - (v.coordinates[1] * self.coordinates[2]))
        cross.append(-1 * ((v.coordinates[2] * self.coordinates[0]) - (v.coordinates[0] * self.coordinates[2])))
        cross.append((v.coordinates[1] * self.coordinates[0]) - (v.coordinates[0] * self.coordinates[1]))
        return Vector(cross)

    def area_parallelogram(self, v):
        it = self.cross(v)
        return math.sqrt(sum([x**2 for x in it.coordinates]))

    def area_triangle(self, v):
        return 0.5 * self.area_parallelogram(v)
    
    def norm(self):
        try:
            coor = pow(self.mag(), -1)
            coor1 = [coor*x for x in self.coordinates]
            return Vector(coor1)
        except ZeroDivisionError:
            raise Exception("Can't divide by zero!")
        
    def __str__(self):
        return 'Vector: {}'.format(self.coordinates)


    def __eq__(self, v):
        return self.coordinates == v.coordinates


def main():
    ff = Vector([8.462, 7.893, -8.187]).cross(Vector([6.984, -5.975, 4.778]))
    print(ff)

    ff = Vector([5,3,2]).cross(Vector([-1,0,3]))
    print(ff)
    

    ff = Vector([-8.987, -9.838, 5.031]).area_parallelogram(Vector([-4.268, -1.861, -8.866]))
    print(ff)

    ff = Vector([1.5, 9.547, 3.691]).area_triangle(Vector([-6.007, 0.124, 5.772]))
    print(ff)


    
if __name__ == "__main__":
    main()
    
