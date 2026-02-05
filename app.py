from flask import Flask, render_template, request, jsonify
import sys
import io

app = Flask(__name__)

# --- БАЗА ДАННЫХ ЗАДАЧ (20 БИЛЕТОВ) ---
TASKS = [
    {"id": 1, "title": "1. Hello World", "description": "Напишите программу, которая выводит фразу: Hello Python", "initial_code": "", "expected_output": "Hello Python", "explanation": "Используйте функцию print('текст')."},
    {"id": 2, "title": "2. Простая арифметика", "description": "Посчитайте и выведите результат выражения: (25 + 15) * 3 - 10", "initial_code": "", "expected_output": "110", "explanation": "Математические действия в Python: + (сложение), - (вычитание), * (умножение)."},
    {"id": 3, "title": "3. Переменные", "description": "Дано: a = 4, b = 6. Вычислите периметр (P) прямоугольника и выведите его.", "initial_code": "a = 4\nb = 6\n", "expected_output": "20", "explanation": "Создайте переменную P и присвойте ей значение (a + b) * 2."},
    {"id": 4, "title": "4. Типы данных", "description": "Дана строка s = '2024'. Преобразуйте её в число, вычтите 24 и выведите результат.", "initial_code": "s = '2024'\n", "expected_output": "2000", "explanation": "Функция int(s) превращает строку в целое число."},
    {"id": 5, "title": "5. Условный оператор", "description": "В переменной x лежит число 15. Если оно делится на 3, выведите 'Div3', иначе 'No'.", "initial_code": "x = 15\n", "expected_output": "Div3", "explanation": "Используйте if x % 3 == 0: ... else: ..."},
    {"id": 6, "title": "6. Цикл for (сумма)", "description": "Найдите сумму всех целых чисел от 1 до 100 включительно.", "initial_code": "", "expected_output": "5050", "explanation": "Создайте переменную-счетчик и прибавляйте i в цикле for i in range(1, 101)."},
    {"id": 7, "title": "7. Генерация списка", "description": "Создайте список квадратов чисел от 1 до 5: [1, 4, 9, 16, 25].", "initial_code": "squares = []\n", "expected_output": "[1, 4, 9, 16, 25]", "explanation": "Используйте squares.append(i**2) внутри цикла."},
    {"id": 8, "title": "8. Поиск в списке", "description": "В списке numbers найдите количество чисел, равных 5.", "initial_code": "numbers = [1, 5, 2, 5, 5, 3, 4]\n", "expected_output": "3", "explanation": "Метод списка .count(5) вернет количество вхождений."},
    {"id": 9, "title": "9. Строки и срезы", "description": "Дана строка 'Abrakadabra'. Выведите её задом наперед.", "initial_code": "s = 'Abrakadabra'\n", "expected_output": "arbadakarbA", "explanation": "Используйте срез s[::-1] для разворота строки."},
    {"id": 10, "title": "10. While", "description": "Найдите минимальную степень двойки, которая больше 1000.", "initial_code": "n = 1\n", "expected_output": "1024", "explanation": "Цикл while n <= 1000: n *= 2."},
    {"id": 11, "title": "11. Делители числа", "description": "Напишите код, который находит все натуральные делители числа 30.", "initial_code": "n = 30\ndivs = []\n", "expected_output": "[1, 2, 3, 5, 6, 10, 15, 30]", "explanation": "Перебирайте числа от 1 до n и проверяйте остаток n % i == 0."},
    {"id": 12, "title": "12. Максимум в списке", "description": "Без использования max() найдите самое большое число в списке.", "initial_code": "nums = [4, 10, 2, 15, 7]\n", "expected_output": "15", "explanation": "Предположите, что первый элемент — максимум, и сравнивайте его с остальными в цикле."},
    {"id": 13, "title": "13. Функции", "description": "Напишите функцию is_even(n), возвращающую True, если число четное, и False иначе. Проверьте для 10.", "initial_code": "def is_even(n):\n    pass\n\nprint(is_even(10))", "expected_output": "True", "explanation": "Функция должна возвращать результат сравнения n % 2 == 0."},
    {"id": 14, "title": "14. Методы строк", "description": "Посчитайте, сколько раз слово 'python' встречается в тексте (без учета регистра).", "initial_code": "text = 'Python is cool. I love python.'\n", "expected_output": "2", "explanation": "Используйте text.lower().count('python')."},
    {"id": 15, "title": "15. Сортировка", "description": "Отсортируйте список по возрастанию любым способом.", "initial_code": "a = [5, 2, 9, 1]\n", "expected_output": "[1, 2, 5, 9]", "explanation": "Используйте метод a.sort()."},
    {"id": 16, "title": "16. ЕГЭ №16 (Рекурсия)", "description": "Алгоритм вычисления F(n):\nF(n) = 1 при n = 1\nF(n) = n * F(n - 1) при n > 1\nЧему равно значение F(5)?", "initial_code": "def F(n):\n    pass\n\nprint(F(5))", "expected_output": "120", "explanation": "Рекурсия: если n==1 вернуть 1, иначе вернуть n * F(n-1)."},
    {"id": 17, "title": "17. ЕГЭ №12 (Редактор)", "description": "Строка s = '8' * 50. Пока в строке есть '8888' или '222', если '8888' в s — заменить на '22', иначе заменить '222' на '8'.", "initial_code": "s = '8' * 50\nwhile '8888' in s or '222' in s:\n    # Ваш код\n    pass\nprint(s)", "expected_output": "88", "explanation": "Используйте s.replace('что', 'на что', 1)."},
    {"id": 18, "title": "18. ЕГЭ №5 (Алгоритмы)", "description": "Дано N = 13. Переведите в двоичную. К этой записи добавьте в конец '01'. Выведите результат в десятичной системе.", "initial_code": "N = 13\nb = bin(N)[2:]\n# Добавьте код\n", "expected_output": "53", "explanation": "Добавьте строку '01' к двоичной записи и используйте int(result, 2)."},
    {"id": 19, "title": "19. ЕГЭ №8 (Комбинаторика)", "description": "Сколько 3-буквенных слов можно составить из букв 'KOT'?", "initial_code": "count = 0\nletters = 'KOT'\n# Вложенные циклы\nprint(count)", "expected_output": "27", "explanation": "Используйте 3 вложенных цикла for (по одному на каждую позицию буквы)."},
    {"id": 20, "title": "20. ЕГЭ №25 (Делители)", "description": "Найдите числа в [100; 130] с ровно 3 делителями.", "initial_code": "res = []\n# Ваш код\nprint(res)", "expected_output": "[121]", "explanation": "Для каждого числа от 100 до 130 считайте количество делителей."}
]

