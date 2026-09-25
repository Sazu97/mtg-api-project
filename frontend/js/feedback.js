/**
 * MTG Collection Vault — Sistema de Feedback y Modales
 */

const toastContainer = document.getElementById("toast-container");

function showToast(message, type = "success") {
    if (!toastContainer) return;

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;

    const iconName = type === "success" ? "check_circle" : "error";
    const iconColor = type === "success" ? "var(--secondary)" : "var(--error)";
    const title = type === "success" ? "Operación Exitosa" : "Aviso del Sistema";

    toast.innerHTML = `
    <span class="material-symbols-outlined" style="color: ${iconColor}; font-size: 20px;">${iconName}</span>
    <div style="flex: 1; min-width: 0;">
        <p style="font-weight: 700; font-size: 0.85rem;">${title}</p>
        <p style="color: var(--text-muted); font-size: 0.8rem; margin-top: 2px;">${message}</p>
    </div>
    <button class="btn-icon" style="padding: 2px;" onclick="this.parentElement.remove()">
        <span class="material-symbols-outlined" style="font-size: 14px;">close</span>
    </button>
    `;

    toastContainer.appendChild(toast);

    setTimeout(() => {
        if (toast.parentElement) toast.remove();
    }, 4000);
}

function openModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.remove("hidden");
}

function closeModal(id) {
    const modal = document.getElementById(id);
    if (modal) modal.classList.add("hidden");
}
