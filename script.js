function toggleItem(id, direction = 1) {
    const item = document.getElementById(id);
    const textElement = item.nextElementSibling; 
    const originalName = item.getAttribute('data-name'); 
    
    // 1. GESTION DES COMPTEURS (Cœurs, Skultulas, etc.)
    const maxCountAttr = item.getAttribute('data-max');
    if (maxCountAttr) {
        const maxCount = parseInt(maxCountAttr);
        let currentCount = parseInt(item.getAttribute('data-current-count') || "0");
        
        currentCount += direction;

        // Reset si on dépasse le max ou si on descend sous 0
        if (currentCount > maxCount) {
            currentCount = 0;
        } else if (currentCount < 0) {
            currentCount = maxCount; // Boucle vers le max au clic droit depuis 0
        }

        // Mise à jour visuelle
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
                
                // AJOUT : Si on atteint exactement le max, on ajoute la classe 'maxed'
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

// Chargement et configuration initiale
window.addEventListener('load', () => {
    const allItems = document.querySelectorAll('.item');
    allItems.forEach(item => {
        // Clic droit pour reculer
        item.addEventListener('contextmenu', (e) => {
            e.preventDefault();
            toggleItem(item.id, -1);
        });

        // Restauration de la sauvegarde
        const savedValue = localStorage.getItem(item.id);
        const textElement = item.nextElementSibling;
        const originalName = item.getAttribute('data-name');
        const maxCountAttr = item.getAttribute('data-max');
        
        if (savedValue !== null && savedValue !== "-1") {
            // Cas des compteurs
            if (maxCountAttr) {
                const maxCount = parseInt(maxCountAttr);
                const currentCount = parseInt(savedValue);

                if (currentCount > 0) {
                    item.classList.add('active');
                    item.setAttribute('data-current-count', currentCount);
                    if (textElement) {
                        textElement.innerText = currentCount;
                        // AJOUT : Vérification du max au chargement
                        if (currentCount === maxCount) {
                            textElement.classList.add('maxed');
                        }
                    }
                }
            } 
            // Cas des items à niveaux
            else {
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