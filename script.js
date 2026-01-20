/**
 * Gère l'activation, les niveaux, les compteurs et les étoiles des items.
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

    // 1. GESTION DES ÉTOILES (0 étoile = Arme active, 1-5 = Étoiles visibles)
    if (item.hasAttribute('data-stars')) {
        let currentStars = parseInt(item.getAttribute('data-stars') || "-1");
        const starImg = document.getElementById('star-' + id);

        currentStars += direction;

        // Cycle : -1 (éteint), 0 (allumé sans étoile), 1, 2, 3, 4, 5 étoiles
        if (currentStars > 5) currentStars = -1;
        if (currentStars < -1) currentStars = 5;

        item.setAttribute('data-stars', currentStars);
        localStorage.setItem(id + '-stars', currentStars);

        if (currentStars === -1) {
            // État éteint
            item.classList.remove('active');
            if (starImg) {
                starImg.classList.remove('visible');
                starImg.src = "";
            }
        } else if (currentStars === 0) {
            // État allumé mais 0 étoile
            item.classList.add('active');
            if (starImg) {
                starImg.classList.remove('visible');
                starImg.src = "";
            }
        } else {
            // État allumé avec étoiles (1 à 5)
            item.classList.add('active');
            if (starImg) {
                starImg.src = `../images/HW/star${currentStars}.png`;
                starImg.classList.add('visible');
            }
        }
        return; 
    }

    // 2. GESTION DES COMPTEURS (Cœurs, clés, etc.)
    const maxCountAttr = item.getAttribute('data-max');
    if (maxCountAttr) {
        const maxCount = parseInt(maxCountAttr);
        let currentCount = parseInt(item.getAttribute('data-current-count') || "0");
        
        currentCount += direction;

        if (currentCount > maxCount) {
            currentCount = 0;
        } else if (currentCount < 0) {
            currentCount = maxCount; 
        }

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
                if (currentCount === maxCount) {
                    textElement.classList.add('maxed');
                } else {
                    textElement.classList.remove('maxed');
                }
            }
        }
        
        item.setAttribute('data-current-count', currentCount);
        localStorage.setItem(id, currentCount);
        return;
    }

    // 3. GESTION DES NIVEAUX OU ITEMS SIMPLES
    const levelsAttr = item.getAttribute('data-levels');
    const levels = levelsAttr ? levelsAttr.split(',') : [];
    let currentLevel = parseInt(item.getAttribute('data-current-level') || "-1");

    currentLevel += direction;
    const maxLevels = levels.length > 0 ? levels.length : 1;

    if (currentLevel >= maxLevels) {
        currentLevel = -1;
    } else if (currentLevel < -1) {
        currentLevel = maxLevels - 1; 
    }

    if (currentLevel === -1) {
        item.classList.remove('active');
        if (levels.length > 0) item.src = levels[0];
    } else {
        item.classList.add('active');
        if (levels.length > 0) item.src = levels[currentLevel];
    }

    item.setAttribute('data-current-level', currentLevel);
    localStorage.setItem(id, currentLevel);
}

// --- LOGIQUE DE POPUP GÉNÉRALISÉE ---

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
    const modals = document.querySelectorAll('.modal');
    modals.forEach(m => m.style.display = 'none');
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

// --- CHARGEMENT ET CONFIGURATION INITIALE ---

window.addEventListener('load', () => {
    const allItems = document.querySelectorAll('.item');
    
    allItems.forEach(item => {
        // Clic droit pour décrémenter
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            toggleItem(item.id, -1);
        });

        // Restauration des sélections de popups
        const savedChoice = localStorage.getItem(item.id + '-selected');
        if (savedChoice) {
            item.src = savedChoice;
            item.classList.add('active');
        }

        // Restauration des ÉTOILES (Armes)
        if (item.hasAttribute('data-stars')) {
            const savedStars = localStorage.getItem(item.id + '-stars');
            if (savedStars !== null && savedStars !== "-1") {
                item.setAttribute('data-stars', savedStars);
                item.classList.add('active'); // L'arme est active pour 0, 1, 2, 3, 4, 5
                
                const starImg = document.getElementById('star-' + item.id);
                if (starImg && savedStars !== "0") {
                    starImg.src = `../images/HW/star${savedStars}.png`;
                    starImg.classList.add('visible');
                }
            }
        }

        // Restauration standard (compteurs et niveaux)
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
            } else if (!savedChoice && !item.hasAttribute('data-stars')) {
                item.classList.add('active');
                item.setAttribute('data-current-level', savedValue);
                const levelsAttr = item.getAttribute('data-levels');
                if (levelsAttr) {
                    const levels = levelsAttr.split(',');
                    const levelIndex = parseInt(savedValue);
                    if (levels[levelIndex]) item.src = levels[levelIndex];
                }
            }
        }
    });
});

window.addEventListener('click', (event) => {
    if (!event.target.closest('.modal-content')) {
        closeAllPopups();
    }
});