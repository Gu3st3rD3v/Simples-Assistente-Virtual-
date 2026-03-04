const chatContainer = document.getElementById('chat-container');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

async function enviarMensagem() {
    const texto = userInput.value.trim();
    if (!texto) return;

    // 1. Adiciona sua mensagem na tela
    adicionarMensagem(texto, 'user');
    userInput.value = '';

    // 2. Cria um balão de "pensando..."
    const botMsgDiv = adicionarMensagem("Digitando...", 'bot');

    try {
        // 3. Faz a chamada para o seu servidor no Render
        // IMPORTANTE: Se o JS estiver no mesmo servidor que o Python, use '/perguntar'
        const response = await fetch('/perguntar', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ pergunta: texto })
        });

        const data = await response.json();
        
        // 4. Substitui o "digitando" pela resposta real
        botMsgDiv.innerText = data.resposta;

    } catch (error) {
        botMsgDiv.innerText = "Ops, tive um problema para me conectar ao servidor.";
        console.error("Erro:", error);
    }
}

function adicionarMensagem(texto, tipo) {
    const div = document.createElement('div');
    div.classList.add('message', tipo);
    div.innerText = texto;
    chatContainer.appendChild(div);
    
    // Rola para o final do chat
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return div;
}

// Ouvintes de eventos
sendBtn.addEventListener('click', enviarMensagem);
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') enviarMensagem();
});
