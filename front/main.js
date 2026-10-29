const API_URL = (window.location.port === '5000') ? 'http://localhost:5000/api' : '/api';
let cachedPlayer = null;
let currentUser = null;

/* ==========================================================================
   1. GESTION DES FENÊTRES MODALES (AUTHENTIFICATION & PROFIL)
   ========================================================================== */

function openAuthModal() { 
  document.getElementById('auth-modal').style.display = 'flex'; 
}

function closeAuthModal() { 
  document.getElementById('auth-modal').style.display = 'none'; 
}

function openProfileModal() { 
  document.getElementById('profile-modal').style.display = 'flex';
  loadLeaderboard();
  if (currentUser) {
    document.getElementById('profile-info').innerHTML = `<strong>Joueur connecté :</strong> ${currentUser}`;
  } else {
    document.getElementById('profile-info').innerHTML = `<em>Non connecté (Joueur anonyme)</em>`;
  }
}

function closeProfileModal() { 
  document.getElementById('profile-modal').style.display = 'none'; 
}

async function registerUser() {
  const user = document.getElementById('auth-user').value.trim();
  const pass = document.getElementById('auth-pass').value.trim();

  if (!user || !pass) {
    document.getElementById('log').innerText = "Veuillez remplir tous les champs !";
    return;
  }

  try {
    const res = await fetch(`${API_URL}/register`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password: pass })
    });
    const data = await res.json();
    document.getElementById('log').innerText = data.message;
    if (res.ok) {
      currentUser = data.username;
      showAuthenticatedState();
      closeAuthModal();
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur de connexion au serveur lors de l'inscription.";
  }
}

async function loginUser() {
  const user = document.getElementById('auth-user').value.trim();
  const pass = document.getElementById('auth-pass').value.trim();

  if (!user || !pass) {
    document.getElementById('log').innerText = "Veuillez remplir tous les champs !";
    return;
  }

  try {
    const res = await fetch(`${API_URL}/login`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ username: user, password: pass })
    });
    const data = await res.json();
    document.getElementById('log').innerText = data.message;
    if (res.ok) {
      currentUser = data.username;
      showAuthenticatedState();
      closeAuthModal();
    }
  } catch (err) {
    document.getElementById('log').innerText = "Identifiants incorrects.";
  }
}

function showAuthenticatedState() {
  const btnAuth = document.getElementById('btn-auth-modal');
  if (btnAuth) btnAuth.style.display = 'none';

  const btnProfile = document.getElementById('btn-profile');
  if (btnProfile) btnProfile.style.display = 'inline-block';

  const badge = document.getElementById('user-badge');
  if (badge) {
    badge.style.display = 'inline-block';
    badge.innerText = `👤 ${currentUser}`;
  }
}

async function loadLeaderboard() {
  try {
    const res = await fetch(`${API_URL}/leaderboard`);
    const data = await res.json();
    const container = document.getElementById('leaderboard-list');
    if (!container) return;
    
    if (!data.leaderboard || data.leaderboard.length === 0) {
      container.innerHTML = '<div style="color: #aaa; text-align: center;">Aucun score enregistré.</div>';
      return;
    }

    container.innerHTML = '';
    data.leaderboard.forEach((item, index) => {
      const row = document.createElement('div');
      row.style.display = 'flex';
      row.style.justify = 'space-between';
      row.style.padding = '6px 0';
      row.style.borderBottom = '1px solid #2d2d3f';
      
      const rank = index === 0 ? '🥇' : (index === 1 ? '🥈' : (index === 2 ? '🥉' : `#${index + 1}`));
      row.innerHTML = `<span>${rank} <strong>${item.username}</strong> (${item.class})</span>
                       <strong style="color: #f1c40f;">${item.high_score} Salles</strong>`;
      container.appendChild(row);
    });
  } catch (err) {
    console.error("Erreur de chargement du classement :", err);
  }
}

/* ==========================================================================
   2. BOUCLE DE JEU & MISE À JOUR DE L'INTERFACE
   ========================================================================== */

async function selectClass(classId) {
  try {
    const res = await fetch(`${API_URL}/select_class`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ class_id: classId })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerText = data.message;
    
    document.getElementById('class-select-zone').style.display = 'none';
    document.getElementById('game-zone').style.display = 'block';
    document.getElementById('nav-zone').style.display = 'block';
    document.getElementById('action-zone').style.display = 'none';
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de la sélection du héros.";
  }
}

function returnToMainMenu() {
  if (confirm("Revenir au menu principal et abandonner la partie en cours ?")) {
    cachedPlayer = null;
    document.getElementById('game-zone').style.display = 'none';
    document.getElementById('tree-zone').style.display = 'none';
    document.getElementById('action-zone').style.display = 'none';
    document.getElementById('class-select-zone').style.display = 'block';
    document.getElementById('log').innerText = "Sélectionne une classe pour entrer dans le labyrinthe.";
  }
}

