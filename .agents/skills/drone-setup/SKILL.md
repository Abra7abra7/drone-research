---
name: drone-setup
description: Configure and troubleshoot the autonomous UAV development environment on macOS (Apple Silicon). Use this skill when a user asks how to set up the repository, when an ArduPilot build fails, when there are MAVSDK connection errors, or when the SITL simulation won't arm due to throttle or safety check issues. It ensures all dependencies like empy==3.3.4 and gnureadline are present and simulation parameters are correctly set via extra_params.parm.
---

# Drone Setup Skill

This skill provides a robust workflow for setting up and troubleshooting the ArduPilot + Gazebo + MAVSDK simulation environment on macOS.

## Core Setup Workflow

When asked to "set up" or "initialize" the environment, follow these steps:

### 1. Dependency Synchronization
Use `uv` to ensure all Python dependencies are present. The environment MUST have:
- `empy==3.3.4` (Critical for ArduPilot build)
- `gnureadline` (Critical for MAVProxy on macOS)
- `mavsdk`, `pymavlink`, `opencv-python`

**Command:**
```bash
uv sync
```

### 2. ArduPilot SITL Configuration
Ensure the simulation is "ready to fly" without manual intervention.
- Check for `extra_params.parm` in the root. If missing, create it with:
  ```text
  ARMING_SKIPCHK -1
  RC3_MIN 1000
  RC3_MAX 2000
  RC3_TRIM 1000
  RC3_REVERSED 0
  ```
- This bypasses all safety checks and resets the throttle at boot.

### 3. Verification of Plugin Paths
Ensure Gazebo can find the ArduPilot plugins. Check `~/.zshrc` or the current environment for:
- `GZ_SIM_SYSTEM_PLUGIN_PATH`
- `GZ_SIM_RESOURCE_PATH`

### 4. Cleanup & Reset
If the simulation hangs or ports are blocked:
**Command:**
```bash
pkill -9 -f "arducopter|gz|sim_vehicle|mavproxy"
```

## Troubleshooting Guide

### Issue: ArduPilot Build Fails
**Symptom:** `SIM_VEHICLE: Build failed` with `you need to install empy with 'python3 -m pip install empy==3.3.4'`.
**Solution:** `uv add empy==3.3.4` and `uv sync`.

### Issue: MAVProxy fails on start
**Symptom:** `ModuleNotFoundError: No module named 'gnureadline'`.
**Solution:** `uv add gnureadline` and `uv sync`.

### Issue: "Throttle too high" or Arming Fails
**Symptom:** Drone refused to arm via MAVSDK or MAVProxy.
**Solution:** Ensure `sim_vehicle.py` is called with `--add-param-file=extra_params.parm`. Verify `RC3_MIN` is 1000.

### Issue: Connection Refused (MAVSDK)
**Symptom:** `fly.py` hangs on "Waiting for drone...".
**Solution:** 
1. Ensure Gazebo is in **PLAY** mode.
2. Ensure `sim_vehicle.py` has an output mapping to `14551` (e.g., `--out=udp:127.0.0.1:14551`).

## Automated Start Script
Always recommend using `./start_sim.sh` as the primary entry point, as it consolidates all the above fixes.

## Example 1: Broken Build
User: "Skúšam spustiť simuláciu ale vyhodilo mi to Build Failed."
Agent: [Checks logs, finds empy error] -> "Chýba ti dôležitá závislosť empy. Pridávam ju do projektu..." -> `uv add empy==3.3.4` -> `uv sync`.

## Example 2: Clean Setup
User: "Mám nový Mac, ako tu rozbehnem ten drona?"
Agent: "Pripravím ti prostredie..." -> `uv sync` -> Verifikuje cesty k pluginom -> Vytvorí `extra_params.parm` -> Odporučí `./start_sim.sh`.
