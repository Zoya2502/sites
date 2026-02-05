from flask import Flask, render_template, request, jsonify
import sys
import io

app = Flask(__name__)

# --- РАСШИРЕННЫЙ СПРАВОЧНИК ---
MATERIALS = {
    "01. Введение и Переменные": """
    <div class="manual-block">
        <h3>Первая программа</h3>
        <p>Команда <code>print()</code> выводит текст или числа в консоль. Это основной способ увидеть результат работы программы.</p>
        <pre>
print("Привет!")      # Текст всегда в кавычках
print(100)            # Числа без кавычек
print("Ответ:", 5+5)  # Можно совмещать</pre>

        <h3>Переменные</h3>
        <p>Переменная — это именованная ячейка памяти. Представьте коробку, на которой написано имя, а внутри лежит значение.</p>
        <pre>
name = "Alex"    # Строковая переменная (str)
age = 15         # Целое число (int)
rating = 4.8     # Дробное число (float)
is_admin = True  # Логическая переменная (bool)</pre>
        
        <div class="note">
            <b>Важно:</b> Имена переменных не могут начинаться с цифры и не должны содержать пробелов (используйте <code>_</code>).
        </div>
    </div>
    """,
    "02. Математика": """
    <div class="manual-block">
        <h3>Арифметические операции</h3>
        <ul>
            <li><code>+</code> Сложение</li>
            <li><code>-</code> Вычитание</li>
            <li><code>*</code> Умножение</li>
            <li><code>/</code> Деление (результат всегда дробный: 10/2 = 5.0)</li>
        </ul>
        <h3>Продвинутые операции</h3>
        <ul>
            <li><code>//</code> <b>Целочисленное деление</b>. Отбрасывает дробную часть. <br><code>10 // 3 = 3</code> (в 10 тройка помещается 3 раза).</li>
            <li><code>%</code> <b>Остаток от деления</b>. <br><code>10 % 3 = 1</code> (10 - 9 = 1). Часто используется для проверки на четность: <code>x % 2 == 0</code>.</li>
            <li><code>**</code> <b>Возведение в степень</b>. <br><code>2 ** 3 = 8</code>.</li>
        </ul>
        <h3>Функции модуля math</h3>
        <pre>
import math
print(math.sqrt(25))  # Корень квадратный -> 5.0
print(math.ceil(4.1)) # Округление вверх -> 5
print(math.floor(4.9))# Округление вниз -> 4</pre>
    </div>
    """,
    "03. Условный оператор (If)": """
    <div class="manual-block">
        <h3>Логика программы</h3>
        <p>Используйте <code>if</code>, <code>elif</code> (иначе если) и <code>else</code> (иначе), чтобы программа могла выбирать путь.</p>
        <pre>
money = 50

if money >= 500:
    print("Идем в ресторан")
elif money >= 100:
    print("Идем в кафе")
else:
    print("Сидим дома")</pre>
        
        <h3>Логические связки</h3>
        <ul>
            <li><code>and</code> — Истина, если ОБА условия верны. <br><code>if age > 10 and age < 20:</code></li>
            <li><code>or</code> — Истина, если ХОТЯ БЫ ОДНО верно. <br><code>if day == "Sat" or day == "Sun":</code></li>
            <li><code>not</code> — Инверсия (НЕ).</li>
        </ul>
    </div>
    """,
    "04. Циклы (Loops)": """
    <div class="manual-block">
        <h3>Цикл For</h3>
        <p>Используется, когда известно количество повторений. Функция <code>range(start, stop, step)</code> генерирует числа.</p>
        <pre>
# Числа от 0 до 4
for i in range(5):
    print(i)

# Числа от 1 до 10 с шагом 2
for i in range(1, 11, 2):
    print(i) # 1, 3, 5, 7, 9</pre>

        <h3>Цикл While</h3>
        <p>Работает, пока условие истинно. Опасен тем, что можно уйти в бесконечный цикл, если забыть изменить переменную.</p>
        <pre>
x = 5
while x > 0:
    print(x)
    x -= 1  # Уменьшаем x, иначе цикл не кончится!</pre>
    </div>
    """,
    "05. Списки (Lists)": """
    <div class="manual-block">
        <h3>Основы</h3>
        <p>Упорядоченная коллекция элементов. Нумерация начинается с <b>нуля</b>.</p>
        <pre>
nums = [10, 20, 30, 40]
print(nums[0])   # 10
print(nums[-1])  # 40 (последний элемент)</pre>

        <h3>Методы списков</h3>
        <ul>
            <li><code>nums.append(50)</code> — добавить в конец.</li>
            <li><code>nums.insert(1, 15)</code> — вставить по индексу.</li>
            <li><code>nums.pop()</code> — удалить последний элемент.</li>
            <li><code>nums.sort()</code> — сортировать (навсегда меняет список).</li>
            <li><code>len(nums)</code> — длина списка.</li>
            <li><code>sum(nums)</code> — сумма чисел.</li>
        </ul>
    </div>
    """,
    "06. Строки (Strings)": """
    <div class="manual-block">
        <h3>Методы строк</h3>
        <p>Строки неизменяемы. Методы возвращают <i>новую</i> строку.</p>
        <pre>
s = "  Python  "
print(s.strip())       # Убрать пробелы по краям
print(s.lower())       # Маленькие буквы
print(s.replace("P", "J")) # Замена
print(s.count("t"))    # Подсчет вхождений</pre>
        
        <h3>Срезы (Slicing)</h3>
        <p>Универсальный способ вырезать кусок данных.</p>
        <pre>
s = "Hello World"
print(s[0:5])  # "Hello" (с 0 по 4)
print(s[6:])   # "World" (с 6 до конца)
print(s[::-1]) # "dlroW olleH" (разворот)</pre>
    </div>
    """,
    "07. Словари и Множества": """
    <div class="manual-block">
        <h3>Множества (Set)</h3>
        <p>Хранят только уникальные элементы. Порядок не важен.</p>
        <pre>
a = [1, 1, 2, 2, 3]
uniq = set(a) # {1, 2, 3}</pre>

        <h3>Словари (Dictionary)</h3>
        <p>Хранят пары "Ключ: Значение". Очень быстрый поиск по ключу.</p>
        <pre>
d = {"Alex": 5, "Bob": 3}
print(d["Alex"]) # 5
d["Bob"] = 4     # Изменить значение
d["Eva"] = 5     # Добавить новую пару</pre>
    </div>
    """,
    "08. Функции": """
    <div class="manual-block">
        <h3>Создание своих команд</h3>
        <p>Функции позволяют упаковать код в блок и вызывать его по имени.</p>
        <pre>
def greet(name):
    return "Привет, " + name

print(greet("Ivan"))  # Привет, Ivan</pre>
        <div class="note">
            <code>return</code> возвращает результат и немедленно прекращает работу функции.
        </div>
    </div>
    """,
    "09. ЕГЭ №5, №14 (Системы счисления)": """
    <div class="manual-block">
        <h3>Встроенные функции</h3>
        <ul>
            <li><code>bin(x)</code> — перевод в двоичную (префикс '0b').</li>
            <li><code>oct(x)</code> — перевод в восьмеричную ('0o').</li>
            <li><code>hex(x)</code> — перевод в 16-ричную ('0x').</li>
            <li><code>int('101', 2)</code> — перевод ИЗ двоичной в десятичную.</li>
        </ul>
        <h3>Алгоритм (ручной перевод)</h3>
        <pre>
# Перевод числа x в систему с основанием N
res = ""
while x > 0:
    res = str(x % N) + res
    x //= N</pre>
    </div>
    """,
    "10. ЕГЭ №8 (Комбинаторика)": """
    <div class="manual-block">
        <h3>Библиотека itertools</h3>
        <p>Мощнейший инструмент для перебора вариантов.</p>
        <pre>
from itertools import product, permutations

# product - Размещение с повторением (слова из букв)
# Слова длины 3 из букв A, B
for p in product('AB', repeat=3):
    word = ''.join(p) # 'AAA', 'AAB'...</pre>
    </div>
    """,
    "11. ЕГЭ №25 (Маски и Делители)": """
    <div class="manual-block">
        <h3>Маски (fnmatch)</h3>
        <p>Позволяет проверять строки на соответствие шаблону.</p>
        <ul>
            <li><code>?</code> — ровно один любой символ.</li>
            <li><code>*</code> — любая последовательность (в том числе пустая).</li>
        </ul>
        <pre>
from fnmatch import fnmatch
if fnmatch("12345", "12*5"): ...</pre>

        <h3>Поиск делителей</h3>
        <p>Эффективный перебор — до корня из числа.</p>
    </div>
    """,
    "12. Рекурсия (ЕГЭ №16, №23)": """
    <div class="manual-block">
        <h3>Основы рекурсии</h3>
        <p>Функция вызывает саму себя. Чтобы она не зациклилась, нужно Базовое Условие (выход).</p>
        <pre>
# Факториал числа
def F(n):
    if n == 1: return 1      # База
    return n * F(n - 1)      # Шаг</pre>
    </div>
    """
}

