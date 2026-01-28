/**
 * Nom du Projet : [https://faudatv.github.io/Tracker-Zelda/]
 * Auteur : [FaudaTV]
 * GitHub : https://github.com/FaudaTV
 * Licence : GNU AGPLv3
 * * Note : Les images Nintendo sont la propriété de Nintendo.
 */

/**
 * Gère l'activation, les niveaux, les compteurs, les étoiles HW 
 * et les améliorations BOTW.
 */
function toggleItem(id, direction = 1) {
    const item = document.getElementById(id);
    if (!item) return;

    const textElement = item.nextElementSibling; 
    const originalName = item.getAttribute('data-name'); 
    
    // --- RESET UNIVERSEL (CLIC DROIT / DIRECTION -1) ---
    if (direction === -1 && localStorage.getItem(id + '-selected')) {
        const defaultImg = item.getAttribute('data-default-img') || item.src;
        item.src = defaultImg;
        item.classList.remove('active');
        localStorage.removeItem(id + '-selected');
        return;
    }

    // 1. GESTION DES AMÉLIORATIONS BOTW (0 à 4 étoiles ★)
    if (item.classList.contains('botw-upgrade')) {
        let currentLevel = parseInt(item.getAttribute('data-upgrade') || "-1");
        const starContainer = document.getElementById('stars-' + id);

        currentLevel += direction;

        // Cycle : -1 (éteint), 0 (actif sans étoile), 1, 2, 3, 4 étoiles
        if (currentLevel > 4) currentLevel = -1;
        if (currentLevel < -1) currentLevel = 4;

        item.setAttribute('data-upgrade', currentLevel);
        localStorage.setItem(id + '-upgrade', currentLevel);
        
        updateBotwDisplay(item, starContainer, currentLevel);
        return;
    }

    // 2. GESTION DES ÉTOILES HYRULE WARRIORS (Images stars.png)
    if (item.hasAttribute('data-stars')) {
        let currentStars = parseInt(item.getAttribute('data-stars') || "-1");
        const starImg = document.getElementById('star-' + id);

        currentStars += direction;

        if (currentStars > 5) currentStars = -1;
        if (currentStars < -1) currentStars = 5;

        item.setAttribute('data-stars', currentStars);
        localStorage.setItem(id + '-stars', currentStars);

        if (currentStars === -1) {
            item.classList.remove('active');
            if (starImg) {
                starImg.classList.remove('visible');
                starImg.src = "";
            }
        } else {
            item.classList.add('active');
            if (starImg) {
                if (currentStars === 0) {
                    starImg.classList.remove('visible');
                    starImg.src = "";
                } else {
                    starImg.src = `../images/HW/star${currentStars}.png`;
                    starImg.classList.add('visible');
                }
            }
        }
        return; 
    }

    // 3. GESTION DES COMPTEURS (Cœurs, clés, etc.)
    const maxCountAttr = item.getAttribute('data-max');
    if (maxCountAttr) {
        const maxCount = parseInt(maxCountAttr);
        let currentCount = parseInt(item.getAttribute('data-current-count') || "0");
        
        currentCount += direction;

        if (currentCount > maxCount) currentCount = 0;
        else if (currentCount < 0) currentCount = maxCount; 

        item.setAttribute('data-current-count', currentCount);
        localStorage.setItem(id, currentCount);

        if (currentCount === 0) {
            item.classList.remove('active');
            if (textElement) {
                textElement.innerText = originalName;
                textElement.classList.remove('maxed');
            }
        } else {
            item.classList.add('active');
            if (textElement) {
                textElement.innerText = currentCount;
                textElement.classList.toggle('maxed', currentCount === maxCount);
            }
        }
        return;
    }

    // 4. GESTION DES NIVEAUX OU ITEMS SIMPLES
    const levelsAttr = item.getAttribute('data-levels');
    const levels = levelsAttr ? levelsAttr.split(',') : [];
    let currentLevel = parseInt(item.getAttribute('data-current-level') || "-1");

    currentLevel += direction;
    const maxLevels = levels.length > 0 ? levels.length : 1;

    if (currentLevel >= maxLevels) currentLevel = -1;
    else if (currentLevel < -1) currentLevel = maxLevels - 1; 

    item.setAttribute('data-current-level', currentLevel);
    localStorage.setItem(id, currentLevel);

    if (currentLevel === -1) {
        item.classList.remove('active');
        if (levels.length > 0) item.src = levels[0];
    } else {
        item.classList.add('active');
        if (levels.length > 0) item.src = levels[currentLevel];
    }
}

