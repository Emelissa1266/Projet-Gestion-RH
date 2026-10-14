document.addEventListener('DOMContentLoaded', function() {
    const toggleButton = document.getElementById('theme-toggle');
    const storageKey = 'rh-dashboard-theme';
    const savedTheme = localStorage.getItem(storageKey) || 'dark';

    document.body.classList.toggle('light-mode', savedTheme === 'light');
    updateToggleButton(toggleButton, savedTheme);

    if (!toggleButton) {
        return;
    }

    toggleButton.addEventListener('click', function() {
        const isLight = document.body.classList.toggle('light-mode');
        const theme = isLight ? 'light' : 'dark';
        localStorage.setItem(storageKey, theme);
        updateToggleButton(toggleButton, theme);
    });
});

function updateToggleButton(button, theme) {
    if (!button) {
        return;
    }
    button.textContent = theme === 'light' ? 'Mode Sombre' : 'Mode Clair';
    button.classList.toggle('btn-light', theme === 'dark');
    button.classList.toggle('btn-dark', theme === 'light');
}
