#!/bin/zsh

# Tento skript pošle potrebné príkazy priamo do bežiaceho drona
# Používa mavproxy.py na pozadí pre jednorazový zápis

echo "📡 Posielam konfiguračné príkazy do drona..."

# MAVProxy 'shortcuts' cez UDP kanál
mavproxy.py --master=udp:127.0.0.1:14550 --cmd="param set ARMING_SKIPCHK 64; rc 3 1000; output add 127.0.0.1:14551; exit" --nowait

echo "✅ Konfigurácia úspešná: ARMING_SKIPCHK=64, Throttle=1000, Port 14551 pridaný."
echo "🚀 Teraz môžeš spustiť misiu: uv run python fly.py"
