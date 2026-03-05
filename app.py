import os
from flask import Flask, render_template, request, jsonify
from g4f.client import Client

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

        # --- MOTOR GEOMETRY AI G4F (SEM CHAVE) ---
        client = Client()
        try:
            # Forçamos a instrução para ela sempre falar em Português e ser programadora
            prompt_sistema = f"Você é a Geometry AI, uma inteligência artificial programadora. Responda sempre em Português do Brasil. Pergunta: {pergunta}"
            
            response = client.chat.completions.create(
                model="gpt-4o", # Ela vai tentar usar o motor do GPT-4
                messages=[{"role": "user", "content": prompt_sistema}],
            )
            
            resposta_final = response.choices[0].message.content
            return jsonify({"resposta": resposta_final})

        except Exception as e:
            print(f"Erro no motor principal: {e}")
            return jsonify({"resposta": "Tive um problema no meu núcleo de processamento. Tente novamente em instantes."})

    except Exception:
        return jsonify({"resposta": "Erro de conexão com o servidor."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
    
