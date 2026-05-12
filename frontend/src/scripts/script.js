// --- VARIÁVEIS GLOBAIS AMZ ---
let servidorSelecionado = null;
const URL_BASE_BOT = "https://celestial-bot-zj6o.onrender.com"; 

// --- NAVEGAÇÃO PRINCIPAL (CORRIGIDA) ---

function acessarTelaBot() {
    // Esconde a Landing Page
    document.getElementById('site-principal').style.display = 'none';
    
    // Mostra o Painel do Bot
    const painel = document.getElementById('painel-loritta');
    painel.classList.remove('hidden');
    painel.style.display = 'flex';
    
    // Garante que a primeira tela do bot seja a AMZ BOT (bot-landing)
    document.getElementById('bot-landing').classList.remove('hidden');
    document.getElementById('lista-servidores').classList.add('hidden');
    document.getElementById('config-limpeza').classList.add('hidden');
    
    window.scrollTo(0, 0);
}

function voltarAoInicio() {
    // Esconde o Painel do Bot
    const painel = document.getElementById('painel-loritta');
    painel.style.display = 'none';
    painel.classList.add('hidden');
    
    // Mostra a Landing Page
    const site = document.getElementById('site-principal');
    site.style.display = 'flex';
    site.classList.remove('hidden');
    
    window.scrollTo(0, 0);
}

// Esta é a função que o botão "Voltar ao Hub" dentro do painel chama
function voltarAoInicioBot() {
    voltarAoInicio(); // Chama a função que reseta a tela para o Hub principal
}

// --- COMUNICAÇÃO COM O MONGODB (MANTIDA) ---

async function abrirListaServidores() {
    document.getElementById('bot-landing').classList.add('hidden');
    document.getElementById('config-limpeza').classList.add('hidden');
    document.getElementById('lista-servidores').classList.remove('hidden');

    const container = document.getElementById('container-servidores');
    container.innerHTML = '<p class="text-white/50 col-span-2 text-center animate-pulse py-10 uppercase text-[10px] tracking-widest font-mono">Buscando dados no MongoDB...</p>';

    try {
        const response = await fetch(`${URL_BASE_BOT}/api/bot-servidores`);
        if (!response.ok) throw new Error();
        
        const servidores = await response.json();
        container.innerHTML = "";

        servidores.forEach(srv => {
            const guildId = typeof srv === 'string' ? srv : srv.guild_id;
            const guildNome = srv.nome || "Servidor Discord";

            container.innerHTML += `
                <div class="server-card">
                    <div class="flex items-center gap-4">
                        <div class="w-12 h-12 bg-white/5 border border-white/10 flex items-center justify-center font-black text-[10px]">AMZ</div>
                        <div>
                            <h4 class="text-white font-bold text-sm uppercase italic">${guildNome}</h4>
                            <p class="text-neutral-600 font-mono text-[9px] uppercase tracking-widest">${guildId}</p>
                        </div>
                    </div>
                    <button onclick="abrirConfigLimpeza('${guildId}', '${guildNome}')" class="bg-white text-black px-4 py-2 text-[10px] font-black uppercase hover:bg-neutral-300 transition">
                        Configurar
                    </button>
                </div>`;
        });
    } catch (error) {
        container.innerHTML = '<p class="text-red-500/50 col-span-2 text-center py-10 uppercase text-[10px] font-bold">Erro na conexão com o banco de dados.</p>';
    }
}

function abrirConfigLimpeza(guildId, nome) {
    servidorSelecionado = guildId;
    document.getElementById('lista-servidores').classList.add('hidden');
    document.getElementById('config-limpeza').classList.remove('hidden');
    document.getElementById('nome-servidor-atual').innerText = nome;
}

async function enviarConfiguracao() {
    const canalId = document.getElementById('canal_id').value;
    const dias = document.getElementById('dias').value;
    const statusMsg = document.getElementById('status_msg');
    const icon = document.getElementById('icon-sync');

    if(!canalId) { alert("ID do canal obrigatório."); return; }

    icon.classList.add('animate-spin');
    statusMsg.classList.remove('hidden');
    statusMsg.innerText = "⏳ SINCRONIZANDO...";

    try {
        const response = await fetch(`${URL_BASE_BOT}/api/configurar-limpeza`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ servidor: servidorSelecionado, canal_id: canalId, dias: dias })
        });

        if (response.ok) {
            statusMsg.innerText = "✅ SUCESSO NO MONGODB";
            statusMsg.style.color = "white";
        } else { throw new Error(); }
    } catch (error) {
        statusMsg.innerText = "❌ ERRO DE CONEXÃO";
        statusMsg.style.color = "#ff4444";
    } finally {
        icon.classList.remove('animate-spin');
    }
}