# --- ЗАДАЧИ 8 КЛАСС (РОВНО 20 ШТУК) ---
TASKS_8 = [
    {
        "id": 1, 
        "title": "1. Переменные и вывод", 
        "description": "<b>Дано:</b> Имя ученика — 'Ivan'.<br><br><b>Задача:</b><br>1. Создайте переменную <code>name</code> и присвойте ей строку 'Ivan'.<br>2. Выведите на экран фразу: <code>Привет, Ivan</code>", 
        "initial_code": "# Ваш код здесь\n", 
        "expected_output": "Привет, Ivan", 
        "explanation": "<ul><li>Создайте переменную: <code>name = 'Ivan'</code></li><li>Используйте принт: <code>print('Привет,', name)</code></li></ul>"
    },
    {
        "id": 2, 
        "title": "2. Простая математика", 
        "description": "<b>Дано:</b> Два числа: a = 10, b = 4.<br><br><b>Задача:</b><br>Выведите остаток от деления числа <code>a</code> на число <code>b</code>.", 
        "initial_code": "a = 10\nb = 4\n", 
        "expected_output": "2", 
        "explanation": "<ul><li>Остаток от деления в Python обозначается символом <code>%</code>.</li><li>Напишите <code>print(a % b)</code>.</li></ul>"
    },
    {
        "id": 3, 
        "title": "3. Условный оператор", 
        "description": "<b>Дано:</b> Число x = 50.<br><br><b>Задача:</b><br>Проверьте условие: если x больше 100, выведите 'Big', иначе выведите 'Small'.", 
        "initial_code": "x = 50\n", 
        "expected_output": "Small", 
        "explanation": "<ul><li>Используйте конструкцию <code>if ... else ...</code></li><li><code>if x > 100: ... else: ...</code></li></ul>"
    },
    {
        "id": 4, 
        "title": "4. Циклы (Повторение)", 
        "description": "<b>Задача:</b><br>Выведите слово 'Code' 3 раза. Каждое слово должно быть с новой строки.", 
        "initial_code": "", 
        "expected_output": "Code\nCode\nCode", 
        "explanation": "<ul><li>Используйте цикл <code>for i in range(3):</code></li><li>Внутри цикла напишите <code>print('Code')</code></li></ul>"
    },
    {
        "id": 5, 
        "title": "5. Работа со списком", 
        "description": "<b>Дано:</b> Список чисел: <code>a = [5, 10, 15]</code>.<br><br><b>Задача:</b><br>Найдите и выведите сумму всех чисел в этом списке.", 
        "initial_code": "a = [5, 10, 15]\n", 
        "expected_output": "30", 
        "explanation": "<ul><li>Для суммирования есть готовая функция <code>sum()</code>.</li><li><code>print(sum(a))</code></li></ul>"
    },
    {
        "id": 6, 
        "title": "6. Замена в строке", 
        "description": "<b>Дано:</b> Строка <code>s = 'Hello World'</code>.<br><br><b>Задача:</b><br>Замените в этой строке все пробелы на нижнее подчеркивание <code>_</code> и выведите результат.", 
        "initial_code": "s = 'Hello World'\n", 
        "expected_output": "Hello_World", 
        "explanation": "<ul><li>У строк есть метод <code>.replace('старое', 'новое')</code>.</li><li><code>print(s.replace(' ', '_'))</code></li></ul>"
    },
    {
        "id": 7, 
        "title": "7. Индексы", 
        "description": "<b>Дано:</b> Строка 'Python'.<br><br><b>Задача:</b><br>Выведите <b>последнюю</b> букву этой строки, используя отрицательный индекс.", 
        "initial_code": "s = 'Python'\n", 
        "expected_output": "n", 
        "explanation": "<ul><li>В Python индекс <code>-1</code> означает последний элемент.</li><li><code>print(s[-1])</code></li></ul>"
    },
    {
        "id": 8, 
        "title": "8. Фильтрация (Четные числа)", 
        "description": "<b>Дано:</b> Список <code>a = [1, 2, 3, 4]</code>.<br><br><b>Задача:</b><br>Используя цикл, выведите только четные числа из этого списка (каждое с новой строки).", 
        "initial_code": "a = [1, 2, 3, 4]\n", 
        "expected_output": "2\n4", 
        "explanation": "<ul><li>Пройдитесь по списку: <code>for x in a:</code></li><li>Проверьте четность: <code>if x % 2 == 0:</code></li><li>Выведите x.</li></ul>"
    },
    {
        "id": 9, 
        "title": "9. Поиск максимума", 
        "description": "<b>Задача:</b><br>Найдите максимальное число среди трех: 5, 12, 3. Выведите его.", 
        "initial_code": "", 
        "expected_output": "12", 
        "explanation": "<ul><li>Используйте функцию <code>max(5, 12, 3)</code>.</li></ul>"
    },
    {
        "id": 10, 
        "title": "10. Обратный отсчет (While)", 
        "description": "<b>Дано:</b> Переменная <code>x = 3</code>.<br><br><b>Задача:</b><br>Пока x больше 0, выводите x на экран, а затем уменьшайте его на 1.", 
        "initial_code": "x = 3\n", 
        "expected_output": "3\n2\n1", 
        "explanation": "<ul><li><code>while x > 0:</code></li><li><code>print(x)</code></li><li><code>x -= 1</code></li></ul>"
    },
    {
        "id": 11,
        "title": "11. Срезы (Slicing)",
        "description": "<b>Дано:</b> Строка <code>s = 'Programming'</code>.<br><br><b>Задача:</b><br>Выведите первые 3 буквы этого слова.",
        "initial_code": "s = 'Programming'\n",
        "expected_output": "Pro",
        "explanation": "<ul><li>Используйте срез <code>[старт:конец]</code>.</li><li><code>print(s[:3])</code></li></ul>"
    },
    {
        "id": 12,
        "title": "12. Длина списка",
        "description": "<b>Дано:</b> Список <code>a = [10, 20, 30, 40]</code>.<br><br><b>Задача:</b><br>Выведите количество элементов в этом списке.",
        "initial_code": "a = [10, 20, 30, 40]\n",
        "expected_output": "4",
        "explanation": "<ul><li>Для получения длины используйте функцию <code>len(a)</code>.</li></ul>"
    },
    {
        "id": 13,
        "title": "13. Типы данных",
        "description": "<b>Дано:</b> Строка <code>s = '15'</code> и число <code>n = 5</code>.<br><br><b>Задача:</b><br>Преобразуйте строку <code>s</code> в число, прибавьте к нему <code>n</code> и выведите результат.",
        "initial_code": "s = '15'\nn = 5\n",
        "expected_output": "20",
        "explanation": "<ul><li>Функция <code>int(s)</code> превращает строку в число.</li><li><code>print(int(s) + n)</code></li></ul>"
    },
    {
        "id": 14,
        "title": "14. Добавление в список",
        "description": "<b>Дано:</b> Список <code>a = [1, 2]</code>.<br><br><b>Задача:</b><br>Добавьте в конец списка число 3, а затем выведите весь список.",
        "initial_code": "a = [1, 2]\n",
        "expected_output": "[1, 2, 3]",
        "explanation": "<ul><li>Используйте метод <code>.append(3)</code>.</li><li>Затем <code>print(a)</code>.</li></ul>"
    },
    {
        "id": 15,
        "title": "15. Подсчет символов",
        "description": "<b>Дано:</b> Строка <code>s = 'banana'</code>.<br><br><b>Задача:</b><br>Посчитайте, сколько раз буква 'a' встречается в этом слове. Выведите число.",
        "initial_code": "s = 'banana'\n",
        "expected_output": "3",
        "explanation": "<ul><li>Используйте метод <code>.count('a')</code>.</li></ul>"
    },
    {
        "id": 16,
        "title": "16. Сравнение типов",
        "description": "<b>Задача:</b><br>Проверьте, равно ли число 5 строке '5'. Выведите True или False.",
        "initial_code": "",
        "expected_output": "False",
        "explanation": "<ul><li>Число и строка — это разные типы данных.</li><li><code>print(5 == '5')</code></li></ul>"
    },
    {
        "id": 17,
        "title": "17. Логические операторы",
        "description": "<b>Задача:</b><br>Вычислите значение выражения: <code>(True и False) или True</code>.<br>Используйте Python операторы <code>and</code>, <code>or</code>.",
        "initial_code": "",
        "expected_output": "True",
        "explanation": "<ul><li><code>print((True and False) or True)</code></li></ul>"
    },
    {
        "id": 18,
        "title": "18. Функции",
        "description": "<b>Задача:</b><br>Напишите функцию <code>plus(a, b)</code>, которая возвращает сумму двух чисел. Вызовите её для чисел 10 и 20.",
        "initial_code": "def plus(a, b):\n    # Ваш код\n    pass\n\nprint(plus(10, 20))",
        "expected_output": "30",
        "explanation": "<ul><li>Внутри функции напишите <code>return a + b</code>.</li></ul>"
    },
    {
        "id": 19,
        "title": "19. Сортировка",
        "description": "<b>Дано:</b> Список <code>a = [3, 1, 2]</code>.<br><br><b>Задача:</b><br>Отсортируйте список по возрастанию и выведите его.",
        "initial_code": "a = [3, 1, 2]\n",
        "expected_output": "[1, 2, 3]",
        "explanation": "<ul><li>Используйте метод <code>a.sort()</code>.</li><li>Затем <code>print(a)</code>.</li></ul>"
    },
    {
        "id": 20,
        "title": "20. Финал: Повтор строки",
        "description": "<b>Задача:</b><br>Выведите слово 'Python' 5 раз подряд через пробел в одну строку.",
        "initial_code": "",
        "expected_output": "Python Python Python Python Python",
        "explanation": "<ul><li>Можно умножать строки: <code>s = 'Python ' * 5</code>.</li><li>Затем обрежьте лишний пробел: <code>print(s.strip())</code></li></ul>"
    }
]

