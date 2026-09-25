/**
 * MTG Collection Vault — Controlador Principal
 */

const state = {
    sets: [],
    cards: [],
    currentPage: 1,
    limitPerPage: 6,
    filters: { search: '', setId: '', rarity: '' },
    setPendingDelete: null
};

// Referencias principales del DOM
const setsGrid = document.getElementById('sets-container');
const cardsGrid = document.getElementById('cards-container');
const filterSet = document.getElementById('filter-set');
const filterRarity = document.getElementById('filter-rarity');
const searchInput = document.getElementById('card-search-input');
const btnPrev = document.getElementById('btn-prev');
const btnNext = document.getElementById('btn-next');
const currentPageText = document.getElementById('current-page');
const paginationInfo = document.getElementById('pagination-info');

/* --- Cargas de datos asíncronas --- */
async function loadSets() {
    try {
        state.sets = await SetsAPI.getAll();
        UI.renderSets(state.sets, setsGrid);
        UI.populateDropdowns(state.sets, filterSet, document.getElementById('card-set-id'));
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function loadCards() {
    try {
        const params = {
            name: state.filters.search || undefined,
            set_id: state.filters.setId || undefined,
            skip: (state.currentPage - 1) * state.limitPerPage,
            limit: state.limitPerPage
        };

        state.cards = await CardsAPI.getAll(params);

        // Filtro local por rareza si está seleccionada
        const filtered = state.filters.rarity
            ? state.cards.filter(c => c.rarity.toLowerCase() === state.filters.rarity.toLowerCase())
            : state.cards;

        UI.renderCards(filtered, cardsGrid);
        updatePaginationUI();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function updatePaginationUI() {
    currentPageText.innerText = state.currentPage;
    btnPrev.disabled = state.currentPage <= 1;
    btnPrev.style.opacity = state.currentPage <= 1 ? '0.4' : '1';

    const isLastPage = state.cards.length < state.limitPerPage;
    btnNext.disabled = isLastPage;
    btnNext.style.opacity = isLastPage ? '0.4' : '1';
    paginationInfo.innerText = `Página ${state.currentPage} — Registros: ${state.cards.length}`;
}

/* --- Operaciones CRUD: Sets --- */
async function handleSetSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('set-id-field').value;
    const payload = {
        name: document.getElementById('set-name').value.trim(),
        code: document.getElementById('set-code').value.trim().toUpperCase(),
        release_date: document.getElementById('set-date').value || null
    };

    try {
        if (id) {
            await SetsAPI.update(id, payload);
            showToast(`Colección "${payload.name}" actualizada.`);
        } else {
            await SetsAPI.create(payload);
            showToast(`Colección "${payload.name}" registrada con éxito.`);
        }
        closeModal('set-modal');
        await loadSets();
        await loadCards();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function openEditSetModal(id) {
    try {
        const set = await SetsAPI.getById(id);
        document.getElementById('set-id-field').value = set.id;
        document.getElementById('set-name').value = set.name;
        document.getElementById('set-code').value = set.code;
        document.getElementById('set-date').value = set.release_date || '';
        document.getElementById('modal-set-title').innerText = `Editar Colección: ${set.code}`;
        openModal('set-modal');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

function requestDeleteSet(id, name) {
    state.setPendingDelete = id;
    document.getElementById('danger-set-name').innerText = name;
    openModal('danger-modal');
}

async function confirmCascadeDelete() {
    if (!state.setPendingDelete) return;
    try {
        await SetsAPI.delete(state.setPendingDelete);
        showToast('Colección y cartas eliminadas en cascada (204).');
        closeModal('danger-modal');
        state.setPendingDelete = null;
        await loadSets();
        await loadCards();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/* --- Operaciones CRUD: Cards --- */
async function handleCardSubmit(e) {
    e.preventDefault();
    const id = document.getElementById('card-id').value;
    const payload = {
        name: document.getElementById('card-name').value.trim(),
        mana_cost: document.getElementById('card-mana').value.trim() || null,
        set_id: parseInt(document.getElementById('card-set-id').value, 10),
        type_line: document.getElementById('card-type').value.trim(),
        rarity: document.getElementById('card-rarity').value,
        power: document.getElementById('card-power').value.trim() || null,
        toughness: document.getElementById('card-toughness').value.trim() || null
    };

    try {
        if (id) {
            await CardsAPI.update(id, payload);
            showToast(`Carta "${payload.name}" actualizada.`);
        } else {
            await CardsAPI.create(payload);
            showToast(`Carta "${payload.name}" registrada con éxito.`);
        }
        closeModal('card-modal');
        await loadCards();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function openEditCardModal(id) {
    try {
        const card = await CardsAPI.getById(id);
        document.getElementById('card-id').value = card.id;
        document.getElementById('card-name').value = card.name;
        document.getElementById('card-mana').value = card.mana_cost || '';
        document.getElementById('card-set-id').value = card.set_id;
        document.getElementById('card-type').value = card.type_line;
        document.getElementById('card-rarity').value = card.rarity;
        document.getElementById('card-power').value = card.power || '';
        document.getElementById('card-toughness').value = card.toughness || '';
        document.getElementById('modal-card-title').innerText = `Editar Carta: ${card.name}`;
        openModal('card-modal');
    } catch (error) {
        showToast(error.message, 'error');
    }
}

async function deleteCard(id) {
    if (!confirm('¿Seguro que deseas eliminar esta carta?')) return;
    try {
        await CardsAPI.delete(id);
        showToast('Carta eliminada correctamente.');
        await loadCards();
    } catch (error) {
        showToast(error.message, 'error');
    }
}

/* --- Listeners e Inicio --- */
document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('set-form').addEventListener('submit', handleSetSubmit);
    document.getElementById('card-form').addEventListener('submit', handleCardSubmit);
    document.getElementById('btn-confirm-delete').addEventListener('click', confirmCascadeDelete);

    let debounceTimer;
    searchInput.addEventListener('input', (e) => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(() => {
            state.filters.search = e.target.value.trim();
            state.currentPage = 1;
            loadCards();
        }, 300);
    });

    filterSet.addEventListener('change', (e) => {
        state.filters.setId = e.target.value;
        state.currentPage = 1;
        loadCards();
    });

    filterRarity.addEventListener('change', (e) => {
        state.filters.rarity = e.target.value;
        loadCards();
    });

    btnPrev.addEventListener('click', () => {
        if (state.currentPage > 1) {
            state.currentPage--;
            loadCards();
        }
    });

    btnNext.addEventListener('click', () => {
        state.currentPage++;
        loadCards();
    });

    setupNavSpy();
    loadSets();
    loadCards();
});

/* --- Detector de sección activa para el menú superior --- */
function setupNavSpy() {
    const navItems = document.querySelectorAll('.nav-links .nav-item');
    const sections = document.querySelectorAll('section[id]');

    function updateActiveNav() {
        // 150px de margen para compensar la barra superior fija
        const scrollPosition = window.scrollY + 150;

        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');

            if (scrollPosition >= top && scrollPosition < top + height) {
                navItems.forEach(item => {
                    item.classList.remove('active');
                    if (item.getAttribute('href') === `#${id}`) {
                        item.classList.add('active');
                    }
                });
            }
        });
    }

    window.addEventListener('scroll', updateActiveNav, { passive: true });
    updateActiveNav(); // Ejecuta una comprobación inicial al cargar la página
}