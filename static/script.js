// Получаем параметры
const currentTaskId = new URLSearchParams(window.location.search).get('id');
// Получаем класс (8 или 11) из скрытого инпута или URL, с дефолтом
const gradeElem = document.getElementById('currentGrade');
const currentGrade = gradeElem ? gradeElem.value : (new URLSearchParams(window.location.search).get('grade') || '8');

var editor;

// Инициализация редактора
if (document.getElementById('editor')) {
    editor = ace.edit("editor");
    editor.setTheme("ace/theme/monokai");
    editor.session.setMode("ace/mode/python");

    // --- ЛОГИКА ЗАГРУЗКИ (УНИКАЛЬНЫЙ КЛЮЧ ДЛЯ КЛАССА) ---
    if (currentTaskId) {
        // Ключ вида: task_code_8_1 или task_code_11_5
        const storageKey = `task_code_${currentGrade}_${currentTaskId}`;
        const savedCode = localStorage.getItem(storageKey);
        
        if (savedCode) {
            editor.setValue(savedCode);
            editor.clearSelection();
        }
    }

    // --- ЛОГИКА СОХРАНЕНИЯ ---
    editor.session.on('change', function(delta) {
        if (currentTaskId) {
            const code = editor.getValue();
            const storageCodeKey = `task_code_${currentGrade}_${currentTaskId}`;
            const storageStatusKey = `task_status_${currentGrade}_${currentTaskId}`;
            
            localStorage.setItem(storageCodeKey, code);

            const currentStatus = localStorage.getItem(storageStatusKey);
            if (currentStatus !== 'solved') {
                localStorage.setItem(storageStatusKey, 'in-progress');
            }
        }
    });
}

// Сброс кода
function resetCode() {
    if(confirm("Сбросить код к начальному состоянию?")) {
        const initialCode = document.getElementById('initialCodeStore').value;
        editor.setValue(initialCode);
        editor.clearSelection();
        if (currentTaskId) {
             const storageCodeKey = `task_code_${currentGrade}_${currentTaskId}`;
            localStorage.setItem(storageCodeKey, initialCode);
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
        outputBlock.style.color = "#ff4444";
    } else {
        outputBlock.innerText = result.output;
        outputBlock.style.color = "#0f0";
    }
    return result.output;
}

// Проверка решения
async function checkSolution(taskId) {
    const currentOutput = await runCode();
    if (currentOutput === undefined) return; // Если была ошибка сети
    
    const response = await fetch('/check_solution', {
        method: 'POST', headers: { 'Content-Type': 'application/json' },
        // ПЕРЕДАЕМ GRADE на сервер
        body: JSON.stringify({ task_id: taskId, output: currentOutput, grade: currentGrade })
    });
    const result = await response.json();
    
    if (result.correct) {
        alert("Верно! Молодец!");
        const storageStatusKey = `task_status_${currentGrade}_${taskId}`;
        localStorage.setItem(storageStatusKey, 'solved');
        
        const nextBtn = document.getElementById('nextTaskBtn');
        if (nextBtn) nextBtn.style.display = "inline-block";
    } else {
        alert(`Неверно.\nВаш вывод:\n${currentOutput}\n\nОжидалось:\n${result.expected}`);
    }
}

// Раскраска карточек (запуск при загрузке страницы списка)
document.addEventListener("DOMContentLoaded", function() {
    const cards = document.querySelectorAll('.task-card');
    cards.forEach(card => {
        const id = card.getAttribute('data-id'); 
        if(id) {
            // Учитываем GRADE при чтении статуса
            const storageStatusKey = `task_status_${currentGrade}_${id}`;
            const status = localStorage.getItem(storageStatusKey);
            if (status === 'solved') {
                card.classList.add('solved');
            } else if (status === 'in-progress') {
                card.classList.add('in-progress');
            }
        }
    });
});

// Модальные окна и табы
function openModalTab(index) {
    const tabs = document.getElementsByClassName('modal-tab-content');
    for(let t of tabs) t.style.display = 'none';
    const welcome = document.getElementById('modal-welcome');
    if(welcome) welcome.style.display = 'none';
    const target = document.getElementById('modal-tab-' + index);
    if(target) target.style.display = 'block';
}

const modal = document.getElementById("materialsModal");
const btn = document.getElementById("openMaterialsBtn");
const span = document.getElementsByClassName("close")[0];

if (btn) {
    btn.onclick = function() { modal.style.display = "block"; }
    span.onclick = function() { modal.style.display = "none"; }
}

// Клавиши
document.addEventListener('keydown', function(e) {
    if (e.ctrlKey && e.key === 'Enter') {
        if(editor) runCode();
    }
    if (e.key === 'F1') {
        e.preventDefault();
        if(modal) modal.style.display = "block";
    }
});

function showExplanation() {
    const store = document.getElementById('explanationStore');
    if(store) {
        document.getElementById('explanationText').innerHTML = store.innerHTML;
        document.getElementById('explanationModal').style.display = "block";
    }
}

function closeExplanation() {
    document.getElementById('explanationModal').style.display = "none";
}

window.onclick = function(event) {
    const materialsModal = document.getElementById("materialsModal");
    const explanationModal = document.getElementById("explanationModal");
    if (event.target == materialsModal) materialsModal.style.display = "none";
    if (event.target == explanationModal) explanationModal.style.display = "none";
}

// Сброс прогресса ТОЛЬКО для текущего класса
function resetAllProgress() {
    if (confirm(`Вы уверены? Это удалит прогресс только для ${currentGrade} класса.`)) {
        // Проходим по всем ключам LocalStorage
        const keysToRemove = [];
        for (let i = 0; i < localStorage.length; i++) {
            const key = localStorage.key(i);
            // Если ключ содержит маркер текущего класса (например "_8_")
            if (key.includes(`_${currentGrade}_`)) {
                keysToRemove.push(key);
            }
        }
        
        keysToRemove.forEach(k => localStorage.removeItem(k));
        
        alert("Прогресс сброшен.");
        location.reload();
    }
}