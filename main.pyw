# Импортируем библиотеки для обыкновенных дробей и создания приложений
from fractions import Fraction as fr
import tkinter as tk

# Создаем окно приложения
win = tk.Tk()
win.title('Horner of the Python')
win.geometry(f'570x460+280+50')
win.resizable(False, False)
win.columnconfigure(0, minsize = 470)
win.columnconfigure(1, minsize = 100)
win.config(bg = '#425ccf') 

# Создаем верхнее текстовое поле 
lab = tk.Label(text = "Введите уравнения или число:", 
font = ('Verdana', 15), bg = '#425ccf')
lab.grid(row = 0, column = 0, stick = 'we')

# Создаем панель ввода коэффициентов
ent = tk.Entry(win, font = ('Verdana', 15), width = 15, selectbackground = '#425ccf',
selectforeground = 'white', justify = tk.CENTER, bg = '#425ccf')
ent.grid(row = 1, column = 0, stick = 'we', padx = 5)
ent.focus()

# Создаем флажок для возможности ввода уравнения в общем виде
flag_var = tk.StringVar()
flag_var.set('only_odds')
flag = tk.Checkbutton(win, text = 'Вводить только коэффициенты', variable = flag_var, onvalue = 'only_odds', offvalue = 'full', font = ('Verdana', 15), bg = '#425ccf', activebackground = '#425ccf', padx = 5)
flag.grid(row = 2, column = 0, stick = 'w')

# Создаем текстовое поле для вывода ответа (сначала инструкция)
labby = tk.Label(win, text = '''Введите целые коэффициенты приведенного
многочлена через пробел в порядке убывания
степеней (степень не больше 9) или его общий вид.
ВВОД: 8 -38 67 -53 -16 60 или 
8x^5 - 38x^4 + 67x^3 - 53x^2 - 16x + 60
ВЫВОД: 
Исходное уравнение:
8x⁵ - 38x⁴ + 67x³ - 53x² - 16x + 60 = 0
Результат разложения на множители:
(4x + 3)(x - 2)²(2x² - 3x + 5) = 0
Рациональные корни уравнения: 2 -3/4
Вы также можете ввести одно число 
ВВОД: 360 (в режиме коэффициентов)
ВЫВОД: 360 = 2³ × 3² × 5 ''', font = ('Verdana', 15), bg = '#425ccf', 
padx = 5, justify = tk.LEFT, relief = "ridge")
labby.grid(row = 3, column = 0, columnspan = 2, stick = 'w')

# Сделаем возможность запускать программу клавишей ENTER
def solve(event):
    if event.char == '\r':
        gorner()
win.bind('<Key>', solve)  


# -------------------- Функции для главного алгоритма -------------------- №
# Функция будет выдавать уравнение с коэффициентами заданного списка
def get_equation(lst): 
    q = ''
    i = len(lst) - 1
    for elem in lst:
        if elem > 0 and elem != 1:
            q += ' + ' + str(elem) + 'x' + powers[i]
        elif elem < 0 and elem != -1:
            q += ' - ' + str(-elem) + 'x' + powers[i]
        elif elem == 1:
            q += ' + x' + powers[i]
        elif elem == -1:
            q += ' - x' + powers[i]
        elif elem == 0:
            q += ''
        i -= 1
        
    # Кастомизируем уравнение
    q = list(q)
    for i in range(3):
        del q[0]
    if lst[-1] != 0:
        del q[-1]
    if q != [] and q[-1] == ' ':
        q.append('1')
    q = ''.join(q)
    return q

def factors(x): # Определяем функцию нахождения всех делителей заданного числа
    if x < 0:
        x = -x
    factors_x = []
    d = 1
    while d <= x // 2:
        if x % d == 0:
            factors_x.append(d)
        d += 1
    factors_x.append(x)
    return factors_x

def sign(a):
    if a > 0:
        return ' - '
    elif a < 0:
        return ' + '

def nod(lst): # Функция для нахождения НОД от заданного списка чисел
    top_d = 1
    for d in range(2, abs(min(lst)) + 1):
        for e in lst:
            if e % d != 0:
                break
        else:
            top_d = d
    return top_d


def convert_odds(odds) -> list:
    odds = odds.replace('+', ' + ').replace('-', ' - ')
    odds = odds.split()
    odds_pow = []

    # Удаляем из массива odds все, кроме коэффициентов
    for i in range(len(odds)):
        if '^' in odds[i]:
            if odds[i][-2].isdigit():
                labby['text'] += 'Наивысшая степень не может быть больше 9-ой'
                labby['fg'] = 'red'
                return
            odds_pow.append(int(odds[i][-1]))
            odds[i] = odds[i][:-3]

        elif 'x' in odds[i]:
            odds[i] = odds[i][:-1]
            odds_pow.append(1)

        elif odds[i].isdigit():
            odds_pow.append(0)

        if odds[i] == '':
            odds[i] = '1'

    # Добавим "-" к отрицательным коэффициентам
    for i in range(1, len(odds)):
        if odds[i-1] == '-':
            odds[i] = '-' + odds[i]
    odds = list(map(int, odds[::2]))

    # Создадим словарь "data" вида {"степень": "коэффициент", ...}
    data = dict(zip(odds_pow, odds))

    # В массив "helpy" добавим все коэффициенты, включая нули
    helpy = []
    for p in range(max(odds_pow), -1, -1):
        if p in odds_pow:
            helpy.append(data[p])
        else:
            helpy.append(0)       
    odds = helpy
    if len(odds) == 1:
        raise ValueError
    return odds


