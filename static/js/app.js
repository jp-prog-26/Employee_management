/**
 * EmpControl - Interacciones Frontend (camelCase Edition)
 */
document.addEventListener('DOMContentLoaded', () => {
    initTheme();
    initSidebar();
    initModals();
    initTableFilters();
    initAlerts();
    initFormValidation();
    initDemoStates();
});

/* 0. Dark Mode */
function initTheme() {
    const btn = document.getElementById('themeToggleBtn');
    if (!btn) return;
    let theme = localStorage.getItem('theme') || (matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    const apply = (t) => {
        document.documentElement.setAttribute('data-theme', t);
        const icon = btn.querySelector('i');
        if (icon) icon.className = t === 'dark' ? 'fa-solid fa-sun' : 'fa-solid fa-moon';
    };
    apply(theme);
    btn.addEventListener('click', () => {
        theme = theme === 'dark' ? 'light' : 'dark';
        localStorage.setItem('theme', theme);
        apply(theme);
    });
}

/* 1. Sidebar */
function initSidebar() {
    const toggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (!toggle || !sidebar || !overlay) return;
    const close = () => { sidebar.classList.remove('open'); overlay.classList.remove('active'); };
    toggle.addEventListener('click', () => { sidebar.classList.toggle('open'); overlay.classList.toggle('active'); });
    overlay.addEventListener('click', close);
}

/* 2. Modals */
function initModals() {
    document.querySelectorAll('[data-modal-target]').forEach(b => {
        b.addEventListener('click', (e) => {
            e.preventDefault();
            const target = document.querySelector(b.getAttribute('data-modal-target'));
            if (target) target.classList.add('active');
        });
    });
    const closeModal = (m) => m.classList.remove('active');
    document.querySelectorAll('[data-close-modal]').forEach(b => b.addEventListener('click', () => closeModal(b.closest('.modalOverlay'))));
    document.querySelectorAll('.modalOverlay').forEach(m => m.addEventListener('click', e => e.target === m && closeModal(m)));
    document.addEventListener('keydown', e => e.key === 'Escape' && document.querySelectorAll('.modalOverlay.active').forEach(closeModal));
}

/* 3. Table Search & Filter */
function initTableFilters() {
    const search = document.getElementById('tableSearch');
    const filters = document.querySelectorAll('.filterBtn');
    const rows = document.querySelectorAll('#employeeTableBody tr');
    if (!rows.length) return;

    let query = '', status = 'ALL';
    const apply = () => {
        let count = 0;
        rows.forEach(r => {
            const txt = r.textContent.toLowerCase();
            const badge = r.querySelector('.badge');
            const st = badge ? badge.textContent.trim().toUpperCase() : '';
            const match = txt.includes(query) && (status === 'ALL' || st.includes(status));
            r.style.display = match ? '' : 'none';
            if (match) count++;
        });
        const empty = document.getElementById('searchEmptyState');
        if (empty) empty.style.display = count === 0 ? 'flex' : 'none';
    };

    if (search) search.addEventListener('input', e => { query = e.target.value.toLowerCase().trim(); apply(); });
    filters.forEach(b => b.addEventListener('click', () => {
        filters.forEach(f => f.classList.remove('active'));
        b.classList.add('active');
        status = b.getAttribute('data-filter') || 'ALL';
        apply();
    }));
}

/* 4. Alerts */
function initAlerts() {
    document.querySelectorAll('.alertClose').forEach(b => b.addEventListener('click', () => {
        const a = b.closest('.alert');
        if (a) a.remove();
    }));
}

/* 5. Form Validation */
function initFormValidation() {
    document.querySelectorAll('form[data-validate]').forEach(f => {
        const inputs = f.querySelectorAll('input[required], select[required]');
        const check = (i) => {
            const g = i.closest('.formGroup');
            const valid = i.value.trim() !== '';
            if (g) {
                g.classList.toggle('hasError', !valid);
                g.classList.toggle('hasSuccess', valid);
                const err = g.querySelector('.formError');
                if (err) err.style.display = valid ? 'none' : 'flex';
            }
            return valid;
        };
        inputs.forEach(i => {
            i.addEventListener('blur', () => check(i));
            i.addEventListener('input', () => i.closest('.formGroup')?.classList.contains('hasError') && check(i));
        });
        f.addEventListener('submit', e => {
            let valid = true;
            inputs.forEach(i => !check(i) && (valid = false));
            if (!valid) e.preventDefault();
        });
    });
}

/* 6. Demo States */
function initDemoStates() {
    const btns = document.querySelectorAll('[data-demo-state]');
    if (!btns.length) return;
    const views = {
        table: document.getElementById('tableViewState'),
        loading: document.getElementById('loadingViewState'),
        empty: document.getElementById('emptyViewState'),
        error: document.getElementById('errorViewState')
    };
    btns.forEach(b => b.addEventListener('click', () => {
        const st = b.getAttribute('data-demo-state');
        Object.values(views).forEach(v => v && (v.style.display = 'none'));
        if (views[st]) views[st].style.display = 'block';
        btns.forEach(x => { x.classList.remove('btnPrimary'); x.classList.add('btnSecondary'); });
        b.classList.remove('btnSecondary'); b.classList.add('btnPrimary');
    }));
}