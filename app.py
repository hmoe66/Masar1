import os
from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

# تخزين الأوامر الحالية بسرعة فائقة
current_command = {"action": "none", "value": ""}

DISPLAY_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>Gaming & Media Pro - Ultra Fast</title>
    <style>
        * { box-sizing: border-box; }
        body { background: #0b0b0f; color: #fff; font-family: 'Segoe UI', Tahoma, sans-serif; margin: 0; padding: 15px; text-align: center; overflow-x: hidden; }
        h1 { color: #00ffcc; font-size: 2.2rem; margin: 5px 0 15px 0; text-shadow: 0 0 10px rgba(0,255,204,0.3); }
        .grid-container { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; max-width: 1400px; margin: 0 auto; }
        .panel { background: #14141c; padding: 15px; border-radius: 12px; border: 1px solid #22223b; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
        iframe { width: 100%; height: 450px; border-radius: 8px; border: none; background: #000; }
        .games-list { display: grid; grid-template-columns: 1fr; gap: 10px; max-height: 450px; overflow-y: auto; }
        .game-btn { background: #1f1f2e; color: #fff; border: 1px solid #33334d; padding: 12px; border-radius: 8px; cursor: pointer; font-weight: bold; transition: all 0.2s ease; text-align: right; }
        .game-btn:hover { background: #00ffcc; color: #000; border-color: #00ffcc; transform: translateY(-2px); }
        #ping-status { margin-top: 10px; font-size: 1rem; color: #00ffcc; background: #121218; padding: 8px; border-radius: 6px; display: inline-block; border: 1px solid #1f1f2e; }
    </style>
</head>
<body>
    <h1>⚡ نظام الألعاب والترفيه الخارق (Ultra Fast)</h1>
    <div id="ping-status">النظام متصل وجاهز للأوامر السريعة...</div>
    
    <div class="grid-container" style="margin-top: 15px;">
        <div class="panel">
            <h3 style="margin-top:0; color:#ff0055;">🎥 شاشة التشغيل واللعب الرئيسية</h3>
            <iframe id="main-frame" src="https://www.youtube.com/embed/5qap5aO4i9A?enablejsapi=1" allowfullscreen></iframe>
        </div>
        <div class="panel">
            <h3 style="margin-top:0; color:#00ffcc;">🎮 منصة الألعاب السريعة</h3>
            <div class="games-list">
                <div class="game-btn" onclick="launchGame('https://pacman.live/')">🟡 باكمان الأسطورية (Pacman)</div>
                <div class="game-btn" onclick="launchGame('https://tetris.com/play-tetris')">🧱 تترس الكلاسيكية (Tetris)</div>
                <div class="game-btn" onclick="launchGame('https://www.google.com/logos/2010/pacman10-i.html')">🕹️ آركيد جوجل السريع</div>
                <div class="game-btn" onclick="launchGame('https://html5games.com/')">🚀 متجر ألعاب HTML5 الشامل</div>
            </div>
        </div>
    </div>

    <script>
        setInterval(async () => {
            try {
                let res = await fetch('/get-command');
                let data = await res.json();
                let status = document.getElementById('ping-status');
                let frame = document.getElementById('main-frame');

                if (data.action === 'play') {
                    status.innerText = "⚡ تشغيل الوسائط بسرعة فائقة";
                    frame.src = "https://www.youtube.com/embed/" + data.value + "?autoplay=1";
                } else if (data.action === 'game') {
                    status.innerText = "🎮 تشغيل اللعبة بأداء عالي";
                    frame.src = data.value;
                } else if (data.action === 'reset') {
                    status.innerText = "🏠 العودة للرئيسية";
                    frame.src = "https://www.youtube.com/embed/5qap5aO4i9A";
                }
            } catch(e) {}
        }, 500);

        function launchGame(url) {
            document.getElementById('main-frame').src = url;
        }
    </script>
</body>
</html>
"""

CONTROLLER_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎮 ريموت الألعاب السريع</title>
    <style>
        body { background: #0b0b0f; color: #fff; font-family: Tahoma, sans-serif; padding: 15px; text-align: center; }
        h2 { color: #00ffcc; margin-bottom: 10px; }
        .box { background: #14141c; padding: 15px; border-radius: 12px; max-width: 400px; margin: 0 auto; border: 1px solid #22223b; }
        input { width: 100%; padding: 12px; margin-bottom: 10px; background: #1f1f2e; border: 1px solid #33334d; color: #fff; border-radius: 8px; font-size: 1rem; box-sizing: border-box; }
        button { width: 100%; padding: 14px; margin-bottom: 10px; border: none; border-radius: 8px; font-size: 1.1rem; font-weight: bold; cursor: pointer; transition: 0.1s; }
        button:active { transform: scale(0.97); }
        .btn-red { background: #ff0055; color: #fff; }
        .btn-blue { background: #00ffcc; color: #000; }
        .btn-dark { background: #2a2a3d; color: #fff; }
    </style>
</head>
<body>
    <div class="box">
        <h2>⚡ ريموت الألعاب الخارق</h2>
        <p style="font-size: 0.9rem; color: #888;">تحكم فوري عبر الإنترنت</p>

        <input type="text" id="yt-code" placeholder="معرف فيديو يوتيوب (مثال: dQw4w9WgXcQ)">
        <button class="btn-red" onclick="sendCmd('play', document.getElementById('yt-code').value)">🎬 تشغيل يوتيوب فوري</button>
        
        <button class="btn-blue" onclick="sendCmd('game', 'https://pacman.live/')">🟡 تشغيل لعبة باكمان</button>
        <button class="btn-blue" onclick="sendCmd('game', 'https://tetris.com/play-tetris')">🧱 تشغيل لعبة تترس</button>
        
        <button class="btn-dark" onclick="sendCmd('reset', '')">🏠 العودة للرئيسية</button>
    </div>

    <script>
        async function sendCmd(action, value) {
            await fetch('/send-command', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ action: action, value: value })
            });
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(DISPLAY_HTML)

@app.route('/controller')
def controller():
    return render_template_string(CONTROLLER_HTML)

@app.route('/send-command', methods=['POST'])
def send():
    global current_command
    current_command = request.json
    return jsonify({"status": "ok"})

@app.route('/get-command', methods=['GET'])
def get():
    return jsonify(current_command)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