function renderMap(p) {
  const mapGrid = document.getElementById('map-grid');
  if (!mapGrid || !p) return;

  mapGrid.innerHTML = '';
  const currentX = p.pos_x || 0;
  const currentY = p.pos_y || 0;
  const visited = p.visited_rooms || {};

  for (let y = currentY + 2; y >= currentY - 2; y--) {
    for (let x = currentX - 2; x <= currentX + 2; x++) {
      const cell = document.createElement('div');
      cell.className = 'map-cell';
      const key = `${x},${y}`;

      if (x === currentX && y === currentY) {
        cell.classList.add('current');
        cell.innerText = '🔴';
      } else if (visited[key]) {
        const room = visited[key];
        cell.classList.add(room.type);
        if (room.type === 'monster') cell.innerText = '⚔️';
        else if (room.type === 'boss') cell.innerText = '👑';
        else if (room.type === 'chest') cell.innerText = '🎁';
        else if (room.type === 'merchant') cell.innerText = '🛒';
        else if (room.type === 'altar') cell.innerText = '⛩️';
        else cell.innerText = '🟩';
      } else {
        cell.innerText = '▪️';
      }
      mapGrid.appendChild(cell);
    }
  }
}

function updatePlayerUI(p) {
  if (!p) return;
  cachedPlayer = p;

  document.getElementById('inv-class').innerText = p.class_name;
  document.getElementById('inv-level').innerText = p.level;
  document.getElementById('inv-xp').innerText = `${p.xp} / ${p.xp_to_next}`;
  document.getElementById('inv-gold').innerText = p.gold || 0;
  document.getElementById('inv-pts').innerText = p.skill_points;
  
  document.getElementById('inv-hp').innerText = `${p.hp}/${p.max_hp} PV`;
  document.getElementById('inv-mp').innerText = `${p.mp}/${p.max_mp} PM`;
  document.getElementById('inv-def').innerText = p.defense;
  document.getElementById('inv-rooms').innerText = p.rooms_cleared;

  if (p.weapon) {
    document.getElementById('inv-weapon-name').innerText = p.weapon.name;
    document.getElementById('inv-weapon-damage').innerText = `Dégâts : ${p.weapon.min} - ${p.weapon.max}`;
  }

  if (p.armor) {
    document.getElementById('inv-armor-name').innerText = p.armor.name;
    document.getElementById('inv-armor-def').innerText = `Défense : +${p.armor.def}`;
  }

  const unlockedContainer = document.getElementById('inv-unlocked-skills');
  if (unlockedContainer) {
    unlockedContainer.innerHTML = '';
    if (!p.unlocked_skills || p.unlocked_skills.length === 0) {
      unlockedContainer.innerHTML = '<small style="color: #888;">Aucune</small>';
    } else {
      const learnedSkills = p.skill_tree.filter(s => p.unlocked_skills.includes(s.id));
      learnedSkills.forEach(skill => {
        const item = document.createElement('div');
        item.style.fontSize = '0.8em';
        item.style.marginBottom = '4px';
        item.innerHTML = `✅ <strong>${skill.name}</strong>`;
        unlockedContainer.appendChild(item);
      });
    }
  }

  const consList = document.getElementById('inv-consumables-list');
  if (consList) {
    consList.innerHTML = '';
    if (!p.inventory || p.inventory.length === 0) {
      consList.innerHTML = '<small style="color: #888;">Vide</small>';
    } else {
      p.inventory.forEach((item, index) => {
        const el = document.createElement('div');
        el.className = 'item-option';
        el.style.fontSize = '0.85em';
        el.style.cursor = 'pointer';
        el.innerHTML = `🧪 <strong>${item.name}</strong>`;
        el.onclick = () => useConsumable(index);
        consList.appendChild(el);
      });
    }
  }

  renderMap(p);
}

/* ==========================================================================
   3. DÉPLACEMENTS ET ÉVÉNEMENTS DU LABYRINTHE
   ========================================================================== */

