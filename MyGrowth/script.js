
// Estado Inicial
let habits = JSON.parse(localStorage.getItem('habits')) || [];
let projects = JSON.parse(localStorage.getItem('projects')) || [];
let points = parseInt(localStorage.getItem('points')) || 0;
let achievements = JSON.parse(localStorage.getItem('achievements')) || [];
let consecutiveDays = JSON.parse(localStorage.getItem('consecutiveDays')) || 0;
let currentDate = localStorage.getItem('currentDate') || new Date().toDateString();
let editingHabitId = null;
let editingProjectId = null;

// Validação de Pontos
if (points < 0 || points > (habits.length * 10 + projects.length * 20) * 1000) {
    points = 0;
    localStorage.setItem('points', '0');
}

// Lista de Conquistas Possíveis
const allAchievements = [
    { name: 'Primeiro Passo', icon: '<i class="fas fa-shoe-prints"></i>', requirement: 'Complete 1 execução de qualquer hábito', condition: habit => habit.progress >= 1 },
    { name: 'Meta Semanal', icon: '<i class="fas fa-check-circle"></i>', requirement: 'Complete 7 execuções semanais de um hábito', condition: habit => habit.progress >= habit.dailyExecutions * 7 },
    { name: '5 Dias Seguidos', icon: '<i class="fas fa-fire"></i>', requirement: 'Mantenha 5 dias consecutivos de progresso', condition: () => consecutiveDays >= 5 },
    { name: 'Mestre de Projetos', icon: '<i class="fas fa-trophy"></i>', requirement: 'Conclua 3 projetos', condition: () => projects.filter(p => p.tasks.every(t => t.completed)).length >= 3 }
];

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    resetWeeklyProgress();
    setupTabs();
    renderHabits();
    renderProjects();
    renderDailySummary();
    renderAchievementsSummary();
    renderAchievements();
    updateGamification();
    startTimeReminders();
    setupDragAndDrop();

    // Delegação de eventos para checkboxes
    document.getElementById('projectsList').addEventListener('change', (e) => {
        if (e.target.matches('.task-list input[type="checkbox"]')) {
            const projectId = parseInt(e.target.closest('.task-list').dataset.projectId);
            const taskIndex = parseInt(e.target.dataset.taskIndex);
            console.log(`Checkbox clicado: projectId=${projectId}, taskIndex=${taskIndex}, checked=${e.target.checked}`);
            updateTask(projectId, taskIndex, e.target.checked);
        }
    });

    // Delegação de eventos para botões de edição e exclusão
    document.getElementById('habitsList').addEventListener('click', (e) => {
        if (e.target.closest('.edit-button')) {
            const habitId = parseInt(e.target.closest('.habit-card').dataset.habitId);
            console.log(`Botão de edição de hábito clicado: habitId=${habitId}`);
            editHabit(habitId);
        } else if (e.target.closest('.delete-button')) {
            const habitId = parseInt(e.target.closest('.delete-button').dataset.habitId);
            console.log(`Botão de exclusão de hábito clicado: habitId=${habitId}`);
            deleteHabit(habitId);
        }
    });

    document.getElementById('projectsList').addEventListener('click', (e) => {
        if (e.target.closest('.edit-button')) {
            const projectId = parseInt(e.target.closest('.project-card').dataset.projectId);
            console.log(`Botão de edição de projeto clicado: projectId=${projectId}`);
            editProject(projectId);
        } else if (e.target.closest('.delete-button')) {
            const projectId = parseInt(e.target.closest('.delete-button').dataset.projectId);
            console.log(`Botão de exclusão de projeto clicado: projectId=${projectId}`);
            deleteProject(projectId);
        }
    });

    // Filtro de projetos
    document.getElementById('projectFilter').addEventListener('change', (e) => {
        const filter = e.target.value;
        console.log(`Filtro de projetos alterado: ${filter}`);
        renderProjectsWithFilter(filter);
    });
});

