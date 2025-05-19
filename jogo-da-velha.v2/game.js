let board = ["", "", "", "", "", "", "", "", ""];
let currentPlayer = "X";
let gameActive = true;
let score = { X: 0, O: 0 };

const winningCombinations = [
[0, 1, 2], [3, 4, 5], [6, 7, 8], // Linhas
[0, 3, 6], [1, 4, 7], [2, 5, 8], // Colunas
[0, 4, 8], [2, 4, 6] // Diagonais
];

// Inicializar o jogo
function initGame() {
    document.querySelectorAll(".cell").forEach(cell => {
        cell.addEventListener("click", handleCellClick);
        cell.textContent = "";
    });
    document.getElementById("resetButton").addEventListener("click", resetGame);
    updateScore();
    updatePlayer();
    document.getElementById("gameMessage").textContent = "";
}

// Lidar com clique em uma célula
function handleCellClick(event) {
    const index = event.target.dataset.index;
    if (board[index] === "" && gameActive) {
        board[index] = currentPlayer;
        event.target.textContent = currentPlayer;
        event.target.style.pointerEvents = "none"; // Desativa cliques na célula
        if (checkWin()) {
        document.getElementById("gameMessage").textContent = `Jogador ${currentPlayer} venceu!`;
        score[currentPlayer]++;
        updateScore();
        gameActive = false;
        } else if (board.every(cell => cell !== "")) {
        document.getElementById("gameMessage").textContent = "Empate!";
        gameActive = false;
        } else {
        currentPlayer = currentPlayer === "X" ? "O" : "X";
        updatePlayer();
        }
    }
}

// Verificar vitória
function checkWin() {
    return winningCombinations.some(combo => {
        return combo.every(index => board[index] === currentPlayer);
    });
}

// Atualizar placar
function updateScore() {
    document.getElementById("scoreX").textContent = score.X;
    document.getElementById("scoreO").textContent = score.O;
}

// Atualizar jogador atual
function updatePlayer() {
    document.getElementById("currentPlayer").textContent = currentPlayer;
}

// Reiniciar jogo
function resetGame() {
    board = ["", "", "", "", "", "", "", "", ""];
    currentPlayer = "X";
    gameActive = true;
    document.querySelectorAll(".cell").forEach(cell => {
        cell.textContent = "";
        cell.style.pointerEvents = "auto";
    });
    document.getElementById("gameMessage").textContent = "";
    updatePlayer();
}

// Iniciar o jogo
initGame();