"""Build the complete, dependency-free learning page from content.json."""
import json
from html import escape as esc
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOPICS = json.loads((ROOT / 'content.json').read_text())

def item(text):
    before, sep, after = text.partition(':')
    if sep and len(before) <= 50:
        return f'<strong>{esc(before)}:</strong>{esc(after)}'
    return esc(text)

def chart(name):
    # All drawings are schematic. The accompanying text is the full explanation.
    axis = '<path class="axis" d="M30 12V132H185"/><text x="6" y="22">p</text><text x="179" y="155">x</text>'
    normal = '<path class="supply" d="M40 116L164 23"/><path class="demand" d="M40 23L164 116"/>'
    caption = ''
    extra = ''
    if name == 'gleichgewicht':
        extra = normal + '<path class="guide" d="M30 70H102V132"/><circle cx="102" cy="70" r="4"/><text x="111" y="68">E</text><text x="153" y="22">A</text><text x="158" y="113">N</text>'
        caption = 'A = Angebot, N = Nachfrage. E = Gleichgewicht. Gestrichelte Linien zeigen Preis und Menge.'
    elif name == 'extern':
        extra = normal + '<path class="shift" d="M40 86L135 15"/><circle cx="81" cy="54" r="4"/><circle cx="102" cy="70" r="4"/><path class="guide" d="M30 54H81V132M30 70H102V132"/>'
        caption = 'Petrol: private Kosten. Orange: einschließlich externer Kosten. Neues Gleichgewicht: Preis höher, Menge geringer.'
    elif name == 'monopol':
        extra = normal + '<path class="guide" d="M30 70H102V132M30 49H75V132"/><circle cx="102" cy="70" r="4"/><circle cx="75" cy="49" r="4"/><text x="48" y="43">M</text><text x="110" y="83">W</text>'
        caption = 'Vereinfachter Vergleich aus dem Unterricht: M = Monopol, W = Wettbewerb. Monopol: höherer Preis, geringere Menge.'
    elif name == 'mindestlohn':
        axis = axis.replace('>p<', '>L<')
        extra = normal + '<path class="floor" d="M30 44H179"/><path class="guide" d="M68 44V132M137 44V132"/><circle cx="68" cy="44" r="4"/><circle cx="137" cy="44" r="4"/>'
        caption = 'L = Lohn, x = Arbeit. Orange: bindender Mindestlohn. Links: nachgefragte Arbeit; rechts: angebotene Arbeit. Abstand = Angebotsüberschuss.'
    elif name == 'anomalie':
        axis = axis.replace('>p<', '>L<')
        extra = '<path class="supply" d="M170 19Q45 67 170 122"/><path class="guide" d="M30 71H180"/><text x="34" y="63">Existenz</text>'
        caption = 'L = Lohn, x = angebotene Arbeit. Unterhalb der Existenzsicherung: Lohn sinkt, angebotene Arbeit nimmt wieder zu.'
    return f'<figure><svg viewBox="0 0 200 165" role="img" aria-label="{esc(caption, quote=True)}">{axis}{extra}</svg><figcaption>{esc(caption)}</figcaption></figure>'

ids = set()
parts = []
short = ['Ordnung', 'Preise', 'Planwirt.', 'Markt', 'Güter', 'Monopole', 'Ext. Kosten', 'Arbeit', 'Soz. Markt', 'Sicherung']
options = ''.join(f'<option value="{t["id"]}">{i+1:02} {short[i]}</option>' for i,t in enumerate(TOPICS))
toc = ''.join(f'<li><a href="#{t["id"]}">{i+1:02} {esc(t["short"])}</a></li>' for i,t in enumerate(TOPICS))
for i, topic in enumerate(TOPICS):
    assert topic['id'] not in ids
    ids.add(topic['id'])
    blocks=[]
    jumps=''.join(f'<li><a href="#{b["id"]}">{esc(b["title"])}</a></li>' for b in topic['blocks'])
    for block in topic['blocks']:
        assert block['id'] not in ids
        ids.add(block['id'])
        tag='ol' if block['kind']=='steps' else 'ul'
        body=f'<{tag}>'+''.join(f'<li>{item(x)}</li>' for x in block['items'])+f'</{tag}>'
        if block['chart']: body+=chart(block['chart'])
        if block['note']: body+=f'<p class="note">{esc(block["note"])}</p>'
        blocks.append(f'<section class="block" id="{block["id"]}" aria-labelledby="{block["id"]}-title"><h3 id="{block["id"]}-title">{esc(block["title"])}</h3>{body}</section>')
    prev = f'<a href="#{TOPICS[i-1]["id"]}" rel="prev">← Zurück</a>' if i else '<a href="#anfang">↑ Anfang</a>'
    nxt = f'<a href="#{TOPICS[i+1]["id"]}" rel="next">Weiter →</a>' if i+1<len(TOPICS) else '<a href="#anfang">↑ Anfang</a>'
    parts.append(f'''<article class="chapter" id="{topic['id']}" tabindex="-1" aria-labelledby="{topic['id']}-title">
<p class="chapter-number">{i+1:02} / {len(TOPICS):02}</p><h2 id="{topic['id']}-title">{esc(topic['title'])}</h2>
<details class="local-toc"><summary>Unterthemen</summary><ul>{jumps}</ul></details>
{''.join(blocks)}<nav class="chapter-nav" aria-label="Nach {esc(topic['short'])}">{prev}{nxt}</nav></article>''')

