document.getElementById('habit-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const name = document.getElementById('habit-name').value;
    const frequency = document.getElementById('habit-frequency').value;
    const goal = document.getElementById('habit-goal').value;

    const habits = JSON.parse(localStorage.getItem('habits')) || [];
    habits.push({ name, frequency, goal, progress: 0, completedToday: false });
    localStorage.setItem('habits', JSON.stringify(habits));

    displayHabits();
    this.reset();
});

function displayHabits() {
    const habits = JSON.parse(localStorage.getItem('habits')) || [];
    const habitList = document.getElementById('habit-list');
    habitList.innerHTML = '';

    habits.forEach((habit, index) => {
        const card = document.createElement('div');
        card.className = 'habit-card';
        card.innerHTML = `
            <span>${habit.name} (${habit.progress}/${habit.goal})</span>
            <input type="checkbox" ${habit.completedToday ? 'checked' : ''} onchange="toggleHabit(${index})">
            <div class="progress-bar" style="width: ${(habit.progress/habit.goal)*100}%"></div>
        `;
        habitList.appendChild(card);
    });
}

function toggleHabit(index) {
    const habits = JSON.parse(localStorage.getItem('habits'));
    habits[index].completedToday = !habits[index].completedToday;
    if (habits[index].completedToday) {
        habits[index].progress = Math.min(habits[index].progress + 1, habits[index].goal);
        updatePoints(10); // Adiciona 10 pontos
    }
    localStorage.setItem('habits', JSON.stringify(habits));
    displayHabits();
    checkAchievements();
}

function updatePoints(points) {
    let totalPoints = parseInt(localStorage.getItem('points')) || 0;
    totalPoints += points;
    localStorage.setItem('points', totalPoints);
    document.getElementById('points').textContent = `Pontos: ${totalPoints}`;
}

function checkAchievements() {
    const achievements = JSON.parse(localStorage.getItem('achievements')) || [];
    const habits = JSON.parse(localStorage.getItem('habits')) || [];
    if (habits.some(h => h.progress >= 5) && !achievements.includes('5-dias')) {
        achievements.push('5-dias');
        localStorage.setItem('achievements', JSON.stringify(achievements));
        alert('Conquista desbloqueada: 5 Dias Seguidos!');
    }
    displayAchievements();
}

function displayAchievements() {
    const achievements = JSON.parse(localStorage.getItem('achievements')) || [];
    const achievementList = document.getElementById('achievement-list');
    achievementList.innerHTML = achievements.map(a => `<div>${a}</div>`).join('');
}