/**
 * Mise à jour visuelle spécifique pour BOTW
 */
function updateBotwDisplay(item, container, level) {
    if (level === -1) {
        item.classList.remove('active');
        if (container) container.innerHTML = "";
    } else {
        item.classList.add('active');
        if (container) {
            container.innerHTML = "★".repeat(level);
        }
    }
}

// --- LOGIQUE DE POPUP ---

function openItemPopup(event, modalId) {
    if(event) event.stopPropagation();
    closeAllPopups();

    const modal = document.getElementById(modalId);
    if (!modal) return;

    const triggerItem = event.currentTarget; 
    const rect = triggerItem.getBoundingClientRect();
    
    modal.setAttribute('data-target-id', triggerItem.id);
    modal.style.left = (rect.right + 10) + 'px';
    modal.style.top = (rect.top + window.scrollY) + 'px';
    modal.style.display = 'block';
}

function closeAllPopups() {
    document.querySelectorAll('.modal').forEach(m => m.style.display = 'none');
}

function selectPopupItem(imgSrc, modalId) {
    const modal = document.getElementById(modalId);
    const targetId = modal.getAttribute('data-target-id');
    const targetItem = document.getElementById(targetId);
    
    if (targetItem) {
        targetItem.src = imgSrc;
        targetItem.classList.add('active');
        localStorage.setItem(targetId + '-selected', imgSrc);
    }
    closeAllPopups();
}

// --- CHARGEMENT INITIAL ---

window.addEventListener('load', () => {
    const allItems = document.querySelectorAll('.item');
    
    allItems.forEach(item => {
        // Clic droit universel
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            toggleItem(item.id, -1);
        });

        // 1. Restauration BOTW
        if (item.classList.contains('botw-upgrade')) {
            const savedUpgrade = localStorage.getItem(item.id + '-upgrade');
            if (savedUpgrade !== null) {
                const level = parseInt(savedUpgrade);
                item.setAttribute('data-upgrade', level);
                updateBotwDisplay(item, document.getElementById('stars-' + item.id), level);
            }
        }

        // 2. Restauration HW (Étoiles images)
        if (item.hasAttribute('data-stars')) {
            const savedStars = localStorage.getItem(item.id + '-stars');
            if (savedStars !== null && savedStars !== "-1") {
                item.setAttribute('data-stars', savedStars);
                item.classList.add('active');
                const starImg = document.getElementById('star-' + item.id);
                if (starImg && savedStars !== "0") {
                    starImg.src = `../images/HW/star${savedStars}.png`;
                    starImg.classList.add('visible');
                }
            }
        }

        // 3. Restauration Popups
        const savedChoice = localStorage.getItem(item.id + '-selected');
        if (savedChoice) {
            item.src = savedChoice;
            item.classList.add('active');
        }

        // 4. Restauration Compteurs et Niveaux standards
        const savedValue = localStorage.getItem(item.id);
        const textElement = item.nextElementSibling;
        const maxCountAttr = item.getAttribute('data-max');
        
        if (savedValue !== null && savedValue !== "-1") {
            if (maxCountAttr) {
                const currentCount = parseInt(savedValue);
                if (currentCount > 0) {
                    item.classList.add('active');
                    item.setAttribute('data-current-count', currentCount);
                    if (textElement) {
                        textElement.innerText = currentCount;
                        if (currentCount === parseInt(maxCountAttr)) textElement.classList.add('maxed');
                    }
                }
            } else if (!savedChoice && !item.hasAttribute('data-stars') && !item.classList.contains('botw-upgrade')) {
                item.classList.add('active');
                item.setAttribute('data-current-level', savedValue);
                const levelsAttr = item.getAttribute('data-levels');
                if (levelsAttr) {
                    const levels = levelsAttr.split(',');
                    if (levels[savedValue]) item.src = levels[savedValue];
                }
            }
        }
    });
});

window.addEventListener('click', (e) => {
    if (!e.target.closest('.modal-content')) closeAllPopups();
});