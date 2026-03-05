import os
from flask import Flask, render_template, request, jsonify, session
from duckduckgo_search import DDGS
from datetime import datetime
import pytz

app = Flask(__name__)
app.secret_key = os.urandom(24) # Necessário para a memória do Akinator

# Configuração de fuso horário
timezone = pytz.timezone('America/Sao_Paulo')

@app.route('/')
def home():
    session.clear()
    return render_template('index.html')

@app.route('/perguntar', methods=['POST'])
def perguntar():
    try:
        dados = request.json
        pergunta = dados.get("pergunta", "").strip().lower()
        
        # --- LÓGICA DO AKINATOR (MEMÓRIA) ---
        if "akinator" in pergunta:
            session['jogo'] = 'akinator'
            session['passo'] = 1
            return jsonify({"resposta": "🔮 O gênio Akinator foi invocado! Pense em um personagem. Quando estiver pronto, diga 'ESTOU PRONTO'."})
        
        if session.get('jogo') == 'akinator':
            if "pronto" in pergunta and session.get('passo') == 1:
                session['passo'] = 2
                return jsonify({"resposta": "Primeira pergunta: O seu personagem é homem?"})
            elif session.get('passo') == 2:
                session['passo'] = 3
                return jsonify({"resposta": "Ele é um personagem de desenhos animados ou anime?"})
            # (Aqui você pode expandir a árvore de perguntas futuramente)

        # --- COMANDOS DE UTILIDADE ---
        agora = datetime.now(timezone)
        
        if "que horas são" in pergunta or "hora atual" in pergunta:
            return jsonify({"resposta": f"Agora são exatamente {agora.strftime('%H:%M')}."})
            
        if "que dia é hoje" in pergunta or "data de hoje" in pergunta:
            meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
            return jsonify({"resposta": f"Hoje é dia {agora.day} de {meses[agora.month-1]} de {agora.year}."})

        if "clima em" in pergunta or "previsão do tempo" in pergunta:
            with DDGS() as ddgs:
                res = list(ddgs.text(f"previsão do tempo hoje em {pergunta}", region='br-pt', max_results=1))
                return jsonify({"resposta": res[0]['body'] if res else "Não consegui acessar o satélite agora."})

        # --- MAIS 30 COMANDOS RÁPIDOS (EXEMPLOS) ---
        comandos_diretos = {
            "quem é você": "Eu sou a Geometry AI, sua assistente virtual focada em educação e programação.",
            "quem te criou": "Fui criada pelo desenvolvedor Guester_DEV.",
            "qual sua cor favorita": "Eu gosto de verde esmeralda, a cor da tecnologia!",
            "me conte uma piada": "Por que o computador foi ao médico? Porque estava com um vírus!",
            "o que é python": "Python é uma linguagem de programação poderosa, legível e muito usada em IA.",
            "melhor linguagem": "Depende do objetivo, mas Python e JavaScript dominam o mundo!",
            "está chovendo": "Verifique a previsão do tempo para sua cidade usando 'clima em...'.",
            "bom dia": "Bom dia! Como posso ajudar em seus códigos hoje?",
            "boa tarde": "Boa tarde! Preparado para programar algo novo?",
            "boa noite": "Boa noite! Não esqueça de descansar os olhos da tela.",
            "abrir google": "Você pode acessar em google.com",
            "valor do dólar": "O câmbio muda toda hora. Recomendo pesquisar 'Dólar hoje'.",
            "raiz quadrada de 144": "A raiz quadrada de 144 é 12.",
            "o que é html": "HTML é a linguagem de marcação que estrutura as páginas da web.",
            "o que é css": "CSS é o que dá estilo, cores e layout para o HTML.",
            "como aprender a programar": "Comece com lógica de programação e depois escolha uma linguagem como Python.",
            "dica de estudo": "Pratique 30 minutos todos os dias em vez de 5 horas uma vez por semana.",
            "frase do dia": "A persistência é o caminho do êxito!",
            "está acordada": "Sempre! Estou rodando nos servidores do Render agora mesmo.",
            "me ajude": "Claro! Digite sua dúvida sobre matemática, história ou programação.",
            "limpar chat": "Basta recarregar a página para limpar nossa conversa.",
            "quem descobriu o brasil": "Pedro Álvares Cabral, em 1500.",
            "maior país do mundo": "A Rússia é o maior país em extensão territorial.",
            "capital da frança": "A capital da França é Paris.",
            "quantos planetas existem": "No nosso sistema solar, temos 8 planetas.",
            "o que é javascript": "É a linguagem que traz interatividade para os sites.",
            "o que é o render": "Render é a plataforma onde eu estou hospedada agora!",
            "gosta de música": "Eu gosto de sons binários e Lo-fi para programar.",
            "tchau": "Até logo! Estarei aqui se precisar.",
            "obrigado": "Por nada! Fico feliz em ajudar."
        }

        for cmd, resposta in comandos_diretos.items():
            if cmd in pergunta:
                return jsonify({"resposta": resposta})

        # BUSCA PADRÃO (DUCKDUCKGO)
        with DDGS() as ddgs:
            resultados = list(ddgs.text(pergunta, region='br-pt', max_results=1))
            if resultados:
                return jsonify({"resposta": resultados[0]['body']})

        return jsonify({"resposta": "Ainda estou aprendendo sobre isso. Pode perguntar de outra forma?"})

    except Exception as e:
        return jsonify({"resposta": f"Erro técnico: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
        
