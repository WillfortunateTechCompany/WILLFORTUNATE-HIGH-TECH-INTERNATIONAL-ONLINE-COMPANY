
from flask import Flask, request, jsonify, send_file, render_template_string
import edge_tts
import asyncio
import tempfile
import os
import uuid

app = Flask(__name__)

VOICES = {
    "sw": {
        "Female": [
            ("sw-KE-ZuriNeural", "Zuri - Kiswahili Female")
        ],
        "Male": [
            ("sw-KE-RafikiNeural", "Rafiki - Kiswahili Male")
        ]
    },
    "en": {
        "Female": [
            ("en-US-AriaNeural", "Aria - Warm Female"),
            ("en-US-JennyNeural", "Jenny - Friendly Female"),
            ("en-GB-SoniaNeural", "Sonia - British Female")
        ],
        "Male": [
            ("en-US-GuyNeural", "Guy - Deep Male"),
            ("en-US-AndrewNeural", "Andrew - Natural Male"),
            ("en-GB-RyanNeural", "Ryan - British Male")
        ]
    }
}

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>VOICECRAFT AI | Professional Voice Studio</title>

<style>
*{margin:0;padding:0;box-sizing:border-box}

body{
 background:#080c15;
 color:#f5f5f5;
 font-family:Segoe UI,Arial,sans-serif;
 min-height:100vh;
}

header{
 height:76px;
 padding:0 7%;
 display:flex;
 align-items:center;
 justify-content:space-between;
 background:#0e1421;
 border-bottom:1px solid #263044;
}

.brand{
 font-size:24px;
 font-weight:900;
 letter-spacing:2px;
}

