// Получаем ID текущей задачи из URL
const currentTaskId = new URLSearchParams(window.location.search).get('id');

var editor;

// Инициализация редактора
if (document.getElementById('editor')) {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");

    // --- ЛОГИКА ЗАГРУЗКИ СОХРАНЕННОГО КОДА ---
    if (currentTaskId) {
        // Проверяем, есть ли сохраненный код для этой задачи
        const savedCode = localStorage.getItem('task_code_' + currentTaskId);
        
        if (savedCode) {
            // Если есть, вставляем его в редактор
            editor.setValue(savedCode);
            editor.clearSelection(); // Убираем выделение текста
        }
    }

    // --- ЛОГИКА СОХРАНЕНИЯ ПРИ ИЗМЕНЕНИИ ---
    editor.session.on('change', function(delta) {
        if (currentTaskId) {
            // 1. Сохраняем сам код
            const code = editor.getValue();
            localStorage.setItem('task_code_' + currentTaskId, code);

            // 2. Меняем статус на "в процессе" (желтый), если задача еще не решена
            const currentStatus = localStorage.getItem('task_status_' + currentTaskId);
            if (currentStatus !== 'solved') {
                localStorage.setItem('task_status_' + currentTaskId, 'in-progress');
            }
        }
    });
}

// Функция СБРОСА кода к начальному состоянию
function resetCode() {
    if(confirm("Вы уверены, что хотите сбросить код к начальному состоянию?")) {
        const initialCode = document.getElementById('initialCodeStore').value;
        editor.setValue(initialCode);
        editor.clearSelection();
        // Обновляем сохранение
        if (currentTaskId) {
            localStorage.setItem('task_code_' + currentTaskId, initialCode);
        }
    }
}

// Запуск кода
async function runCode() {
    const code = editor.getValue();
    const outputBlock = document.getElementById('outputBlock');
    outputBlock.innerText = "Выполнение...";
    outputBlock.style.color = "#ccc";

    const response = await fetch('/run_code', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: code })
    });
    const result = await response.json();
    if (result.error) {
        outputBlock.innerText = "Ошибка:\n" + result.error;
        outputBlock.style.color = "ff4444"; // Красный оттенок
    } else {
        outputBlock.innerText = result.output;
        outputBlock.style.color = "#0f0";
    }
    return result.output;
}

// Проверка решения
async function checkSolution(taskId) {
    const currentOutput = await runCode();
    if (!currentOutput && currentOutput !== "") return;
    
    const response = await fetch('/check_solution', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ task_id: taskId, output: currentOutput })
    });
    const result = await response.json();
    
    if (result.correct) {
        alert("Верно! Молодец!");
        // Сохраняем статус "РЕШЕНО"
        localStorage.setItem('task_status_' + taskId, 'solved');
        
        const nextBtn = document.getElementById('nextTaskBtn');
        if (nextBtn) nextBtn.style.display = "inline-block";
    } else {
        alert(`Неверно.\nВаш вывод:\n${currentOutput}\n\nОжидалось:\n${result.expected}`);
    }
}

// Раскраска карточек в меню
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.task-card');
    cards.forEach(card => {
        const id = card.getAttribute('data-id'); 
        if(id) {
            const status = localStorage.getItem('task_status_' + id);
            if (status === 'solved') {
                card.classList.add('solved');
            } else if (status === 'in-progress') {
                card.classList.add('in-progress');
            }
        }
    });
});

// Модальное окно (Табы)
function openModalTab(index) {
    const tabs = document.getElementsByClassName('modal-tab-content');
    for(let t of tabs) t.style.display = 'none';
    document.getElementById('modal-welcome').style.display = 'none';
    const target = document.getElementById('modal-tab-' + index);
    if(target) target.style.display = 'block';
}

const modal = document.getElementById("materialsModal");
const btn = document.getElementById("openMaterialsBtn");
const span = document.getElementsByClassName("close")[0];

if (btn) {
    btn.onclick = function() { modal.style.display = "block"; }
    span.onclick = function() { modal.style.display = "none"; }
    window.onclick = function(event) { if (event.target == modal) modal.style.display = "none"; }
}

// Горячие клавиши
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        if(editor) runCode();
    }
    // F1 для справки
    if (e.key === 'F1') {
        e.preventDefault();
        if(modal) modal.style.display = "block";
    }
});

// --- ЛОГИКА ОКНА ПОДСКАЗКИ ---
function showExplanation() {
    const text = document.getElementById('explanationStore').innerHTML;
    document.getElementById('explanationText').innerHTML = text;
    document.getElementById('explanationModal').style.display = "block";
}

function closeExplanation() {
    document.getElementById('explanationModal').style.display = "none";
}

// Закрытие по клику вне окна (для обоих модальных окон)
window.onclick = function(event) {
    const materialsModal = document.getElementById("materialsModal");
    const explanationModal = document.getElementById("explanationModal");
    
    if (event.target == materialsModal) {
        materialsModal.style.display = "none";
    }
    if (event.target == explanationModal) {
        explanationModal.style.display = "none";
    }
}

// --- ЛОГИКА СБРОСА ВСЕГО ПРОГРЕССА ---
function resetAllProgress() {
    if (confirm("Вы уверены? Это действие удалит все отметки 'решено' и 'в процессе', а также весь сохраненный код. Отменить будет невозможно.")) {
        // Очищаем всё хранилище
        localStorage.clear();
        
        // Перезагружаем страницу, чтобы пользователь увидел изменения
        alert("Прогресс сброшен.");
        location.reload();
    }
}