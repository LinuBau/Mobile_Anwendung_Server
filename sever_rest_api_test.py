import random
import time
from flask import Flask, json, render_template, render_template_string, request, jsonify
import os


app = Flask(__name__)

# Liste zur Speicherung der JSON-Objekte
json_list = []
chats = {}
context = ('certificates/cert.pem', 'certificates/key.pem')
data_path = "data.json"
base_Url = "./user_data"

# GET-Route: Gibt die Liste der JSON-Dateien zurück
@app.route('/json', methods=['GET'])
def get_json_list1():
    json_list = on_start()
    return jsonify(json_list)

@app.route('/json/', methods=['GET'])
def get_json_list2():
    on_start()
    return jsonify(json_list)

@app.route('/delete',methods = ['GET'])
def delete_json_list():
    json_list.clear()
    on_shutdown()
    return jsonify({"message":"JSON List wurde gelöscht"}),201

# POST-Route: Fügt ein neues JSON-Objekt zur Liste hinzu
@app.route('/json', methods=['POST'])
def add_json_to_list1():
    if request.is_json:
        send_json = request.get_json()
        new_json = {
            "AnzeigeName": send_json.get("AnzeigeName") ,
            "Beschreibung": send_json.get("Beschreibung") ,
            "erstellerId": send_json.get("erstellerId"),
            "timestamp": int(time.time() * 1000)
        }
        json_list.append(new_json)
        on_shutdown()
        return jsonify({"message": "JSON hinzugefügt!", "data": new_json}), 201
    else:
        return jsonify({"message": "Request ist kein JSON!"}), 400

@app.route('/json/', methods=['POST'])
def add_json_to_list2():
    if request.is_json:
        send_json = request.get_json()
        new_json = {
            "AnzeigeName": send_json.get("AnzeigeName") ,
            "Beschreibung": send_json.get("Beschreibung") ,
            "ErstellerId": send_json.get("ErstellerId"),
            "timestamp": int(time.time() * 1000)
        }
        return jsonify({"message": "JSON hinzugefügt!", "data": new_json}), 201
    else:
        return jsonify({"message": "Request ist kein JSON!"}), 400
    
@app.route('/create/',methods=['GET'])
def create_list():
    anzeige_namen = [
    "TechNova", "CreativeSolutions", "EcoWave", "SpeedyTech", "CyberGuru", 
    "InnovateNow", "BrightFuture", "DreamVision", "SmartWorld", "CodeMasters", 
    "FutureMinds", "VisionaryTech", "QuantumLeap", "NextGenTech", "AlphaWave", 
    "GreenEnergy", "TechSavvy", "EcoMinds", "BlueHorizon", "InfinityTech", 
    "MindBloom", "BrightIdeas", "StartUpGenius", "DynamicDreams", "DigitalEra", 
    "GigaPulse", "NeonInnovation", "SparkSolutions", "QuantumVision", "EpicCreators", 
    "BrightStar", "DeepDiveTech", "FutureVision", "SmartEco", "BrightTech", 
    "CreativeWaves", "NextEra", "DreamTech", "TechFusion", "VisionaryMinds", 
    "DynamicForce", "SolarTech", "QuantumMinds", "InnovationHub", "TechWhizz", 
    "BrightSky", "EcoFutures", "BrightMinds", "CodeCraft", "EpicInnovators"
]
    beschreibungen = [
    "Innovatives Startup", "Technologisches Powerhouse", "Nachhaltige Lösungen", "Schnelle Entwicklungen", 
    "Führend in der Technologie", "Kreative Visionen", "Zukunftsorientiert", "Erstellt die Welt von morgen", 
    "Smarter Tech für alle", "Fortschrittliche Softwarelösungen", "Visionäre Projekte", "Quantum-Innovation", 
    "Entwicklungen der nächsten Generation", "Die nächste große Sache", "Neue Energie", 
    "Umweltfreundlich und zukunftsweisend", "Tech mit Verstand", "Führend in grüner Technologie", 
    "Lösungen für morgen", "Grenzenlose Möglichkeiten", "Ideen sprießen", "Technologie der Zukunft", 
    "Für kreative Unternehmer", "Revolutionäre Träume", "Digitaler Fortschritt", "Hochleistungs-Technologie", 
    "Zukunftsweisende Innovationen", "Lösungen, die strahlen", "Technologie für den Fortschritt", 
    "Einfallsreiche Schöpfer", "Sterne, die leuchten", "Tiefgehende Innovation", "Visionäre von morgen", 
    "Technologie für eine grüne Welt", "Ideen, die strahlen", "Kreative Köpfe", "Die Zukunft gestalten", 
    "Träume werden wahr", "Technologie trifft Kreativität", "Die Zukunft formen", "Zukunftsvisionäre", 
    "Dynamische Kräfte", "Solare Technologien", "Denken in Quanten", "Innovationszentrum", "Tech-Zauberer", 
    "Helle Zukunft", "Nachhaltige Technologien", "Glänzende Ideen", "Code-Handwerk", "Bahnbrechende Innovationen"
    ]
    
    
    for i in range(50):
        eintrag = {
        "AnzeigeName": random.choice(anzeige_namen),
        "Beschreibung": random.choice(beschreibungen),
        "erstellerId": random.randint(1000,9998),  # Zufällige Ersteller-ID zwischen 1 und 1000
        "timestamp" : int(time.time() * 1000) - random.randint(10,100)
        }
        json_list.append(eintrag)
    
    on_shutdown()
    return jsonify({"message": "Json wurde hinzugefügt","data":json_list}),201

