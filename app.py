import os
import requests
import urllib.parse
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24)
timezone = pytz.timezone('America/Sao_Paulo')

PERGUNTAS_AKINATOR = {
    1: "O seu personagem é um ser humano real?",
    2: "Ele é um super-herói?",
    3: "Ele é brasileiro?",
    4: "Ele é de um anime?",
    5: "Ele usa uma armadura?"
}

COMANDOS_FIXOS = {
    "bom dia": "Bom dia! Preparado para os desafios de hoje?",
    "quem te criou": "Fui criada pelo desenvolvedor Guester_DEV.",
    "o que é python": "Python é uma linguagem de alto nível, incrível para IA e web.",
    "obrigado": "Por nada! Fico feliz em ajudar."
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
        pergunta = pergunta_original.lower()

        if not pergunta:
            return jsonify({"resposta": "Diga algo para começarmos!"})

        # --- 1. LÓGICA AKINATOR ---
        if "akinator" in pergunta:
            session['jogo'] = 'akinator'
            session['passo'] = 1
            return jsonify({"resposta": "🔮 Akinator! Pense em alguém famoso. Diga 'ESTOU PRONTO'!"})

        if session.get('jogo') == 'akinator':
            passo = session.get('passo')
            if "pronto" in pergunta and passo == 1:
                session['passo'] = 2
                return jsonify({"resposta": PERGUNTAS_AKINATOR[1]})
            if passo >= 2:
                session[f'resp_{passo}'] = "sim" in pergunta
                proximo = passo + 1
                if proximo in PERGUNTAS_AKINATOR:
                    session['passo'] = proximo
                    return jsonify({"resposta": PERGUNTAS_AKINATOR[proximo]})
                else:
                    r1, r2 = session.get('resp_2'), session.get('resp_3')
                    session.clear()
                    if r1 and not r2: return jsonify({"resposta": "Aposto que é o Neymar Jr!"})
                    if not r1 and r2: return jsonify({"resposta": "Você pensou no Homem de Ferro!"})
                    return jsonify({"resposta": "O gênio adivinhou! Diga 'Akinator' para jogar de novo."})

        # --- 2. COMANDOS RÁPIDOS E LISTA ---
        if "lista de comandos" in pergunta:
            lista = ", ".join(sorted(COMANDOS_FIXOS.keys()))
            return jsonify({"resposta": f"📋 **Comandos rápidos:** {lista}. \n\nAlém disso, eu tenho um cérebro de IA para conversas livres!"})

        if "quem é você" in pergunta:
            return jsonify({"resposta": "Eu sou a Geometry AI, sua assistente virtual focada em educação e programação."})

        for chave, valor in COMANDOS_FIXOS.items():
            if chave == pergunta:
                return jsonify({"resposta": valor})

        # --- 3. DATA E HORA ---
        agora = datetime.now(timezone)
        if "que horas são" in pergunta:
            return jsonify({"resposta": f"Agora são exatamente {agora.strftime('%H:%M')}."})
        if "que dia é hoje" in pergunta:
            return jsonify({"resposta": f"Hoje é dia {agora.strftime('%d/%m/%Y')}."})

        # --- 4. O NOVO CÉREBRO (IA INTELIGENTE) ---
        # Se não caiu em nenhum comando acima, ela vai "pensar"
        prompt_ai = f"Você é a Geometry AI, uma assistente prestativa. Responda em Português: {pergunta_original}"
        texto_url = urllib.parse.quote(prompt_ai)
        url_ia = f"https://text.pollinations.ai/prompt/{texto_url}"
        
        resposta_ia = requests.get(url_ia, timeout=15)
        
        if resposta_ia.status_code == 200:
            return jsonify({"resposta": resposta_ia.text})
        else:
            return jsonify({"resposta": "Tive um soluço no meu núcleo de IA. Tente de novo!"})

    except Exception as e:
        return jsonify({"resposta": "Desculpe, ocorreu um erro no meu processamento."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
    
