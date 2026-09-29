/**
 * MTG Collection Vault — Cliente API con Axios
 * Centraliza la comunicación HTTP con el backend FastAPI.
 */

const API_BASE_URL = window.API_BASE_URL || 'http://127.0.0.1:8000';

const apiClient = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json'
    },
    timeout: 5000
});

// Interceptor para extraer detalles de error legibles
apiClient.interceptors.response.use(
    (response) => response,
    (error) => {
        let message = 'Error de conexión con el servidor.';
        if (error.response) {
            const detail = error.response.data?.detail;
            if (Array.isArray(detail)) {
                // Parseo de errores de validación Pydantic v2
                message = detail
                    .map((err) => {
                        const field = err.loc.slice(1).join('.') || err.loc[0] || 'campo';
                        return `${field}: ${err.msg}`;
                    })
                    .join(', ');
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
    getAll: async (skip = 0, limit = 100) => {
        const response = await apiClient.get('/sets/', { params: { skip, limit } });
        return response.data;
    },

    getById: async (id) => {
        const response = await apiClient.get(`/sets/${id}`);
        return response.data;
    },

    create: async (setData) => {
        const response = await apiClient.post('/sets/', setData);
        return response.data;
    },

    update: async (id, setData) => {
        const response = await apiClient.put(`/sets/${id}`, setData);
        return response.data;
    },

    delete: async (id) => {
        await apiClient.delete(`/sets/${id}`);
        return true;
    }
};

/* ==========================================================================
    SERVICIOS: CARTAS (CARDS)
   ========================================================================== */
const CardsAPI = {
    getAll: async (filters = {}) => {
        const params = {};
        if (filters.skip !== undefined) params.skip = filters.skip;
        if (filters.limit !== undefined) params.limit = filters.limit;
        if (filters.name) params.name = filters.name.trim();
        if (filters.set_id) params.set_id = filters.set_id;

        const response = await apiClient.get('/cards/', { params });
        return response.data;
    },

    getById: async (id) => {
        const response = await apiClient.get(`/cards/${id}`);
        return response.data;
    },

    create: async (cardData) => {
        const response = await apiClient.post('/cards/', cardData);
        return response.data;
    },

    update: async (id, cardData) => {
        const response = await apiClient.put(`/cards/${id}`, cardData);
        return response.data;
    },

    delete: async (id) => {
        await apiClient.delete(`/cards/${id}`);
        return true;
    }
};