@app.route('/panel')
def control_panel():
    return render_template('control_panel.html')

@app.route('/getUserId',methods = ['GET'])
def createUserID():
    # useridd 9999 ist für die den fall das diese nicht zu geteil werden kann
    userid = random.randint(1000,9998)
    eintrag = {
        "AnzeigeName": "",
        "Beschreibung":  "",
        "erstellerId": userid  # Zufällige Ersteller-ID zwischen 1 und 1000
        }
    create_user_folder(userid)
    return jsonify(eintrag)

@app.route('/getUserId',methods = ['POST'])
def validetUserID():
    if request.is_json:
        user_id = request.get_json()
        user_path = os.path.join(base_Url,str(user_id))
        if os.path.exists(user_path):
            return jsonify(user_id), 200
        
    return jsonify({'error': 'Path dos not exist'}),400 

def generate_chat_id(user1_id, user2_id):
    return f"chat_{sorted([user1_id, user2_id])[0]}_{sorted([user1_id, user2_id])[1]}"

def get_user_id_from_keys():
     sorted_keys = []
     keys = chats.keys()
     for key in keys:
        parts =  key.split('_')
        sorted_keys.append(sorted([int(parts [1]),int(parts [2])]))     
     print(sorted_keys)
     return sorted_keys
     
     

def ensure_user_directory(user_id):
    """Erstellt den Benutzerordner, falls nicht vorhanden"""
    user_dir = os.path.join(base_Url, user_id)
    if not os.path.exists(user_dir):
        os.makedirs(user_dir)
    return user_dir

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.json
    if not data or 'sender' not in data or 'receiver' not in data or 'message' not in data:
        return jsonify({'error': 'Fehlende Daten'}), 400
    
    # Generiere oder hole Chat-ID
    chat_id = generate_chat_id(data['sender'], data['receiver'])
    
    # Erstelle neue Nachrichtenliste falls noch nicht vorhanden
    if chat_id not in chats:
        chats[chat_id] = []
    
    # Füge neue Nachricht hinzu
    message = {
        'sender': data['sender'],
        'receiver': data['receiver'],
        'message': data['message'],
        'timestamp': int(time.time() * 1000),  # Unix Timestamp in Millisekunden
        'message_id': len(chats[chat_id])  # Message-ID innerhalb des Chats
    }
    
    chats[chat_id].append(message)
    
    
    return jsonify({
        'status': 'erfolg',
        'chat_id': chat_id,
        'message_id': message['message_id'],
        'timestamp': message['timestamp']
    })

