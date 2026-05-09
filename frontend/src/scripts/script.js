// --- VARIÁVEIS GLOBAIS AMZ ---
let servidorSelecionado = null;
const URL_BASE_BOT = "https://celestial-bot-zj6o.onrender.com"; // Seu Backend no Render
const CLIENT_ID = '1479103284064026787'; // ID do Celestial Bot

// Pega a URL atual automaticamente (funciona tanto no PC quanto no GitHub Pages)
const REDIRECT_URI = window.location.origin + window.location.pathname;

// --- AUTENTICAÇÃO DISCORD ---
function fazerLoginDiscord() {
    const url = `https://discord.com/api/oauth2/authorize?client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&response_type=token&scope=identify%20guilds`;
    window.location.href = url;
}

window.addEventListener('load', () => {
    const fragment = new URLSearchParams(window.location.hash.slice(1));
    const token = fragment.get('access_token');
    
    if (token) {
        // Limpa a URL para ficar mais limpa
        window.history.replaceState({}, document.title, window.location.pathname);
        mostrarPainel();
    }
});

// --- NAVEGAÇÃO DE INTERFACE ---
function mostrarPainel() {
    document.getElementById('site-principal').classList.add('hidden');
    const painel = document.getElementById('painel-loritta');
    painel.classList.remove('hidden');
    painel.classList.add('flex');
    voltarAoInicioBot();
}

function voltarAoInicio() {
    document.getElementById('painel-loritta').classList.remove('flex');
    document.getElementById('painel-loritta').classList.add('hidden');
    const site = document.getElementById('site-principal');
    site.classList.remove('hidden');
    site.classList.add('flex');
}

function voltarAoInicioBot() {
    document.getElementById('bot-landing').classList.remove('hidden');
    document.getElementById('lista-servidores').classList.add('hidden');
    document.getElementById('config-limpeza').classList.add('hidden');
}

// --- COMUNICAÇÃO COM O BOT (RENDER) ---
async function abrirListaServidores() {
    document.getElementById('bot-landing').classList.add('hidden');
    document.getElementById('config-limpeza').classList.add('hidden');
    document.getElementById('lista-servidores').classList.remove('hidden');

    const container = document.getElementById('container-servidores');
    container.innerHTML = '<p class="text-white/50 col-span-2 text-center animate-pulse py-10 uppercase text-[10px] tracking-widest">Consultando MongoDB via Render...</p>';

    try {
        const response = await fetch(`${URL_BASE_BOT}/api/bot-servidores`);
        if (!response.ok) throw new Error(`Erro: ${response.status}`);
        
        const servidores = await response.json();
        container.innerHTML = "";

        if (!Array.isArray(servidores) || servidores.length === 0) {
            container.innerHTML = '<p class="text-white/50 col-span-2 text-center py-10 uppercase text-[10px] tracking-widest">Nenhum servidor ativo encontrado.</p>';
            return;
        }

        servidores.forEach(srv => {
            const guildId = typeof srv === 'string' ? srv : srv.guild_id;
            const guildNome = srv.nome || "Servidor Discord";

            container.innerHTML += `
                <div class="server-card">
                    <div class="flex items-center gap-4">
                        <div class="server-icon bg-white/10 flex items-center justify-center font-black text-xs">AMZ</div>
                        <div>
                            <h4 class="text-white font-bold text-sm">${guildNome}</h4>
                            <p class="text-neutral-500 text-[10px] uppercase tracking-widest">ID: ${guildId}</p>
                        </div>
                    </div>
                    <button onclick="abrirConfigLimpeza('${guildId}', '${guildNome}')" 
                            class="btn-config">
                        Configurar
                    </button>
                </div>
            `;
        });
    } catch (error) {
        container.innerHTML = '<p class="text-red-400 col-span-2 text-center py-10 uppercase text-[10px] font-bold">Erro de conexão com o Bot. Verifique o Render.</p>';
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

    if(!canalId) {
        alert("Por favor, insira o ID do canal.");
        return;
    }

    icon.classList.add('animate-spin');
    statusMsg.classList.remove('hidden');
    statusMsg.innerText = "⏳ Sincronizando com MongoDB...";
    statusMsg.className = "text-[9px] uppercase tracking-widest text-center mt-6 font-black text-white/50";

    try {
        const response = await fetch(`${URL_BASE_BOT}/api/configurar-limpeza`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                servidor: servidorSelecionado, 
                canal_id: canalId, 
                dias: dias 
            })
        });

        if (response.ok) {
            statusMsg.innerText = "✅ Sincronizado com sucesso!";
            statusMsg.classList.add("text-white");
        } else {
            throw new Error();
        }
    } catch (error) {
        statusMsg.innerText = "❌ Erro ao salvar configurações.";
        statusMsg.classList.add("text-red-500");
    } finally {
        icon.classList.remove('animate-spin');
    }
}