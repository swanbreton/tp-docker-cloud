const API_URL = (window.location.port === '5000') ? 'http://localhost:5000/api' : '/api';

async function renderTree() {
  try {
    const res = await fetch(`${API_URL}/player_state`, {
      method: 'GET',
      headers: { 'Accept': 'application/json' }
    });
    
    if (!res.ok) {
      document.getElementById('log').innerText = "Aucune partie en cours. Retourne au jeu pour choisir un héros.";
      return;
    }

    const data = await res.json();
    const p = data.player;

    if (!p) {
      document.getElementById('log').innerText = "Aucune partie en cours. Retourne au jeu pour choisir un héros.";
      return;
    }

    document.getElementById('tree-pts').innerText = p.skill_points;

    const wrapper = document.getElementById('tree-nodes-wrapper');
    wrapper.innerHTML = '';

    if (p.skill_tree) {
      const branch = document.createElement('div');
      branch.className = 'tree-branch';

      p.skill_tree.forEach((skill) => {
        const isUnlocked = p.unlocked_skills.includes(skill.id);
        const node = document.createElement('div');

        if (isUnlocked) {
          node.className = 'tree-node unlocked';
          node.innerHTML = `✅ <strong>${skill.name}</strong><br><br><small>${skill.desc}</small>`;
        } else if (p.skill_points > 0) {
          node.className = 'tree-node';
          node.innerHTML = `🌟 <strong>${skill.name}</strong><br><br><small>${skill.desc}</small>`;
          node.onclick = () => learnSkill(skill.id);
        } else {
          node.className = 'tree-node locked';
          node.innerHTML = `🔒 <strong>${skill.name}</strong><br><br><small>${skill.desc}</small>`;
        }

        branch.appendChild(node);
      });

      wrapper.appendChild(branch);
    }
  } catch (err) {
    document.getElementById('log').innerText = "Erreur de chargement de l'arbre de compétences.";
  }
}

async function learnSkill(skillId) {
  try {
    const res = await fetch(`${API_URL}/learn_skill`, {
      method: 'POST',
      headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' },
      body: JSON.stringify({ skill_id: skillId })
    });
    const data = await res.json();

    if (!res.ok) {
      document.getElementById('log').innerText = data.message;
      return;
    }

    document.getElementById('log').innerHTML = data.message;
    renderTree();
  } catch (err) {
    document.getElementById('log').innerText = "Erreur lors du déblocage.";
  }
}

// Initialisation au chargement de la page
renderTree();