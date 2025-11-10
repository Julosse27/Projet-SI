import asyncio
from bleak import BleakScanner

async def scanner_bluetooth():
    devices = await BleakScanner.discover()
    for device in devices:
        print(f"Nom: {device.name}")
        print(f"Adresse MAC: {device.address}")
        print("-" * 50)

asyncio.run(scanner_bluetooth())