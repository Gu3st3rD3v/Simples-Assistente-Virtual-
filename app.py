import os
import requests
import urllib.parse
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip()
        
        if not pergunta:
            return jsonify({"resposta": "Por favor, digite sua dúvida."})

        # --- MOTOR GEOMETRY AI DEFINITIVO (SEM CHAVE E ANTI-BLOQUEIO) ---
        try:
            # Instrução mestre para ela ser programadora e falar em PT-BR
            prompt_sistema = f"Você é a Geometry AI, uma inteligência artificial programadora. Responda sempre em Português do Brasil. Pergunta: {pergunta}"
            
            # Prepara o texto para virar um link válido
            texto_formatado = urllib.parse.quote(prompt_sistema)
            url = f"https://text.pollinations.ai/prompt/{texto_formatado}"
            
            # Faz a pergunta para a IA
            resposta = requests.get(url, timeout=30)
            
            if resposta.status_code == 200:
                resposta_final = resposta.text
                return jsonify({"resposta": resposta_final})
            else:
                return jsonify({"resposta": "Ocorreu um congestionamento na rede. Tente de novo!"})

        except Exception as e:
            print(f"Erro de conexão com o motor: {e}")
            return jsonify({"resposta": "Minha conexão falhou. Pode repetir a pergunta?"})

    except Exception:
        return jsonify({"resposta": "Erro interno no servidor da Geometry AI."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

    except Exception:
        return jsonify({"resposta": "Erro de conexão com o servidor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