# --- МАКСИМАЛЬНО ПОДРОБНЫЙ СПРАВОЧНИК ---
MATERIALS = {
    "1. Самые основы: Вывод данных": """
<h3>Как заставить компьютер говорить?</h3>
<p>Для этого в Python есть команда <code>print()</code>. Представьте, что это мегафон.</p>
<ul>
    <li>Если вы хотите вывести <b>текст</b>, его обязательно нужно брать в кавычки: <code>print("Привет")</code>.</li>
    <li>Если вы хотите вывести <b>число</b> или результат задачи, кавычки не нужны: <code>print(5 + 5)</code>.</li>
</ul>
<p><b style="color:red;">Важно:</b> Если вы забудете закрыть скобку или кавычку, программа выдаст ошибку <i>SyntaxError</i> (ошибка в тексте).</p>
<pre>
print("Я учу Python") # Выведет текст
print(2025)           # Выведет число
</pre>
    """,
    "2. Переменные: Коробки для данных": """
<h3>Что такое переменная?</h3>
<p>Представьте, что переменная — это <b>подписанная коробка</b>. Вы кладете туда число или текст, чтобы использовать их потом.</p>
<ul>
    <li><code>a = 5</code> — мы положили число 5 в коробку с надписью "a".</li>
    <li><code>name = "Иван"</code> — мы положили текст в коробку "name".</li>
</ul>
<h3>Типы данных (что лежит в коробке):</h3>
<ol>
    <li><b>int</b> (целое число) — например, 10, -5, 0.</li>
    <li><b>float</b> (дробное число) — всегда пишется через <b>точку</b>: 3.14.</li>
    <li><b>str</b> (строка) — любой текст в кавычках.</li>
</ol>
<p><b>Преобразование:</b> Иногда из строки "10" нужно сделать число 10. Для этого пишем <code>int("10")</code>.</p>
    """,
    "3. Математика: Считаем как профи": """
<h3>Основные действия:</h3>
<ul>
    <li><code>+</code> Сложение</li>
    <li><code>-</code> Вычитание</li>
    <li><code>*</code> Умножение</li>
    <li><code>/</code> Обычное деление (результат всегда будет дробным: 5 / 2 = 2.5)</li>
</ul>
<h3>"Королевские" действия для ЕГЭ:</h3>
<ul>
    <li><code>//</code> <b>Целочисленное деление</b>. Откидывает хвост. (7 // 2 = 3).</li>
    <li><code>%</code> <b>Остаток от деления</b>. (7 % 2 = 1). <i>Часто используется, чтобы проверить, четное ли число: <code>x % 2 == 0</code>.</i></li>
    <li><code>**</code> <b>Степень</b>. (2 ** 3 — это два в кубе = 8).</li>
</ul>
    """,
    "4. Условия: Выбор пути (If/Else)": """
<h3>Как научить программу думать?</h3>
<p>Используйте <code>if</code> (если). Это развилка на дороге.</p>
<pre>
x = 10
if x > 5:
    print("Число большое")
else:
    print("Число маленькое")
</pre>
<h3>Золотые правила отступов:</h3>
<p>В Python после <code>if</code> или <code>else</code> ставится <b>двоеточие</b>. А следующая строка <b>ОБЯЗАТЕЛЬНО</b> должна иметь отступ (4 пробела или клавиша Tab). Если отступа нет — программа сломается.</p>
    """,
    "5. Циклы: Повторение — мать учения": """
<h3>Цикл For (для счета)</h3>
<p>Нужен, чтобы повторить что-то 10, 100 или 1000 раз.</p>
<pre>
for i in range(5):
    print("Привет") # Напечатает "Привет" 5 раз
</pre>
<p>Функция <code>range(1, 6)</code> создаст числа от 1 до 5 (последнее число 6 <b>не включается</b>!).</p>
<h3>Цикл While (пока)</h3>
<p>Работает, пока условие верно. Например: пока в баке есть бензин — едем.</p>
<pre>
liters = 5
while liters > 0:
    print("Едем...")
    liters = liters - 1
</pre>
    """,
    "6. Списки: Огромный склад": """
<p>Список — это одна большая коробка со множеством ячеек. Каждая ячейка имеет свой номер (индекс).</p>
<p><b style="color:orange;">Внимание:</b> Счет в Python начинается с <b>0</b>!</p>
<pre>
a = [10, 20, 30]
print(a[0]) # Выведет 10
a.append(40) # Добавит 40 в конец списка
</pre>
<h3>Полезные штуки для списков:</h3>
<ul>
    <li><code>len(a)</code> — сколько элементов в списке.</li>
    <li><code>sum(a)</code> — сложить все числа внутри.</li>
    <li><code>max(a)</code> — найти самое большое число.</li>
</ul>
    """,
    "7. Строки: Работа с текстом": """
<p>Строка — это цепочка символов.</p>
<pre>
s = "Программирование"
print(s[0]) # Выведет "П"
print(s.lower()) # Сделает всё маленькими буквами
</pre>
<h3>Срезы (Как отрезать кусок строки):</h3>
<p>Пишется в квадратных скобках: <code>s[начало : конец]</code>.</p>
<ul>
    <li><code>s[0:2]</code> — первые две буквы.</li>
    <li><code>s[::-1]</code> — <b>магия!</b> Разворачивает строку задом наперед.</li>
</ul>
    """,
    "8. Рекурсия (Задача ЕГЭ №16)": """
<p>Рекурсия — это когда функция вызывает саму себя. Как матрешка.</p>
<pre>
def F(n):
    if n == 1:
        return 1 # База (когда матрешки кончились)
    return n * F(n-1) # Шаг (вызываем матрешку поменьше)
</pre>
<p>Всегда проверяйте условие выхода (if n == 1), иначе программа будет работать вечно и зависнет.</p>
    """,
    "9. Системы счисления (Задача ЕГЭ №5)": """
<p>В ЕГЭ часто просят перевести число в двоичную систему (нули и единицы).</p>
<ul>
    <li><code>bin(10)</code> — переведет число 10 в двоичную: <code>'0b1010'</code>.</li>
    <li>Чтобы убрать мусор <code>'0b'</code> в начале, используйте срез: <code>bin(10)[2:]</code>.</li>
    <li>Чтобы перевести <b>ОБРАТНО</b> в обычное число: <code>int('1010', 2)</code>.</li>
</ul>
    """
}

