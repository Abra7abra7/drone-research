import asyncio
from mavsdk import System

async def run():
    print("🚀 PRIPÁJAM SA K SIMULÁCIU (MAVSDK)...")
    
    drone = System()
    # Použijeme robustnejšie udpin spojenie na porte 14551
    await drone.connect(system_address="udpin://0.0.0.0:14551")

    print("📡 Čakám na spojenie s dronom...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Dron je online!")
            break

    print("🌍 Čakám na GPS fix...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("✅ GPS pripravený!")
            break

    print("🛫 Vzlietame do 5 metrov...")
    await drone.action.arm()
    await drone.action.takeoff()
    
    # Nastavíme výšku
    await drone.action.set_takeoff_altitude(5.0)

    await asyncio.sleep(10)

    print("🛬 Pristávame...")
    await drone.action.land()
    
    await asyncio.sleep(5)
    print("🏁 Misia dokončená.")

if __name__ == "__main__":
    asyncio.run(run())