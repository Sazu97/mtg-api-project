/**
 * MTG Collection Vault — Renderizado de Componentes UI
 */

function escapeHtml(text) {
    if (text === null || text === undefined) return '';
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

const UI = {
    // Renderiza el listado de colecciones
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

        container.innerHTML = sets.map(set => `
        <article class="set-card">
        <div>
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <div class="set-badge-code">${escapeHtml(set.code)}</div>
                    <div>
                    <h3 style="font-size: 1.1rem; font-weight: 700;">${escapeHtml(set.name)}</h3>
                    <span class="text-muted mono" style="font-size: 0.75rem;">
                        ${set.release_date ? `Lanzamiento: ${set.release_date}` : 'Sin fecha'}
                    </span>
                    </div>
                </div>
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
            <button class="btn-icon danger" title="Eliminar en cascada" onclick="requestDeleteSet(${set.id}, '${escapeHtml(set.name)}')">
                <span class="material-symbols-outlined">delete_sweep</span>
            </button>
            </div>
        </div>
        </article>
    `).join('');
    },

    // Renderiza el catálogo de cartas
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
            const ptBadge = (card.power !== null && card.toughness !== null && card.power !== '' && card.toughness !== '')
                ? `<div class="card-pt">${escapeHtml(card.power)}/${escapeHtml(card.toughness)}</div>`
                : '';

            return `
        <article class="card-item">
            <div>
                <div class="card-top">
                    <h3 class="card-name">${escapeHtml(card.name)}</h3>
                    ${card.mana_cost ? `<span class="card-mana">${escapeHtml(card.mana_cost)}</span>` : ''}
                </div>
                <p class="card-type">${escapeHtml(card.type_line)}</p>
            </div>
            <div>
                <div class="card-bottom-info">
                    <span class="rarity-badge ${rarityClass}">${escapeHtml(card.rarity)}</span>
                    <span class="text-muted mono" style="font-size: 0.8rem;">${escapeHtml(setCode)}</span>
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
    },

    // Rellena los selectores desplegables de colecciones
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