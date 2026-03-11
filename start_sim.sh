#!/bin/zsh

# --- 1. Vyčistenie starých procesov ---
echo "🧹 Čistím staré procesy..."
pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"

# --- 2. Spustenie Mozgu (ArduPilot) v novom okne ---
echo "🧠 Spúšťam ArduPilot SITL v Bratislave..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source ~/.zshrc && sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --location=48.148598,17.107748,0,0 --map --console"'

# --- 3. Spustenie Sveta (Gazebo Server) v novom okne ---
echo "🌍 Spúšťam Gazebo Server..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source ~/.zshrc && gz sim -s iris_runway.sdf"'

# --- 4. Spustenie Očí (Gazebo GUI) v novom okne ---
echo "👁️ Spúšťam Gazebo GUI..."
osascript -e 'tell app "Terminal" to do script "cd '$PWD' && source ~/.zshrc && gz sim -g"'

echo "✅ Simulácia sa štartuje v nových oknách."
echo "💡 Nezabudni kliknúť na PLAY v Gazebo a potom spustiť: source drone_cmd.sh"
