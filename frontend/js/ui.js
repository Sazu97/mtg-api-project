/**
 * MTG Collection Vault — Renderizado de Componentes UI
 */

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    return String(text)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

/* Convierte texto tipo {2}{U}{B} en iconos vectoriales oficiales de Mana Font */
function formatManaSymbols(cost) {
    if (!cost) return "";
    return cost.replace(/\{([a-zA-Z0-9/]+)\}/g, (_, sym) => {
        const clean = sym.toLowerCase().replace("/", "");
        return `<i class="ms ms-${clean} ms-cost ms-shadow"></i>`;
    });
}

/* Caché en memoria para optimizar peticiones a Scryfall */
const oracleCache = new Map();

/* Consulta el texto oficial de reglas y datos de coleccionista de la carta */
function loadCardOracle(card) {
    const oracleContainer = document.getElementById(`oracle-${card.id}`);
    const collectorBadge = document.getElementById(`collector-${card.id}`);

    function applyCardData(data) {
        if (oracleContainer) {
            if (data && data.oracle_text) {
                oracleContainer.innerHTML = formatManaSymbols(escapeHtml(data.oracle_text)).replace(/\n/g, '<br>');
            } else {
                oracleContainer.style.display = 'none';
            }
        }

        if (collectorBadge && data && data.collector_number) {
            const setCode = card.set ? card.set.code : `ID:${card.set_id}`;
            const rarityCode = (data.rarity || card.rarity || 'C')[0].toUpperCase();
            const formattedNum = String(data.collector_number).padStart(4, '0');
            collectorBadge.textContent = `${setCode} · ${rarityCode} ${formattedNum}`;
        }
    }

    if (oracleCache.has(card.name)) {
        applyCardData(oracleCache.get(card.name));
        return;
    }

    fetch(`https://api.scryfall.com/cards/named?fuzzy=${encodeURIComponent(card.name)}`)
        .then(res => res.ok ? res.json() : null)
        .then(data => {
            oracleCache.set(card.name, data);
            applyCardData(data);
        })
        .catch(() => {
            oracleCache.set(card.name, null);
            applyCardData(null);
        });
}

