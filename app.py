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
            <li><code>nums.count(20)</code> — сколько раз встречается число 20.</li>
            <li><code>nums.sort()</code> — сортировать (навсегда меняет список).</li>
            <li><code>len(nums)</code> — длина списка.</li>
            <li><code>sum(nums)</code> — сумма чисел.</li>
            <li><code>max(nums)</code> — максимальное число.</li>
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
d["Bob"] = 4     # Изменить значение</pre>
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
from itertools import product

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
        <p>Эффективный перебор — до корня из числа, либо просто перебор от 1 до N.</p>
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

# --- ЗАДАЧИ 8 КЛАСС (ОТ ПРОСТОГО К СЛОЖНОМУ) ---
TASKS_8 = [
    {"id": 1, "title": "1: Гипотенуза треугольника", "description": "<b>Задача:</b> Даны катеты прямоугольного треугольника: a = 3 и b = 4. Вычислите длину гипотенузы по теореме Пифагора. Не используйте библиотеку math.", "initial_code": "", "expected_output": "5.0", "explanation": "<ul>Квадратный корень из числа x — это то же самое, что x в степени 0.5</ul>"},
    {"id": 2, "title": "2. Срез строки с шагом", "description": "<b>Задача:</b> Дана строка s = '1a2b3c4d'. Получите из неё только цифры, используя срезы (slicing) с шагом, и выведите их как одну строку.", "initial_code": 's = "1a2b3c4d"', "expected_output": "1234", "explanation": "<ul>Синтаксис среза: [start:stop:step]. Вам нужно начинать с 0 и брать каждый второй символ.</ul>"},
    {"id": 3, "title": "3. Високосный год", "description": "<b>Задача:</b> Напишите условие для года year = 2024. Год високосный, если он делится на 4, НО не делится на 100, ЕСЛИ ТОЛЬКО он не делится на 400. Выведите True или False.", "initial_code": "year = 2024", "expected_output": "True", "explanation": "<ul>Используйте оператор % (остаток от деления) и логические связки and, or, not.</ul>"},
    {"id": 4, "title": "4. Сумма цифр числа", "description": "<b>Задача:</b> Дано число num = 12345. Найдите сумму его цифр (1+2+3+4+5), не используя цикл, а используя преобразование типов и функцию sum().", "initial_code": "num = 12345", "expected_output": "15", "explanation": "<ul>Число можно превратить в строку, строку — в список чисел (через генератор), а потом сложить.</ul>"},
    {"id": 5, "title": "5. Второй максимум", "description": "<b>Задача:</b> Дан список arr = [10, 20, 4, 45, 99]. Найдите второе по величине число, не используя встроенную сортировку .sort().", "initial_code": "arr = [10, 20, 4, 45, 99]\n", "expected_output": "45", "explanation": "<ul>Можно удалить максимум и найти максимум снова, либо пройтись циклом, храня две переменные: max1 и max2.</ul>"},
    {"id": 6, "title": "6. FizzBuzz", "description": "<b>Задача:</b> Для чисел от 1 до 15: если число делится на 3, печатаем 'Fizz', если на 5 — 'Buzz', если на 3 и на 5 — 'FizzBuzz', иначе — само число.", "initial_code": "", "expected_output": "1 2 Fizz 4 Buzz Fizz 7 8 Fizz Buzz 11 Fizz 13 14 FizzBuzz", "explanation": "<ul>Сначала проверяйте самое сложное условие (деление и на 3, и на 5).</ul>"},
    {"id": 7, "title": "7. Простые числа", "description": "<b>Задача:</b> Напишите код, который проверяет, является ли число n = 29 простым (делится только на 1 и на себя). Выведите True или False.", "initial_code": "n = 29", "expected_output": "True", "explanation": "<ul>Попробуйте поделить число n на все числа от 2 до n-1 в цикле. Если хоть раз разделилось без остатка — число составное.</ul>"},
    {"id": 8, "title": "8. Сжатие списка", "description": "<b>Задача:</b> Дан список data = [1, 1, 2, 3, 3, 3, 4, 1]. Создайте новый список, где подряд идущие дубликаты схлопнуты в один (как в команде uniq).", "initial_code": "data = [1, 1, 2, 3, 3, 3, 4, 1]\n", "expected_output": "[1, 2, 3, 4, 1]", "explanation": "<ul>Пройдитесь по списку и добавляйте элемент в новый список только если он отличается от последнего добавленного.</ul>"},
    {"id": 9, "title": "9. Анаграмма", "description": "<b>Задача:</b> Напишите функцию is_anagram(s1, s2), которая проверяет, состоят ли две строки из одних и тех же букв (например, 'listen' и 'silent').", "initial_code": "", "expected_output": "True", "explanation": "<ul>Анаграммы становятся одинаковыми, если их отсортировать.</ul>"},
    {"id": 10, "title": "10. Инверсия словаря", "description": "<b>Задача:</b> Дан словарь d = {'a': 1, 'b': 2, 'c': 1}. Создайте новый словарь, где ключи и значения меняются местами. Если значения повторяются, можно сохранить любое.", "initial_code": "d = {'a': 1, 'b': 2, 'c': 1}\n", "expected_output": "{1: 'c', 2: 'b'}", "explanation": "<ul>Используйте dict comprehension или цикл .items().</ul>"},
    {"id": 11, "title": "11. Подсчет слов", "description": "<b>Задача:</b> Дана строка text = 'apple banana apple orange banana apple'. Создайте словарь, где ключ — слово, а значение — количество его повторений.", "initial_code": 'text = "apple banana apple orange banana apple"', "expected_output": "{'apple': 3, 'banana': 2, 'orange': 1}", "explanation": "<ul>Разбейте строку методом .split(), затем используйте цикл или Counter из модуля collections.</ul>"},
    {"id": 12, "title": "12. Шифр Цезаря", "description": "<b>Задача:</b> Зашифруйте слово 'abc' сдвигом на 2 буквы вперед (a->c, b->d, c->e). Используйте функции ord() и chr().", "initial_code": "word = 'abc'", "expected_output": "cde", "explanation": "<ul>ord('a') возвращает код символа. Прибавьте сдвиг, затем верните символ через chr().</ul>"},
    {"id": 13, "title": "13. List Comprehension", "description": "<b>Задача:</b> Дан список чисел от 1 до 10. Создайте список, содержащий квадраты только четных чисел, используя List Comprehension.", "initial_code": "", "expected_output": "[4, 16, 36, 64, 100]", "explanation": "<ul>Общий синтаксис спискового включения: [выражение for переменная in список if условие]. Вам нужно возвести x в квадрат, где x берется из диапазона, но только если x % 2 == 0.</ul>"},
    {"id": 14, "title": "14. Подсчет", "description": "<b>Задача:</b> Сколько раз 'a' встречается в 'banana'?", "initial_code": "s = 'banana'\n", "expected_output": "3", "explanation": "<ul><li><code>s.count('a')</code></li></ul>"},
    {"id": 15, "title": "15. Четность", "description": "<b>Задача:</b> Выведите четные числа из [1, 2, 3, 4].", "initial_code": "a = [1, 2, 3, 4]\n", "expected_output": "2\n4", "explanation": "<ul><li><code>if x % 2 == 0:</code></li></ul>"},
    {"id": 16, "title": "16. Максимум", "description": "<b>Задача:</b> Найдите максимальное число из 5, 12, 3.", "initial_code": "", "expected_output": "12", "explanation": "<ul><li><code>max(5, 12, 3)</code></li></ul>"},
    {"id": 17, "title": "17. Подсчет гласных", "description": "<b>Задача:</b> Посчитайте количество гласных (a, e, i, o, u) в строке 'hello world'", "initial_code": "", "expected_output": "3", "explanation": "<ul>Создайте строку со всеми гласными 'aeiou'. В цикле проверяйте каждый символ вашей строки: если он in (входит в) строку гласных, увеличивайте счетчик.</ul>"},
    {"id": 18, "title": "18. Функции", "description": "<b>Задача:</b> Напишите функцию sum2(a, b), возвращающую a+b. Выведите для 10, 20.", "initial_code": "def sum2(a, b):\n    pass\nprint(sum2(10, 20))", "expected_output": "30", "explanation": "<ul><li><code>return a + b</code></li></ul>"},
    {"id": 19, "title": "19. Сортировка", "description": "<b>Задача:</b> Отсортируйте [3, 1, 2] по возрастанию.", "initial_code": "a = [3, 1, 2]\n", "expected_output": "[1, 2, 3]", "explanation": "<ul><li><code>a.sort()</code></li></ul>"},
    {"id": 20, "title": "20. Палиндром", "description": "<b>Задача:</b> Напишите функцию, которая проверяет, является ли слово палиндромом (читается одинаково с обеих сторон). Проверьте слово 'radar'.", "initial_code": "", "expected_output": "True", "explanation": "<ul>Слово является палиндромом, если слово == перевернутое_слово.</ul>"}
]

