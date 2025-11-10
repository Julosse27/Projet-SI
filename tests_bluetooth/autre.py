import asyncio
from bleak import BleakScanner, BleakClient

async def recuperer_nom_via_connexion(adresse_mac):
    """
    Tente de récupérer le nom en se connectant au périphérique
    """
    try:
        async with BleakClient(adresse_mac, timeout=5.0) as client:
            # Chercher le service Generic Access (0x1800) qui contient le nom
            for service in client.services:
                if service.uuid.startswith("00001800"):
                    for char in service.characteristics:
                        # Device Name characteristic (0x2A00)
                        if char.uuid.startswith("00002a00"):
                            nom_bytes = await client.read_gatt_char(char.uuid)
                            return nom_bytes.decode('utf-8', errors='ignore')
            return None
    except:
        return None

async def scanner_peripheriques(tenter_connexion=False):
    """
    Scanne les périphériques Bluetooth BLE à proximité
    """
    print("Recherche des périphériques Bluetooth...")
    print("(Cela peut prendre quelques secondes)\n")
    
    # Scanner pendant 10 secondes
    devices = await BleakScanner.discover(timeout=10.0)
    
    if not devices:
        print("Aucun périphérique Bluetooth trouvé.")
        return []
    
    print(f"Trouvé {len(devices)} périphérique(s) :\n")
    
    resultats = []
    for i, device in enumerate(devices, 1):
        nom = device.name if device.name else "Inconnu"
        
        # Si pas de nom et option activée, tenter connexion
        if nom == "Inconnu" and tenter_connexion:
            print(f"[{i}/{len(devices)}] Tentative de connexion pour récupérer le nom...")
            nom_connecte = await recuperer_nom_via_connexion(device.address)
            if nom_connecte:
                nom = nom_connecte
        
        print(f"Nom: {nom}")
        print(f"Adresse MAC: {device.address}")
        
        print("-" * 60)
        
        resultats.append({
            "nom": nom,
            "mac": device.address
        })
    
    return resultats

async def obtenir_infos_peripherique(adresse_mac):
    """
    Se connecte à un périphérique et récupère des informations détaillées
    """
    print(f"\nConnexion à {adresse_mac}...")
    
    try:
        async with BleakClient(adresse_mac) as client:
            print(f"Connecté: {client.is_connected}")
            
            # Récupérer les services disponibles
            print("\nServices disponibles:")
            for service in client.services:
                print(f"\nService: {service.uuid}")
                print(f"Description: {service.description}")
                
                for char in service.characteristics:
                    print(f"  - Caractéristique: {char.uuid}")
                    print(f"    Propriétés: {char.properties}")
    
    except Exception as e:
        print(f"Erreur lors de la connexion: {e}")

async def scanner_continu(duree=30):
    """
    Scanner en continu avec détection des nouveaux périphériques
    """
    print(f"Scanner continu pendant {duree} secondes...")
    print("Appuyez sur Ctrl+C pour arrêter\n")
    
    peripheriques_vus = set()
    
    def callback(device, advertising_data):
        if device.address not in peripheriques_vus:
            peripheriques_vus.add(device.address)
            nom = device.name if device.name else "Inconnu"
            print(f"[NOUVEAU] {nom} - MAC: {device.address}")
    
    try:
        scanner = BleakScanner(callback)
        await scanner.start()
        await asyncio.sleep(duree)
        await scanner.stop()
    except KeyboardInterrupt:
        print("\nScan arrêté.")

async def main():
    """
    Fonction principale avec menu interactif
    """
    while True:
        print("\n" + "="*60)
        print("SCANNER BLUETOOTH")
        print("="*60)
        print("1. Scanner les périphériques (rapide)")
        print("2. Scanner avec tentative de connexion (lent mais + de noms)")
        print("3. Scanner en continu")
        print("4. Se connecter à un périphérique")
        print("5. Quitter")
        print("="*60)
        
        choix = input("\nVotre choix: ")
        
        if choix == "1":
            peripheriques = await scanner_peripheriques(tenter_connexion=False)
            
        elif choix == "2":
            print("\n⚠️  Ce mode est plus lent car il tente de se connecter à chaque périphérique")
            peripheriques = await scanner_peripheriques(tenter_connexion=True)
            
        elif choix == "3":
            duree = input("Durée du scan (secondes, défaut=30): ")
            duree = int(duree) if duree.isdigit() else 30
            await scanner_continu(duree)
            
        elif choix == "4":
            mac = input("Entrez l'adresse MAC: ")
            await obtenir_infos_peripherique(mac)
            
        elif choix == "5":
            print("Au revoir!")
            break
            
        else:
            print("Choix invalide.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nProgramme arrêté.")