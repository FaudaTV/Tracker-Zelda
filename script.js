/**
 * Gère l'activation, les niveaux et les compteurs des items standards.
 */
function toggleItem(id, direction = 1) {
    const item = document.getElementById(id);
    const textElement = item.nextElementSibling; 
    const originalName = item.getAttribute('data-name'); 
    
    // --- RESET UNIVERSEL POUR LES OBJETS À POPUP (CLIC DROIT) ---
    // Si l'objet a une sélection enregistrée et qu'on fait un clic droit
    if (direction === -1 && localStorage.getItem(id + '-selected')) {
        const defaultImg = item.getAttribute('data-default-img') || item.src;
        item.src = defaultImg;
        item.classList.remove('active');
        localStorage.removeItem(id + '-selected');
        return;
    }

    // 1. GESTION DES COMPTEURS (Cœurs, clés, etc.)
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

    // 2. GESTION DES NIVEAUX OU ITEMS SIMPLES
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

/**
 * Ouvre une popup spécifique à côté de l'élément cliqué.
 */
function openItemPopup(event, modalId) {
    if(event) event.stopPropagation();
    
    // Ferme les autres popups ouvertes
    closeAllPopups();

    const modal = document.getElementById(modalId);
    if (!modal) return;

    const triggerItem = event.currentTarget; 
    const rect = triggerItem.getBoundingClientRect();
    
    // On lie la popup à l'item déclencheur pour savoir quoi mettre à jour
    modal.setAttribute('data-target-id', triggerItem.id);
    
    // Positionnement à droite de l'item
    modal.style.left = (rect.right + 10) + 'px';
    modal.style.top = (rect.top + window.scrollY) + 'px';
    modal.style.display = 'block';
}

/**
 * Ferme toutes les fenêtres modales/popups.
 */
function closeAllPopups() {
    const modals = document.querySelectorAll('.modal');
    modals.forEach(m => m.style.display = 'none');
}

/**
 * Sélectionne un item dans la popup et met à jour l'item parent.
 */
function selectPopupItem(imgSrc, modalId) {
    const modal = document.getElementById(modalId);
    const targetId = modal.getAttribute('data-target-id');
    const targetItem = document.getElementById(targetId);
    
    if (targetItem) {
        targetItem.src = imgSrc;
        targetItem.classList.add('active');
        
        // Sauvegarde spécifique pour les sélections de popup
        localStorage.setItem(targetId + '-selected', imgSrc);
    }
    
    closeAllPopups();
}

// --- CHARGEMENT ET CONFIGURATION INITIALE ---

window.addEventListener('load', () => {
    const allItems = document.querySelectorAll('.item');
    
    allItems.forEach(item => {
        // 1. Désactiver le menu contextuel et gérer le clic droit
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            toggleItem(item.id, -1);
        });

        // 2. Restauration des sélections de popups (ex: animal choisi)
        const savedChoice = localStorage.getItem(item.id + '-selected');
        if (savedChoice) {
            item.src = savedChoice;
            item.classList.add('active');
        }

        // 3. Restauration standard (compteurs et niveaux)
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
            } else {
                // Si l'item n'a pas déjà été activé par une sélection de popup
                if (!savedChoice) {
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
        }
    });
});

// Fermeture des popups si on clique n'importe où ailleurs sur la page
window.addEventListener('click', (event) => {
    // Si on ne clique pas à l'intérieur d'une popup
    if (!event.target.closest('.modal-content')) {
        closeAllPopups();
    }
});