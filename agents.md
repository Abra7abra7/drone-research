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
1. **Turbo Start**: `./start_sim.sh` (Opens 3 terminal windows automatically).
2. **Setup Drone**: Click **PLAY** in Gazebo, then run `./drone_cmd.sh`.
3. **Start Mission**: `uv run python fly.py`

### Detailed Workflow (Manual)
1. **Kill processes**: `pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"`
2. **SITL (T1)**: `sim_vehicle.py -v ArduCopter -f gazebo-iris --model JSON --map --console`
   - In MAVProxy: `param set ARMING_SKIPCHK 64`, `rc 3 1000`, `output add 127.0.0.1:14551`.
3. **GZ Server (T2)**: `gz sim -s iris_runway.sdf`
4. **GZ GUI (T3)**: `gz sim -g` (Press **PLAY**).
5. **Mission (T4)**: `uv run python fly.py`

## Critical Configuration Notes
- **Lock-step**: Set to `0` in `iris_with_gimbal/model.sdf` for macOS stability.
- **Port 14550**: Reserved for **QGroundControl** (Standard MAVProxy output).
- **Port 14551**: Dedicated to **MAVSDK** (`fly.py`) via `udpin://0.0.0.0:14551`.
- **Arming Bypass**: Use `ARMING_SKIPCHK = 64` for ArduCopter 4.8.0-dev in simulation.
- **GPU Acceleration**: Metal (MPS) is enabled and verified for PyTorch.

## Core Logic Files
- `fly.py`: Main autonomous mission script using MAVSDK async patterns.
- `pyproject.toml`: Modern project configuration (uv).
- `docs/architecture_setup.md`: Full architectural deep-dive.
