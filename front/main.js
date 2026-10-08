const API_URL = 'http://localhost:5000/api';
let cachedPlayer = null;

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
  } catch (err) {
    document.getElementById('log').innerText = "Erreur de connexion au serveur.";
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

  // Arme
  if (p.weapon) {
    document.getElementById('inv-weapon-name').innerText = p.weapon.name;
    document.getElementById('inv-weapon-damage').innerText = `Dégâts : ${p.weapon.min} - ${p.weapon.max}`;
    document.getElementById('inv-weapon-desc').innerText = p.weapon.desc || '-';
  }

  // Armure
  if (p.armor) {
    document.getElementById('inv-armor-name').innerText = p.armor.name;
    document.getElementById('inv-armor-def').innerText = `Défense : +${p.armor.def}`;
    document.getElementById('inv-armor-desc').innerText = p.armor.desc || '-';
  }

  // Compétences
  const unlockedContainer = document.getElementById('inv-unlocked-skills');
  if (unlockedContainer) {
    unlockedContainer.innerHTML = '';
    if (!p.unlocked_skills || p.unlocked_skills.length === 0) {
      unlockedContainer.innerHTML = '<div style="font-size: 0.85em; color: #888;">Aucune compétence</div>';
    } else {
      const learnedSkills = p.skill_tree.filter(s => p.unlocked_skills.includes(s.id));
      learnedSkills.forEach(skill => {
        const item = document.createElement('div');
        item.className = 'skill-node unlocked';
        item.style.marginBottom = '5px';
        item.innerHTML = `✅ <strong>${skill.name}</strong><br><small style="color: #2ed573;">${skill.desc}</small>`;
        unlockedContainer.appendChild(item);
      });
    }
  }

  // Sac à dos
  const consList = document.getElementById('inv-consumables-list');
  if (consList) {
    consList.innerHTML = '';
    if (!p.inventory || p.inventory.length === 0) {
      consList.innerHTML = '<div style="font-size: 0.85em; color: #888;">Sac vide</div>';
    } else {
      p.inventory.forEach((item, index) => {
        const el = document.createElement('div');
        el.className = 'item-option';
        el.style.fontSize = '0.85em';
        el.innerHTML = `🧪 <strong>${item.name}</strong><br><small>${item.desc}</small>`;
        el.onclick = () => useConsumable(index);
        consList.appendChild(el);
      });
    }
  }
}

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
      }, 1500);
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du déplacement.";
  }
}

function showMerchantOptions(stock) {
  const container = document.getElementById('merchant-options');
  container.innerHTML = '';

  if (!stock || stock.length === 0) {
    container.innerHTML = '<p style="color: #aaa;">Le marchand n\'a plus rien à vendre.</p>';
    return;
  }

  stock.forEach((item, idx) => {
    const el = document.createElement('div');
    el.className = 'item-option';
    
    let info = '';
    if (item.min) {
      info = `⚔️ Dégâts: ${item.min}-${item.max}`;
    } else if (item.def) {
      info = `🛡️ Défense: +${item.def}`;
    } else {
      info = `🧪 Effet: ${item.desc}`;
    }

    el.innerHTML = `<strong>${item.name}</strong><br>
                    <small style="color: #70a1ff;">${info}</small> | 
                    <strong style="color: #f1c40f;">Prix: ${item.price} Gold</strong>`;
    
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
    document.getElementById('log').innerText = "Erreur lors de l'interaction.";
  }
}

async function openSkillTree() {
  if (!cachedPlayer) {
    document.getElementById('log').innerText = "Choisis un héros d'abord !";
    return;
  }
  if (cachedPlayer.skill_points <= 0) {
    document.getElementById('log').innerText = "Gagne un niveau pour débloquer un choix de compétence !";
    return;
  }
  try {
    const res = await fetch(`${API_URL}/draft_skills`);
    const data = await res.json();
    document.getElementById('game-zone').style.display = 'none';
    document.getElementById('tree-zone').style.display = 'block';
    renderDraftUI(data.choices);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur de chargement des compétences.";
  }
}

function renderDraftUI(choices) {
  const container = document.getElementById('draft-container');
  container.innerHTML = '';
  if (!choices || choices.length === 0) {
    container.innerHTML = '<p style="text-align: center;">Toutes les compétences ont déjà été débloquées !</p>';
    return;
  }
  choices.forEach(skill => {
    const card = document.createElement('div');
    card.className = 'class-option';
    card.style.padding = '12px';
    card.innerHTML = `
      <strong style="color: #d4af37; font-size: 1.05em;">🌟 ${skill.name}</strong><br>
      <small style="color: #2ed573;">${skill.desc}</small>
    `;
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
    if (data.player.skill_points > 0) {
      openSkillTree();
    } else {
      closeSkillTree();
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de la sélection.";
  }
}

function closeSkillTree() {
  document.getElementById('tree-zone').style.display = 'none';
  document.getElementById('game-zone').style.display = 'block';
}

async function attack() {
  try {
    const res = await fetch(`${API_URL}/attack`, { 
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    handleCombatResult(data);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de l'attaque.";
  }
}

async function defend() {
  try {
    const res = await fetch(`${API_URL}/defend`, { 
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    handleCombatResult(data);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de la parade.";
  }
}

async function specialAttack() {
  try {
    const res = await fetch(`${API_URL}/special_attack`, { 
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    });
    const data = await res.json();
    handleCombatResult(data);
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du coup spécial.";
  }
}

async function flee() {
  try {
    const res = await fetch(`${API_URL}/flee`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' }
    });
    const data = await res.json();

    updatePlayerUI(data.player);
    document.getElementById('log').innerHTML = data.message;

    if (data.player_dead) {
      alert("TON ÂME EST DÉVORÉE PAR LE CHAOS ! Partie terminée.");
      document.getElementById('game-zone').style.display = 'none';
      document.getElementById('tree-zone').style.display = 'none';
      document.getElementById('class-select-zone').style.display = 'block';
    } else if (data.fled) {
      document.getElementById('action-zone').style.display = 'none';
      document.getElementById('nav-zone').style.display = 'block';
    } else if (data.monster) {
      document.getElementById('m-hp').innerText = `${data.monster.hp}/${data.monster.max_hp}`;
    }
  } catch (err) {
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
    document.getElementById('tree-zone').style.display = 'none';
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
  container.innerHTML = '';
  items.forEach(item => {
    const el = document.createElement('div');
    el.className = 'item-option';
    if (item.min) {
      el.innerHTML = `⚔️ <strong>${item.name}</strong> [Tier ${item.tier}]<br>
                      <small style="color: #ffa502;">Dégâts : ${item.min}-${item.max}</small> | 
                      <small style="color: #2ed573;">${item.desc}</small>`;
    } else if (item.def) {
      el.innerHTML = `🛡️ <strong>${item.name}</strong> [Tier ${item.tier}]<br>
                      <small style="color: #70a1ff;">Défense : +${item.def}</small> | 
                      <small style="color: #2ed573;">${item.desc}</small>`;
    } else {
      el.innerHTML = `🧪 <strong>${item.name}</strong> (Consommable)<br>
                      <small style="color: #70a1ff;">Effet : ${item.desc}</small>`;
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
    if (data.monster) {
      document.getElementById('m-hp').innerText = `${data.monster.hp}/${data.monster.max_hp}`;
    } else if (!data.monster && document.getElementById('action-zone').style.display === 'block') {
      document.getElementById('action-zone').style.display = 'none';
      document.getElementById('nav-zone').style.display = 'block';
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors de l'utilisation de l'objet.";
  }
}