from flask import Flask, render_template, request, jsonify
import sys
import io

app = Flask(__name__)

# --- БАЗА ДАННЫХ ЗАДАЧ (20 БИЛЕТОВ, БЕЗ ФАЙЛОВ) ---
TASKS = [
    # --- БЛОК 1: ОСНОВЫ (1-5) ---
    {"id": 1, "title": "1. Hello World", "description": "Напишите программу, которая выводит фразу: Hello Python", "initial_code": "", "expected_output": "Hello Python", "explanation": "print('Hello Python')"},
    {"id": 2, "title": "2. Простая арифметика", "description": "Посчитайте и выведите результат выражения: (25 + 15) * 3 - 10", "initial_code": "", "expected_output": "110", "explanation": "print((25 + 15) * 3 - 10)"},
    {"id": 3, "title": "3. Переменные", "description": "Дано: a = 4, b = 6. Вычислите периметр (P) прямоугольника и выведите его.", "initial_code": "a = 4\nb = 6\n", "expected_output": "20", "explanation": "P = (a + b) * 2"},
    {"id": 4, "title": "4. Типы данных", "description": "Дана строка s = '2024'. Преобразуйте её в число, вычтите 24 и выведите результат.", "initial_code": "s = '2024'\n", "expected_output": "2000", "explanation": "n = int(s)\nprint(n - 24)"},
    {"id": 5, "title": "5. Условный оператор", "description": "В переменной x лежит число 15. Если оно делится на 3, выведите 'Div3', иначе 'No'.", "initial_code": "x = 15\n", "expected_output": "Div3", "explanation": "if x % 3 == 0:..."},
    
    # --- БЛОК 2: ЦИКЛЫ И СПИСКИ (6-10) ---
    {"id": 6, "title": "6. Цикл for (сумма)", "description": "Найдите сумму всех целых чисел от 1 до 100 включительно.", "initial_code": "", "expected_output": "5050", "explanation": "sum = 0\nfor i in range(1, 101):..."},
    {"id": 7, "title": "7. Генерация списка", "description": "Создайте список квадратов чисел от 1 до 5: [1, 4, 9, 16, 25].", "initial_code": "squares = []\n", "expected_output": "[1, 4, 9, 16, 25]", "explanation": "squares.append(i**2)"},
    {"id": 8, "title": "8. Поиск в списке", "description": "В списке numbers найдите количество чисел, равных 5.", "initial_code": "numbers = [1, 5, 2, 5, 5, 3, 4]\n", "expected_output": "3", "explanation": "count = 0..."},
    {"id": 9, "title": "9. Строки и срезы", "description": "Дана строка 'Abrakadabra'. Выведите её задом наперед.", "initial_code": "s = 'Abrakadabra'\n", "expected_output": "arbadakarbA", "explanation": "print(s[::-1])"},
    {"id": 10, "title": "10. While", "description": "Найдите минимальную степень двойки, которая больше 1000.", "initial_code": "n = 1\n", "expected_output": "1024", "explanation": "while n <= 1000: n *= 2"},
    
    # --- БЛОК 3: АЛГОРИТМЫ (11-15) ---
    {"id": 11, "title": "11. Делители числа", "description": "Напишите код, который находит все натуральные делители числа 30.", "initial_code": "n = 30\ndivs = []\n", "expected_output": "[1, 2, 3, 5, 6, 10, 15, 30]", "explanation": "if n % i == 0: divs.append(i)"},
    {"id": 12, "title": "12. Максимум в списке", "description": "Без использования max() найдите самое большое число в списке.", "initial_code": "nums = [4, 10, 2, 15, 7]\n", "expected_output": "15", "explanation": "mx = nums[0]..."},
    {"id": 13, "title": "13. Функции", "description": "Напишите функцию is_even(n), возвращающую True, если число четное.", "initial_code": "def is_even(n):\n    pass\n\nprint(is_even(10))", "expected_output": "True", "explanation": "return n % 2 == 0"},
    {"id": 14, "title": "14. Методы строк", "description": "Посчитайте, сколько раз слово 'python' встречается в тексте.", "initial_code": "text = 'Python is cool. I love python.'\n", "expected_output": "2", "explanation": "text.lower().count('python')"},
    {"id": 15, "title": "15. Сортировка", "description": "Отсортируйте список по возрастанию любым способом.", "initial_code": "a = [5, 2, 9, 1]\n", "expected_output": "[1, 2, 5, 9]", "explanation": "a.sort()"},

    # --- БЛОК 4: ЕГЭ (ЧИСТЫЕ АЛГОРИТМЫ) ---
    {
        "id": 16, 
        "title": "16. ЕГЭ №16 (Рекурсия)", 
        "description": "Алгоритм вычисления функции F(n) задан соотношениями:\nF(n) = 1 при n = 1\nF(n) = n * F(n - 1) при n > 1\nЧему равно значение функции F(5)? Напишите программу для вычисления.", 
        "expected_output": "120", 
        "explanation": "Если n==1 вернуть 1. Иначе вернуть n * F(n-1)."
    },
    {
        "id": 17, 
        "title": "17. ЕГЭ №12 (Редактор строк)", 
        "description": "Дана строка, состоящая из 50 цифр '8'. Имеется редактор с командами: заменить '8888' на '22' и заменить '222' на '8'.\nНАЙДИТЕ, какая строка получится, если применять замены, пока это возможно (пока есть вхождения '8888' или '222'). Приоритет любой.", 
        "expected_output": "88", 
        "explanation": "Используйте цикл while. Внутри проверяйте if '8888' in s... replace(..., 1). Важно указывать 1 (одна замена за раз)!"
    },
    {
        "id": 18, 
        "title": "18. ЕГЭ №5 (Алгоритмы)", 
        "description": "На вход алгоритма подаётся число N = 13. Алгоритм строит по нему новое число R:\n1. Строится двоичная запись числа N.\n2. К этой записи дописываются разряды: если число чётное, слева '10', если нечётное, слева '1' и справа '01'.\nЧему равно число R (в десятичной системе)?", 
        "expected_output": "53", 
        "explanation": "Если N % 2 == 0: s = '10' + bin_n. Иначе: s = '1' + bin_n + '01'. Результат int(s, 2)."
    },
    {
        "id": 19, 
        "title": "19. ЕГЭ №8 (Комбинаторика)", 
        "description": "Сколько существует различных трехбуквенных слов, которые можно составить из букв 'K', 'O', 'T', используя буквы сколько угодно раз?", 
        "expected_output": "27", 
        "explanation": "Три вложенных цикла по буквам 'KOT'. Счетчик +1 на каждой итерации."
    },
    {
        "id": 20, 
        "title": "20. ЕГЭ №25 (Делители)", 
        "description": "Найдите все натуральные числа в диапазоне [100; 130], у которых ровно 3 делителя. Выведите эти числа списком.", 
        "expected_output": "[121]", 
        "explanation": "Перебираем числа. Для каждого числа считаем делители от 1 до самого числа. Если count == 3, добавляем в список."
    }
]

