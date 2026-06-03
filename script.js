document.addEventListener('DOMContentLoaded', () => {
    // --- LIVE TIME & DATE ---
    const timeEl = document.getElementById('live-time');
    const dateEl = document.getElementById('live-date');

    function updateTime() {
        const now = new Date();
        
        // Time
        const timeOptions = { hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false };
        timeEl.textContent = now.toLocaleTimeString('fr-FR', timeOptions);

        // Date
        const dateOptions = { weekday: 'long', day: 'numeric', month: 'long', year: 'numeric' };
        let dateString = now.toLocaleDateString('fr-FR', dateOptions);
        // Capitalize first letter of day
        dateString = dateString.charAt(0).toUpperCase() + dateString.slice(1);
        dateEl.textContent = dateString;
    }
    
    updateTime();
    setInterval(updateTime, 1000);

    // --- MOTIVATIONAL QUOTES ---
    const quotes = [
        { text: "La meilleure façon de prédire l'avenir, c'est de le créer.", author: "Peter Drucker" },
        { text: "Le code est comme l'humour. Quand il faut l'expliquer, c'est mauvais.", author: "Cory House" },
        { text: "Faites-le simple, mais significatif.", author: "Don Norman" },
        { text: "Chaque grand développeur a commencé par résoudre de petits problèmes.", author: "Anonyme" },
        { text: "La simplicité est la sophistication suprême.", author: "Léonard de Vinci" },
        { text: "Un bon design est un design invisible.", author: "Dieter Rams" }
    ];

    const quoteText = document.getElementById('quote-text');
    const quoteAuthor = document.getElementById('quote-author');

    function rotateQuote() {
        const randomIndex = Math.floor(Math.random() * quotes.length);
        const selected = quotes[randomIndex];
        
        // Fade out
        quoteText.style.opacity = 0;
        quoteAuthor.style.opacity = 0;
        
        setTimeout(() => {
            quoteText.textContent = `« ${selected.text} »`;
            quoteAuthor.textContent = `- ${selected.author}`;
            
            // Fade in
            quoteText.style.opacity = 1;
            quoteAuthor.style.opacity = 1;
        }, 300);
    }

    // Add transitions for quotes
    quoteText.style.transition = 'opacity 0.3s ease';
    quoteAuthor.style.transition = 'opacity 0.3s ease';
    
    // Rotate quote every 15 seconds
    setInterval(rotateQuote, 15000);

    // --- TODO LIST WIDGET ---
    const todoForm = document.getElementById('todo-form');
    const todoInput = document.getElementById('todo-input');
    const todoList = document.getElementById('todo-list');
    const todoCount = document.getElementById('todo-count');

    // Default tasks if none exist
    let tasks = JSON.parse(localStorage.getItem('dashboard-tasks')) || [
        { id: 1, text: "Configurer le dépôt Git local", completed: true },
        { id: 2, text: "Créer le fichier .gitignore", completed: false },
        { id: 3, text: "Publier le projet sur GitHub", completed: false },
        { id: 4, text: "Déployer sur Netlify", completed: false }
    ];

    function saveTasks() {
        localStorage.setItem('dashboard-tasks', JSON.stringify(tasks));
    }

    function renderTasks() {
        todoList.innerHTML = '';
        let completedCount = 0;

        tasks.forEach(task => {
            if (task.completed) completedCount++;

            const li = document.createElement('li');
            li.className = `todo-item ${task.completed ? 'completed' : ''}`;
            li.dataset.id = task.id;

            li.innerHTML = `
                <div class="todo-item-content">
                    <input type="checkbox" ${task.completed ? 'checked' : ''}>
                    <span>${escapeHTML(task.text)}</span>
                </div>
                <button class="delete-btn" aria-label="Supprimer"><i class="fa-regular fa-trash-can"></i></button>
            `;

            // Event Listeners
            const checkbox = li.querySelector('input[type="checkbox"]');
            checkbox.addEventListener('change', () => toggleTask(task.id));

            const deleteBtn = li.querySelector('.delete-btn');
            deleteBtn.addEventListener('click', () => deleteTask(task.id));

            todoList.appendChild(li);
        });

        todoCount.textContent = `${completedCount} sur ${tasks.length} terminées`;
    }

    function addTask(text) {
        const newTask = {
            id: Date.now(),
            text: text,
            completed: false
        };
        tasks.push(newTask);
        saveTasks();
        renderTasks();
    }

    function toggleTask(id) {
        tasks = tasks.map(task => {
            if (task.id === id) {
                return { ...task, completed: !task.completed };
            }
            return task;
        });
        saveTasks();
        renderTasks();
    }

    function deleteTask(id) {
        tasks = tasks.filter(task => task.id !== id);
        saveTasks();
        renderTasks();
    }

    todoForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const text = todoInput.value.trim();
        if (text) {
            addTask(text);
            todoInput.value = '';
        }
    });

    function escapeHTML(str) {
        return str.replace(/[&<>'"]/g, 
            tag => ({
                '&': '&amp;',
                '<': '&lt;',
                '>': '&gt;',
                "'": '&#39;',
                '"': '&quot;'
            }[tag] || tag)
        );
    }

    // --- NOTES WIDGET ---
    const notesTextarea = document.getElementById('notes-textarea');
    const notesStatus = document.getElementById('notes-status');

    // Load notes
    notesTextarea.value = localStorage.getItem('dashboard-notes') || "Voici vos notes rapides. Modifiez-les et elles se sauvegarderont automatiquement !";

    let saveTimeout;
    notesTextarea.addEventListener('input', () => {
        notesStatus.textContent = 'Enregistrement...';
        notesStatus.classList.add('saving');
        
        clearTimeout(saveTimeout);
        saveTimeout = setTimeout(() => {
            localStorage.setItem('dashboard-notes', notesTextarea.value);
            notesStatus.textContent = 'Enregistré';
            notesStatus.classList.remove('saving');
        }, 1000);
    });

    // Initial render
    renderTasks();
});
