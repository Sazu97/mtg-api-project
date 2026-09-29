/**
 * MTG Collection Vault — Sistema de Feedback y Modales
 */

function getToastContainer() {
    let container = document.getElementById("toast-container");
    if (!container) {
        container = document.createElement("div");
        container.id = "toast-container";
        document.body.appendChild(container);
    }
    return container;
}

function showToast(message, type = "success") {
    const container = getToastContainer();

    const toast = document.createElement("div");
    toast.className = `toast toast-${type}`;

    const iconName = type === "success" ? "check_circle" : "error";
    const iconColor = type === "success" ? "var(--secondary)" : "var(--error)";
    const titleText = type === "success" ? "Operación Exitosa" : "Aviso del Sistema";

    // Estructura segura: Icono fijo y contenedor de textos
    const icon = document.createElement("span");
    icon.className = "material-symbols-outlined";
    icon.style.color = iconColor;
    icon.style.fontSize = "20px";
    icon.textContent = iconName;

    const contentDiv = document.createElement("div");
    contentDiv.style.flex = "1";
    contentDiv.style.minWidth = "0";

    const titleEl = document.createElement("p");
    titleEl.style.fontWeight = "700";
    titleEl.style.fontSize = "0.85rem";
    titleEl.textContent = titleText;

    const msgEl = document.createElement("p");
    msgEl.style.color = "var(--text-muted)";
    msgEl.style.fontSize = "0.8rem";
    msgEl.style.marginTop = "2px";
    msgEl.textContent = message;

    contentDiv.appendChild(titleEl);
    contentDiv.appendChild(msgEl);

    const closeBtn = document.createElement("button");
    closeBtn.className = "btn-icon";
    closeBtn.style.padding = "2px";
    closeBtn.setAttribute("aria-label", "Cerrar notificación");
    closeBtn.innerHTML = '<span class="material-symbols-outlined" style="font-size: 14px;">close</span>';
    closeBtn.addEventListener("click", () => toast.remove());

    toast.appendChild(icon);
    toast.appendChild(contentDiv);
    toast.appendChild(closeBtn);

    container.appendChild(toast);

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