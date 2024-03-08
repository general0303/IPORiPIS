import random


class Soda:
    def __init__(self, addition=None):
        self.addition = addition
        self.show_my_drink = lambda: print(f"Газировка и {self.addition}") \
            if self.addition is not None else print("Обычная газировка")


class TriangleChecker:
    def __init__(self, val):
        self.val = val

    def is_triangle(self):
        if all(isinstance(val, (int, float)) for val in self.val):
            if min(self.val) >= 0:
                sort_val = sorted(self.val)
                print("Ура, можно построить треугольник!") if sort_val[0] + sort_val[1] > sort_val[2] \
                    else print("Жаль, но из этого треугольник не сделать.")
            else:
                print("С отрицательными числами (и 0) ничего не выйдет!")
        else:
            print("Нужно вводить только числа!")


class Employee:
    cnt = 0

    def __init__(self, name, age):
        self.__class__.cnt += 1
        self.name = name
        self.age = age

    def display_employee(self):
        print(f"Name: {self.name}, age: {self.age}")

    @staticmethod
    def display_count():
        print(Employee.cnt)


class Child:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def display_child(self):
        print(f"Name: {self.name}, age: {self.age}")

    @staticmethod
    def school():
        print(random.randint(1, 5000))


class KgToLb:
    def __init__(self, kg: (int, float)):
        self.__kg = kg

    @property
    def kg(self):
        return self.__kg

    @kg.setter
    def kg(self, new_kg):
        if isinstance(new_kg, (int, float)):
            self.__kg = new_kg
        else:
            raise ValueError('Килограммы задаются только числами')

    def to_lb(self):
        return self.__kg * 2.205


if __name__ == "__main__":
    a, b = Soda(), Soda(addition="мята")
    a.show_my_drink(), b.show_my_drink()
    print("_____________________________")
    t1, t2, t3, t4 = TriangleChecker([3, 4, 5]), TriangleChecker([3, 4, 7]), \
                     TriangleChecker([-1, 2, 3]), TriangleChecker(["a", 2, 3])
    t1.is_triangle(), t2.is_triangle(), t3.is_triangle(), t4.is_triangle()
    print("_____________________________")
    e1, e2, e3 = Employee("Ivan", 22), Employee("Semen", 26), Employee("Marina", 25)
    e1.display_employee(), e2.display_employee(), e3.display_employee()
    e1.display_count()
    c1, c2 = Child("Ivan", 5), Child("Ivan", 7)
    c1.display_child(), c2.display_child()
    c1.school(), c2.school()
    print("_____________________________")
    kg_to_lb = KgToLb(5)
    print(kg_to_lb.kg)
    kg_to_lb.kg = 6
    print(kg_to_lb.kg)
    print(kg_to_lb.to_lb())
    kg_to_lb.kg = "a"
    print(kg_to_lb.kg)