# --- ЗАДАЧИ 11 КЛАСС (ЕГЭ: ОТ ПРОСТОГО К СЛОЖНОМУ) ---
TASKS_11 = [
    # --- БАЗОВЫЙ УРОВЕНЬ ---
    {
        "id": 1, 
        "title": "1. Анализ кода (ЕГЭ №6)", 
        "description": "<b>Дано:</b> Фрагмент программы:<br><pre>s = 0\nn = 1\nwhile s < 50:\n    s = s + 10\n    n = n * 2</pre><b>Задача:</b><br>Определите, что выведет эта программа (значение n).", 
        "initial_code": "s = 0\nn = 1\n# Допишите код\n", 
        "expected_output": "32", 
        "explanation": "<ul><li>Просто допишите <code>print(n)</code> и запустите.</li><li>Цикл выполнится 5 раз (s=10,20,30,40,50). 2^5 = 32.</li></ul>"
    },
    {
        "id": 2, 
        "title": "2. Логика (ЕГЭ №2)", 
        "description": "<b>Дано:</b> Выражение <code>(x ИЛИ y) И (НЕ z)</code>.<br><b>Задача:</b> Выведите True/False при x=1, y=0, z=0.", 
        "initial_code": "x, y, z = 1, 0, 0\n", 
        "expected_output": "True", 
        "explanation": "<ul><li><code>print((x or y) and (not z))</code></li></ul>"
    },
    {
        "id": 3, 
        "title": "3. Системы счисления (ЕГЭ №5)", 
        "description": "<b>Задача:</b> Переведите число 60 в двоичную систему. Выведите результат без '0b'.", 
        "initial_code": "n = 60\n", 
        "expected_output": "111100", 
        "explanation": "<ul><li><code>bin(n)[2:]</code></li></ul>"
    },
    {
        "id": 4, 
        "title": "4. Геометрия (ЕГЭ №6)", 
        "description": "<b>Задача:</b> Черепаха рисует квадрат 10x10. Сколько целочисленных точек внутри?", 
        "initial_code": "", 
        "expected_output": "100", 
        "explanation": "<ul><li>Площадь квадрата: 10 * 10 = 100.</li></ul>"
    },
    {
        "id": 5, 
        "title": "5. Сортировка (ЕГЭ №26 База)", 
        "description": "<b>Задача:</b> Дан список цен. Отсортируйте его по убыванию.", 
        "initial_code": "a = [10, 50, 5, 100]\n", 
        "expected_output": "[100, 50, 10, 5]", 
        "explanation": "<ul><li><code>a.sort(reverse=True)</code></li></ul>"
    },

    # --- СРЕДНИЙ УРОВЕНЬ (АЛГОРИТМЫ) ---
    {
        "id": 6, 
        "title": "6. Комбинаторика (ЕГЭ №8)", 
        "description": "<b>Задача:</b> Сколько слов длины 2 можно составить из букв 'A', 'B'? (Буквы повторяются).", 
        "initial_code": "count = 0\nletters = 'AB'\n", 
        "expected_output": "4", 
        "explanation": "<ul><li>Два вложенных цикла по буквам.</li><li><code>count += 1</code> внутри.</li></ul>"
    },
    {
        "id": 7, 
        "title": "7. Поиск в списке (ЕГЭ №9)", 
        "description": "<b>Задача:</b> Найдите число, которое встречается в списке <code>[1, 2, 3, 1, 4]</code> ровно 2 раза.", 
        "initial_code": "a = [1, 2, 3, 1, 4]\n", 
        "expected_output": "1", 
        "explanation": "<ul><li>Переберите уникальные <code>set(a)</code>.</li><li>Если <code>a.count(x) == 2</code>, выведите x.</li></ul>"
    },
    {
        "id": 8, 
        "title": "8. IP-адреса (ЕГЭ №13)", 
        "description": "<b>Задача:</b> Найдите сумму чисел IP-адреса '10.0.0.1'.", 
        "initial_code": "ip = '10.0.0.1'\n", 
        "expected_output": "11", 
        "explanation": "<ul><li><code>ip.split('.')</code></li><li>Суммируйте <code>int()</code> частей.</li></ul>"
    },
    {
        "id": 9, 
        "title": "9. Редактор строк (ЕГЭ №12)", 
        "description": "<b>Алгоритм:</b> Пока нашлось '11', заменить '11' на '2' (один раз).<br><b>Дано:</b> Строка из 10 единиц.", 
        "initial_code": "s = '1' * 10\n", 
        "expected_output": "22222", 
        "explanation": "<ul><li><code>while '11' in s:</code></li><li><code>s = s.replace('11', '2', 1)</code></li></ul>"
    },
    {
        "id": 10, 
        "title": "10. Арифметика СС (ЕГЭ №14)", 
        "description": "<b>Задача:</b> Сколько цифр '1' в троичной записи числа 100?", 
        "initial_code": "x = 100\n", 
        "expected_output": "2", 
        "explanation": "<ul><li>Цикл <code>while x > 0</code>.</li><li>Если <code>x % 3 == 1</code>, счетчик +1.</li><li><code>x //= 3</code>.</li></ul>"
    },

    # --- ПРОДВИНУТЫЙ УРОВЕНЬ ---
    {
        "id": 11, 
        "title": "11. Делители (ЕГЭ №25)", 
        "description": "<b>Задача:</b> Найдите все натуральные делители числа 6.", 
        "initial_code": "n = 6\nres = []\n", 
        "expected_output": "[1, 2, 3, 6]", 
        "explanation": "<ul><li>Цикл <code>for i in range(1, n+1):</code></li><li>Если <code>n % i == 0</code>, добавить в список.</li></ul>"
    },
    {
        "id": 12, 
        "title": "12. Рекурсия (ЕГЭ №16)", 
        "description": "<b>Дано:</b> F(1)=1; F(n) = n + F(n-1).<br><b>Задача:</b> Найти F(4).", 
        "initial_code": "def F(n):\n    pass\nprint(F(4))", 
        "expected_output": "10", 
        "explanation": "<ul><li>База: <code>if n==1: return 1</code></li><li>Шаг: <code>return n + F(n-1)</code></li></ul>"
    },
    {
        "id": 13, 
        "title": "13. Обработка пар (ЕГЭ №17)", 
        "description": "<b>Задача:</b> Найти кол-во пар соседей в <code>[10, 5, 2]</code>, сумма которых кратна 3.", 
        "initial_code": "a = [10, 5, 2]\n", 
        "expected_output": "1", 
        "explanation": "<ul><li><code>for i in range(len(a)-1):</code></li><li>Проверка <code>(a[i]+a[i+1]) % 3 == 0</code>.</li></ul>"
    },
    {
        "id": 14, 
        "title": "14. Маски (ЕГЭ №25)", 
        "description": "<b>Задача:</b> Проверьте, подходит ли число 42 под маску '4?'. ? означает один символ",  
        "expected_output": "True", 
        "explanation": "<ul><li>Для решения задачи стоит применить библиотеку.</li></ul>"
    },
    {
        "id": 15, 
        "title": "15. Цепочки (ЕГЭ №24)", 
        "description": "<b>Задача:</b> Макс. длина цепочки из 'A' в строке 'AAABAA'.", 
        "initial_code": "s = 'AAABAA'\n", 
        "expected_output": "3", 
        "explanation": "<ul><li>Разбейте по 'B': <code>s.split('B')</code>.</li><li>Найдите макс длину элемента в списке.</li></ul>"
    },

    # --- СЛОЖНЫЙ УРОВЕНЬ (HARD) ---
    {
        "id": 16, 
        "title": "16. Теория игр (ЕГЭ №19)", 
        "description": "<b>Дано:</b> Куча=8. Ходы: +1, *2. Победа >= 16.<br><b>Задача:</b> Выведите 'Yes', если можно выиграть 1 ходом.", 
        "initial_code": "s = 8\n", 
        "expected_output": "Yes", 
        "explanation": "<ul><li>Проверьте <code>8*2 >= 16</code>.</li></ul>"
    },
    {
        "id": 17, 
        "title": "17. Динамика с ограничениями (№23)", 
        "description": "<b>Дано:</b> Исполнитель с командами: <b>+1</b> и <b>+2</b>.<br><b>Задача:</b> Сколько существует программ, которые преобразуют число <b>2</b> в <b>12</b>, при этом траектория вычислений <b>не содержит</b> число <b>7</b>?", 
        "initial_code": "def F(start, end):\n    # Допишите условия\n    pass\n\nprint(F(2, 12))", 
        "expected_output": "25", 
        "explanation": "<ul><li>Стандартная рекурсия: <code>return F(start+1, end) + F(start+2, end)</code>.</li><li><b>Ключевое условие:</b> Если <code>start == 7</code>, эта ветка траектории 'плохая' и должна вернуть 0 путей.</li><li>Добавьте проверку <code>if start == 7: return 0</code> ПЕРЕД рекурсивным вызовом.</li></ul>"
    },
    {
        "id": 18, 
        "title": "18. Эффективность (ЕГЭ №27)", 
        "description": "<b>Задача:</b> Найди максимальную сумму пары РАЗНЫХ чисел в <code>[10, 2, 5, 24, 1, 6]</code>.", 
        "initial_code": "a = [10, 2, 5, 24, 1, 6]\n", 
        "expected_output": "34", 
        "explanation": "<ul><li>Сортируем. Берем два самых больших.</li></ul>"
    },
    {
        "id": 19, 
        "title": "19. Сложная логика (ЕГЭ №15)", 
        "description": "<b>Задача:</b> Проверьте треугольник со сторонами 3, 4, 5 на прямоугольность (Пифагор).", 
        "initial_code": "a,b,c = 3,4,5\n", 
        "expected_output": "True", 
        "explanation": "<ul><li><code>a**2 + b**2 == c**2</code></li></ul>"
    },
    {
        "id": 20, 
        "title": "20. Финал (№24 Сложные цепочки)", 
        "description": "<b>Дано:</b> Текстовый файл (здесь строка <code>s</code>), состоящий из символов A, B, C, D.<br><br><b>Задача:</b><br>Найдите максимальную длину подцепочки, которая не содержит букву 'D'.", 
        "initial_code": "s = 'ABCAADDAABBCAАDDDA'\n", 
        "expected_output": "7", 
        "explanation": "<ul><li>Цепочки, не содержащие 'D', разделены буквой 'D'.</li><li>Разбейте строку по букве 'D': <code>parts = s.split('D')</code>.</li><li>Вы получите список подцепочек: <code>['ABCAA', 'AABBC', 'A']</code>.</li><li>Найдите максимальную длину элемента в этом списке. Можно циклом или так: <code>max(len(p) for p in parts)</code>.</li></ul>"
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