async function move(direction) {
  try {
    const res = await fetch(`${API_URL}/move`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ direction: direction })
    });
    const data = await res.json();
    
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;

    document.getElementById('nav-zone').style.display = 'none';
    document.getElementById('action-zone').style.display = 'block';
    
    document.getElementById('monster-info').style.display = 'none';
    document.getElementById('chest-info').style.display = 'none';
    document.getElementById('merchant-info').style.display = 'none';
    document.getElementById('altar-info').style.display = 'none';

    if (data.event === 'monster') {
      document.getElementById('monster-info').style.display = 'block';
      document.getElementById('m-name').innerText = data.monster.name;
      document.getElementById('m-hp').innerText = `${data.monster.hp}/${data.monster.max_hp}`;

      const fleeBtn = document.getElementById('flee-btn');
      if (fleeBtn) {
        fleeBtn.style.display = (data.is_boss || data.monster.is_boss) ? 'none' : 'inline-block';
      }
    } else if (data.event === 'chest') {
      document.getElementById('chest-info').style.display = 'block';
      showChestOptions(data.chest);
    } else if (data.event === 'merchant') {
      document.getElementById('merchant-info').style.display = 'block';
      showMerchantOptions(data.merchant_stock);
    } else if (data.event === 'altar') {
      document.getElementById('altar-info').style.display = 'block';
    } else {
      setTimeout(() => {
        document.getElementById('action-zone').style.display = 'none';
        document.getElementById('nav-zone').style.display = 'block';
      }, 1200);
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du déplacement.";
  }
}

/* ==========================================================================
   4. INTERACTIONS (COMBAT, COFFRE, MARCHAND, AUTEL, CONSUMMABLES)
   ========================================================================== */

async function attack() {
  try {
    const res = await fetch(`${API_URL}/attack`, { method: 'POST' });
    const data = await res.json();
    handleCombatResult(data);
  } catch (e) {
    document.getElementById('log').innerText = "Erreur lors de l'attaque.";
  }
}

async function defend() {
  try {
    const res = await fetch(`${API_URL}/defend`, { method: 'POST' });
    const data = await res.json();
    handleCombatResult(data);
  } catch (e) {
    document.getElementById('log').innerText = "Erreur lors de la parade.";
  }
}

async function specialAttack() {
  try {
    const res = await fetch(`${API_URL}/special_attack`, { method: 'POST' });
    const data = await res.json();
    handleCombatResult(data);
  } catch (e) {
    document.getElementById('log').innerText = "Erreur lors du coup spécial.";
  }
}

async function flee() {
  try {
    const res = await fetch(`${API_URL}/flee`, { method: 'POST' });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
    if (data.fled) {
      document.getElementById('action-zone').style.display = 'none';
      document.getElementById('nav-zone').style.display = 'block';
    }
  } catch (e) {
    document.getElementById('log').innerText = "Erreur lors de la fuite.";
  }
}

function handleCombatResult(data) {
  updatePlayerUI(data.player);
  document.getElementById('log').innerHTML = data.message;
  if (data.monster) {
    document.getElementById('m-hp').innerText = `${data.monster.hp}/${data.monster.max_hp}`;
  }
  if (data.player_dead) {
    alert("TON ÂME EST DÉVORÉE PAR LE CHAOS ! Partie terminée.");
    document.getElementById('game-zone').style.display = 'none';
    document.getElementById('class-select-zone').style.display = 'block';
  } else if (data.monster_dead) {
    setTimeout(() => {
      document.getElementById('action-zone').style.display = 'none';
      document.getElementById('nav-zone').style.display = 'block';
    }, 1200);
  }
}

function showChestOptions(items) {
  const container = document.getElementById('chest-options');
  if (!container) return;
  container.innerHTML = '';
  items.forEach(item => {
    const el = document.createElement('div');
    el.className = 'item-option';
    el.style.cursor = 'pointer';
    el.style.margin = '5px 0';
    if (item.min) {
      el.innerHTML = `⚔️ <strong>${item.name}</strong> (Dégâts: ${item.min}-${item.max})`;
    } else if (item.def) {
      el.innerHTML = `🛡️ <strong>${item.name}</strong> (Def: +${item.def})`;
    } else {
      el.innerHTML = `🧪 <strong>${item.name}</strong> (${item.desc})`;
    }
    el.onclick = () => selectLoot(item);
    container.appendChild(el);
  });
}

async function selectLoot(lootItem) {
  try {
    const res = await fetch(`${API_URL}/equip`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ item: lootItem })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
    document.getElementById('action-zone').style.display = 'none';
    document.getElementById('nav-zone').style.display = 'block';
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du ramassage.";
  }
}

function showMerchantOptions(stock) {
  const container = document.getElementById('merchant-options');
  if (!container) return;
  container.innerHTML = '';
  if (!stock || stock.length === 0) {
    container.innerHTML = '<p style="color: #aaa;">Marchand sans marchandise.</p>';
    return;
  }
  stock.forEach((item, idx) => {
    const el = document.createElement('div');
    el.className = 'item-option';
    el.style.cursor = 'pointer';
    el.style.margin = '5px 0';
    el.innerHTML = `<strong>${item.name}</strong> - <strong style="color: #f1c40f;">${item.price} Gold</strong>`;
    el.onclick = () => buyItem(idx);
    container.appendChild(el);
  });
}

