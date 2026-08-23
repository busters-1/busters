import sys, json, re

sys.stdout.reconfigure(encoding='utf-8')

with open('e:/브리미르/rune_codex.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Update Title and Headers
html = html.replace('<title>브리미르(Brimir) 룬 도감 마스터</title>', '<title>브리미르(Brimir) 버스터즈 — 룬 도감</title>')
html = html.replace('<h1>⚔️ 브리미르(Brimir) 마스터 아카이브</h1>', '<h1>⚔️ 브리미르(Brimir) 버스터즈</h1>')
html = html.replace('<p>공식 라이브 데이터베이스 · 인게임 100% 한글화 · 정량 메커니즘 엔진 연동</p>', '<p>브리미르: 심장으로의 순례 룬 도감 & 빌드 덱 시뮬레이터</p>')
html = html.replace('<a href="rune_codex.html" class="nav-tab active">', '<a href="brimir_busters.html" class="nav-tab active">')

# 2. Clean table header column
html = html.replace('<th class="col-active">부여 액티브 스킬 (색상별 분기 & 계수)</th>', '<th class="col-active">부여 액티브 스킬 (색상별 분기)</th>')

# 3. Clean up Sort Select (remove active_mult_desc)
html = re.sub(r'\s*<option value="active_mult_desc">.*?</option>', '', html)

# 4. Clean RUNES_DATA
start_pos = html.find('const RUNES_DATA = [')
if start_pos == -1:
    print("Error: RUNES_DATA start not found!")
    sys.exit(1)

array_start = html.find('[', start_pos)
array_end = html.find('];', array_start) + 1

raw_json = html[array_start:array_end]
runes = json.loads(raw_json)
print(f"Loaded {len(runes)} runes successfully.")

stripped_passives = 0
stripped_actives = 0

for r in runes:
    # Clean passive: keep name & description, delete detailed_effect
    if 'passive' in r and isinstance(r['passive'], dict):
        if 'detailed_effect' in r['passive']:
            del r['passive']['detailed_effect']
            stripped_passives += 1
    
    # Clean actives: keep name, cooldown, description, is_ranged, delete multiplier
    if 'actives' in r and isinstance(r['actives'], list):
        for act in r['actives']:
            if 'multiplier' in act:
                del act['multiplier']
                stripped_actives += 1

print(f"Sanitized: {stripped_passives} passive detailed effects removed, {stripped_actives} active multipliers removed.")

clean_json = json.dumps(runes, ensure_ascii=False, indent=2)
html = html[:array_start] + clean_json + html[array_end:]

# 5. Clean JS rendering functions
# Remove detailed_effect from search query matching
html = re.sub(r'\s*\(\s*r\.passive\.detailed_effect\s*&&\s*r\.passive\.detailed_effect\.toLowerCase\(\)\.includes\(query\)\s*\)\s*\|\|', '', html)
html = re.sub(r'\|\|\s*\(\s*r\.passive\.detailed_effect\s*&&\s*r\.passive\.detailed_effect\.toLowerCase\(\)\.includes\(query\)\s*\)', '', html)

# Remove active_mult_desc sort branch if present in script
html = re.sub(
    r"\}\s*else\s*if\s*\(currentSort\s*===\s*'active_mult_desc'\)\s*\{[^}]*\}",
    "",
    html
)

# Remove multBadge in table render
html = html.replace(
    "const multBadge = act.multiplier ? `<span class=\"active-mult\">계수 ${act.multiplier}x</span>` : '';",
    "const multBadge = '';"
)

# Remove passive detail in table render
html = re.sub(
    r'const pDetail = \(hasPassive && p\.detailed_effect.*?\n\s*`<div class="passive-detail">\$\{p\.detailed_effect\}</div>` : \'\';',
    "const pDetail = '';",
    html
)

# Remove detailed_effect from modal
old_modal_passive_detail = "${r.passive?.detailed_effect ? `<div style=\"font-size:12px; color:#58a6ff; margin-top:4px; font-weight:bold;\">${r.passive.detailed_effect}</div>` : ''}"
html = html.replace(old_modal_passive_detail, "")

# Remove multiplier from modal active header
old_modal_act = "${(a.multiplier ? `<span class=\"active-mult\">계수 ${a.multiplier}x</span>` : '')}"
html = html.replace(old_modal_act, "")

# 6. Write to e:/브리미르/brimir_busters.html
with open('e:/브리미르/brimir_busters.html', 'w', encoding='utf-8') as out:
    out.write(html)

print("Successfully generated e:/브리미르/brimir_busters.html!")
