# Architektúra a Nastavenie UAV Drone Research

Tento dokument vysvetľuje vnútorné fungovanie tvojho vývojového prostredia, komunikačné toky a dôležité konštanty.

## 1. Systémová Architektúra & Komunikácia

Celý stack funguje ako distribuovaný systém, kde jednotlivé komponenty komunikujú cez sieťové porty (localhost).

```mermaid
graph TD
    MAVSDK[MAVSDK Python Script] <-->|UDP 14551| MAVProxy[MAVProxy]
    QGC[QGroundControl] <-->|UDP 14550| MAVProxy
    MAVProxy <-->|TCP 5760| ArduPilot[ArduPilot SITL]
    ArduPilot <-->|UDP 9002| Gazebo[Gazebo Sim + Plugin]
    Gazebo <-->|GZ Transport| GUI[Gazebo GUI]
```

### Komunikačné kanály:
| Port | Protokol | Odosielateľ | Príjemca | Účel |
| :--- | :--- | :--- | :--- | :--- |
| **9002** | UDP | Gazebo Plugin | ArduPilot | Prenos dát zo senzorov a motory. |
| **5760** | TCP | ArduPilot | MAVProxy | Hlavný MAVLink prúd. |
| **14550** | UDP | MAVProxy | QGC | Výstup pre QGroundControl. |
| **14551** | UDP | MAVProxy | MAVSDK | Vyhradený port pre `fly.py`. |
| **5501** | UDP | sim_vehicle.py | ArduPilot | Vnútorný SITL konfiguračný port. |

---

## 2. Kľúčové Nastavenia

### Environmentálne Premenné (v `~/.zshrc`)
Tieto cesty umožňujú Gazebu nájsť tvoj skompilovaný plugin a modely bez toho, aby museli byť v systémových priečinkoch.
- `GZ_SIM_SYSTEM_PLUGIN_PATH`: Smeruje na `~/ardupilot_gazebo_install/lib/ardupilot_gazebo`.
- `GZ_SIM_RESOURCE_PATH`: Smeruje na modely a svety v `~/ardupilot_gazebo_install/share/...`.

### Model SDF (`iris_with_gimbal/model.sdf`)
- **Lock-step (0):** Je vypnutý. Pri hodnote 1 by Gazebo čakalo na ArduPilot pred každým fyzikálnym krokom. Na macOS to často spôsobuje "zmrznutie" simulátora, preto sme ho pre stabilitu vypli.
- **FDM Address (127.0.0.1):** Adresuje lokálny ArduPilot proces.

---

## 3. Postup pri Spúšťaní (Step-by-Step)

### A. Turbo Štart (Odporúčané)
1. Spusti `./start_sim.sh`.
2. V Gazebo klikni na **Play**.
3. Počkaj v okne SITL na `AP: ArduPilot Ready`.
4. Spusti misiu: `uv run python fly.py`.

### B. Manuálny postup (V prípade potreby)
Vždy dodržiavaj toto poradie:

1. **Čistenie:** `pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"`
2. **Autopilot (T1):** `sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --location=Bratislava --add-param-file=extra_params.parm --out=udp:127.0.0.1:14551 --map --console`
3. **Simulačný Server (T2):** `gz sim -s iris_runway.sdf`
4. **Simulačné GUI (T3):** `gz sim -g`
5. **Aktivácia:** V SITL počkaj na fix, v GUI klikni na **Play**.
6. **Misia (T4):** `uv run python fly.py`

---

## 4. Riešenie Problémov (FAQ)
- **"Link is down":** Zvyčajne znamená, že simulácia nie je v stave "Play" alebo nebeží Gazebo Server.
- **"Throttle too high":** Opravené v `extra_params.parm`. Ak sa objaví, skontroluj, či sa parameter korektne načítal pri štarte SITL.
- **"Address already in use":** Iný proces (napr. QGroundControl) blokuje porty. Použi `pkill -9 -f "mavproxy|arducopter"` a reštartuj.
- **Dron nerobí nič:** Skontroluj, či si v SITL uvidíš "GPS OK". V Bratislave trvá fix cca 10-30 sekúnd.
