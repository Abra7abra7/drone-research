import asyncio
from mavsdk import System
from mavsdk.offboard import VelocityBodyYawspeed

async def run():
    drone = System()
    await drone.connect(system_address="udpin://0.0.0.0:14551")

    print("📡 Čakám na spojenie...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print("✅ Pripojené!")
            break

    print("🌍 Čakám na GPS fix...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok:
            print("✅ GPS fix získaný!")
            break

    print("🛫 Vzlietam do 10 metrov...")
    await drone.action.arm()
    await drone.action.set_takeoff_altitude(10.0)
    await drone.action.takeoff()
    await asyncio.sleep(12) # Počkáme na dosiahnutie výšky

    print("🚀 Prechádzam na Offboard Control...")
    # Nastavíme počiatočnú rýchlosť 0 pre bezpečnú aktiváciu
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    
    try:
        await drone.offboard.start()
    except Exception as e:
        print(f"❌ Chyba štartu Offboard: {e}")
        await drone.action.land()
        return

    # 1. Let vpred k budove
    print("🏙️ Letím k budove (5m/s vpred)...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(5.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(6) # Letíme 30 metrov

    # 2. Pomalý oblet a stúpanie (Inšpekcia)
    print("🔍 Stúpam a robím inšpekciu (hore 2m/s)...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, -2.0, 0.0))
    await asyncio.sleep(3) # Stúpneme o 6 metrov

    # 3. Návrat späť
    print("🏠 Návrat do počiatočného bodu...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(-5.0, 0.0, 2.0, 0.0))
    await asyncio.sleep(6) # Letíme späť a klesáme na pôvodnú výšku

    # 4. Zastavenie
    print("🛑 Zastavujem...")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))
    await asyncio.sleep(2)

    await drone.offboard.stop()
    print("🛬 Pristávam...")
    await drone.action.land()
    
    await asyncio.sleep(5)
    print("🏁 Pokročilá misia (Offboard) dokončená.")

if __name__ == "__main__":
    asyncio.run(run())