# --- СПРАВОЧНИК (ОСТАВЛЯЕМ КАК БЫЛ) ---
MATERIALS = {
    "1. Введение": """<p>Python (Пайтон) — это мощный язык программирования.</p><h3>Основные команды</h3><ul><li><code>print("Текст")</code> — вывод.</li><li><code>input()</code> — ввод.</li></ul>""",
    "2. Переменные": """<p>Переменные хранят данные.</p><ul><li><b>int</b>: 5</li><li><b>str</b>: "Привет"</li></ul>""",
    "3. Условия": """<pre>if x > 0:\n    print("Yes")\nelse:\n    print("No")</pre>""",
    "4. Циклы": """<pre>for i in range(5):\n    print(i)</pre>""",
    "5. Списки": """<pre>a = [1, 2, 3]\na.append(4)</pre>""",
    "6. Строки": """<pre>s = "Hello"\ns.replace("l", "z")</pre>""",
    "7. Рекурсия (ЕГЭ 16)": """<p>Функция вызывает саму себя.</p><pre>def F(n):\n    if n == 1: return 1\n    return n * F(n-1)</pre>""",
    "8. Системы счисления (ЕГЭ 5)": """<pre>bin(10)  # '0b1010' (в двоичную)\nint('1010', 2) # 10 (в десятичную)</pre>"""
}


# --- FLASK ---
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
        next_task = next((t for t in TASKS if t['id'] == int(task_id) + 1), None)
        return render_template('solve.html', task=task, materials=MATERIALS, next_id=next_task['id'] if next_task else None)
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
        clean_user = str(user_output).replace(" ", "").replace("\n", "").replace("\r", "").strip()
        clean_expected = str(task['expected_output']).replace(" ", "").replace("\n", "").replace("\r", "").strip()
        if clean_user == clean_expected:
            return jsonify({'correct': True})
        else:
            return jsonify({'correct': False, 'expected': task['expected_output']})
    return jsonify({'correct': False, 'expected': "Ошибка ID"})

if __name__ == '__main__':
    app.run(debug=True)