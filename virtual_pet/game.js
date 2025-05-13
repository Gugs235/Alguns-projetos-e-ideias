let pet = {
  name: "Buddy",
  hunger: 100,
  happiness: 100,
  cleanliness: 100,
  energy: 100,
  coins: 0,
  level: 1
};

function updateStats() {
  document.getElementById("hungerFill").style.width = pet.hunger + "%";
  document.getElementById("happinessFill").style.width = pet.happiness + "%";
  document.getElementById("cleanlinessFill").style.width = pet.cleanliness + "%";
  document.getElementById("energyFill").style.width = pet.energy + "%";
  document.getElementById("coins").textContent = pet.coins;
  document.getElementById("petName").textContent = pet.name;
}

function feed() {
  pet.hunger = Math.min(pet.hunger + 20, 100);
  pet.coins -= 5;
  updateStats();
}

function play() {
  pet.happiness = Math.min(pet.happiness + 20, 100);
  pet.energy = Math.max(pet.energy - 10, 0);
  pet.coins += 10;
  updateStats();
}

function clean() {
  pet.cleanliness = Math.min(pet.cleanliness + 20, 100);
  updateStats();
}

function rest() {
  pet.energy = Math.min(pet.energy + 20, 100);
  pet.happiness = Math.max(pet.happiness - 5, 0);
  updateStats();
}

function decreaseStats() {
  pet.hunger = Math.max(pet.hunger - 1, 0);
  pet.happiness = Math.max(pet.happiness - 1, 0);
  pet.cleanliness = Math.max(pet.cleanliness - 1, 0);
  pet.energy = Math.max(pet.energy - 1, 0);
  updateStats();
}

// Load saved pet data
function loadPet() {
  const saved = localStorage.getItem("pet");
  if (saved) pet = JSON.parse(saved);
  updateStats();
}

// Save pet data
function savePet() {
  localStorage.setItem("pet", JSON.stringify(pet));
}

// Decrease stats every 10 seconds
setInterval(() => {
  decreaseStats();
  savePet();
}, 10000);

// Initial load
loadPet();