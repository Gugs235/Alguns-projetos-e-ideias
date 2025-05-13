let pet = {
  name: "",
  hunger: 100,
  happiness: 100,
  cleanliness: 100,
  energy: 100,
  coins: 0,
  level: 1,
  experience: 0,
  inventory: []
};

const shopItems = [
  { id: 1, name: "Fancy Hat", price: 50, type: "cosmetic" },
  { id: 2, name: "Tasty Treat", price: 20, type: "food" },
  { id: 3, name: "Shiny Toy", price: 30, type: "toy" }
];

// Game State
let isPlayingMiniGame = false;
let ball = { x: 150, y: 100, radius: 10, dx: 5, dy: 5 };
let score = 0;
const canvas = document.getElementById("miniGameCanvas");
const ctx = canvas.getContext("2d");

// Initialize Game
function initGame() {
  const saved = localStorage.getItem("pet");
  if (saved) {
    pet = JSON.parse(saved);
    updateStats();
    updatePetSprite();
    document.getElementById("gameContainer").classList.remove("hidden");
  } else {
    document.getElementById("nameModal").style.display = "flex";
  }
}

// Start Game
function startGame() {
  const nameInput = document.getElementById("petNameInput").value.trim();
  if (nameInput) {
    pet.name = nameInput;
    document.getElementById("nameModal").style.display = "none";
    document.getElementById("gameContainer").classList.remove("hidden");
    updateStats();
    savePet();
  } else {
    alert("Please enter a name for your pet!");
  }
}

// Update Stats UI
function updateStats() {
  document.getElementById("hungerFill").style.width = pet.hunger + "%";
  document.getElementById("happinessFill").style.width = pet.happiness + "%";
  document.getElementById("cleanlinessFill").style.width = pet.cleanliness + "%";
  document.getElementById("energyFill").style.width = pet.energy + "%";
  document.getElementById("coins").textContent = pet.coins;
  document.getElementById("level").textContent = pet.level;
  document.getElementById("petName").textContent = pet.name || "My Pet";
  updatePetSprite();
}

// Update Pet Sprite Based on State
function updatePetSprite() {
  const sprite = document.getElementById("petSprite");
  if (pet.hunger < 30) {
    sprite.className = "my-4 hungry";
  } else if (pet.happiness < 30) {
    sprite.className = "my-4 sad";
  } else {
    sprite.className = "my-4 happy";
  }
}

// Core Actions
function feed() {
  if (pet.coins >= 5) {
    pet.hunger = Math.min(pet.hunger + 20, 100);
    pet.coins -= 5;
    addExperience(10);
    updateStats();
    savePet();
  } else {
    alert("Not enough coins!");
  }
}

function clean() {
  pet.cleanliness = Math.min(pet.cleanliness + 20, 100);
  addExperience(10);
  updateStats();
  savePet();
}

function rest() {
  pet.energy = Math.min(pet.energy + 20, 100);
  pet.happiness = Math.max(pet.happiness - 5, 0);
  addExperience(10);
  updateStats();
  savePet();
}

// Experience and Leveling
function addExperience(points) {
  pet.experience += points;
  if (pet.experience >= pet.level * 100) {
    pet.level += 1;
    pet.experience = 0;
    pet.coins += 50; // Bonus coins for leveling up
    alert(`Level Up! Your pet is now level ${pet.level}!`);
  }
  updateStats();
}

// Save and Load
function savePet() {
  localStorage.setItem("pet", JSON.stringify(pet));
}

// Decrease Stats Over Time
function decreaseStats() {
  pet.hunger = Math.max(pet.hunger - 2, 0);
  pet.happiness = Math.max(pet.happiness - 2, 0);
  pet.cleanliness = Math.max(pet.cleanliness - 2, 0);
  pet.energy = Math.max(pet.energy - 2, 0);
  updateStats();
  savePet();
}

// Mini-Game
function startMiniGame() {
  if (pet.energy < 10) {
    alert("Your pet is too tired to play!");
    return;
  }
  isPlayingMiniGame = true;
  score = 0;
  ball = { x: 150, y: 100, radius: 30, dx: 5, dy: 5 };
  canvas.style.display = "block";
  canvas.addEventListener("click", handleCanvasClick);
  requestAnimationFrame(updateMiniGame);
}

function handleCanvasClick(event) {
  const rect = canvas.getBoundingClientRect();
  const clickX = event.clientX - rect.left;
  const clickY = event.clientY - rect.top;
  const dist = Math.sqrt((clickX - ball.x) ** 2 + (clickY - ball.y) ** 2);
  if (dist < ball.radius) {
    score += 10;
    ball.dx *= 1.1;
    ball.dy *= 1.1;
  }
}

function updateMiniGame() {
  if (!isPlayingMiniGame) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ball.x += ball.dx;
  ball.y += ball.dy;
  if (ball.x + ball.radius > canvas.width || ball.x - ball.radius < 0) ball.dx = -ball.dx;
  if (ball.y + ball.radius > canvas.height || ball.y - ball.radius < 0) ball.dy = -ball.dy;
  ctx.beginPath();
  ctx.arc(ball.x, ball.y, ball.radius, 0, Math.PI * 2);
  ctx.fillStyle = "red";
  ctx.fill();
  ctx.closePath();
  ctx.fillStyle = "black";
  ctx.font = "16px Arial";
  ctx.fillText(`Score: ${score}`, 10, 20);
  if (score >= 20) { //pontuação
    endMiniGame();
  } else {
    requestAnimationFrame(updateMiniGame);
  }
}

function endMiniGame() {
  isPlayingMiniGame = false;
  canvas.style.display = "none";
  canvas.removeEventListener("click", handleCanvasClick);
  pet.happiness = Math.min(pet.happiness + 20, 100);
  pet.energy = Math.max(pet.energy - 10, 0);
  pet.coins += score;
  addExperience(score);
  updateStats();
  savePet();
  alert(`Game Over! You earned ${score} coins!`);
}

// Shop
function openShop() {
  const shopItemsDiv = document.getElementById("shopItems");
  shopItemsDiv.innerHTML = "";
  shopItems.forEach(item => {
    const button = document.createElement("button");
    button.className = "bg-blue-500 text-white px-4 py-2 m-2 rounded hover:bg-blue-600";
    button.textContent = `${item.name} - ${item.price} Coins`;
    button.onclick = () => buyItem(item);
    shopItemsDiv.appendChild(button);
  });
  document.getElementById("shopModal").style.display = "flex";
}

function buyItem(item) {
  if (pet.coins >= item.price) {
    pet.coins -= item.price;
    pet.inventory.push(item);
    if (item.type === "food") pet.hunger = Math.min(pet.hunger + 30, 100);
    else if (item.type === "toy") pet.happiness = Math.min(pet.happiness + 20, 100);
    updateStats();
    savePet();
    alert(`Bought ${item.name}!`);
  } else {
    alert("Not enough coins!");
  }
}

function closeShop() {
  document.getElementById("shopModal").style.display = "none";
}

// Periodic Updates
setInterval(decreaseStats, 10000);

// Start Game
initGame();