// Configuração das Abas
function setupTabs() {
    const tabs = document.querySelectorAll('.tab-link');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(tab => {
        tab.addEventListener('click', (e) => {
            e.preventDefault();
            tabs.forEach(t => t.classList.remove('active'));
            contents.forEach(c => c.classList.remove('active'));

            tab.classList.add('active');
            const tabId = tab.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
}

// Função para ativar aba explicitamente
function activateTab(tabId) {
    const tabs = document.querySelectorAll('.tab-link');
    const contents = document.querySelectorAll('.tab-content');

    tabs.forEach(t => t.classList.remove('active'));
    contents.forEach(c => c.classList.remove('active'));

    const targetTab = document.querySelector(`.tab-link[data-tab="${tabId}"]`);
    const targetContent = document.getElementById(tabId);

    if (targetTab && targetContent) {
        targetTab.classList.add('active');
        targetContent.classList.add('active');
    } else {
        console.error(`Erro ao ativar aba: ${tabId}`);
    }
}

// Configuração de Drag and Drop
function setupDragAndDrop() {
    const habitsList = document.getElementById('habitsList');
    habitsList.addEventListener('dragstart', (e) => {
        const card = e.target.closest('.habit-card');
        if (card) {
            e.dataTransfer.setData('text/plain', card.dataset.habitId);
            card.classList.add('dragging');
            console.log(`Iniciando arraste: habitId=${card.dataset.habitId}`);
        }
    });

    habitsList.addEventListener('dragend', (e) => {
        const card = e.target.closest('.habit-card');
        if (card) {
            card.classList.remove('dragging');
            console.log(`Fim do arraste: habitId=${card.dataset.habitId}`);
        }
    });

    habitsList.addEventListener('dragover', (e) => {
        e.preventDefault(); // Necessário para permitir drop
    });

    habitsList.addEventListener('drop', (e) => {
        e.preventDefault();
        const draggedId = parseInt(e.dataTransfer.getData('text/plain'));
        const targetCard = e.target.closest('.habit-card');
        if (!targetCard) return;

        const targetId = parseInt(targetCard.dataset.habitId);
        if (draggedId === targetId) return;

        const draggedIndex = habits.findIndex(h => h.id === draggedId);
        const targetIndex = habits.findIndex(h => h.id === targetId);

        if (draggedIndex === -1 || targetIndex === -1) {
            console.error(`Erro ao reordenar: draggedId=${draggedId}, targetId=${targetId}`);
            return;
        }

        const [draggedHabit] = habits.splice(draggedIndex, 1);
        habits.splice(targetIndex, 0, draggedHabit);

        saveData();
        renderHabits();
        console.log(`Hábito reordenado: id=${draggedId} movido para posição=${targetIndex}`);
    });
}

// Formulário de Hábitos
document.getElementById('habitForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
    const id = parseInt(document.getElementById('editingHabitId').value) || null;
    const name = document.getElementById('habitName').value.trim();
    const frequency = document.getElementById('habitFrequency').value;
    const dailyExecutions = parseInt(document.getElementById('dailyExecutions').value);
    const times = document.getElementById('habitTimes').value.trim();

    let isValid = true;
    document.getElementById('nameError').style.display = 'none';
    document.getElementById('executionsError').style.display = 'none';
    document.getElementById('timesError').style.display = 'none';

    if (!name || name.length > 50) {
        document.getElementById('nameError').style.display = 'block';
        isValid = false;
    }
    if (isNaN(dailyExecutions) || dailyExecutions < 1 || dailyExecutions > 5) {
        document.getElementById('executionsError').style.display = 'block';
        isValid = false;
    }
    let timesArray = [];
    if (times) {
        timesArray = times.split(',').map(t => t.trim());
        const timeRegex = /^([0-1]?[0-9]|2[0-3]):[0-5][0-9]$/;
        if (timesArray.length !== dailyExecutions || !timesArray.every(t => timeRegex.test(t))) {
            document.getElementById('timesError').style.display = 'block';
            isValid = false;
        }
    }

    if (!isValid) return;

    if (id !== null) {
        // Modo de edição
        console.log(`Editando hábito: id=${id}, nome=${name}`);
        const habit = habits.find(h => h.id === id);
        if (habit) {
            habit.name = name;
            habit.frequency = frequency;
            habit.dailyExecutions = dailyExecutions;
            habit.times = timesArray;
            // Resetar progresso se execuções mudarem
            if (habit.dailyExecutions !== dailyExecutions) {
                habit.dailyCompletions = [];
                habit.progress = 0;
                habit.completionDates = [];
            }
            showNotification(`Hábito "${name}" atualizado com sucesso!`);
        } else {
            console.error(`Hábito não encontrado para edição: id=${id}`);
            showNotification('Erro: Hábito não encontrado.');
            return;
        }
        editingHabitId = null;
        document.getElementById('editingHabitId').value = '';
    } else {
        // Modo de adição
        console.log(`Adicionando novo hábito: nome=${name}`);
        const newHabit = {
            id: Date.now(),
            name,
            frequency,
            dailyExecutions,
            times: timesArray,
            progress: 0,
            dailyCompletions: [],
            completionDates: []
        };
        habits.push(newHabit);
        showNotification(`Hábito "${name}" adicionado com sucesso!`);
    }

    saveData();
    renderHabits();
    renderDailySummary();
    resetHabitForm();
    activateTab('home');
});

// Formulário de Projetos
document.getElementById('projectForm').addEventListener('submit', (e) => {
    e.preventDefault();

    const id = parseInt(document.getElementById('editingProjectId').value) || null;
    const name = document.getElementById('projectName').value.trim();
    const description = document.getElementById('projectDescription').value.trim();
    const tasks = document.getElementById('projectTasks').value.trim();

    let isValid = true;
    document.getElementById('projectNameError').style.display = 'none';
    document.getElementById('tasksError').style.display = 'none';

    if (!name || name.length > 50) {
        document.getElementById('projectNameError').style.display = 'block';
        isValid = false;
    }
    const tasksArray = tasks.split(',').map(t => t.trim()).filter(t => t);
    if (tasksArray.length === 0) {
        document.getElementById('tasksError').style.display = 'block';
        isValid = false;
    }

    if (!isValid) return;

    if (id !== null) {
        // Modo de edição
        console.log(`Editando projeto: id=${id}, nome=${name}`);
        const project = projects.find(p => p.id === id);
        if (project) {
            // Preservar estado de tarefas concluídas, se possível
            const newTasks = tasksArray.map((task, index) => ({
                name: task,
                completed: project.tasks[index]?.completed || false
            }));
            project.name = name;
            project.description = description;
            project.tasks = newTasks;
            showNotification(`Projeto "${name}" atualizado com sucesso!`);
        } else {
            console.error(`Projeto não encontrado para edição: id=${id}`);
            showNotification('Erro: Projeto não encontrado.');
            return;
        }
        editingProjectId = null;
        document.getElementById('editingProjectId').value = '';
    } else {
        // Modo de adição
        console.log(`Adicionando novo projeto: nome=${name}`);
        const newProject = {
            id: Date.now(),
            name,
            description,
            tasks: tasksArray.map(task => ({ name: task, completed: false }))
        };
        projects.push(newProject);
        showNotification(`Projeto "${name}" adicionado com sucesso!`);
    }

    saveData();
    renderProjects();
    resetProjectForm();
    activateTab('projects');
});

// Renderização
function renderHabits() {
    const container = document.getElementById('habitsList');
    container.innerHTML = '';

    const today = new Date().toDateString();
    if (currentDate !== today) {
        habits.forEach(habit => {
            habit.dailyCompletions = [];
        });
        currentDate = today;
        saveData();
    }

    habits.forEach(habit => {
        const todayCompletions = habit.dailyCompletions;
        const maxProgress = habit.dailyExecutions * 7;
        const progressPercentage = Math.min((habit.progress / maxProgress) * 100, 100);
        const card = document.createElement('div');
        card.className = 'habit-card';
        card.dataset.habitId = habit.id;
        card.setAttribute('draggable', 'true');
        card.innerHTML = `
            <h3>${habit.name}</h3>
            <p>Frequência: ${habit.frequency === 'diario' ? 'Diário' : 'Semanal'}</p>
            <p>Execuções hoje: ${todayCompletions.length}/${habit.dailyExecutions}</p>
            <p>Progresso semanal: ${habit.progress}/${maxProgress}</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progressPercentage}%"></div>
            </div>
            <div class="execution-list">
                ${Array.from({ length: habit.dailyExecutions }, (_, i) => {
                    const time = habit.times[i] || `Execução ${i + 1}`;
                    const isChecked = todayCompletions.includes(time);
                    const isDisabled = todayCompletions.length >= habit.dailyExecutions && !isChecked;
                    return `
                        <div class="execution-item">
                            <label>
                                <input type="checkbox" ${isChecked ? 'checked' : ''} 
                                       ${isDisabled ? 'disabled' : ''}
                                       onchange="updateProgress(${habit.id}, this.checked, '${time}')">
                                ${time}
                            </label>
                        </div>
                    `;
                }).join('')}
            </div>
            <div class="button-group">
                <button class="edit-button" aria-label="Editar hábito ${habit.name}">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="delete-button" data-habit-id="${habit.id}" aria-label="Excluir hábito ${habit.name}">
                    <i class="fas fa-trash"></i> Excluir
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderProjects(projs = projects) {
    console.log('Renderizando projetos:', projs);
    const container = document.getElementById('projectsList');
    container.innerHTML = '';

    projs.forEach(project => {
        const completedTasks = project.tasks.filter(t => t.completed).length;
        const totalTasks = project.tasks.length;
        const progressPercentage = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
        const card = document.createElement('div');
        card.className = 'project-card';
        card.dataset.projectId = project.id;
        card.innerHTML = `
            <h3>${project.name}</h3>
            ${project.description ? `<p>${project.description}</p>` : ''}
            <p>Tarefas concluídas: ${completedTasks}/${totalTasks}</p>
            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progressPercentage}%"></div>
            </div>
            <div class="task-list" data-project-id="${project.id}">
                ${project.tasks.map((task, index) => `
                    <div class="task-item">
                        <label>
                            <input type="checkbox" data-task-index="${index}" ${task.completed ? 'checked' : ''}>
                            ${task.name}
                        </label>
                    </div>
                `).join('')}
            </div>
            <div class="button-group">
                <button class="edit-button" aria-label="Editar projeto ${project.name}">
                    <i class="fas fa-edit"></i> Editar
                </button>
                <button class="delete-button" data-project-id="${project.id}" aria-label="Excluir projeto ${project.name}">
                    <i class="fas fa-trash"></i> Excluir
                </button>
            </div>
        `;
        container.appendChild(card);
    });
}

function renderProjectsWithFilter(filter) {
    let filteredProjects = projects;
    if (filter === 'completed') {
        filteredProjects = projects.filter(p => p.tasks.every(t => t.completed));
    } else if (filter === 'pending') {
        filteredProjects = projects.filter(p => !p.tasks.every(t => t.completed));
    }
    renderProjects(filteredProjects);
    console.log(`Projetos filtrados: ${filter}, total=${filteredProjects.length}`);
}

function renderDailySummary() {
    const container = document.getElementById('dailySummary');
    const pendingHabits = habits.map(h => {
        const todayCompletions = h.dailyCompletions;
        return todayCompletions.length < h.dailyExecutions ? 
            `${h.name}: ${todayCompletions.length}/${h.dailyExecutions} concluído` : null;
    }).filter(h => h);
    container.innerHTML = pendingHabits.length === 0 
        ? '<p>Todos os hábitos de hoje foram concluídos! 🎉</p>'
        : `<p>Hábitos pendentes hoje:</p><ul>${pendingHabits.map(h => `<li>${h}</li>`).join('')}</ul>`;
}

function renderAchievementsSummary() {
    const container = document.getElementById('achievementsSummary');
    container.innerHTML = '<h3>Conquistas Desbloqueadas</h3>';
    if (achievements.length === 0) {
        container.innerHTML += '<p>Nenhuma conquista desbloqueada ainda.</p>';
        return;
    }
    const grid = document.createElement('div');
    grid.className = 'achievements-grid';
    achievements.forEach(a => {
        const achievement = allAchievements.find(ach => ach.name === a);
        if (achievement) {
            grid.innerHTML += `<div class="badge">${achievement.icon} ${a}</div>`;
        }
    });
    container.appendChild(grid);
}

function renderAchievements() {
    const container = document.getElementById('achievementsList');
    container.innerHTML = '';
    allAchievements.forEach(a => {
        const isUnlocked = achievements.includes(a.name);
        const badge = document.createElement('div');
        badge.className = `badge ${isUnlocked ? '' : 'locked'}`;
        badge.innerHTML = isUnlocked 
            ? `${a.icon} ${a.name}`
            : `${a.icon} ${a.name} <small>(${a.requirement})</small>`;
        container.appendChild(badge);
    });
}

// Funções de Exclusão
function deleteHabit(habitId) {
    const habit = habits.find(h => h.id === habitId);
    if (!habit) {
        console.error(`Hábito não encontrado para exclusão: id=${habitId}`);
        showNotification('Erro: Hábito não encontrado.');
        return;
    }
    if (confirm(`Tem certeza que deseja excluir o hábito "${habit.name}"?`)) {
        habits = habits.filter(h => h.id !== habitId);
        saveData();
        renderHabits();
        renderDailySummary();
        showNotification(`Hábito "${habit.name}" excluído com sucesso!`);
        console.log(`Hábito excluído: id=${habitId}, nome=${habit.name}`);
    }
}

function deleteProject(projectId) {
    const project = projects.find(p => p.id === projectId);
    if (!project) {
        console.error(`Projeto não encontrado para exclusão: id=${projectId}`);
        showNotification('Erro: Projeto não encontrado.');
        return;
    }
    if (confirm(`Tem certeza que deseja excluir o projeto "${project.name}"?`)) {
        projects = projects.filter(p => p.id !== projectId);
        saveData();
        renderProjects();
        showNotification(`Projeto "${project.name}" excluído com sucesso!`);
        console.log(`Projeto excluído: id=${projectId}, nome=${project.name}`);
    }
}

// Edição de Hábitos e Projetos
function editHabit(id) {
    console.log(`Iniciando edição de hábito: id=${id}`);
    const habit = habits.find(h => h.id === id);
    if (!habit) {
        console.error(`Hábito não encontrado: id=${id}`);
        return;
    }

    editingHabitId = id;
    document.getElementById('editingHabitId').value = id;
    document.getElementById('habitFormTitle').textContent = 'Editar Hábito';
    document.getElementById('habitSubmitButton').textContent = 'Salvar Alterações';
    document.getElementById('habitName').value = habit.name;
    document.getElementById('habitFrequency').value = habit.frequency;
    document.getElementById('dailyExecutions').value = habit.dailyExecutions;
    document.getElementById('habitTimes').value = habit.times.join(', ');
    
    activateTab('habits');
}

function editProject(id) {
    console.log(`Iniciando edição de projeto: id=${id}`);
    const project = projects.find(p => p.id === id);
    if (!project) {
        console.error(`Projeto não encontrado: id=${id}`);
        return;
    }

    editingProjectId = id;
    document.getElementById('editingProjectId').value = id;
    document.getElementById('projectFormTitle').textContent = 'Editar Projeto';
    document.getElementById('projectSubmitButton').textContent = 'Salvar Alterações';
    document.getElementById('projectName').value = project.name;
    document.getElementById('projectDescription').value = project.description;
    document.getElementById('projectTasks').value = project.tasks.map(t => t.name).join(', ');
    
    activateTab('projects');
}

function resetHabitForm() {
    document.getElementById('habitFormTitle').textContent = 'Adicionar Hábito';
    document.getElementById('habitSubmitButton').textContent = 'Adicionar Hábito';
    document.getElementById('habitForm').reset();
    document.getElementById('editingHabitId').value = '';
    document.getElementById('nameError').style.display = 'none';
    document.getElementById('executionsError').style.display = 'none';
    document.getElementById('timesError').style.display = 'none';
}

function resetProjectForm() {
    document.getElementById('projectFormTitle').textContent = 'Adicionar Projeto';
    document.getElementById('projectSubmitButton').textContent = 'Adicionar Projeto';
    document.getElementById('projectForm').reset();
    document.getElementById('editingProjectId').value = '';
    document.getElementById('projectNameError').style.display = 'none';
    document.getElementById('tasksError').style.display = 'none';
}

// Lógica de Progresso
function updateProgress(id, completed, time) {
    console.log(`updateProgress: habitId=${id}, completed=${completed}, time=${time}`);
    const habit = habits.find(h => h.id === id);
    if (!habit) {
        console.error('Hábito não encontrado:', id);
        return;
    }

    const todayCompletions = habit.dailyCompletions;
    const maxProgress = habit.dailyExecutions * 7;

    if (completed && todayCompletions.length < habit.dailyExecutions && !todayCompletions.includes(time)) {
        habit.dailyCompletions.push(time);
        habit.progress = Math.min(habit.progress + 1, maxProgress);
        points += 10;
        habit.completionDates.push(new Date().toISOString().split('T')[0]);
        checkConsecutiveDays(habit);
        checkAchievements(habit);
    } else if (!completed && todayCompletions.includes(time)) {
        habit.dailyCompletions = habit.dailyCompletions.filter(c => c !== time);
        habit.progress = Math.max(habit.progress - 1, 0);
        points = Math.max(points - 10, 0);
        habit.completionDates.pop();
    } else {
        return;
    }

    saveData();
    renderHabits();
    renderDailySummary();
    renderAchievementsSummary();
    renderAchievements();
    updateGamification();
}

function updateTask(projectId, taskIndex, completed) {
    console.log(`updateTask: projectId=${projectId}, taskIndex=${taskIndex}, completed=${completed}`);
    const project = projects.find(p => p.id === projectId);
    if (!project) {
        console.error('Projeto não encontrado:', projectId);
        return;
    }
    if (taskIndex < 0 || taskIndex >= project.tasks.length) {
        console.error('Índice de tarefa inválido:', taskIndex);
        return;
    }

    const wasCompleted = project.tasks[taskIndex].completed;
    project.tasks[taskIndex].completed = completed;
    console.log('Tarefa atualizada:', project.tasks[taskIndex]);

    if (completed && !wasCompleted) {
        points += 5;
        console.log('Pontos adicionados: +5, total=', points);
        if (project.tasks.every(t => t.completed)) {
            points += 20;
            console.log('Projeto concluído, pontos adicionados: +20, total=', points);
            showNotification(`Projeto "${project.name}" concluído! 🎉`);
        }
    } else if (!completed && wasCompleted) {
        points = Math.max(points - 5, 0);
        console.log('Pontos removidos: -5, total=', points);
    }

    console.log('Estado dos projetos antes de salvar:', projects);
    saveData();
    renderProjects();
    renderAchievementsSummary();
    renderAchievements();
    updateGamification();
    console.log('Projetos após renderização:', projects);
}

// Gamificação
function checkConsecutiveDays(habit) {
    const dates = [...new Set(habit.completionDates)].sort();
    let currentStreak = 1;
    for (let i = 1; i < dates.length; i++) {
        const prevDate = new Date(dates[i - 1]);
        const currDate = new Date(dates[i]);
        const diffDays = (currDate - prevDate) / (1000 * 60 * 60 * 24);
        if (diffDays === 1) {
            currentStreak++;
        } else if (diffDays > 1) {
            currentStreak = 1;
        }
    }
    consecutiveDays = Math.max(consecutiveDays, currentStreak);
    saveData();
}

function updateGamification() {
    const level = Math.floor(points / 100);
    const levelNames = ['Iniciante', 'Explorador', 'Mestre'];
    document.getElementById('points').textContent = points;
    document.getElementById('level').textContent = levelNames[Math.min(level, levelNames.length - 1)];
}

function checkAchievements(habit) {
    const newAchievements = [];

    allAchievements.forEach(a => {
        if (!achievements.includes(a.name) && a.condition(habit)) {
            newAchievements.push(a.name);
            showNotification(`Conquista desbloqueada: ${a.name}! 🎉`);
        }
    });

    if (newAchievements.length > 0) {
        achievements.push(...newAchievements);
        saveData();
        renderAchievementsSummary();
        renderAchievements();
    }
}

// Notificações
function showNotification(message) {
    console.log('Notificação exibida:', message);
    const notification = document.createElement('div');
    notification.className = 'notification';
    notification.textContent = message;
    document.body.appendChild(notification);
    setTimeout(() => notification.classList.add('show'), 100);
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

// Lembretes
function startTimeReminders() {
    setInterval(() => {
        const now = new Date();
        const currentTime = `${now.getHours().toString().padStart(2, '0')}:${now.getMinutes().toString().padStart(2, '0')}`;
        habits.forEach(habit => {
            habit.times.forEach(time => {
                const [hours, minutes] = time.split(':').map(Number);
                const timeDate = new Date(now);
                timeDate.setHours(hours, minutes, 0, 0);
                const diffMs = timeDate - now;
                if (diffMs > 0 && diffMs <= 5 * 60 * 1000) {
                    showNotification(`Lembrete: ${habit.name} às ${time}!`);
                }
            });
        });
    }, 60 * 1000);
}

// Reset Semanal
function resetWeeklyProgress() {
    const today = new Date();
    const lastReset = localStorage.getItem('lastReset')
        ? new Date(localStorage.getItem('lastReset'))
        : null;

    if (!lastReset || (today.getDay() === 0 && today.toDateString() !== lastReset.toDateString())) {
        habits.forEach(habit => {
            habit.progress = 0;
            habit.dailyCompletions = [];
            habit.completionDates = [];
        });
        localStorage.setItem('lastReset', today.toISOString());
        currentDate = today.toDateString();
        saveData();
    }
}

function isToday(dateString) {
    if (!dateString) return false;
    const date = new Date(dateString);
    const today = new Date();
    return date.toDateString() === today.toDateString();
}

// Persistência
function saveData() {
    console.log('Salvando dados no localStorage:', { habits, projects, points, achievements, consecutiveDays, currentDate });
    localStorage.setItem('habits', JSON.stringify(habits));
    localStorage.setItem('projects', JSON.stringify(projects));
    localStorage.setItem('points', points.toString());
    localStorage.setItem('achievements', JSON.stringify(achievements));
    localStorage.setItem('consecutiveDays', consecutiveDays.toString());
    localStorage.setItem('currentDate', currentDate);
}

// Reset Total
document.getElementById('resetButton').addEventListener('click', () => {
    if (confirm('Tem certeza que deseja reiniciar tudo? Todos os hábitos, projetos, pontos e conquistas serão perdidos.')) {
        localStorage.clear();
        habits = [];
        projects = [];
        points = 0;
        achievements = [];
        consecutiveDays = 0;
        currentDate = new Date().toDateString();
        editingHabitId = null;
        editingProjectId = null;
        saveData();
        renderHabits();
        renderProjects();
        renderDailySummary();
        renderAchievementsSummary();
        renderAchievements();
        updateGamification();
        showNotification('Programa reiniciado com sucesso!');
    }
});

document.querySelector('.nav-toggle').addEventListener('click', () => {
    document.querySelector('.nav-tabs').classList.toggle('active');
});