# Startanleitung für Mario Kart Wii Profi AI

**Note:** If you encounter a "socket module not found" error when loading the Lua script, this repository includes a fix. See `SOCKET_FIX.md` for details.

## 1. Dolphin vorbereiten
1. Starte Dolphin Emulator und lade Mario Kart Wii.
2. Wähle den gewünschten Track.
3. Starte das Rennen, aber noch ohne manuelle Steuerung.
4. Lua-Scripting aktivieren:
   - Gehe zu 'Tools -> Lua Scripting' in Dolphin.
   - Lade das Skript 'dolphin/lua/mkw_pro_ai.lua'.

## 2. Python-Environment starten
1. Terminal im Ordner 'python/' öffnen.
2. Libraries installieren:
   ```bash
   pip install -r requirements.txt
   ```
3. RL-Loop starten:
   ```bash
   python mk_pro_ai_loop.py
   ```
- Agent verbindet sich via UDP mit Lua.
- Empfängt Kart- und Gegnerdaten.
- Berechnet Actions und sendet sie zurück an Dolphin.

## 3. Ablauf während des Rennens
- Lua sendet State-Daten pro Frame an Python.
- Python berechnet Reward und Action, speichert Transition.
- Lua setzt Buttons (Drift, Wheelie, Gas, Bremse, Items).
- Python loggt Stats für Visualisierung.

## 4. Tipps
- Erst nur ein Rennen testen, um UDP-Verbindung zu prüfen.
- Ports 12345/12346 müssen frei sein.
- Logging hilft, Verhalten zu analysieren.
- Nach mehreren Rennen Stats mit 'stats_plot.py' auswerten.