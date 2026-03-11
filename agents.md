# UAV Research & AI Development Agent Context

## Project Overview
This repository is a specialized development environment for autonomous UAVs (Drones) on Apple Silicon (M4/M3). It integrates ArduPilot flight control, Gazebo simulation, and MAVSDK for AI-driven missions.

## Tech Stack
- **Flight Controller**: ArduPilot (SITL) compiled natively for arm64.
- **Simulator**: Gazebo Harmonic (GZ Sim).
- **Control API**: MAVSDK (Python) with `uv` for package management.
- **AI/ML**: PyTorch with **MPS (Metal Performance Shaders)** acceleration enabled.
- **Dependencies**: `mavsdk`, `pymavlink`, `opencv-python`, `torch`, `torchvision`, `numpy`.

## Key Paths & Environment
- **ArduPilot Source**: `/Users/abra/Developer/drones/drone-research/ardupilot`
- **Gazebo Plugins**: `/Users/abra/ardupilot_gazebo_install`
- **Plugin Paths**: Defined in `~/.zshrc` via `GZ_SIM_SYSTEM_PLUGIN_PATH` and `GZ_SIM_RESOURCE_PATH`.
- **Python Setup**: Managed by `uv`, uses `.venv`.

## Simulation Workflow (Quick Start)
1. **Cleanup (Orderly Reset)**: `pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"`
2. **Turbo Start**: `./start_sim.sh`
   - This cleans old processes, builds ArduPilot (if needed), sets Bratislava location, and links MAVSDK.
3. **Setup Drone**: Wait for `AP: ArduPilot Ready` in SITL, then click **PLAY** in Gazebo.
4. **Start Mission**: `uv run python fly.py`

### Detailed Workflow (Manual)
1. **Kill processes**: `pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"`
2. **SITL (T1)**: `sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --location=Bratislava --add-param-file=extra_params.parm --out=udp:127.0.0.1:14551 --map --console`
3. **GZ Server (T2)**: `gz sim -s iris_runway.sdf`
4. **GZ GUI (T3)**: `gz sim -g` (Press **PLAY** after SITL is ready).
5. **Mission (T4)**: `uv run python fly.py`

## Critical Configuration Notes
- **Lock-step**: Set to `0` in `iris_with_gimbal/model.sdf` for macOS stability.
- **Port 14550**: Reserved for **QGroundControl** (Standard MAVProxy output).
- **Port 14551**: Dedicated to **MAVSDK** (`fly.py`) via `udpin://0.0.0.0:14551`.
- **Arming Bypass**: Use `ARMING_SKIPCHK = -1` in `extra_params.parm` for ArduCopter 4.8.0-dev.
- **Throttle Reset**: `extra_params.parm` forces `RC3_MIN=1000` to prevent "Throttle too high" errors.
- **Dependencies**: Ensure `gnureadline` and `empy==3.3.4` are installed in `.venv`.

## Core Logic Files
- `fly.py`: Main autonomous mission script using MAVSDK async patterns.
- `advanced_mission.py`: Advanced autonomous mission script using Offboard control for dynamic velocity-based navigation.
- `extra_params.parm`: Critical SITL parameter overrides (Arming & Throttle).
- `pyproject.toml`: Modern project configuration (uv).
- `docs/architecture_setup.md`: Full architectural deep-dive.

## Advanced Simulation Workflow (Offboard Control)
For testing more complex autonomy, an advanced environment is provided:
1. **Turbo Start**: `./start_advanced.sh`
   - Launches SITL, Gazebo Server with `advanced_world.sdf`, and Gazebo GUI cleanly.
2. **Setup Drone**: Wait for `AP: ArduPilot Ready` in SITL, then click **PLAY** in Gazebo.
3. **Start Mission**: `uv run python advanced_mission.py`
   - This script demonstrates Offboard mode, which is highly recommended for AI-driven maneuvers (like obstacle avoidance via computer vision), as it sidesteps issues with MAVSDK's Mission API in SITL.
