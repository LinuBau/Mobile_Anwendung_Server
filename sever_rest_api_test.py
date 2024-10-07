import random
from flask import Flask, json, render_template_string, request, jsonify

app = Flask(__name__)

# Liste zur Speicherung der JSON-Objekte
json_list = []
context = ('certificates/cert.pem', 'certificates/key.pem')

# GET-Route: Gibt die Liste der JSON-Dateien zurück
@app.route('/json', methods=['GET'])
def get_json_list1():
    return jsonify(json_list)

@app.route('/json/', methods=['GET'])
def get_json_list2():
    return jsonify(json_list)

# POST-Route: Fügt ein neues JSON-Objekt zur Liste hinzu
@app.route('/json', methods=['POST'])
def add_json_to_list1():
    if request.is_json:
        new_json = request.get_json()
        json_list.append(new_json)
        return jsonify({"message": "JSON hinzugefügt!", "data": new_json}), 201
    else:
        return jsonify({"message": "Request ist kein JSON!"}), 400

@app.route('/json/', methods=['POST'])
def add_json_to_list2():
    if request.is_json:
        new_json = request.get_json()
        json_list.append(new_json)
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
    
   
    return jsonify({"message": "Json wurde hinzugefügt","data":json_list}),201

@app.route('/panel')
def control_panel():
    html_content = '''
    <!DOCTYPE html>
    <html lang="de">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Kontrollpanel</title>
    </head>
    <body>
        <h1>Kontrollpanel für die Flask-App</h1>
        
        <!-- Button zum Abrufen der JSON-Liste -->
        <form action="/json" method="get">
            <button type="submit">JSON-Liste abrufen</button>
        </form>
        
        <br>

        <!-- Button zum Erstellen von 50 Einträgen -->
        <form action="/create/" method="get">
            <button type="submit">50 JSON-Einträge erstellen</button>
        </form>

        <br>

        <!-- Formular zum Hinzufügen eines einzelnen JSON-Eintrags -->
        <form action="/json" method="post">
            <label for="anzeigeName">AnzeigeName:</label>
            <input type="text" id="anzeigeName" name="AnzeigeName" required><br><br>
            
            <label for="beschreibung">Beschreibung:</label>
            <input type="text" id="beschreibung" name="Beschreibung" required><br><br>
            
            <label for="erstellerId">ErstellerId:</label>
            <input type="number" id="erstellerId" name="erstellerId" required><br><br>
            
            <button type="submit">JSON-Eintrag hinzufügen</button>
        </form>
    </body>
    </html>
    '''
    return render_template_string(html_content)

    

    
# Startet den Server
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000,ssl_context = context)