.brand span{color:#dfb96c}

.brand small{font-size:12px}

.header-label{
 color:#9ca7b9;
 font-size:11px;
 letter-spacing:2px;
}

main{
 max-width:1000px;
 margin:auto;
 padding:55px 20px;
}

.hero{
 text-align:center;
 margin-bottom:38px;
}

.tag{
 color:#d8b66a;
 font-size:11px;
 letter-spacing:3px;
 margin-bottom:18px;
 font-weight:800;
}

.hero h1{
 font-size:clamp(32px,5vw,53px);
 line-height:1.15;
 margin-bottom:18px;
}

.hero h1 span{color:#e0bc73}

.hero p{
 color:#a5afbf;
 line-height:1.8;
 max-width:650px;
 margin:auto;
}

.studio{
 background:linear-gradient(145deg,#141e30,#101725);
 border:1px solid #303c50;
 border-radius:20px;
 padding:30px;
 box-shadow:0 25px 80px #0006;
}

.section-heading{
 display:flex;
 justify-content:space-between;
 align-items:center;
 margin-bottom:30px;
}

.section-heading h2{
 font-size:24px;
 margin-bottom:7px;
}

.section-heading p{
 font-size:13px;
 color:#9ca9bc;
}

.live{
 color:#65d7a2;
 font-size:11px;
 font-weight:bold;
}

label{
 display:block;
 font-size:11px;
 font-weight:800;
 letter-spacing:1.2px;
 color:#d8c99e;
 margin-bottom:11px;
}

textarea{
 width:100%;
 min-height:220px;
 padding:18px;
 background:#090f1b;
 border:1px solid #35435b;
 border-radius:12px;
 color:white;
 font:15px/1.8 Segoe UI,sans-serif;
 outline:none;
 resize:vertical;
}

textarea:focus,select:focus{
 border-color:#dfb96c;
}

.text-info{
 display:flex;
 justify-content:space-between;
 margin-top:10px;
 color:#8794a8;
 font-size:11px;
}

.settings{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:18px;
 margin-top:28px;
}

select{
 width:100%;
 padding:14px;
 border-radius:9px;
 border:1px solid #34445c;
 background:#0a1220;
 color:white;
 outline:none;
}

.voice-field{margin-top:24px}

.hint{
 color:#8998ad;
 font-size:11px;
 margin-top:9px;
}

.adjustments{
 display:grid;
 grid-template-columns:1fr 1fr;
 gap:30px;
 margin-top:30px;
}

.range-heading{
 display:flex;
 justify-content:space-between;
}

.range-heading span{
 color:#dfb96c;
 font-size:12px;
}

input[type=range]{
 width:100%;
 accent-color:#dfb96c;
}

.range-labels{
 display:flex;
 justify-content:space-between;
 color:#8290a4;
 font-size:10px;
 margin-top:8px;
}

.buttons{
 display:flex;
 gap:12px;
 flex-wrap:wrap;
 margin-top:30px;
}

button{
 border:0;
 border-radius:9px;
 padding:15px 19px;
 font-weight:800;
 font-size:11px;
 cursor:pointer;
 transition:.2s;
}

button:hover{
 transform:translateY(-2px);
 filter:brightness(1.15);
}

button:disabled{
 opacity:.5;
 cursor:not-allowed;
 transform:none;
}

.generate{
 flex:2;
 background:linear-gradient(120deg,#f2d18c,#c29a51);
 color:#10121a;
}

.preview{
 background:#27374e;
 color:white;
}

.stop{
 background:#472b36;
 color:#ffd8df;
}

.status{
 color:#dfb96c;
 font-size:12px;
 margin-top:20px;
 min-height:20px;
 line-height:1.6;
}

.result{
 border:1px solid #35445c;
 background:#0b1320;
 padding:20px;
 border-radius:12px;
 margin-top:20px;
}

.result-heading{
 display:flex;
 justify-content:space-between;
 margin-bottom:15px;
}

.result-heading h3{font-size:16px}

.result-heading span{
 color:#65d7a2;
 font-size:10px;
}

audio{
 width:100%;
 margin-bottom:15px;
}

.download{
 display:block;
 text-align:center;
 padding:15px;
 background:#1e704d;
 color:white;
 text-decoration:none;
 font-size:12px;
 font-weight:900;
 border-radius:9px;
}

.tip{
 background:#0b1422;
 border-left:3px solid #d8b66a;
 padding:17px;
 margin-top:28px;
}

.tip strong{
 color:#dfb96c;
 font-size:11px;
}

.tip p{
 color:#a4b0c0;
 font-size:12px;
 line-height:1.7;
 margin-top:8px;
}

.features{
 display:grid;
 grid-template-columns:repeat(3,1fr);
 gap:15px;
 margin-top:30px;
}

.features div{
 background:#111a29;
 border:1px solid #273348;
 border-radius:12px;
 padding:22px;
}

.features strong{
 color:#dfb96c;
 font-size:12px;
}

.features h3{
 margin:12px 0 8px;
 font-size:15px;
}

.features p{
 font-size:12px;
 line-height:1.6;
 color:#9ba8bb;
}

footer{
 border-top:1px solid #202a3a;
 padding:30px;
 text-align:center;
 color:#d8b66a;
 font-size:11px;
 letter-spacing:2px;
}

footer p{
 color:#8793a5;
 margin-top:10px;
 letter-spacing:0;
}

@media(max-width:650px){
 header{padding:0 18px}
 .header-label{display:none}
 main{padding:35px 13px}
 .studio{padding:19px}
 .settings,.adjustments,.features{
  grid-template-columns:1fr;
 }
 .buttons{flex-direction:column}
 .buttons button{width:100%}
 .section-heading{
  align-items:flex-start;
  gap:10px;
 }
}
</style>
</head>

<body>

<header>
 <div class="brand">VOICE<span>CRAFT</span><small> AI</small></div>
 <div class="header-label">PROFESSIONAL TEXT TO SPEECH STUDIO</div>
</header>

<main>

<section class="hero">
 <div class="tag">YOUR PERSONAL AI VOICE STUDIO</div>
 <h1>Turn Your Text Into <span>Beautiful Speech.</span></h1>
 <p>Transform English and Kiswahili text into natural,
 expressive and professional AI narration.</p>
</section>

<section class="studio">

<div class="section-heading">
 <div>
  <h2>Create Your Voice</h2>
  <p>Enter your text and customize your narration.</p>
 </div>
 <span class="live">● READY</span>
</div>

<label for="text">YOUR TEXT / MAANDISHI YAKO</label>

<textarea id="text" maxlength="10000"
placeholder="Paste or type your text here...

Karibu kwenye VoiceCraft AI. Andika ujumbe wako hapa..."></textarea>

<div class="text-info">
 <span id="wordCount">0 words</span>
 <span id="charCount">0 / 10,000</span>
</div>

<div class="settings">
 <div>
  <label for="language">LANGUAGE / LUGHA</label>
  <select id="language">
   <option value="sw">Kiswahili</option>
   <option value="en">English</option>
  </select>
 </div>

 <div>
  <label for="gender">VOICE GENDER</label>
  <select id="gender">
   <option value="Female">Female voices</option>
   <option value="Male">Male voices</option>
  </select>
 </div>
</div>

<div class="voice-field">
 <label for="voice">CHOOSE YOUR AI VOICE</label>
 <select id="voice"></select>
 <div id="voiceDescription" class="hint">
 Select a voice to begin.
 </div>
</div>

<div class="adjustments">

 <div>
  <div class="range-heading">
   <label for="speed">SPEAKING SPEED</label>
   <span id="speedValue">0%</span>
  </div>
  <input id="speed" type="range" min="-30" max="30" value="0">
  <div class="range-labels">
   <span>Slow</span><span>Fast</span>
  </div>
 </div>

 <div>
  <div class="range-heading">
   <label for="pitch">VOICE PITCH</label>
   <span id="pitchValue">0 Hz</span>
  </div>
  <input id="pitch" type="range" min="-20" max="20" value="0">
  <div class="range-labels">
   <span>Deep</span><span>High</span>
  </div>
 </div>

</div>

<div class="buttons">
 <button id="generate" class="generate">✦ GENERATE AI VOICE</button>
 <button id="preview" class="preview">▶ PREVIEW VOICE</button>
 <button id="stop" class="stop">■ STOP</button>
</div>

<div id="status" class="status">
 Your studio is ready. Enter text to begin.
</div>

<section id="result" class="result" hidden>
 <div class="result-heading">
  <h3>Your Generated Audio</h3>
  <span>MP3 AUDIO</span>
 </div>
 <audio id="audio" controls></audio>
 <a id="download" class="download" href="#">
  ↓ DOWNLOAD MP3
 </a>
</section>

<div class="tip">
 <strong>PROFESSIONAL TIP</strong>
 <p>Use correct punctuation, paragraphs and complete sentences
 for more natural narration. Select the correct language
 for your text.</p>
</div>

</section>

<section class="features">
 <div>
  <strong>01</strong>
  <h3>Natural Voices</h3>
  <p>Male and female AI narration.</p>
 </div>
 <div>
  <strong>02</strong>
  <h3>Two Languages</h3>
  <p>English and Kiswahili support.</p>
 </div>
 <div>
  <strong>03</strong>
  <h3>MP3 Downloads</h3>
  <p>Generate and save your audio.</p>
 </div>
</section>

</main>

<footer>
 VOICECRAFT AI PROFESSIONAL
 <p>Give every word a voice.</p>
</footer>

<script>
const voices = {
 sw: {
  Female: [
   ["sw-KE-ZuriNeural","Zuri - Kiswahili Female"]
  ],
  Male: [
   ["sw-KE-RafikiNeural","Rafiki - Kiswahili Male"]
  ]
 },
 en: {
  Female: [
   ["en-US-AriaNeural","Aria - Warm Female"],
   ["en-US-JennyNeural","Jenny - Friendly Female"],
   ["en-GB-SoniaNeural","Sonia - British Female"]
  ],
  Male: [
   ["en-US-GuyNeural","Guy - Deep Male"],
   ["en-US-AndrewNeural","Andrew - Natural Male"],
   ["en-GB-RyanNeural","Ryan - British Male"]
  ]
 }
};

const $ = id => document.getElementById(id);

let currentAudio = null;
let busy = false;

function updateVoices(){
 const language = $("language").value;
 const gender = $("gender").value;

 $("voice").innerHTML = "";

 voices[language][gender].forEach(item=>{
  const option = document.createElement("option");
  option.value = item[0];
  option.textContent = item[1];
  $("voice").appendChild(option);
 });

 $("voiceDescription").textContent =
  gender + " voice selected. Choose your preferred voice.";
}

$("language").addEventListener("change",updateVoices);
$("gender").addEventListener("change",updateVoices);

$("text").addEventListener("input",()=>{
 const value = $("text").value;

 $("charCount").textContent =
  value.length + " / 10,000";

 const words = value.trim()
  ? value.trim().split(/\s+/).length
  : 0;

 $("wordCount").textContent = words + " words";
});

$("speed").addEventListener("input",event=>{
 const value = Number(event.target.value);
 $("speedValue").textContent =
  (value>0?"+":"") + value + "%";
});

$("pitch").addEventListener("input",event=>{
 const value = Number(event.target.value);
 $("pitchValue").textContent =
  (value>0?"+":"") + value + " Hz";
});

async function generateVoice(preview=false){
 if(busy)return;

 let text = $("text").value.trim();

 if(preview){
  text = $("language").value === "sw"
   ? "Karibu kwenye VoiceCraft AI. Hii ni sauti yako ya kitaalamu."
   : "Welcome to VoiceCraft AI. Experience beautiful professional narration.";
 }

 if(!text){
  $("status").textContent="Please enter your text first.";
  return;
 }

 busy=true;
 $("generate").disabled=true;
 $("preview").disabled=true;
 $("status").textContent="Generating your professional AI voice...";

 try{
  const response=await fetch("/generate",{
   method:"POST",
   headers:{"Content-Type":"application/json"},
   body:JSON.stringify({
    text:text,
    voice:$("voice").value,
    rate:Number($("speed").value),
    pitch:Number($("pitch").value)
   })
  });

  if(!response.ok){
   const error=await response.json();
   throw new Error(error.error || "Generation failed.");
  }

  const blob=await response.blob();

  if(!blob.size)throw new Error("Empty audio file.");

  if(currentAudio)URL.revokeObjectURL(currentAudio);

  currentAudio=URL.createObjectURL(blob);

  $("audio").src=currentAudio;
  $("result").hidden=false;
  $("download").href=currentAudio;
  $("download").download="VoiceCraft-Narration.mp3";
  $("download").style.display=preview?"none":"block";

  $("status").textContent="Your voice is ready. Listen or download your MP3.";

  await $("audio").play();

 }catch(error){
  $("status").textContent="Error: "+error.message;
 }finally{
  busy=false;
  $("generate").disabled=false;
  $("preview").disabled=false;
 }
}

$("generate").addEventListener("click",()=>generateVoice(false));
$("preview").addEventListener("click",()=>generateVoice(true));

$("stop").addEventListener("click",()=>{
 $("audio").pause();
 $("audio").currentTime=0;
 $("status").textContent="Playback stopped.";
});

updateVoices();
</script>

</body>
</html>
"""


@app.route("/")
def home():
    return render_template_string(HTML)


@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json(silent=True) or {}

    text = str(data.get("text", "")).strip()
    voice = data.get("voice", "")

    try:
        rate = max(-30, min(30, int(data.get("rate", 0))))
        pitch = max(-20, min(20, int(data.get("pitch", 0))))
    except (TypeError, ValueError):
        return jsonify({"error": "Invalid speed or pitch."}), 400

    if not text:
        return jsonify({"error": "Please enter your text."}), 400

    if len(text) > 10000:
        return jsonify({"error": "Maximum 10,000 characters allowed."}), 400

    valid_voices = [
        voice_id
        for language in VOICES.values()
        for gender in language.values()
        for voice_id, name in gender
    ]

    if voice not in valid_voices:
        return jsonify({"error": "Invalid voice selected."}), 400

    filename = os.path.join(
        tempfile.gettempdir(),
        f"voicecraft_{uuid.uuid4().hex}.mp3"
    )

    try:
        async def create_audio():
            speech = edge_tts.Communicate(
                text=text,
                voice=voice,
                rate=f"{rate:+d}%",
                pitch=f"{pitch:+d}Hz"
            )
            await speech.save(filename)

        asyncio.run(create_audio())

        if not os.path.exists(filename) or os.path.getsize(filename) == 0:
            raise RuntimeError("No audio was generated.")

        response = send_file(
            filename,
            mimetype="audio/mpeg",
            as_attachment=True,
            download_name="VoiceCraft-Narration.mp3"
        )

        response.call_on_close(
            lambda: os.path.exists(filename) and os.remove(filename)
        )

        return response

    except Exception:
        app.logger.exception("Voice generation error")

        if os.path.exists(filename):
            os.remove(filename)

        return jsonify({
            "error": "Voice generation failed. Check your internet connection and try again."
        }), 500


if __name__ == "__main__":
    print("\n====================================")
    print("     VOICECRAFT AI PROFESSIONAL")
    print("====================================")
    print("Open: http://127.0.0.1:5000")
    print("====================================\n")

    app.run(host="127.0.0.1", port=5000, debug=False)
