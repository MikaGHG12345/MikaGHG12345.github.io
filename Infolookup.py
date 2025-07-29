from flask import Flask, request
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, PhoneNumberType
import requests
from faker import Faker
import random
app = Flask(__name__)

    
type_mapping = {
    PhoneNumberType.MOBILE: "📱 Mobile",
    PhoneNumberType.FIXED_LINE: "☎️ Festnetz",
    PhoneNumberType.FIXED_LINE_OR_MOBILE: "📞 Festnetz oder Mobil",
    PhoneNumberType.TOLL_FREE: "💸 Kostenlos",
    PhoneNumberType.PREMIUM_RATE: "💰 Premium",
    PhoneNumberType.VOIP: "🌐 VoIP",
    PhoneNumberType.PERSONAL_NUMBER: "🧍 Persönlich",
    PhoneNumberType.PAGER: "📟 Pager",
    PhoneNumberType.UAN: "🆔 UAN",
    PhoneNumberType.VOICEMAIL: "📮 Voicemail",
    PhoneNumberType.UNKNOWN: "❓ Unbekannt"
}

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>DOXTERMINAL</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
    <style>
        body {{
            background: url('https://i.postimg.cc/PJTVw9vL/70214552-pin-page.jpg') center center / cover no-repeat, #0a0a0a;
            position: relative;
            color: #e6d9b8;
            font-family: 'Cinzel', serif;
            user-select: none;
            margin: 0;
            padding: 0;
            min-height: 100vh;
            overflow-x: hidden;
        }}
        body::before {{
            content: "";
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: linear-gradient(120deg, #0a0a0a 80%, #23221f 100%);
            opacity: 0.7;
            z-index: 0;
        }}
        .container {{
            position: relative;
            z-index: 1;
            padding: 60px 0 0 0;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            min-height: 100vh;
        }}
        .ascii {{
            font-family: monospace;
            color: #c9b99a;
            font-size: 1.15rem;
            margin-bottom: 18px;
            text-align: center;
            letter-spacing: 1px;
            line-height: 1.1;
            opacity: 0.9;
            text-shadow: 0 0 18px #000, 0 0 8px #c9b99a88;
        }}
        h1 {{
            font-family: 'Cinzel', serif;
            font-weight: 900;
            font-size: 3.3rem;
            color: #e6d9b8;
            text-shadow: 0 0 32px #000, 2px 2px 24px #c9b99a88;
            margin-bottom: 10px;
            letter-spacing: 4px;
            border-bottom: 2px solid #c9b99a44;
            padding-bottom: 12px;
            text-transform: uppercase;
            filter: drop-shadow(0 0 12px #c9b99a);
        }}
        .subtitle {{
            font-size: 1.18rem;
            color: #b8a77a;
            margin-bottom: 38px;
            letter-spacing: 2.5px;
            text-shadow: 0 0 12px #000;
            font-family: 'Cinzel', serif;
            text-align: center;
        }}
        .mode-toggle {{
            display: flex;
            justify-content: center;
            margin-bottom: 22px;
            gap: 18px;
        }}
        .mode-btn {{
            background: #181818;
            color: #c9b99a;
            border: 2px solid #c9b99a;
            border-radius: 8px;
            font-family: 'Cinzel', serif;
            font-size: 1.1rem;
            font-weight: 700;
            padding: 10px 32px;
            cursor: pointer;
            transition: background 0.2s, color 0.2s, border-color 0.2s;
            box-shadow: 0 0 12px #000 inset;
            letter-spacing: 2px;
        }}
        .mode-btn.active {{
            background: #c9b99a;
            color: #23221f;
            border-color: #fffbe6;
            box-shadow: 0 0 22px #c9b99a;
        }}
        form {{
            width: 100%;
            max-width: 440px;
            display: flex;
            gap: 15px;
            margin-bottom: 32px;
        }}
        .hidden {{ display: none; }}
        input[type="text"] {{
            flex-grow: 1;
            padding: 14px 18px;
            font-size: 1.25rem;
            border: 2px solid #c9b99a;
            border-radius: 8px;
            background: #181818cc;
            color: #e6d9b8;
            box-shadow: 0 0 22px #000 inset, 0 0 8px #c9b99a44;
            transition: border-color 0.3s, background 0.3s;
            font-family: 'Cinzel', serif;
        }}
        input[type="text"]:focus {{
            border-color: #fffbe6;
            outline: none;
            background: #23221fcc;
            color: #fffbe6;
            box-shadow: 0 0 18px #c9b99a;
        }}
        button {{
            padding: 14px 28px;
            font-weight: 900;
            font-size: 1.15rem;
            background: linear-gradient(90deg,#23221f 60%,#c9b99a 100%);
            border: 2px solid #c9b99a;
            border-radius: 8px;
            color: #c9b99a;
            cursor: pointer;
            text-transform: uppercase;
            letter-spacing: 2.5px;
            box-shadow: 0 0 16px #000 inset, 0 0 8px #c9b99a44;
            transition: background 0.3s, color 0.3s;
            font-family: 'Cinzel', serif;
        }}
        button:hover {{
            background: #c9b99a;
            color: #23221f;
            box-shadow: 0 0 22px #c9b99a;
        }}
        .result {{
            max-width: 650px;
            background: #181818e6;
            border: 2px solid #c9b99a;
            padding: 28px;
            border-radius: 10px;
            font-size: 1.18rem;
            line-height: 1.55;
            color: #e6d9b8;
            box-shadow: 0 0 28px #000 inset, 0 0 40px #c9b99a22;
            white-space: pre-wrap;
            user-select: text;
            margin-bottom: 44px;
            font-family: monospace;
            letter-spacing: 1.5px;
            backdrop-filter: blur(1.5px);
            text-shadow: 0 0 8px #c9b99a44;
            border-left: 6px solid #b8a77a;
            border-right: 6px solid #b8a77a;
        }}
        ::selection {{
            background: #c9b99aaa;
            color: #23221f;
        }}
        .footer {{
            color: #c9b99a88;
            font-size: 1.05rem;
            margin-top: 44px;
            text-align: center;
            letter-spacing: 2.5px;
            font-family: 'Cinzel', serif;
            text-shadow: 0 0 12px #000;
        }}
        @media (max-width: 700px) {{
            h1 {{ font-size: 2.1rem; }}
            .result {{ font-size: 1rem; padding: 12px; }}
            .container {{ padding: 20px 0 0 0; }}
        }}
    </style>
    <script>
        function setMode(mode) {{
            document.getElementById('mode').value = mode;
            document.getElementById('numberField').classList.toggle('hidden', mode !== 'number');
            document.getElementById('ipField').classList.toggle('hidden', mode !== 'ip');
            document.getElementById('btn-number').classList.toggle('active', mode === 'number');
            document.getElementById('btn-id').classList.toggle('active', mode === 'id');
        }}
        window.onload = function() {{
            setMode('number');
        }};
    </script>
</head>
<body>
    <div class="container">
        <div class="ascii"></div>
        <h1>༺𓆩𝐁͢⧉𝐘͢⩔𝐓͢⟆⧬𓆪༻ᴾᴴ</h1> 
        <div class="subtitle">Number & IP Lookup.<br><span style="color:#a08c5c;"></span></div>
        <div class="mode-toggle">
            <button type="button" id="btn-number" class="mode-btn" onclick="setMode('number')">Number</button>
            <button type="button" id="btn-ip" class="mode-btn" onclick="setMode('ip')">IP</button>
            <button type="button" id="btn-id" class="mode-btn" onclick="setMode('id')">Fake ID</button>
        </div>
        <form method="POST">
            <input type="hidden" name="mode" id="mode" value="number">
            <input name="number" id="numberField" type="text" placeholder="+49..." autocomplete="off">
            <input name="ip" id="ipField" type="text" placeholder="IP-Adresse..." autocomplete="off" class="hidden">
            <button type="submit">DOX</button>
        </form>
        <a href="/downloads" class="mode-btn" style="display:block;text-align:center;margin-bottom:24px;">Downloads</a>
        <a href="/anleitungen" class="mode-btn" style="display:block;text-align:center;margin-bottom:24px;">Anleitungen</a>
        <div class="result">{}</div>
        <div class="footer">⸸ ༺𓆩𝐁͢⧉𝐘͢⩔𝐓͢⟆⧬𓆪༻ᴾᴴ ⸸</div>
    </div>
</body>
</html>
'''
#bei <h1> kannst dein tag eiinfügen z.b <h1>༺𓆩𝐁͢⧉𝐘͢⩔𝐓͢⟆⧬𓆪༻ᴾᴴ </h1> das gleiche bei <div class="footer"> z.b <div class="footer">⸸ ༺𓆩𝐁͢⧉𝐘͢⩔𝐓͢⟆⧬𓆪༻ᴾᴴ ⸸</div> Viel spaß :)
def generate_fake_identity():
    fake = Faker('de_DE')
    gender = random.choice(['male', 'female'])
    if gender == 'male':
        name = fake.first_name_male() + " " + fake.last_name()
    else:
        name = fake.first_name_female() + " " + fake.last_name()
    address = fake.street_address()
    city = fake.city()
    zip_code = fake.postcode()
    birthday = fake.date_of_birth(minimum_age=18, maximum_age=60).strftime('%d.%m.%Y')
    email = fake.email()
    phone = fake.phone_number()
    identity = {
        "name": name,
        "gender": "männlich" if gender == "male" else "weiblich",
        "birthday": birthday,
        "address": address,
        "zip": zip_code,
        "city": city,
        "email": email,
        "phone": phone
    }
    lines = ["{"]
    for k, v in identity.items():
        lines.append(f'  "{k}": "{v}",')
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return '<pre style="font-family: monospace; font-size:1.08rem; color:#c9b99a; margin:0;">' + "\n".join(lines) + '</pre>'

def get_ip_info(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,message,country,regionName,city,zip,lat,lon,isp,org,query")
        data = r.json()
        if data.get("status") != "success":
            return {"error": data.get("message", "Invalid IP")}
        return {
            "ip": data.get("query", ""),
            "country": data.get("country", ""),
            "region": data.get("regionName", ""),
            "city": data.get("city", ""),
            "zip": data.get("zip", ""),
            "lat": data.get("lat", ""),
            "lon": data.get("lon", ""),
            "isp": data.get("isp", ""),
            "org": data.get("org", "")
        }
    except Exception as e:
        return {"error": str(e)}
def generate_result_html(info):
    if not info.get("valid"):
        return f'<span style="color:#e74c3c;"><b>[!] Invalid number or error:</b> {info.get("error", "Invalid format")}</span>'
    dump = {
        "number": info.get("number", ""),
        "local_format": info.get("local", ""),
        "international": info.get("international", ""),
        "location": info.get("location", ""),
        "country": f"{info.get('country', '')} ({info.get('country_code', '')})",
        "carrier": info.get("carrier", ""),
        "timezones": info.get("timezones", ""),
        "type": info.get("type", "")
    }
    lines = ["{"]
    for k, v in dump.items():
        lines.append(f'  "{k}": "{v}",')
    lines[-1] = lines[-1].rstrip(",")
    lines.append("}")
    return f'<pre style="font-family: monospace; font-size:1.08rem; color:#c9b99a; margin:0;">\n' + "\n".join(lines) + '\n</pre>'

from flask import send_from_directory

@app.route('/downloads')
def downloads():
    files = ['Banchecker.apk', "GalleryEye.apk", "AndroidHardresetDONTINSTALLONYOURDEVICE.apk", "VoiceChanger.apk", "Networktool.py", "Stark VPN.apk", "MT_Manager_v2.14.0_23092056_.apk"]  # Liste deiner Dateien im downloads-Ordner
    links = ''.join([
        f'''
        <li style="margin-bottom:18px;">
            <a href="/download/{fname}" style="
                display:inline-block;
                padding:12px 32px;
                background:linear-gradient(90deg,#23221f 60%,#c9b99a 100%);
                color:#23221f;
                font-family:'Cinzel',serif;
                font-size:1.18rem;
                font-weight:700;
                border-radius:8px;
                border:2px solid #c9b99a;
                text-decoration:none;
                box-shadow:0 0 18px #c9b99a44;
                transition:background 0.2s,color 0.2s;
            " onmouseover="this.style.background='#c9b99a';this.style.color='#23221f';"
              onmouseout="this.style.background='linear-gradient(90deg,#23221f 60%,#c9b99a 100%)';this.style.color='#23221f';"
            >{fname}</a>
        </li>
        ''' for fname in files
    ])
    return f'''
    <html>
    <head>
        <title>Downloads</title>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
        <style>
            body {{
                background: url('https://i.postimg.cc/PJTVw9vL/70214552-pin-page.jpg') center center / cover no-repeat, #181818;
                color: #e6d9b8;
                font-family: 'Cinzel', serif;
                margin: 0;
                min-height: 100vh;
            }}
            .container {{
                max-width: 600px;
                margin: 80px auto 0 auto;
                background: #181818e6;
                border: 2px solid #c9b99a;
                border-radius: 14px;
                box-shadow: 0 0 44px #000, 0 0 22px #c9b99a44;
                padding: 44px 32px 32px 32px;
                text-align: center;
            }}
            h2 {{
                font-size: 2.2rem;
                color: #c9b99a;
                margin-bottom: 32px;
                letter-spacing: 2px;
                text-shadow: 0 0 18px #000, 0 0 8px #c9b99a88;
            }}
            ul {{
                list-style: none;
                padding: 0;
                margin: 0 0 32px 0;
            }}
            a.back {{
                display: inline-block;
                margin-top: 18px;
                color: #c9b99a;
                font-size: 1.1rem;
                text-decoration: none;
                border-bottom: 1px solid #c9b99a44;
                padding-bottom: 2px;
                transition: color 0.2s;
            }}
            a.back:hover {{
                color: #fffbe6;
                border-bottom: 1px solid #fffbe6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⸸ APK & File Downloads ⸸</h2>
            <ul>
                {links}
            </ul>
            <a href="/" class="back">Zurück zur Hauptseite</a>
        </div>
    </body>
    </html>
    '''

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_from_directory('downloads', filename, as_attachment=True)

@app.route('/anleitungen')
def anleitungen():
    tools = [
        ("Ethical Network Analyse Tool", "ethical-network"),
        ("GalleryEye", "galleryeye"),
        ("VoiceChanger", "voicechanger"),
        ("Android Hardreset", "hardreset"),
        ("Ddos Attack", "Ddos Attack"),
        ("RV Scan", "RV Scan"),
    ]
    buttons = ''.join([
        f'''
        <li style="margin-bottom:18px;">
            <a href="/anleitung/{slug}" style="
                display:inline-block;
                padding:12px 32px;
                background:linear-gradient(90deg,#23221f 60%,#c9b99a 100%);
                color:#23221f;
                font-family:'Cinzel',serif;
                font-size:1.18rem;
                font-weight:700;
                border-radius:8px;
                border:2px solid #c9b99a;
                text-decoration:none;
                box-shadow:0 0 18px #c9b99a44;
                transition:background 0.2s,color 0.2s;
            " onmouseover="this.style.background='#c9b99a';this.style.color='#23221f';"
              onmouseout="this.style.background='linear-gradient(90deg,#23221f 60%,#c9b99a 100%)';this.style.color='#23221f';"
            >{name}</a>
        </li>
        ''' for name, slug in tools
    ])
    return f'''
    <html>
    <head>
        <title>Anleitungen</title>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
        <style>
            body {{
                background: url('https://i.postimg.cc/PJTVw9vL/70214552-pin-page.jpg') center center / cover no-repeat, #181818;
                color: #e6d9b8;
                font-family: 'Cinzel', serif;
                margin: 0;
                min-height: 100vh;
            }}
            .container {{
                max-width: 600px;
                margin: 80px auto 0 auto;
                background: #181818e6;
                border: 2px solid #c9b99a;
                border-radius: 14px;
                box-shadow: 0 0 44px #000, 0 0 22px #c9b99a44;
                padding: 44px 32px 32px 32px;
                text-align: center;
            }}
            h2 {{
                font-size: 2.2rem;
                color: #c9b99a;
                margin-bottom: 32px;
                letter-spacing: 2px;
                text-shadow: 0 0 18px #000, 0 0 8px #c9b99a88;
            }}
            ul {{
                list-style: none;
                padding: 0;
                margin: 0 0 32px 0;
            }}
            a.back {{
                display: inline-block;
                margin-top: 18px;
                color: #c9b99a;
                font-size: 1.1rem;
                text-decoration: none;
                border-bottom: 1px solid #c9b99a44;
                padding-bottom: 2px;
                transition: color 0.2s;
            }}
            a.back:hover {{
                color: #fffbe6;
                border-bottom: 1px solid #fffbe6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⸸ Tool-Anleitungen ⸸</h2>
            <ul>
                {buttons}
            </ul>
            <a href="/" class="back">Zurück zur Hauptseite</a>
        </div>
    </body>
    </html>
    '''
@app.route('/anleitung/<tool>')
def anleitung(tool):
    anleitungen = {
        "ethical-network": """
1. Lade die APK im Download-Bereich herunter.
2. Öffne die Datei mit einem Dateimanager.
3. Bei Android: 'Unbekannte Quellen' zulassen.
4. App starten und Netzwerk-Analyse durchführen.
5. Weitere Hinweise findest du im Menü der App.
""",
"galleryeye": """
1. Lade die APKa im Download-Bereich herunter.
2. Guck dir das Video an, um die Funktionen zu verstehen.
""",
        "Ddos Attack": """
Ddos-Atacks tool
To destroy and hit sites
Termux installation commands:
git clone https://github.com/NaserHacker/Ddos-Atacks
cd Ddos-Atacks
chmod +x Ddos-Atacks.py
python2 Ddos-Atacks.py
To extract the IP of any website, we write this command in Termux, for example:
ping www.google.com
If you do not check the website and know the open port, set 80
Don't forget to run tor to avoid blocking the pkg install tor installation command
tor run command
""",
        "RV Scan": """
RV Scan
The tool helps you examine open IPs and ports on the network and examine the domains of sites to detect open ports in them... just by using the Nmap tool instead of writing commands... and the tool has a feature to scan ports and IPs from a .txt text file. Anyone who has used Nmap will know that It is never useful to scan the ip list and port list at the same time... and all of this without root privileges if you are using Termux.

Installation commands for Trimix
pkg update -y
pkg upgrade -y
pkg install git -y
git clone https://github.com/RedVirus-Dev/RV-Scan.git

Linux installation commands:
sudo apt-get update -y
sudo apt-get upgrade -y
sudo apt-get install git -y
git clone https://github.com/RedVirus-Dev/RV-Scan.git

Operation commands:
cd RV-Scan
{!} The tool must be run with bash, not with /.
bash RV-Scan-V1.0.sh

Note: The tool does not require root privileges to run
""",
        "hardreset": """
1. Lade AndroidHardresetDONTINSTALLONYOURDEVICE.apk herunter.
2. Installiere nur auf Testgerät!
3. Starte die App und folge den Warnhinweisen.
4. Gerät wird zurückgesetzt.
"""
    }
    video_links = {
    "galleryeye": '''
    <div style="margin:32px 0;text-align:center;">
        <video width="560" height="315" controls style="border-radius:12px;box-shadow:0 0 22px #c9b99a88;">
            <source src="/static/GalleryEye.mp4" type="video/mp4">
            Dein Browser unterstützt kein Video.
        </video>
        <div style="color:#b8a77a;margin-top:8px;">GalleryEye Video-Anleitung (14 Minuten)</div>
    </div>
    '''
}
    steps = anleitungen.get(tool, "Keine Anleitung gefunden.").strip().split('\n')
    tool_name = {
        "ethical-network": "Ethical Network Analyse Tool",
        "galleryeye": "GalleryEye",
        "Ddos Attack": "Ddos Attack",
        "RV Scan": "RV Scan",
        "hardreset": "Android Hardreset"
    }.get(tool, tool)
    steps_html = ''.join([f"<li>{step}</li>" for step in steps])
    video_html = video_links.get(tool, "")
    return f'''
    <html>
    <head>
        <title>{tool_name} Anleitung</title>
        <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@700;900&display=swap" rel="stylesheet">
        <style>
            body {{
                background: url('https://i.postimg.cc/PJTVw9vL/70214552-pin-page.jpg') center center / cover no-repeat, #181818;
                color: #e6d9b8;
                font-family: 'Cinzel', serif;
                margin: 0;
                min-height: 100vh;
            }}
            .container {{
                max-width: 600px;
                margin: 80px auto 0 auto;
                background: #181818e6;
                border: 2px solid #c9b99a;
                border-radius: 14px;
                box-shadow: 0 0 44px #000, 0 0 22px #c9b99a44;
                padding: 44px 32px 32px 32px;
                text-align: left;
            }}
            h2 {{
                font-size: 2.2rem;
                color: #c9b99a;
                margin-bottom: 32px;
                letter-spacing: 2px;
                text-shadow: 0 0 18px #000, 0 0 8px #c9b99a88;
                text-align: center;
            }}
            ul {{
                list-style: none;
                padding: 0;
                margin: 0 0 32px 0;
            }}
            a.back {{
                display: inline-block;
                margin-top: 18px;
                color: #c9b99a;
                font-size: 1.1rem;
                text-decoration: none;
                border-bottom: 1px solid #c9b99a44;
                padding-bottom: 2px;
                transition: color 0.2s;
            }}
            a.back:hover {{
                color: #fffbe6;
                border-bottom: 1px solid #fffbe6;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>⸸ {tool_name} Anleitung ⸸</h2>
            <ul>
                {steps_html}
            </ul>
            {video_html}
            <a href="/anleitungen" class="back">Zurück zu den Anleitungen</a>
        </div>
    </body>
    </html>
    '''
@app.route('/', methods=['GET', 'POST'])
def index():
    result_html = ''
    if request.method == 'POST':
        mode = request.form.get('mode', 'number')
        if mode == 'number':
            number = request.form.get('number', '').strip()
            try:
                parsed = phonenumbers.parse(number, None)
                if phonenumbers.is_valid_number(parsed):
                    info = {
                        "valid": True,
                        "number": number,
                        "international": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                        "local": phonenumbers.format_number(parsed, phonenumbers.PhoneNumberFormat.NATIONAL),
                        "location": geocoder.description_for_number(parsed, "de"),
                        "carrier": carrier.name_for_number(parsed, "de"),
                        "country": geocoder.description_for_number(parsed, "en"),
                        "country_code": parsed.country_code,
                        "timezones": ', '.join(timezone.time_zones_for_number(parsed)),
                        "type": type_mapping.get(phonenumbers.number_type(parsed), "❓ Unbekannt")
                    }
                else:
                    info = {"valid": False}
            except Exception as e:
                info = {"valid": False, "error": str(e)}
            result_html = generate_result_html(info)
        elif mode == 'ip':
            ip = request.form.get('ip', '').strip()
            ipinfo = get_ip_info(ip)
            if "error" in ipinfo:
                result_html = f'<pre style="font-family: monospace; color:#e74c3c;">[IP ERROR] {ipinfo["error"]}</pre>'
            else:
                ip_dump = [
                    "{",
                    f'  "ip": "{ipinfo["ip"]}",',
                    f'  "country": "{ipinfo["country"]}",',
                    f'  "region": "{ipinfo["region"]}",',
                    f'  "city": "{ipinfo["city"]}",',
                    f'  "zip": "{ipinfo["zip"]}",',
                    f'  "lat": "{ipinfo["lat"]}",',
                    f'  "lon": "{ipinfo["lon"]}",',
                    f'  "isp": "{ipinfo["isp"]}",',
                    f'  "org": "{ipinfo["org"]}"',
                    "}"
                ]
                result_html = f'<pre style="font-family: monospace; font-size:1.08rem; color:#c9b99a; margin:0;">' + "\n".join(ip_dump) + '</pre>'
        elif mode == 'id':
            result_html = generate_fake_identity()
    return HTML_TEMPLATE.format(result_html)
if __name__ == '__main__':
    app.run(debug=True)
