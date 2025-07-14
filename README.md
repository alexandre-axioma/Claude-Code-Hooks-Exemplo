# Claude Code Hooks - Template Personalizado

## Sobre Este Repositório

Este repositório serve como um **esqueleto base** para demonstrar o poder dos hooks no Claude Code. Ele implementa três hooks essenciais que considero fundamentais para uma experiência produtiva e segura com o Claude Code.

O objetivo é fornecer um ponto de partida sólido que você pode:
- **Usar diretamente** em seus projetos
- **Personalizar** conforme suas necessidades específicas  
- **Expandir** criando novos hooks com ajuda do próprio Claude Code
- **Aprender** sobre a arquitetura e possibilidades dos hooks

A documentação completa para criação de hooks personalizados está disponível em `ai_docs/` - use-a junto com assistentes de IA para desenvolver seus próprios hooks de forma interativa.

Template personalizado de hooks para Claude Code com notificações de áudio usando arquivos WAV locais do ElevenLabs.

## Pré-requisitos

- **[Astral UV](https://docs.astral.sh/uv/getting-started/installation/)** - Instalador rápido de pacotes Python
- **[Claude Code](https://docs.anthropic.com/en/docs/claude-code)** - CLI da Anthropic para Claude AI

## Passo 0: Instalação do UV

Antes de usar este template, você precisa ter o **UV** instalado. Escolha o método apropriado para seu sistema operacional:

### macOS
```bash
# Via Homebrew (recomendado)
brew install uv

# Via curl
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Linux
```bash
# Via curl
curl -LsSf https://astral.sh/uv/install.sh | sh

# Via pip
pip install uv
```

### Windows
```powershell
# Via PowerShell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Via pip
pip install uv
```

Após a instalação, verifique se está funcionando:
```bash
uv --version
```

## Funcionalidades

Este template implementa 3 hooks essenciais com notificações sonoras:

### 1. **Notification Hook** 
**Dispara:** Quando Claude precisa de input do usuário  
**Áudio:** Reproduz aleatoriamente de `audio/notification/`  
**Observabilidade:** Salva logs em `logs/notification.json`

### 2. **PreToolUse Hook**
**Dispara:** Antes de executar qualquer ferramenta  
**Segurança:** Bloqueia comandos `rm -rf` e acesso a arquivos `.env`  
**Áudio:** Reproduz aleatoriamente de `audio/blocked/` quando bloqueia  
**Observabilidade:** Salva logs em `logs/pre_tool_use.json`

### 3. **Stop Hook**
**Dispara:** Quando Claude termina de responder  
**Áudio:** Reproduz aleatoriamente de `audio/completed/`  
**Observabilidade:** Salva logs em `logs/stop.json` e conversa em `logs/chat.json`

## Estrutura do Projeto

```
.claude/
├── settings.json              # Configuração dos hooks
└── hooks/                     # Scripts dos hooks
    ├── notification.py        # Hook de notificação
    ├── pre_tool_use.py       # Hook de segurança
    ├── stop.py               # Hook de finalização
    └── utils/
        ├── audio/            # Arquivos WAV
        │   ├── notification/ # Sons para notificações
        │   ├── blocked/      # Sons para comandos bloqueados
        │   └── completed/    # Sons para tarefas concluídas
        └── tts/
            └── audio_player.py # Reprodutor de áudio

ai_docs/                      # Documentação dos hooks do Claude Code
logs/                        # Logs automáticos (criados dinamicamente)
```

## Como Configurar

### 1. **Gerar Arquivos de Áudio**

1. Acesse [ElevenLabs](https://elevenlabs.io/)
2. Escolha sua voz preferida
3. Gere os seguintes textos como arquivos WAV:

**Para notificações:** (`audio/notification/`)
- "Alexandre, seu agente precisa de sua entrada"
- "Alexandre, preciso da sua ajuda"  
- "Alexandre, sua atenção é necessária"

**Para comandos bloqueados:** (`audio/blocked/`)
- "Comando bloqueado"
- "Operação não permitida"
- "Acesso negado"

**Para tarefas concluídas:** (`audio/completed/`)
- "Tarefa concluída, Alexandre"
- "Trabalho finalizado, Alexandre"
- "Processo terminado, Alexandre"

### 2. **Instalar Template**

```bash
# Clone ou copie este repositório para seu projeto
cp -r .claude/ /caminho/do/seu/projeto/

# Os hooks já estão configurados e prontos para usar
```

### 3. **Usar em Novos Projetos**

Sempre que iniciar um novo projeto com Claude Code:

```bash
# Copie a pasta .claude para o novo projeto
cp -r /template/claude-hooks/.claude/ ./

# Os hooks funcionarão automaticamente
```

## Arquivos de Áudio Flexíveis

O sistema detecta automaticamente quantos arquivos WAV existem em cada pasta e escolhe aleatoriamente:

- ✅ **Adicione quantos quiser** - Coloque mais arquivos para maior variedade
- ✅ **Nomenclatura livre** - Qualquer nome `.wav` funciona
- ✅ **Zero configuração** - Não precisa editar código

## Características Técnicas

### **Sistema de Áudio Local**
- 🎵 **Sem APIs** - Usa arquivos WAV pré-gravados
- 💰 **Zero custo** - Sem consumo de créditos
- ⚡ **Instantâneo** - Reprodução imediata
- 🎲 **Aleatório** - Varia entre os arquivos disponíveis
- 🔊 **Multiplataforma** - Funciona em macOS, Linux e Windows

### **Observabilidade Automática** 
- 📁 **Criação dinâmica** - Pasta `logs/` criada automaticamente
- 📊 **Logs JSON** - Todos os eventos são salvos
- 💾 **Conversa exportada** - Transcrições em `chat.json`

### **Segurança Integrada**
- 🛡️ **Bloqueio de comandos perigosos** - `rm -rf` prevenido
- 🔒 **Proteção de arquivos sensíveis** - `.env` protegido
- 🔊 **Notificação sonora** - Aviso quando bloquear

## Scripts UV Independentes

Usa [UV single-file scripts](https://docs.astral.sh/uv/guides/scripts/) para:

- **Isolamento** - Cada hook é independente
- **Portabilidade** - Funciona em qualquer ambiente  
- **Simplicidade** - Sem gerenciamento de virtual environments
- **Velocidade** - Execução rápida com UV

## Configuração dos Hooks

O arquivo `.claude/settings.json` está pré-configurado:

```json
{
  "permissions": {
    "allow": [],
    "deny": []
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_tool_use.py"
          }
        ]
      }
    ],
    "Notification": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/notification.py --notify"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/stop.py --chat"
          }
        ]
      }
    ]
  }
}
```

## Como Funciona

1. **Notification**: Claude precisa de input → Som aleatório de notificação
2. **PreToolUse**: Comando perigoso detectado → Bloqueia + som de bloqueio  
3. **Stop**: Tarefa finalizada → Som de conclusão

Todos os eventos são automaticamente registrados nos logs para auditoria.

## Documentação Completa

Consulte `ai_docs/cc_hooks_docs.md` para documentação completa dos hooks do Claude Code.

---

**Template criado para uso pessoal - Alexandre**

*Inspirado no trabalho da comunidade Claude Code e especialmente no repositório [claude-code-hooks-mastery](https://github.com/disler/claude-code-hooks-mastery) que demonstra excelentes práticas de implementação de hooks.*