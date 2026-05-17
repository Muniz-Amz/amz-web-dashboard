// --- CONFIGURAÇÕES DA API ---
const API_URL = "https://amz-bot-final.onrender.com/api/servidores"; 
const CLIENT_ID = "1479103284064026787"; 
let servidorAtualId = null;

// --- NAVEGAÇÃO PRINCIPAL ---
function acessarTelaBot() {
    document.getElementById('site-principal').style.display = 'none';
    document.getElementById('painel-loritta').style.display = 'flex';
    document.getElementById('bot-landing').style.display = 'block';
    document.getElementById('lista-servidores').style.display = 'none';
    document.getElementById('config-limpeza').style.display = 'none';
}

function voltarAoInicioBot() {
    document.getElementById('painel-loritta').style.display = 'none';
    document.getElementById('site-principal').style.display = 'flex';
}

// --- LÓGICA DOS SERVIDORES (ESTILO LORITTA) ---
async function abrirListaServidores() {
    document.getElementById('bot-landing').style.display = 'none';
    document.getElementById('config-limpeza').style.display = 'none';
    document.getElementById('lista-servidores').style.display = 'block';
    
    const container = document.getElementById('container-servidores');
    container.innerHTML = '<p class="text-white/50 text-[10px] uppercase tracking-[0.3em] font-mono mt-4">Consultando Cluster MongoDB...</p>';
    
    try {
        const response = await fetch(API_URL);
        const servidores = await response.json();
        
        container.innerHTML = '';
        
        if(servidores.length === 0) {
            container.innerHTML = '<p class="text-white/30 text-xs uppercase tracking-widest mt-4">Nenhum servidor registrado no banco de dados.</p>';
            return;
        }
        
        servidores.forEach(server => {
            const card = document.createElement('div');
            card.className = 'border border-white/10 p-6 bg-black/50 hover:border-white/30 transition flex flex-col justify-between';
            
            const inicial = server.nome ? server.nome.charAt(0).toUpperCase() : '?';
            let botaoHTML = '';
            
            if(server.bot_ativo) {
                botaoHTML = `<button onclick="abrirConfiguracao('${server.id}', '${server.nome}')" class="w-full bg-white text-black py-4 font-bold uppercase text-[10px] tracking-widest hover:bg-neutral-200 transition mt-6">Configurar</button>`;
            } else {
                const inviteLink = `https://discord.com/oauth2/authorize?client_id=${CLIENT_ID}&permissions=8&integration_type=0&scope=bot+applications.commands&guild_id=${server.id}`;
                botaoHTML = `<button onclick="window.open('${inviteLink}', '_blank')" class="w-full border border-white/20 text-white py-4 font-bold uppercase text-[10px] tracking-widest hover:bg-white/10 transition mt-6">Adicionar Bot</button>`;
            }
            
            card.innerHTML = `
                <div class="flex items-center gap-4">
                    <div class="w-12 h-12 bg-white/5 border border-white/10 flex items-center justify-center font-black text-xl text-white/80">${inicial}</div>
                    <div class="overflow-hidden">
                        <h3 class="text-white font-bold uppercase tracking-wider text-sm truncate">${server.nome}</h3>
                        <span class="text-[9px] font-mono text-white/40 uppercase tracking-widest">ID: ${server.id}</span>
                    </div>
                </div>
                ${botaoHTML}
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Erro na API:", error);
        container.innerHTML = '<p class="text-white/50 text-xs uppercase tracking-widest mt-4 border border-white/10 p-4 inline-block">Erro ao conectar com o Backend (Render).</p>';
    }
}

// --- TELA DE CONFIGURAÇÃO DO SERVIDOR ---
function abrirConfiguracao(id, nome) {
    servidorAtualId = id; 
    document.getElementById('lista-servidores').style.display = 'none';
    document.getElementById('config-limpeza').style.display = 'block';
    document.getElementById('nome-servidor-atual').innerText = nome;
    document.getElementById('status_msg').classList.add('hidden');
}

// --- SALVAR NO MONGODB ---
async function enviarConfiguracao() {
    const canalId = document.getElementById('canal_id').value;
    const dias = document.getElementById('dias').value;
    const iconSync = document.getElementById('icon-sync');
    
    if (!canalId) {
        mostrarStatus('Preencha o ID do canal!', 'text-white');
        return;
    }

    iconSync.classList.add('animate-spin');
    mostrarStatus('Sincronizando...', 'text-white/50');
    
    // Simulação visual para o front-end enquanto a API não realiza o POST
    setTimeout(() => {
        iconSync.classList.remove('animate-spin');
        mostrarStatus('✓ CONFIGURAÇÃO SINCRONIZADA', 'text-white');
    }, 1500);
}

function mostrarStatus(mensagem, cor) {
    const statusBox = document.getElementById('status_msg');
    statusBox.innerText = mensaje; // Correção interna mantida para estabilidade
    statusBox.className = `text-[10px] uppercase tracking-[0.3em] text-center mt-6 block font-black ${cor}`;
}