# -------------------- Функция всего алгоритма -------------------- №
powers = {0:'', 1:'', 2:'²', 3:'³', 4:'⁴', 5:'⁵', 6:'⁶', 7:'⁷', 8:'⁸', 9:'⁹'}
def gorner():
    global labby, powers
    labby['text'] = ''
    odds = ent.get()
    if odds == '':
        return

    try: # Проверка на корректные символы
        if flag_var.get() == 'full': # Если уравнение вводилось в общем виде
            odds = convert_odds(odds)
        else:
            odds = list(map(int, odds.split()))

    except ValueError:
        labby['text'] += 'Некорректный ввод'
        labby['fg'] = 'red'
        return

    while odds[0] == 0: # Удаляем ведущие нули, если они есть
        del odds[0]
        if odds == []:
            labby['text'] += 'Нельзя вводить одни нули!'
            labby['fg'] = 'red'
            return

    if len(odds) > 10:
        labby['text'] += 'Стемень многочлена не больше 9'
        labby['fg'] = 'red'
        return

    elif len(odds) == 1: # Алгоритм для работы с одним числом (факторизация)
        N = int(odds[0])
        if N > 10000:
            labby['text'] += 'Вы ввели слишком большое число'
            labby['fg'] = 'red'
            return

        elif N < 2:
            labby['text'] += 'Вы ввели слишком маленькое число'
            labby['fg'] = 'red'
            return

        primes = [2] # Создаем ряд простых чисел до N
        for e in range(3 , N + 1, 2):
            for d in range(2, e // 2 + 1):
                if e % d == 0:
                    break
            else:
                primes.append(e)

        if N in primes:
            labby['text'] +=  f'{N} - простое число, его нельзя \nразложить на множители'
            labby['fg'] = 'red'
            return
        n = N
        prod_dub = []
        while n != 1:
            for d in primes:
                if n % d == 0:
                    n = n / d
                    prod_dub.append(str(d))
        prod = []
        for p in set(prod_dub):
            c = prod_dub.count(p)
            prod.append(p + powers[c])
        labby['text'] +=  str(N) + ' = ' + " × ".join(prod)
        labby['fg'] = 'black'
        return

    # Алгоритм для работы с уравнением
    labby['text'] += 'Исходное уравнение:\n'
    labby['fg'] = 'black'
    labby['text'] += get_equation(odds) + ' = 0\n' 

    # Главный олгаритм будет находить по 1 корню и выдовать новые коэффициенты
    extra_odds = False
    roots = []
    new_odds = []
    while len(new_odds) != 1: 
        # Обозначаем старший и свободный член
        a = odds[0]
        f = odds[-1]
        # Компилируем дроби (в числителе - делитель 'f', в знаменателе - делитель 'a')
        may_roots = []
        for factor_f in factors(f):
            for factor_a in factors(a):
                fractor = fr(numerator = factor_f, denominator = factor_a)
                may_roots.append(fractor)

        # Добавляем в массив возможных корней отрицательные величины
        negative = []
        for e in may_roots:
            negative.append(-e)
        may_roots += negative
        # Если последний коэффициент станет 0, добавляем корень в массив 'roots'
        for may_root in may_roots:
            new_odds = [a]
            new_odd = new_odds[0]
            for odd in odds[1:]:
                new_odd = may_root * new_odd + odd
                new_odds.append(int(new_odd))
            if new_odd == 0:
                roots.append(may_root)
                new_odds.pop()            
                odds = new_odds
                break
        else:
            extra_odds = True
            break

    # Алгоритм разложения на множители
    if roots == []:
        labby['text'] += 'Данный многочлен не имеет рациональных корней'
        return
    # Добавляем множители с корнями в строку 'prod'
    prod = ''
    unic_roots = set(roots)
    for root in unic_roots:
        num = root.numerator
        den = root.denominator
        if root == 0:
            prod += 'x'
        elif den != 1:
            prod += '(' + str(den) + 'x' + sign(root) + str(abs(num)) + ')'
        else:
            prod += '(' + 'x' + sign(root) + str(abs(root)) + ')'
        p = roots.count(root)
        prod += powers[p]

    labby['text'] += 'Результат разложения на множители:\n'
    if extra_odds:
        # Сокращаем коэффициенты оставшегося многочлена на НОД
        div = nod(odds)
        for i in range(len(odds)):
            odds[i] //= div
        labby['text'] += f'{prod}(' + get_equation(odds) + ') = 0\n'
    else:
        labby['text'] += f'{prod} = 0\n'

    # Выводим корни уравнения
    amount = len(unic_roots)
    labby['text'] += 'Уравнение имеет ' 
    if amount == 1:
        labby['text'] += '1 рациональный корень: '
    else:
        labby['text'] += f'{amount} рациональных корня: '

    unic_roots = list(map(str, unic_roots))
    labby['text'] += ';'.join(unic_roots)
    

# Создаем кнопку 'Решить!'
but = tk.Button(text = 'Решить!', command = lambda: gorner(), 
bg = '#425ccf', activebackground = '#425ccf', font = 'Times 12')
but.grid(row = 1, column = 1, stick = 'we')

win.mainloop()