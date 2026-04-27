#include <iostream>
#include <cmath>
using namespace std;

// Абстрактный базовый класс
class Figura {
public:
    virtual void Print() const = 0;  // чисто виртуальный метод
    virtual double Area() const = 0;
    virtual ~Figura() {}
};

// Производный класс: Прямоугольник
class Pryamougolnik : public Figura {
    double width, height;
public:
    Pryamougolnik(double w, double h) : width(w), height(h) {}

    void Print() const override {
        cout << "[Прямоугольник] ширина=" << width
             << ", высота=" << height
             << ", площадь=" << Area() << endl;
    }

    double Area() const override {
        return width * height;
    }
};

// Производный класс: Круг>
class Krug : public Figura {
    double radius;
public:
    Krug(double r) : radius(r) {}

    void Print() const override {
        cout << "[Круг] радиус=" << radius
             << ", площадь=" << Area() << endl;
    }

    double Area() const override {
        return M_PI * radius * radius;
    }
};

// Производный класс: Треугольник
class Treugolnik : public Figura {
    double a, b, c; // стороны
public:
    Treugolnik(double a, double b, double c) : a(a), b(b), c(c) {}

    void Print() const override {
        cout << "[Треугольник] стороны=" << a << ", " << b << ", " << c
             << ", площадь=" << Area() << endl;
    }

    double Area() const override {
        // Формула Герона
        double s = (a + b + c) / 2.0;
        return sqrt(s * (s - a) * (s - b) * (s - c));
    }
};

// Производный класс: Квадрат
class Kvadrat : public Figura {
    double side;
public:
    Kvadrat(double s) : side(s) {}

    void Print() const override {
        cout << "[Квадрат] сторона=" << side
             << ", площадь=" << Area() << endl;
    }

    double Area() const override {
        return side * side;
    }
};

int main() {
    const int N = 5;

    // Массив указателей на базовый класс
    Figura* figures[N];

    // Заполняем разными объектами производных классов
    figures[0] = new Pryamougolnik(4.0, 6.0);
    figures[1] = new Krug(3.5);
    figures[2] = new Treugolnik(3.0, 4.0, 5.0);
    figures[3] = new Kvadrat(5.0);
    figures[4] = new Krug(1.0);

    // Выводим элементы массива через виртуальный метод Print()
    cout << "=== Массив фигур ===" << endl;
    for (int i = 0; i < N; i++) {
        cout << i + 1 << ". ";
        figures[i]->Print();
    }

    // Освобождаем память
    for (int i = 0; i < N; i++) {
        delete figures[i];
    }

    return 0;
}