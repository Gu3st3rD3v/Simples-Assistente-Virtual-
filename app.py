import os
from flask import Flask, render_template, request, jsonify
from duckduckgo_search import DDGS

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
            return jsonify({"resposta": "Por favor, digite alguma coisa."})
            
        pergunta_min = pergunta.lower()
        if pergunta_min in ["oi", "olá", "ola", "bom dia", "boa noite"]:
            return jsonify({"resposta": "Olá! Eu sou a Geometry AI. O que você gostaria de pesquisar na internet hoje?"})

        # --- SISTEMA DE PESQUISA AVANÇADO ---
        try:
            # Pesquisa a frase inteira no motor de busca e pega o primeiro resultado
            resultados = DDGS().text(pergunta, region='br-pt', max_results=1)
            
            if resultados:
                resumo = resultados[0]['body']
                link = resultados[0]['href']
                
                resposta_formatada = f"{resumo}\n\n(Fonte: {link})"
                return jsonify({"resposta": resposta_formatada})
            else:
                return jsonify({"resposta": "Não encontrei uma resposta clara para isso na internet."})
                
        except Exception as e:
            return jsonify({"resposta": "Desculpe, o servidor de buscas está muito ocupado no momento. Tente novamente."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, tive um problema técnico interno."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            
            # Se achou o resumo, ele responde
            if "extract" in dados_wiki:
                return jsonify({"resposta": dados_wiki["extract"]})
            else:
                return jsonify({"resposta": "Não encontrei informações exatas sobre isso na minha base."})
        except:
            return jsonify({"resposta": "Desculpe, tente pesquisar usando apenas palavras-chave simples (ex: 'Brasil', 'Fotossíntese', 'Albert Einstein')."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, tive um pequeno problema técnico. Tente novamente."})

if __name__ == "__main__":
    # Garante que a porta do Render seja respeitada
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
