from decimal import Decimal, getcontext

from vector import Vector

getcontext().prec = 30


class Line(object):

    NO_NONZERO_ELTS_FOUND_MSG = 'No nonzero elements found'

    def __init__(self, normal_vector=None, constant_term=None):
        self.dimension = 2

        if not normal_vector:
            all_zeros = ['0']*self.dimension
            normal_vector = Vector(all_zeros)
        self.normal_vector = normal_vector

        if not constant_term:
            constant_term = Decimal('0')
        self.constant_term = Decimal(constant_term)

        self.set_basepoint()


    def set_basepoint(self):
        try:
            n = self.normal_vector
            # print(n)  # Vector: (Decimal('4.046'), Decimal('2.836'))
            c = self.constant_term
            basepoint_coords = ['0']*self.dimension
            initial_index = Line.first_nonzero_index(n.coordinates)
            # print(initial_index)  # 0
            initial_coefficient = n.coordinates[initial_index]
            # print(initial_coefficient)  # 4.046
            #basepoint_coords[initial_index] = c/initial_coefficient
            self.basepoint = Vector(basepoint_coords)

        except Exception as e:
            if str(e) == Line.NO_NONZERO_ELTS_FOUND_MSG:
                self.basepoint = None
            else:
                raise e


    def is_parallel(self, l):
        l1 = self.normal_vector
        l2 = l.normal_vector
        return l1.is_parallel(l2)

    
    def are_equal(self, l):
        if not self.is_parallel(l):
            return False

        x = self.basepoint
        y = l.basepoint
        diff = x.subtract(y)
        n = self.normal_vector
        return diff.is_orth(n)

    
    def intersection(self, l):
        try:
            A, B = Decimal(self.normal_vector.coordinates)
            C, D = Decimal(l.normal_vector.coordinates)
            k1 = Decimal(self.constant_term)
            k2 = Decimal(l.constant_term)

            num = D*k1 - B*k2
            y_num = -C*k1 + A*k2
            denom = Decimal('1') / (A*D - B*C)

            return Vector([num, y_num]).scalar_mult(denom)
        except ZeroDivisionError:
            if self == l:
                return self
            else:
                return None
        
    def __str__(self):

        num_decimal_places = 3

        def write_coefficient(coefficient, is_initial_term=False):
            coefficient = round(coefficient, num_decimal_places)
            if coefficient % 1 == 0:
                coefficient = int(coefficient)

            output = ''

            if coefficient < 0:
                output += '-'
            if coefficient > 0 and not is_initial_term:
                output += '+'

            if not is_initial_term:
                output += ' '

            if abs(coefficient) != 1:
                output += '{}'.format(abs(coefficient))

            return output

        n = self.normal_vector

        try:
            initial_index = Line.first_nonzero_index(n.coordinates)
            terms = [write_coefficient(n[i], is_initial_term=(i==initial_index)) + 'x_{}'.format(i+1)
                     for i in range(self.dimension) if round(n[i], num_decimal_places) != 0]
            output = ' '.join(terms)

        except Exception as e:
            if str(e) == self.NO_NONZERO_ELTS_FOUND_MSG:
                output = '0'
            else:
                raise e

        constant = round(self.constant_term, num_decimal_places)
        if constant % 1 == 0:
            constant = int(constant)
        output += ' = {}'.format(constant)

        return output


    @staticmethod
    def first_nonzero_index(iterable):
        for k, item in enumerate(iterable):
            if not MyDecimal(item).is_near_zero():
                return k
        raise Exception(Line.NO_NONZERO_ELTS_FOUND_MSG)


class MyDecimal(Decimal):
    def is_near_zero(self, eps=1e-10):
        return abs(self) < eps


def main():
    l1 = Line(normal_vector=Vector(['7.204', '3.182']), constant_term='8.68')
    l2 = Line(normal_vector=Vector(['8.172', '4.114']), constant_term='9.883')
    print(l1.intersection(l2))


if __name__ == "__main__":
    main()


    