async function buyItem(index) {
  try {
    const res = await fetch(`${API_URL}/buy_item`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ index: index })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
    showMerchantOptions(data.merchant_stock);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de l'achat.";
  }
}

function leaveMerchant() {
  document.getElementById('action-zone').style.display = 'none';
  document.getElementById('nav-zone').style.display = 'block';
}

async function interactAltar(choice) {
  try {
    const res = await fetch(`${API_URL}/interact_altar`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ choice: choice })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
    document.getElementById('action-zone').style.display = 'none';
    document.getElementById('nav-zone').style.display = 'block';
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du rituel.";
  }
}

async function useConsumable(index) {
  try {
    const res = await fetch(`${API_URL}/use_item`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ index: index })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
  } catch (err) {
    document.getElementById('log').innerText = "Erreur d'utilisation d'objet.";
  }
}

/* ==========================================================================
   5. COMPÉTENCES ET ARBRE DE TALENTS
   ========================================================================== */

async function openSkillTree() {
  if (!cachedPlayer) {
    document.getElementById('log').innerText = "Choisis un héros d'abord !";
    return;
  }
  if (cachedPlayer.skill_points <= 0) {
    document.getElementById('log').innerText = "Gagne un niveau pour débloquer des points de compétence !";
    return;
  }
  try {
    const res = await fetch(`${API_URL}/draft_skills`);
    const data = await res.json();
    document.getElementById('game-zone').style.display = 'none';
    document.getElementById('tree-zone').style.display = 'block';
    renderDraftUI(data.choices);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de la récupération des compétences.";
  }
}

function renderDraftUI(choices) {
  const container = document.getElementById('draft-container');
  if (!container) return;
  container.innerHTML = '';
  choices.forEach(skill => {
    const card = document.createElement('div');
    card.className = 'nav-btn';
    card.style.margin = '8px 0';
    card.style.textAlign = 'left';
    card.innerHTML = `<strong>🌟 ${skill.name}</strong><br><small style="color: #2ed573;">${skill.desc}</small>`;
    card.onclick = () => chooseSkill(skill.id);
    container.appendChild(card);
  });
}

async function chooseSkill(skillId) {
  try {
    const res = await fetch(`${API_URL}/learn_skill`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_id: skillId })
    });
    const data = await res.json();
    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;
    closeSkillTree();
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du choix de la compétence.";
  }
}

function closeSkillTree() {
  document.getElementById('tree-zone').style.display = 'none';
  document.getElementById('game-zone').style.display = 'block';
}

/* ==========================================================================
   6. DOCKER & PERSISTANCE
   ========================================================================== */

async function saveCurrentGame() {
  try {
    const res = await fetch(`${API_URL}/save`, { method: 'POST' });
    const data = await res.json();
    document.getElementById('log').innerHTML = "💾 " + data.message;
  } catch (e) {
    document.getElementById('log').innerText = "Erreur lors de la sauvegarde.";
  }
}

async function loadSavedGame() {
  try {
    const res = await fetch(`${API_URL}/load`);
    const data = await res.json();
    if (data.player) {
      updatePlayerUI(data.player);
      if (data.user) {
        currentUser = data.user;
        showAuthenticatedState();
      }
      document.getElementById('class-select-zone').style.display = 'none';
      document.getElementById('game-zone').style.display = 'block';
      document.getElementById('nav-zone').style.display = 'block';
      document.getElementById('log').innerHTML = "📂 " + data.message;
    }
  } catch (e) {
    document.getElementById('log').innerText = "Aucune sauvegarde trouvée.";
  }
}

async function checkSystemHealth() {
  try {
    const res = await fetch(`${API_URL}`);
    const data = await res.json();
    const backBadge = document.getElementById('status-backend');
    if (backBadge) backBadge.innerText = '✅ API';
  } catch (e) {
    const backBadge = document.getElementById('status-backend');
    if (backBadge) backBadge.innerText = '❌ API';
  }

  try {
    const res = await fetch(`${API_URL}/game_server_status`);
    const data = await res.json();
    const gsBadge = document.getElementById('status-gameserver');
    if (gsBadge) {
      gsBadge.innerText = (data.status === 'online') ? '🛡️ GameServer' : '⚠️ GameServer';
    }
  } catch (e) {
    const gsBadge = document.getElementById('status-gameserver');
    if (gsBadge) gsBadge.innerText = '⚠️ GameServer';
  }
}

/* ==========================================================================
   7. INITIALISATION DU SCRIPT
   ========================================================================== */

window.addEventListener('DOMContentLoaded', async () => {
  checkSystemHealth();
  // Forcer l'affichage de l'écran de sélection de héros au lancement
  document.getElementById('class-select-zone').style.display = 'block';
  document.getElementById('game-zone').style.display = 'none';
  document.getElementById('tree-zone').style.display = 'none';
});