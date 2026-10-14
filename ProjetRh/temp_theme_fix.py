from pathlib import Path
import re

TEMPLATE_DIR = Path(__file__).resolve().parent / 'app1' / 'templates'
THEME_BUTTON_HTML = (
    '    <div class="theme-control-bar">\n'
    '        <a href="{% url \'acceuil_arh\' %}" class="btn btn-primary" id="dashboard-return">Retour au Dashboard</a>\n'
    '        <button id="theme-toggle" class="btn btn-secondary">Mode Clair/Sombre</button>\n'
    '    </div>\n'
)
SCRIPT_TAG = '    <script src="{% static \'js/theme-toggle.js\' %}"></script>\n'

style_block = re.compile(r'<style\b[^>]*>.*?</style>', re.IGNORECASE | re.DOTALL)
inline_theme_script = re.compile(
    r'<script\b(?![^>]*\bsrc=)[^>]*>.*?(localStorage\.getItem\(|localStorage\.setItem\(|theme-toggle|document\.getElementById\(\'theme-toggle\'\)|document\.querySelector\(\'#theme-toggle\'\)|classList\.toggle\(\'light-mode\'\)|classList\.add\(currentTheme).*?</script>',
    re.IGNORECASE | re.DOTALL
)
script_include = re.compile(
    r'<script\b[^>]*src=["\'][^"\']*theme-toggle\.js[^"\']*["\'][^>]*>\s*</script>\s*',
    re.IGNORECASE | re.DOTALL
)


def ensure_load_static(text: str) -> str:
    if '{% load static %}' in text:
        return text
    lines = text.splitlines()
    for i, line in enumerate(lines):
        if line.strip().lower().startswith('<html'):
            lines.insert(i + 1, '{% load static %}')
            break
    return '\n'.join(lines)


def ensure_theme_control_bar(text: str) -> str:
    # Remove existing theme control bar if present
    text = re.sub(r'<div class="theme-control-bar">.*?</div>\s*', '', text, flags=re.DOTALL)
    # Remove loose theme toggle buttons
    text = re.sub(r'<div class="d-flex justify-content-between p-3">.*?</div>\s*', '', text, flags=re.DOTALL)
    if '<body>' in text:
        return text.replace('<body>', '<body>\n' + THEME_BUTTON_HTML, 1)
    return text


def normalize_script_includes(text: str) -> str:
    text = script_include.sub('', text)
    text = inline_theme_script.sub('', text)
    text = re.sub(r'<script\b[^>]*src=["\'][^"\']*theme-toggle\.js[^"\']*["\'][^>]*>\s*</script>\s*', '', text, flags=re.IGNORECASE | re.DOTALL)
    if '</body>' in text:
        text = text.replace('</body>', SCRIPT_TAG + '</body>', 1)
    return text


def remove_style_blocks(text: str) -> str:
    return style_block.sub('', text)


def normalize_whitespace(text: str) -> str:
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text


def main() -> None:
    if not TEMPLATE_DIR.exists():
        raise SystemExit(f'Template directory not found: {TEMPLATE_DIR}')

    for path in sorted(TEMPLATE_DIR.glob('*.html')):
        original = path.read_text(encoding='utf-8')
        updated = original
        updated = ensure_load_static(updated)
        updated = remove_style_blocks(updated)
        updated = ensure_theme_control_bar(updated)
        updated = normalize_script_includes(updated)
        updated = normalize_whitespace(updated)
        if updated != original:
            path.write_text(updated, encoding='utf-8')
            print(f'Updated {path.name}')


if __name__ == '__main__':
    main()