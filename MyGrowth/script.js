
// Estado Inicial
let habits = JSON.parse(localStorage.getItem('habits')) || [];
let points = parseInt(localStorage.getItem('points')) || 0;
let achievements = JSON.parse(localStorage.getItem('achievements')) || [];
let consecutiveDays = JSON.parse(localStorage.getItem('consecutiveDays')) || 0;
let currentDate = localStorage.getItem('currentDate') || new Date().toDateString();

// Validação de Pontos
if (points < 0 || points > habits.length * 10 * 1000) {
    points = 0;
    localStorage.setItem('points', '0');
}

// Lista de Conquistas Possíveis
const allAchievements = [
    { name: 'Primeiro Passo', icon: '<i class="fas fa-shoe-prints"></i>', requirement: 'Complete 1 execução de qualquer hábito', condition: habit => habit.progress >= 1 },
    { name: 'Meta Semanal', icon: '<i class="fas fa-check-circle"></i>', requirement: 'Complete 7 execuções semanais de um hábito', condition: habit => habit.progress >= habit.dailyExecutions * 7 },
    { name: '5 Dias Seguidos', icon: '<i class="fas fa-fire"></i>', requirement: 'Mantenha 5 dias consecutivos de progresso', condition: () => consecutiveDays >= 5 }
];

// Inicialização
document.addEventListener('DOMContentLoaded', () => {
    resetWeeklyProgress();
    setupTabs();
    renderHabits();
    renderDailySummary();
    renderAchievementsSummary();
    renderAchievements();
    updateGamification();
    startTimeReminders();
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

// Formulário de Hábitos
document.getElementById('habitForm').addEventListener('submit', (e) => {
    e.preventDefault();
    
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
    saveData();
    renderHabits();
    renderDailySummary();
    e.target.reset();
    // Volta para a tela de Início
    document.querySelector('.tab-link[data-tab="home"]').click();
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
        `;
        container.appendChild(card);
    });
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

// Lógica de Progresso
window.updateProgress = (id, completed, time) => {
    const habit = habits.find(h => h.id === id);
    if (!habit) return;

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
};

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
    localStorage.setItem('habits', JSON.stringify(habits));
    localStorage.setItem('points', points.toString());
    localStorage.setItem('achievements', JSON.stringify(achievements));
    localStorage.setItem('consecutiveDays', consecutiveDays.toString());
    localStorage.setItem('currentDate', currentDate);
}

// Reset Total
document.getElementById('resetButton').addEventListener('click', () => {
    if (confirm('Tem certeza que deseja reiniciar tudo? Todos os hábitos, pontos e conquistas serão perdidos.')) {
        localStorage.clear();
        habits = [];
        points = 0;
        achievements = [];
        consecutiveDays = 0;
        currentDate = new Date().toDateString();
        saveData();
        renderHabits();
        renderDailySummary();
        renderAchievementsSummary();
        renderAchievements();
        updateGamification();
        showNotification('Programa reiniciado com sucesso!');
    }
});
