import os
from groq import Groq
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
timezone = pytz.timezone('America/Sao_Paulo')

# --- CONFIGURAÇÃO DA INTELIGÊNCIA ---
# Substitua pelo seu código gsk_... completo entre as aspas
client = Groq(api_key="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")

PERGUNTAS_AKINATOR = {
    1: "O seu personagem é um ser humano real?",
    2: "Ele é um super-herói?",
    3: "Ele é brasileiro?",
    4: "Ele é de um anime?",
    5: "Ele usa uma armadura?"
}

COMANDOS_FIXOS = {
    "quem é você": "Eu sou a Geometry AI, sua assistente focada em tecnologia.",
    "quem te criou": "Fui desenvolvida pelo Guester_DEV.",
    "lista de comandos": "Comandos: Akinator, Horas, Data e IA livre.",
    "bom dia": "Bom dia! No que posso ser útil hoje?"
}

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta_original = dados.get("pergunta", "").strip()
        msg = pergunta_original.lower()

        if not msg:
            return jsonify({"resposta": "Diga algo!"})

        # 1. AKINATOR
        if "akinator" in msg:
            session['jogo'] = 'akinator'
            session['passo'] = 1
            return jsonify({"resposta": "🔮 Akinator! Pense em alguém. Diga 'ESTOU PRONTO'!"})

        if session.get('jogo') == 'akinator':
            passo = session.get('passo')
            if "pronto" in msg and passo == 1:
                session['passo'] = 2
                return jsonify({"resposta": PERGUNTAS_AKINATOR[1]})
            if passo >= 2:
                session[f'resp_{passo}'] = "sim" in msg
                prox = passo + 1
                if prox in PERGUNTAS_AKINATOR:
                    session['passo'] = prox
                    return jsonify({"resposta": PERGUNTAS_AKINATOR[prox]})
                else:
                    session.clear()
                    return jsonify({"resposta": "Dedução final: Acho que você pensou em alguém famoso! Jogue de novo!"})

        # 2. DATA, HORA E COMANDOS
        agora = datetime.now(timezone)
        if "horas" in msg: return jsonify({"resposta": f"Agora são {agora.strftime('%H:%M')}."})
        if "data" in msg: return jsonify({"resposta": f"Hoje é {agora.strftime('%d/%m/%Y')}."})
        if msg in COMANDOS_FIXOS: return jsonify({"resposta": COMANDOS_FIXOS[msg]})

        # 3. CÉREBRO LLAMA 3 (GROQ)
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "Você é a Geometry AI. Responda de forma curta em português."},
                {"role": "user", "content": pergunta_original}
            ],
            model="llama3-8b-8192",
        )
        return jsonify({"resposta": chat_completion.choices[0].message.content})

    except Exception as e:
        return jsonify({"resposta": f"Erro interno: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    try:
        dados = request.json
        pergunta_original = dados.get("pergunta", "").strip()
        msg = pergunta_original.lower()

        if not msg:
            return jsonify({"resposta": "Estou aguardando sua pergunta!"})

        # 1. AKINATOR
        if "akinator" in msg:
            session['jogo'] = 'akinator'; session['passo'] = 1
            return jsonify({"resposta": "🔮 Akinator ativado! Pense em alguém. Diga 'ESTOU PRONTO'!"})

        if session.get('jogo') == 'akinator':
            passo = session.get('passo')
            if "pronto" in msg and passo == 1:
                session['passo'] = 2
                return jsonify({"resposta": PERGUNTAS_AKINATOR[1]})
            if passo >= 2:
                session[f'resp_{passo}'] = "sim" in msg
                prox = passo + 1
                if prox in PERGUNTAS_AKINATOR:
                    session['passo'] = prox
                    return jsonify({"resposta": PERGUNTAS_AKINATOR[prox]})
                else:
                    r1, r2 = session.get('resp_2'), session.get('resp_3')
                    session.clear()
                    if r1 and not r2: return jsonify({"resposta": "Aposto que é o Neymar Jr!"})
                    if not r1 and r2: return jsonify({"resposta": "Você pensou no Homem de Ferro!"})
                    return jsonify({"resposta": "Acho que é alguém muito famoso! Tente de novo."})

        # 2. DATA E HORA
        agora = datetime.now(timezone)
        if "horas" in msg: return jsonify({"resposta": f"Agora são {agora.strftime('%H:%M')}."})
        if "data" in msg or "dia é hoje" in msg: return jsonify({"resposta": f"Hoje é {agora.strftime('%d/%m/%Y')}."})

        # 3. COMANDOS FIXOS
        if msg in COMANDOS_FIXOS:
            return jsonify({"resposta": COMANDOS_FIXOS[msg]})

        # 4. CÉREBRO LLAMA 3 (VIA GROQ)
        # Se nada acima for ativado, a IA responde livremente
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "Você é a Geometry AI. Responda de forma curta, prestativa e sempre em português brasileiro."
                },
                {
                    "role": "user",
                    "content": pergunta_original,
                }
            ],
            model="llama3-8b-8192", # Modelo super rápido e inteligente
        )
        
        return jsonify({"resposta": chat_completion.choices[0].message.content})