# --- МАРШРУТЫ FLASK (БЕЗ ИЗМЕНЕНИЙ) ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materials')
def materials_page():
    return render_template('materials.html', materials=MATERIALS)

@app.route('/solve')
def solve_menu():
    task_id = request.args.get('id')
    if task_id:
        task = next((t for t in TASKS if t['id'] == int(task_id)), None)
        next_id = int(task_id) + 1 if int(task_id) < len(TASKS) else None
        return render_template('solve.html', task=task, materials=MATERIALS, next_id=next_id)
    return render_template('solve.html', task=None, tasks_list=TASKS, materials=MATERIALS)

@app.route('/run_code', methods=['POST'])
def run_code():
    code = request.json.get('code')
    old_stdout = sys.stdout
    new_stdout = io.StringIO()
    sys.stdout = new_stdout
    error = None
    output = ""
    try:
        exec(code, {})
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
    task = next((t for t in TASKS if t['id'] == int(task_id)), None)
    if task:
        clean_user = str(user_output).replace(" ", "").replace("\n", "").strip()
        clean_expected = str(task['expected_output']).replace(" ", "").replace("\n", "").strip()
        if clean_user == clean_expected:
            return jsonify({'correct': True})
    return jsonify({'correct': False, 'expected': task['expected_output'] if task else ""})

if __name__ == '__main__':
    app.run(debug=True)