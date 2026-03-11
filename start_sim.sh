#!/bin/zsh

# --- 1. Vyčistenie starých procesov a dát ---
echo "🧹 Čistím staré procesy a dočasné súbory drona..."
pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"
rm -f eeprom.bin mav.parm mav.tlog mav.tlog.raw

# --- 2. Spustenie Mozgu (ArduPilot) v novom okne ---
echo "🧠 Spúšťam ArduPilot SITL (Bratislava)..."
# DÔLEŽITÉ: 
# --add-param-file = vypne kontroly a stiahne plyn (RC3)
# --out = automaticky vytvorí link pre MAVSDK (fly.py) na porte 14551
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && '$PWD'/.venv/bin/python ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --location=Bratislava --add-param-file='$PWD'/extra_params.parm --out=udp:127.0.0.1:14551 -w --map --console"'

# --- 3. Spustenie Sveta (Gazebo Server) v novom okne ---
echo "🌍 Spúšťam Gazebo Server..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && gz sim -s iris_runway.sdf"'

# --- 4. Spustenie Očí (Gazebo GUI) v novom okne ---
echo "👁️ Spúšťam Gazebo GUI..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && gz sim -g"'

echo "--------------------------------------------------"
echo "✅ Simulácia je pripravená na štart."
echo "1. Klikni na PLAY v Gazebo GUI."
echo "2. Počkaj, kým v SITL uvidíš 'GPS OK'."
echo "3. Spusti misiu: uv run python fly.py"
echo "--------------------------------------------------"
