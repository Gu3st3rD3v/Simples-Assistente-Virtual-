import os
from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Coloque sua API Key aqui dentro das aspas
genai.configure(api_key="SUA_CHAVE_AQUI")
model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "")
        
        if not pergunta:
            return jsonify({"resposta": "Você enviou uma mensagem vazia."})

        resposta_ia = model.generate_content(pergunta)
        return jsonify({"resposta": resposta_ia.text})
    except Exception as e:
        return jsonify({"resposta": f"Erro na IA: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
            
            if not resultados:
                return jsonify({"resposta": "Não encontrei nada sobre isso. Tente perguntar de outro jeito."})
                
            # Pega o título exato do melhor resultado que o buscador achou
            melhor_titulo = resultados[0]["title"]
            titulo_seguro = urllib.parse.quote(melhor_titulo)
            
            # Passo 2: Pega o resumo desse assunto específico
            url_resumo = f"https://pt.wikipedia.org/api/rest_v1/page/summary/{titulo_seguro}"
            req_resumo = urllib.request.Request(url_resumo, headers={'User-Agent': 'Mozilla/5.0'})
            resposta_resumo = urllib.request.urlopen(req_resumo).read()
            dados_resumo = json.loads(resposta_resumo)
            
            if "extract" in dados_resumo:
                texto_final = dados_resumo["extract"]
                # Tenta pegar o link da fonte para ficar mais profissional
                link_fonte = dados_resumo.get("content_urls", {}).get("desktop", {}).get("page", "")
                if link_fonte:
                    texto_final += f"\n\n(Fonte: {link_fonte})"
                    
                return jsonify({"resposta": texto_final})
            else:
                return jsonify({"resposta": "Achei o tema, mas o artigo está vazio."})
                
        except Exception as e:
            print(f"Erro na pesquisa: {e}") # Ajuda a ver o erro no log do Render
            return jsonify({"resposta": "Desculpe, minha conexão com a base de dados falhou."})
            
    except Exception as e:
        return jsonify({"resposta": "Ops, erro interno."})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
