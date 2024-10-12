import random
from flask import Flask, json, render_template, render_template_string, request, jsonify


app = Flask(__name__)

# Liste zur Speicherung der JSON-Objekte
json_list = []
context = ('certificates/cert.pem', 'certificates/key.pem')
data_path = "data.json"

# GET-Route: Gibt die Liste der JSON-Dateien zurück
@app.route('/json', methods=['GET'])
def get_json_list1():
    return jsonify(json_list)

@app.route('/json/', methods=['GET'])
def get_json_list2():
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
        new_json = request.get_json()
        json_list.append(new_json)
        on_shutdown()
        return jsonify({"message": "JSON hinzugefügt!", "data": new_json}), 201
    else:
        return jsonify({"message": "Request ist kein JSON!"}), 400

@app.route('/json/', methods=['POST'])
def add_json_to_list2():
    if request.is_json:
        new_json = request.get_json()
        json_list.append(new_json)
        on_shutdown()
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
        "erstellerId": random.randint(1, 1000)  # Zufällige Ersteller-ID zwischen 1 und 1000
        }
        json_list.append(eintrag)
    
    on_shutdown()
    return jsonify({"message": "Json wurde hinzugefügt","data":json_list}),201

@app.route('/panel')
def control_panel():
    return render_template('control_panel.html')

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
    app.run(host='0.0.0.0', port=5000,ssl_context = context)

    
