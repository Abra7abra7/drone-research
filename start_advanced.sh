#!/bin/zsh

# --- 1. Vyčistenie starých procesov ---
echo "🧹 Čistím prostredie pre Advanced misiu..."
pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"
rm -f eeprom.bin mav.parm mav.tlog mav.tlog.raw

# --- 2. Spustenie Mozgu (ArduPilot) ---
# Používame rovnaký ArduPilot, ale pripájame MAVSDK na port 14551
echo "🧠 Spúšťam ArduPilot SITL..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && '$PWD'/.venv/bin/python ardupilot/Tools/autotest/sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --location=Bratislava --add-param-file='$PWD'/extra_params.parm --out=udp:127.0.0.1:14551 -w --map --console"'

# --- 3. Spustenie Advanced Sveta (Gazebo Server) ---
echo "🌍 Spúšťam Gazebo Server (Advanced World)..."
# Používame absolútnu cestu k lokálnemu .sdf súboru
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && gz sim -s '$PWD'/ardupilot_gazebo/worlds/advanced_world.sdf"'

# --- 4. Spustenie Očí (Gazebo GUI) ---
echo "👁️ Spúšťam Gazebo GUI..."
# Čakáme chvíľu, kým server naskočí
sleep 3
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source '$PWD'/.venv/bin/activate && gz sim -g"'

echo "--------------------------------------------------"
echo "🚀 ADVANCED SIMULÁCIA JE PRIPRAVENÁ"
echo "1. V Gazebo klikni na PLAY (oranžové tlačidlo vľavo dole)."
echo "2. V SITL termináli počkaj, kým uvidíš 'GPS OK'."
echo "3. Spusti misiu: uv run python advanced_mission.py"
echo "--------------------------------------------------"
