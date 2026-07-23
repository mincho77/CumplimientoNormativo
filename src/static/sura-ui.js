// SURA Brand UI - Utilidades Globales

// 1. Toast (Mensajes efímeros)
function showToast(message, type = 'info') {
    let container = document.getElementById('sura-toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'sura-toast-container';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    toast.className = `sura-toast ${type}`;
    
    // Icono según tipo
    let iconClass = 'ic-alert';
    if (type === 'success') iconClass = 'ic-check';
    else if (type === 'error' || type === 'warning') iconClass = 'ic-alert';

    toast.innerHTML = `
        <span class="ic ${iconClass}" style="font-size:1.5em; color: var(--color-primary);"></span>
        <div style="flex: 1; font-weight: 500;">${message}</div>
    `;

    container.appendChild(toast);

    // Trigger reflow for animation
    void toast.offsetWidth;
    toast.classList.add('show');

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// 2. Modal Base (Confirmaciones / Decisiones)
function showConfirm(title, message, onConfirm, confirmText = 'Aceptar', cancelText = 'Cancelar') {
    const overlay = document.createElement('div');
    overlay.className = 'sura-modal-overlay';
    
    overlay.innerHTML = `
        <div class="sura-modal-card">
            <div class="sura-modal-title">${title}</div>
            <div class="sura-modal-body">${message}</div>
            <div class="sura-modal-actions">
                <button class="btn-secondary" id="sura-modal-cancel">${cancelText}</button>
                <button class="btn-primary" id="sura-modal-confirm">${confirmText}</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    // Animación de entrada
    requestAnimationFrame(() => overlay.classList.add('show'));

    const close = () => {
        overlay.classList.remove('show');
        setTimeout(() => overlay.remove(), 200);
    };

    overlay.querySelector('#sura-modal-cancel').onclick = close;
    overlay.querySelector('#sura-modal-confirm').onclick = () => {
        close();
        if (onConfirm) onConfirm();
    };
}


// 3. Modal Prompt (Entrada de datos)
function showPrompt(title, message, defaultValue, onConfirm, confirmText = 'Guardar', cancelText = 'Cancelar') {
    const overlay = document.createElement('div');
    overlay.className = 'sura-modal-overlay';
    
    overlay.innerHTML = `
        <div class="sura-modal-card">
            <div class="sura-modal-title">${title}</div>
            <div class="sura-modal-body">
                <p style="margin-bottom:12px;">${message}</p>
                <input type="text" id="sura-modal-input" class="form-control" value="${defaultValue || ''}" style="width:100%; padding:10px; border:1px solid var(--gray-200); border-radius:var(--radius-sm); font-family:inherit;">
            </div>
            <div class="sura-modal-actions">
                <button class="btn-secondary" id="sura-modal-cancel">${cancelText}</button>
                <button class="btn-primary" id="sura-modal-confirm">${confirmText}</button>
            </div>
        </div>
    `;

    document.body.appendChild(overlay);

    requestAnimationFrame(() => {
        overlay.classList.add('show');
        overlay.querySelector('#sura-modal-input').focus();
    });

    const close = () => {
        overlay.classList.remove('show');
        setTimeout(() => overlay.remove(), 200);
    };

    overlay.querySelector('#sura-modal-cancel').onclick = close;
    overlay.querySelector('#sura-modal-confirm').onclick = () => {
        const val = overlay.querySelector('#sura-modal-input').value;
        close();
        if (onConfirm) onConfirm(val);
    };
}
