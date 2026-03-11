from mavsdk.offboard import VelocityBodyYawspeed
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
    await drone.action.set_takeoff_altitude(5.0)
    await drone.action.takeoff()
    
    await asyncio.sleep(10)

    print("🚀 Prepínam na Offboard a letíme 20 metrov dopredu...")
    # Pred štartom Offboard módu musíme poslať aspoň jednu sadu príkazov
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    
    try:
        await drone.offboard.start()
    except Exception as e:
        print(f"❌ Chyba štartu Offboard: {e}")
        await drone.action.land()
        return

    # Letíme rýchlosťou 5m/s po dobu 4 sekúnd (spolu 20 metrov)
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(5.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(4)

    # Zastavíme a prepneme späť
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)
    await drone.offboard.stop()

    print("🛬 Pristávame...")
    await drone.action.land()
    
    await asyncio.sleep(5)
    print("🏁 Misia dokončená.")

if __name__ == "__main__":
    asyncio.run(run())