# --- ЗАДАЧИ 11 КЛАСС (ЕГЭ - РОВНО 20 ШТУК) ---
TASKS_11 = [
    {
        "id": 1, 
        "title": "1. Логические выражения (№2)", 
        "description": "<b>Дано:</b> Логическое выражение:<br><code>(x ИЛИ y) И (НЕ z)</code><br><br><b>Задача:</b><br>Вычислите значение этого выражения (True или False), если:<br>x = 1 (True)<br>y = 0 (False)<br>z = 0 (False).", 
        "initial_code": "x = 1\ny = 0\nz = 0\n", 
        "expected_output": "True", 
        "explanation": "<ul><li>В Python: ИЛИ = <code>or</code>, И = <code>and</code>, НЕ = <code>not</code>.</li><li>Напишите: <code>print((x or y) and (not z))</code></li></ul>"
    },
    {
        "id": 2, 
        "title": "2. Двоичная система (№5)", 
        "description": "<b>Дано:</b> Число 60.<br><br><b>Задача:</b><br>Переведите число 60 в двоичную систему счисления. Выведите результат <b>без</b> префикса '0b'.", 
        "initial_code": "n = 60\n", 
        "expected_output": "111100", 
        "explanation": "<ul><li>Функция <code>bin(n)</code> дает '0b111100'.</li><li>Используйте срез <code>[2:]</code>, чтобы отрезать первые два символа.</li></ul>"
    },
    {
        "id": 3, 
        "title": "3. Анализ цикла (№6)", 
        "description": "<b>Дано:</b> Фрагмент программы:<br><pre>s = 0\nn = 1\nwhile s < 50:\n    s = s + 10\n    n = n * 2</pre><b>Задача:</b><br>Определите, что выведет эта программа (значение n), если в конце добавить <code>print(n)</code>.", 
        "initial_code": "s = 0\nn = 1\n# Допишите цикл и вывод\n", 
        "expected_output": "32", 
        "explanation": "<ul><li>Просто перепишите код задачи в редактор и запустите.</li><li>Компьютер выполнит цикл 5 раз. 2 в 5-й степени это 32.</li></ul>"
    },
    {
        "id": 4, 
        "title": "4. Комбинаторика (№8)", 
        "description": "<b>Дано:</b> Буквы 'A', 'B'.<br><br><b>Задача:</b><br>Сколько существует различных слов длины 2, составленных из этих букв? (Буквы могут повторяться). Выведите число.", 
        "initial_code": "count = 0\nletters = 'AB'\n", 
        "expected_output": "4", 
        "explanation": "<ul><li>Слова длины 2 — это два вложенных цикла.</li><li><code>for a in letters:</code></li><li>&nbsp;&nbsp;<code>for b in letters:</code></li><li>&nbsp;&nbsp;&nbsp;&nbsp;<code>count += 1</code></li></ul>"
    },
    {
        "id": 5, 
        "title": "5. Поиск в списке (№9)", 
        "description": "<b>Дано:</b> Список чисел: <code>[1, 2, 3, 1, 4]</code>.<br><br><b>Задача:</b><br>Найдите число, которое встречается в этом списке ровно 2 раза. Выведите это число.", 
        "initial_code": "a = [1, 2, 3, 1, 4]\n", 
        "expected_output": "1", 
        "explanation": "<ul><li>Переберите уникальные числа: <code>for x in set(a):</code></li><li>Проверьте количество: <code>if a.count(x) == 2:</code></li><li>Выведите x.</li></ul>"
    },
    {
        "id": 6, 
        "title": "6. Редактор строк (№12)", 
        "description": "<b>Дано:</b> Строка, состоящая из 10 единиц (<code>'1' * 10</code>).<br><b>Алгоритм:</b><br>Пока в строке нашлось '11': заменить первое вхождение '11' на '2'.<br><br><b>Задача:</b><br>Выведите строку, которая получится в результате.", 
        "initial_code": "s = '1' * 10\n", 
        "expected_output": "22222", 
        "explanation": "<ul><li><code>while '11' in s:</code></li><li><code>s = s.replace('11', '2', 1)</code></li><li>Обязательно укажите <b>1</b> в replace, чтобы менять только одно вхождение.</li></ul>"
    },
    {
        "id": 7, 
        "title": "7. IP-адреса (№13)", 
        "description": "<b>Дано:</b> IP-адрес '10.0.0.1'.<br><br><b>Задача:</b><br>Найдите сумму чисел, из которых состоит этот адрес (10+0+0+1).", 
        "initial_code": "ip = '10.0.0.1'\n", 
        "expected_output": "11", 
        "explanation": "<ul><li>Разбейте строку: <code>parts = ip.split('.')</code></li><li>Пройдитесь циклом, переведите части в int и сложите.</li></ul>"
    },
    {
        "id": 8, 
        "title": "8. Системы счисления (№14)", 
        "description": "<b>Дано:</b> Число 100.<br><br><b>Задача:</b><br>Сколько цифр '1' содержится в троичной записи числа 100?", 
        "initial_code": "x = 100\n", 
        "expected_output": "2", 
        "explanation": "<ul><li>Пока <code>x > 0</code>:</li><li>Проверяем последнюю цифру: <code>if x % 3 == 1: count += 1</code></li><li>Отбрасываем цифру: <code>x //= 3</code></li></ul>"
    },
    {
        "id": 9, 
        "title": "9. Рекурсия (№16)", 
        "description": "<b>Дано:</b> Алгоритм вычисления функции F(n):<br>1. <code>F(n) = 1</code>, при n = 1.<br>2. <code>F(n) = n + F(n-1)</code>, при n > 1.<br><br><b>Задача:</b><br>Чему равно значение F(4)?", 
        "initial_code": "def F(n):\n    # Напишите код функции\n    pass\n\nprint(F(4))", 
        "expected_output": "10", 
        "explanation": "<ul><li>Если <code>n == 1</code>, вернуть 1.</li><li>Иначе вернуть <code>n + F(n-1)</code>.</li></ul>"
    },
    {
        "id": 10, 
        "title": "10. Анализ пар (№17)", 
        "description": "<b>Дано:</b> Список <code>[10, 5, 2]</code>.<br><br><b>Задача:</b><br>Найдите количество пар соседних элементов, сумма которых делится на 3.", 
        "initial_code": "a = [10, 5, 2]\n", 
        "expected_output": "1", 
        "explanation": "<ul><li>Цикл до предпоследнего элемента: <code>range(len(a)-1)</code></li><li>Пара — это <code>a[i]</code> и <code>a[i+1]</code>.</li><li>Проверка: <code>(a[i] + a[i+1]) % 3 == 0</code>.</li></ul>"
    },
    {
        "id": 11, 
        "title": "11. Теория игр (№19)", 
        "description": "<b>Дано:</b> Куча камней S=8. За ход можно добавить +1 камень или умножить кол-во на 2.<br>Победа наступает, если камней >= 16.<br><br><b>Задача:</b><br>Выведите 'Yes', если можно выиграть ПЕРВЫМ же ходом.", 
        "initial_code": "s = 8\n", 
        "expected_output": "Yes", 
        "explanation": "<ul><li>Проверьте два хода.</li><li>8 * 2 = 16. Это победа? Да.</li></ul>"
    },
    {
        "id": 12, 
        "title": "12. Динамика (№23)", 
        "description": "<b>Дано:</b> Исполнитель, который умеет делать команды: <b>+1</b> и <b>*2</b>.<br><br><b>Задача:</b><br>Сколько существует программ (путей), которые преобразуют число <b>1</b> в число <b>3</b>?", 
        "expected_output": "2", 
        "explanation": "<ul><li>Функция перебирает все варианты.</li><li>Путь 1: 1 -> 2 -> 3 (+1, +1)</li><li>Путь 2: 1 -> (1*2)=2 -> 3 (*2, +1)</li><li>Итого 2 пути.</li></ul>"
    },
    {
        "id": 13, 
        "title": "13. Строки и цепочки (№24)", 
        "description": "<b>Дано:</b> Строка <code>s = 'AAABAA'</code>.<br><br><b>Задача:</b><br>Найдите длину самой длинной цепочки, состоящей только из символов 'A'.", 
        "initial_code": "s = 'AAABAA'\n", 
        "expected_output": "3", 
        "explanation": "<ul><li>Можно разбить строку по символу 'B': <code>s.split('B')</code>.</li><li>Получится список <code>['AAA', 'AA']</code>.</li><li>Найдите максимальную длину строки в этом списке.</li></ul>"
    },
    {
        "id": 14, 
        "title": "14. Маски файлов (№25)", 
        "description": "<b>Задача:</b><br>Проверьте с помощью библиотеки <code>fnmatch</code>, соответствует ли число 42 маске <code>'4?'</code> (где ? - один любой символ). Выведите True или False.", 
        "expected_output": "True", 
        "explanation": "<ul><li>Знак ? означает ровно один символ.</li><li>42 подходит под шаблон '4' + 'любой символ'.</li></ul>"
    },
    {
        "id": 15, 
        "title": "15. Сортировка (№26)", 
        "description": "<b>Дано:</b> Список <code>[10, 50, 5]</code>.<br><br><b>Задача:</b><br>Отсортируйте этот список по убыванию и выведите его.", 
        "initial_code": "a = [10, 50, 5]\n", 
        "expected_output": "[50, 10, 5]", 
        "explanation": "<ul><li>Используйте <code>a.sort(reverse=True)</code>.</li></ul>"
    },
    {
        "id": 16, 
        "title": "16. Эффективный перебор (№27)", 
        "description": "<b>Дано:</b> Список <code>[10, 2, 5]</code>.<br><br><b>Задача:</b><br>Найдите максимально возможную сумму пары двух РАЗНЫХ чисел из этого списка.", 
        "initial_code": "a = [10, 2, 5]\n", 
        "expected_output": "15", 
        "explanation": "<ul><li>Максимальная сумма — это сумма двух самых больших чисел.</li><li>10 + 5 = 15.</li></ul>"
    },
    {
        "id": 17, 
        "title": "17. Делители числа", 
        "description": "<b>Задача:</b><br>Найдите все натуральные делители числа 6 и выведите их в виде списка.", 
        "initial_code": "n = 6\nres = []\n", 
        "expected_output": "[1, 2, 3, 6]", 
        "explanation": "<ul><li>Переберите числа от 1 до 6.</li><li>Если <code>6 % i == 0</code>, добавьте i в список.</li></ul>"
    },
    {
        "id": 18, 
        "title": "18. Геометрия (Черепаха)", 
        "description": "<b>Задача:</b><br>Сколько точек с целочисленными координатами находится внутри квадрата размером 2x2?", 
        "initial_code": "", 
        "expected_output": "4", 
        "explanation": "<ul><li>Площадь квадрата равна произведению сторон.</li><li>2 * 2 = 4.</li></ul>"
    },
    {
        "id": 19, 
        "title": "19. Проверка условий", 
        "description": "<b>Дано:</b> Стороны треугольника: 3, 4, 5.<br><br><b>Задача:</b><br>Является ли этот треугольник прямоугольным (теорема Пифагора)? Выведите True или False.", 
        "initial_code": "a, b, c = 3, 4, 5\n", 
        "expected_output": "True", 
        "explanation": "<ul><li>Проверьте: <code>a**2 + b**2 == c**2</code></li></ul>"
    },
    {
        "id": 20, 
        "title": "20. Финал (Системы)", 
        "description": "<b>Задача:</b><br>Переведите число 100 в восьмеричную систему счисления. Выведите результат без префикса '0o'.", 
        "initial_code": "n = 100\n", 
        "expected_output": "144", 
        "explanation": "<ul><li>Функция <code>oct(n)</code>.</li><li>Срез <code>[2:]</code>.</li></ul>"
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materials')
def materials_page():
    return render_template('materials.html', materials=MATERIALS)

@app.route('/solve')
def solve_menu():
    grade = request.args.get('grade')
    task_id = request.args.get('id')
    
    tasks = TASKS_11 if str(grade) == '11' else TASKS_8
    grade_label = grade if grade else '8'

    if task_id:
        task = next((t for t in tasks if t['id'] == int(task_id)), None)
        next_id = int(task_id) + 1 if int(task_id) < len(tasks) else None
        return render_template('solve.html', task=task, materials=MATERIALS, grade=grade_label, next_id=next_id)
    
    return render_template('solve.html', task=None, tasks_list=tasks, materials=MATERIALS, grade=grade_label)

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    error = None
    output = ""
    try:
        # ПЕРЕДАЕМ scope В locals ЧТОБЫ РАБОТАЛА РЕКУРСИЯ
        scope = {}
        exec(code, scope, scope)
        output = new_stdout.getvalue().strip()
    except Exception as e:
        error = str(e)
    finally:
        sys.stdout = old_stdout
    return jsonify({'output': output, 'error': error})

@app.route('/check_solution', methods=['POST'])
def check_solution():
    user_output = request.json.get('output')
    task_id = request.json.get('task_id')
    grade = request.json.get('grade')
    tasks = TASKS_11 if str(grade) == '11' else TASKS_8
    task = next((t for t in tasks if t['id'] == int(task_id)), None)
    
    if task:
        clean_user = str(user_output).replace("\r", "").strip()
        clean_expected = str(task['expected_output']).strip()
        if clean_user == clean_expected:
            return jsonify({'correct': True})
            
    return jsonify({'correct': False, 'expected': task['expected_output'] if task else "Error"})

if __name__ == '__main__':
    app.run(debug=True)