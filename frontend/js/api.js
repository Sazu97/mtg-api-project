/**
 * MTG Collection Vault — Cliente API con Axios
 * Centraliza la comunicación HTTP con el backend FastAPI.
 */

const API_BASE_URL = 'http://127.0.0.1:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 5000
});

// Interceptor para extraer datos o formatear errores legibles
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        let message = 'Error de conexión con el servidor.';
        if (error.response) {
            // Captura detalles devueltos por FastAPI (validaciones Pydantic o HTTPException)
            const detail = error.response.data?.detail;
            if (Array.isArray(detail)) {
                message = detail.map((err) => `${err.loc[1]}: ${err.msg}`).join(', ');
            } else if (typeof detail === 'string') {
                message = detail;
            } else {
                message = `Error HTTP ${error.response.status}`;
            }
        }
        return Promise.reject(new Error(message));
    }
);

/* ==========================================================================
    SERVICIOS: COLECCIONES (SETS)
   ========================================================================== */
const SetsAPI = {
    // GET /sets/
    getAll: async (skip = 0, limit = 100) => {
        const response = await apiClient.get('/sets/', { params: { skip, limit } });
        return response.data;
    },

    // GET /sets/{id}
    getById: async (id) => {
        const response = await apiClient.get(`/sets/${id}`);
        return response.data;
    },

    // POST /sets/
    create: async (setData) => {
        const response = await apiClient.post('/sets/', setData);
        return response.data;
    },

    // PUT /sets/{id}
    update: async (id, setData) => {
        const response = await apiClient.put(`/sets/${id}`, setData);
        return response.data;
    },

    // DELETE /sets/{id}
    delete: async (id) => {
        await apiClient.delete(`/sets/${id}`);
        return true;
    }
};

/* ==========================================================================
    SERVICIOS: CARTAS (CARDS)
   ========================================================================== */
const CardsAPI = {
    // GET /cards/ (soporta filtros por nombre, set_id y paginación)
    getAll: async (filters = {}) => {
        const params = {};
        if (filters.skip !== undefined) params.skip = filters.skip;
        if (filters.limit !== undefined) params.limit = filters.limit;
        if (filters.name) params.name = filters.name;
        if (filters.set_id) params.set_id = filters.set_id;

        const response = await apiClient.get('/cards/', { params });
        return response.data;
    },

    // GET /cards/{id}
    getById: async (id) => {
        const response = await apiClient.get(`/cards/${id}`);
        return response.data;
    },

    // POST /cards/
    create: async (cardData) => {
        const response = await apiClient.post('/cards/', cardData);
        return response.data;
    },

    // PUT /cards/{id}
    update: async (id, cardData) => {
        const response = await apiClient.put(`/cards/${id}`, cardData);
        return response.data;
    },

    // DELETE /cards/{id}
    delete: async (id) => {
        await apiClient.delete(`/cards/${id}`);
        return true;
    }
};