@app.route('/get_messages/<user1_id>/<user2_id>', methods=['GET'])
def get_messages(user1_id, user2_id):
    chat_id = generate_chat_id(user1_id, user2_id)
    
    if chat_id not in chats:
        return jsonify([])
    
    chat =[]
    for message in chats[chat_id]:
        chat.append({
            'sender' : message['sender'],
            'receiver': message['receiver'],
            'message': message['message']
        })
    
    return jsonify({
         chats[chat_id]
    })
@app.route('/getkeysWith/<user_id>',methods = ['GET'])
def get_keys(user_id):
    user_id = int(user_id)
    user_id_chats = []
    keys = get_user_id_from_keys()
    for paar in keys:
        print(user_id)
        print(user_id in paar)
        if  user_id in paar:
            print(paar)
            user_id_chats.append(paar[0] if paar[0] != user_id else paar[1])
    print(user_id_chats)
    return jsonify(user_id_chats)
        

def save_chat(chat_id, messages, sender_id, receiver_id):
    """Speichert den Chat für beide Benutzer"""
    # Speichere für Sender
    sender_dir = ensure_user_directory(sender_id)
    sender_file = os.path.join(sender_dir, f"{chat_id}.json")
    with open(sender_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)
    
    # Speichere für Empfänger
    receiver_dir = ensure_user_directory(receiver_id)
    receiver_file = os.path.join(receiver_dir, f"{chat_id}.json")
    with open(receiver_file, 'w', encoding='utf-8') as f:
        json.dump(messages, f, ensure_ascii=False, indent=4)

def load_all_chats():
    """Lädt alle eindeutigen Chats aus allen Benutzerordnern"""
    all_chats = {}
    
    # Durchsuche alle Benutzerordner
    if os.path.exists(base_Url):
        for user_dir in os.listdir(base_Url):
            user_path = os.path.join(base_Url, user_dir)
            if os.path.isdir(user_path):
                # Durchsuche alle Chat-Dateien im Benutzerordner
                for chat_file in os.listdir(user_path):
                    if chat_file.endswith('.json'):
                        file_path = os.path.join(user_path, chat_file)
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                chat_data = json.load(f)
                                # Verwende den ersten und letzten Benutzer als Schlüssel
                                if chat_data:  # Prüfe ob Chat nicht leer ist
                                    first_msg = chat_data[0]
                                    chat_key = generate_chat_id(
                                        first_msg['sender'],
                                        first_msg['receiver']
                                    )
                                    # Speichere nur wenn noch nicht vorhanden oder neuer
                                    if chat_key not in all_chats or \
                                       len(chat_data) > len(all_chats[chat_key]):
                                        all_chats[chat_key] = chat_data
                        except (json.JSONDecodeError, IndexError, KeyError) as e:
                            print(f"Fehler beim Laden von {file_path}: {e}")
                            continue
    
    return all_chats

    
 
def create_user_folder(user_id):  
    user_folder_path = os.path.join(base_Url,str(user_id))
    try:
        if not os.path.exists(user_folder_path):
            os.makedirs(user_folder_path)
            return jsonify({"status": "success", "message": f"Folder created for user {user_id}."}), 201
        else:
            return jsonify({"status": "info", "message": f"Folder for user {user_id} already exists."}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
    


def on_shutdown():
    with open(data_path,"w") as outfile:
        json.dump(json_list,outfile,indent = 4)
    return jsonify({"message":"JSON List wurde gelöscht"}),201        

def on_start():
    with open(data_path,"r") as input:
        data = json.loads(input.read())
        return data 





    
# Startet den Server
if __name__ == '__main__':
    json_list = on_start()
    c=generate_chat_id(1001,5500)
    message = {
        'sender': 1001,
        'receiver': 5667,
        'message': 'Hallü',
        'timestamp': int(time.time() * 1000),  # Unix Timestamp in Millisekunden
        'message_id': hash(c)  # Message-ID innerhalb des Chats
    }
    chats[c] = []
    chats[c].append(message)

    
    app.run(host='0.0.0.0', port=5000,ssl_context = context)

    
