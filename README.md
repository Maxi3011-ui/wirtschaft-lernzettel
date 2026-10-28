# Wirtschaft – Lernzettel

**Live:** https://maxi3011-ui.github.io/wirtschaft-lernzettel/

Lernstoff für den Wirtschaftstest am 29.10.2026: kompakt, direkt auffindbar und für Apple Watch, Handy sowie Browserdruck gestaltet.

## Stoff

1. Wirtschaftsordnung: Aufgaben und vier Grundfragen.
2. Preisfunktionen, Angebot/Nachfrage und Marktgleichgewicht.
3. Zentralverwaltungswirtschaft / Planwirtschaft: Merkmale, Planung und Probleme.
4. Freie Marktwirtschaft als Vergleichsgrundlage.
5. Öffentliche Güter und Trittbrettfahrerproblem.
6. Unvollkommener Wettbewerb: Monopole, Kartelle und staatliche Maßnahmen.
7. Externe Kosten, Internalisierung und Emissionshandel.
8. Arbeitsmarkt: Gerechtigkeit, anomales Arbeitsangebot, Mindestlohn und Elastizität.
9. Soziale Marktwirtschaft: Leitprinzip, Freiheiten, Strukturelemente und staatliche Aufgaben.
10. Soziale Sicherung bis einschließlich 3.2: Versicherungen, fünf Prinzipien und Fall Max.

Grundlage sind die bereitgestellten Unterrichtsunterlagen und die angekündigte Stoffliste. Die Preisfunktionen ergänzen den nur mit einer Überschrift gefüllten Eintrag 1.2. Ergänzungen und Zuordnungen sind in [QUELLEN.md](QUELLEN.md) dokumentiert. Geldanlage, Banken und die Rentendiskussion aus Politik-Kapitel 1.4 sind ausgenommen. Originalscans, PDFs und persönliche Dateipfade werden nicht mitveröffentlicht.

## Bedienung und kleine Bildschirme

Native Kapitelauswahl bleibt beim Scrollen erreichbar. „Unterthemen“ öffnet Sprunglinks innerhalb eines Kapitels; der Lernstoff selbst bleibt vollständig sichtbar. „Zurück“ und „Weiter“ verbinden benachbarte Kapitel. Kapitel und Abschnitte lassen sich direkt per URL öffnen, etwa `#preisfunktionen`, `#mindestlohn` und `#fall-max`.

Einspaltiger Aufbau ab 160 CSS-Pixeln, Systemschrift, mindestens 44 Pixel hohe Bedienelemente, keine externen Schriften oder Laufzeitbibliotheken. Automatisches helles/dunkles Farbschema. Kein Login, Tracking oder Werbung. Vollständiger Lernstoff steht bereits im HTML; JavaScript verbessert nur die Navigation. [LERNZETTEL.md](LERNZETTEL.md) enthält die Textfassung.

Die Darstellung wurde mit Chromium und WebKit bei 160, 176, 184, 198, 224, 320, 390 und 1280 CSS-Pixeln geprüft. Ein physisches Apple-Watch-Gerät war für die Prüfung nicht verfügbar; die tatsächliche watchOS-Webansicht kann abweichen.

## Bearbeiten und lokal öffnen

`content.json` enthält den Lernstoff; `build.py` erzeugt `index.html` und `LERNZETTEL.md`. `style.css` und `app.js` enthalten Darstellung und Navigation.

```sh
python3 build.py
python3 -m http.server 8892 --bind 127.0.0.1
```

Danach http://127.0.0.1:8892 öffnen. GitHub Pages veröffentlicht aus `main` und dem Stammverzeichnis. Keine Installation und kein Build auf GitHub erforderlich.
