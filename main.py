import asyncio
from mavsdk import System

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14551")

    print("📡 Čakám na drona...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"✅ Dron pripojený!")
            break

    print("🔍 Kontrola senzorov (čakám na GPS fix)...")
    async for health in drone.telemetry.health():
        print(f"   [Stav: GPS={health.is_global_position_ok}, Home={health.is_home_position_ok}]")
        if health.is_global_position_ok and health.is_home_position_ok:
            print("👍 Všetko pripravené na štart!")
            break
        await asyncio.sleep(1) # Počkáme sekundu pred ďalšou kontrolou

    print("-- Aktivujem motory (ARMING)")
    try:
        await drone.action.arm()
    except Exception as e:
        print(f"❌ Arming zlyhal: {e}")
        return

    print("-- ŠTART (Takeoff na 5 metrov)")
    await drone.action.takeoff()

    await asyncio.sleep(10)

    print("-- Pristávam (LAND)")
    await drone.action.land()

if __name__ == "__main__":
    asyncio.run(run())