const UI = {
    renderSets: (sets, container) => {
        if (!container) return;

        if (sets.length === 0) {
            container.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 2rem; color: var(--text-muted);">
                No hay colecciones registradas. Pulsa en "Nueva Colección" para registrar la primera.
            </div>
            `;
            return;
        }

        container.innerHTML = sets.map(set => {
            const setCodeClean = encodeURIComponent(set.code.toLowerCase());
            const artUrl = `https://api.scryfall.com/cards/random?q=set%3A${setCodeClean}&format=image&version=art_crop`;

            return `
            <article class="set-card">
                <div>
                    <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.85rem;">
                        <div style="display: flex; align-items: center; gap: 0.75rem;">
                            <div class="set-icon-badge">
                                <img 
                                    src="https://svgs.scryfall.io/sets/${setCodeClean}.svg" 
                                    alt="${escapeHtml(set.code)}"
                                    class="set-symbol-svg"
                                    onerror="this.style.display='none'; this.nextElementSibling.style.display='block';"
                                />
                                <span class="set-badge-code" style="display: none;">${escapeHtml(set.code)}</span>
                            </div>
                            <div>
                                <h3 style="font-size: 1.1rem; font-weight: 700;">${escapeHtml(set.name)}</h3>
                                <span class="text-muted mono" style="font-size: 0.75rem;">
                                    ${set.release_date ? `Lanzamiento: ${escapeHtml(set.release_date)}` : 'Sin fecha'}
                                </span>
                            </div>
                        </div>
                    </div>

                    <div class="set-art-container">
                        <img 
                            src="${artUrl}" 
                            alt="${escapeHtml(set.name)}" 
                            class="set-art-img"
                            loading="lazy"
                            onerror="this.parentElement.style.display='none'"
                        />
                    </div>

                    <div class="set-card-stats">
                        <div>
                            <span class="text-muted" style="font-size: 0.75rem; display: block;">ID Base de Datos</span>
                            <span class="mono" style="font-weight: 700; font-size: 1.1rem;">#${set.id}</span>
                        </div>
                        <div>
                            <span class="text-muted" style="font-size: 0.75rem; display: block;">Integridad FK</span>
                            <span class="mono" style="color: var(--secondary); font-size: 0.8rem;">Cascade Active</span>
                        </div>
                    </div>
                </div>
                <div class="set-card-actions">
                    <span class="text-muted mono" style="font-size: 0.75rem;">ON DELETE CASCADE</span>
                    <div>
                        <button class="btn-icon" title="Editar" onclick="openEditSetModal(${set.id})">
                            <span class="material-symbols-outlined">edit</span>
                        </button>
                        <button class="btn-icon danger" title="Eliminar en cascada" onclick="requestDeleteSet(${set.id})">
                            <span class="material-symbols-outlined">delete_sweep</span>
                        </button>
                    </div>
                </div>
            </article>
            `;
        }).join('');
    },

    renderCards: (cards, container) => {
        if (!container) return;

        if (cards.length === 0) {
            container.innerHTML = `
            <div style="grid-column: 1 / -1; text-align: center; padding: 3rem; background: var(--bg-surface-card); border-radius: var(--radius-lg);">
                <span class="material-symbols-outlined" style="font-size: 40px; color: var(--text-muted); margin-bottom: 0.5rem;">style</span>
                <h4 style="font-size: 1.1rem; font-weight: 700; margin-bottom: 0.25rem;">No se encontraron cartas</h4>
                <p style="color: var(--text-muted); font-size: 0.85rem;">Prueba con otros términos de búsqueda o registra una nueva carta.</p>
            </div>
            `;
            return;
        }

        container.innerHTML = cards.map(card => {
            const rarityClass = `rarity-${card.rarity.toLowerCase()}`;
            const setCode = card.set ? card.set.code : `ID:${card.set_id}`;
            const collectorNum = String(card.id).padStart(3, '0');
            const formattedMana = formatManaSymbols(card.mana_cost);
            const ptBadge = (card.power !== null && card.toughness !== null && card.power !== '' && card.toughness !== '')
                ? `<div class="card-pt" title="Fuerza / Resistencia">P/T ${escapeHtml(card.power)}/${escapeHtml(card.toughness)}</div>`
                : '';

            const artUrl = `https://api.scryfall.com/cards/named?fuzzy=${encodeURIComponent(card.name)}&format=image&version=art_crop`;

            return `
            <article class="card-item">
                <div>
                    <div class="card-top">
                        <h3 class="card-name">${escapeHtml(card.name)}</h3>
                        ${card.mana_cost ? `<div class="card-mana-group">${formattedMana}</div>` : ''}
                    </div>

                    <div class="card-art-container">
                        <img 
                            src="${artUrl}" 
                            alt="${escapeHtml(card.name)}" 
                            class="card-art-img"
                            loading="lazy"
                            onerror="this.parentElement.style.display='none'"
                        />
                    </div>

                    <p class="card-type">${escapeHtml(card.type_line)}</p>
                    <div class="card-oracle-text" id="oracle-${card.id}"></div>
                </div>
                <div>
                    <div class="card-bottom-info">
                        <span class="rarity-badge ${rarityClass}">${escapeHtml(card.rarity)}</span>
                        <span class="text-muted mono" style="font-size: 0.8rem;" id="collector-${card.id}">${escapeHtml(setCode)} · #${collectorNum}</span>
                        ${ptBadge}
                    </div>
                    <div class="card-actions">
                        <button class="btn-icon" title="Editar" onclick="openEditCardModal(${card.id})">
                            <span class="material-symbols-outlined">edit</span>
                        </button>
                        <button class="btn-icon danger" title="Eliminar" onclick="deleteCard(${card.id})">
                            <span class="material-symbols-outlined">delete</span>
                        </button>
                    </div>
                </div>
            </article>
            `;
        }).join('');

        cards.forEach(card => loadCardOracle(card));
    },

    populateDropdowns: (sets, filterSelect, formSelect) => {
        if (filterSelect) {
            const currentVal = filterSelect.value;
            filterSelect.innerHTML = '<option value="">Todas las colecciones</option>' +
                sets.map(s => `<option value="${s.id}">${escapeHtml(s.name)} (${escapeHtml(s.code)})</option>`).join('');
            filterSelect.value = currentVal;
        }

        if (formSelect) {
            formSelect.innerHTML = '<option value="">Selecciona un set...</option>' +
                sets.map(s => `<option value="${s.id}">${escapeHtml(s.name)} (${escapeHtml(s.code)})</option>`).join('');
        }
    }
};