html=f'''<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="disabled-adaptations" content="watch">
<meta name="theme-color" content="#f5f5ef">
<meta name="description" content="Wirtschaft-Lernzettel: Wirtschaftsordnung, Preisfunktionen, Planwirtschaft, Marktversagen, Arbeitsmarkt, soziale Marktwirtschaft und soziale Sicherung. Für kleine Bildschirme.">
<title>Wirtschaft · Lernzettel</title>
<link rel="icon" href="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E%3Crect width='64' height='64' rx='12' fill='%23295d53'/%3E%3Ctext x='32' y='46' text-anchor='middle' font-family='sans-serif' font-size='40' font-weight='700' fill='%23fff'%3EW%3C/text%3E%3C/svg%3E">
<link rel="stylesheet" href="style.css">
<script src="app.js" defer></script>
</head>
<body id="anfang">
<a class="skip-link" href="#lernstoff">Zum Lernstoff</a>
<div class="shell">
<header class="masthead"><p class="eyebrow">Lernzettel · Test bis 3.2</p><h1>Wirtschaft</h1></header>
<nav class="jump-nav" aria-label="Kapitelauswahl"><label class="sr-only" for="chapter-select">Kapitel auswählen</label><select id="chapter-select">{options}</select><noscript><p>Kapitel über die Übersicht auswählen.</p></noscript></nav>
<details class="full-toc"><summary>Alle Themen</summary><ol>{toc}</ol></details>
<main id="lernstoff">{''.join(parts)}</main>
<footer><details id="sources"><summary>Quellen & Ergänzungen</summary><p>Grundlage: deine Hefteinträge, Arbeitsblätter und Unterrichtsfolien. Stoffgrenze: soziale Sicherung einschließlich 3.2. Rentenreform und private Vorsorge aus Politik 1.4 sind ausgenommen.</p><p>Die Preisfunktionen und ihre Beispiele ergänzen den leeren Eintrag 1.2; die genaue Benennung eurer Vorlage ist nicht überliefert. Modell-Erklärungen, knappe Versicherungsaufgaben und die Falllösung sind zur Verständlichkeit ausgearbeitet.</p><ul><li><a href="https://verwaltung.uni-koeln.de/wirtschaft_und_finanzen/content/investitionscontrolling_beteiligungen_und_stiftungsmanagement/kosten__und_investitionscontrolling/kosten__und_leistungsrechnung/allgemein_zur_klr/klr__lexikon/data/preisfunktion/index_ger.html">Universität Köln: Preisfunktionen</a></li><li><a href="https://www.bundeswirtschaftsministerium.de/Redaktion/DE/Downloads/F/foresight-abschlusskonferenz-abschlussbericht.pdf?__blob=publicationFile&amp;v=26">Wirtschaftsministerium: Preismechanismus</a></li><li><a href="LERNZETTEL.md">Gesamter Lernstoff als Text</a></li></ul><p>Historische Geldbeträge und Begriffe aus den Arbeitsblättern sind keine Angaben zum aktuellen Stand.</p></details><a class="back-top" href="#anfang">↑ Zum Anfang</a></footer>
</div>
</body></html>
'''
(ROOT/'index.html').write_text(html)
md=['# Wirtschaft – Lernzettel','Stoff bis einschließlich 3.2. Grundlage: Unterrichtsmaterial; Ergänzungen siehe QUELLEN.md.']
for t in TOPICS:
    md+=['', '## '+t['title']]
    for b in t['blocks']:
        md+=['','### '+b['title'],'']+['- '+x for x in b['items']]
        if b['note']: md+=['','Hinweis: '+b['note']]
(ROOT/'LERNZETTEL.md').write_text('\n'.join(md)+'\n')
print(f'Built {len(TOPICS)} chapters, {len(ids)-len(TOPICS)} blocks, {len(html.encode())} bytes HTML.')
