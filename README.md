🤖 AutoBot

Bot de automação de teclado e mouse via terminal. Pressiona uma tecla ou clica um botão do mouse repetidamente, com intervalo configurável e hotkeys para ligar/desligar sem sair do programa.


✨ Funcionalidades


Modo Tecla — pressiona qualquer letra, número ou tecla especial repetidamente
Modo Mouse — clica o botão esquerdo, direito ou do meio repetidamente
Intervalo configurável — de 0,001s (1000 ações/s) até 60s entre ações
Hotkeys personalizáveis — defina as teclas F5–F12 para ligar/desligar e sair
Menu interativo no terminal — sem interface gráfica, sem dependências pesadas
Thread em background — o bot roda enquanto você usa outros programas



📋 Pré-requisitos


Python 3.7+
Biblioteca pynput



🚀 Instalação

bash# 1. Clone o repositório
git clone https://github.com/LBenetao/Bot_Autoclicker
cd autobot

# 2. Instale a dependência
pip install pynput


Linux: dependendo do ambiente de desktop, pode ser necessário instalar extras:

bashsudo apt install python3-xlib  # para X11
pip install pynput

Em alguns sistemas é necessário rodar com sudo.




▶️ Como usar

bashpython autobot.py

Ao iniciar, você verá o menu principal:

──────────────────────────────────────────────────
  🤖  AutoBot — Automação de Tecla / Mouse
──────────────────────────────────────────────────

  Modo     : tecla 'l'
  Intervalo: 0.100s  (10.0 ações/s)
  Ligar/Des: F6
  Sair     : F8
  Status   : ⏸  parado
──────────────────────────────────────────────────

  O que deseja configurar?

  [1] Modo (tecla / mouse)
  [2] Qual tecla pressionar
  [3] Intervalo entre ações
  [4] Hotkeys (ligar/desligar e sair)
  [5] ▶  INICIAR BOT
  [0] Sair

Configure o que precisar e escolha [5] INICIAR BOT. O bot começa pausado — use as hotkeys para controlar:

Hotkey padrãoAçãoF6Liga / Desliga o botF8Para o bot e volta ao menu


⚙️ Opções de configuração

Modo de ação

OpçãoDescriçãoTeclaPressiona e solta uma tecla do tecladoMouseClica um botão do mouse

Teclas suportadas

Qualquer letra (a–z) ou número (0–9), além das teclas especiais:

NomeTeclaNomeTeclaspaceEspaçoenterEntertabTabescEscapebackspaceBackspacedeleteDeleteup↑down↓left←right→homeHomeendEndpage_upPage Uppage_downPage DownctrlCtrlshiftShiftaltAltf1–f12F1–F12

Botões do mouse

OpçãoBotão1Esquerdo (padrão)2Direito3Meio (scroll)

Intervalo entre ações

ValorVelocidade0.01~100 ações/s — muito rápido0.05~20 ações/s — rápido0.1~10 ações/s — padrão0.5~2 ações/s — lento1.01 ação/s — muito lento

Aceita qualquer valor entre 0.001 e 60 segundos.

Hotkeys personalizáveis

As teclas de controle do bot podem ser configuradas no menu [4]. Disponíveis: F5 a F12.


🗂️ Estrutura do projeto

autobot/
└── autobot.py   # script principal (single-file)


🛡️ Aviso de uso

Este bot foi criado para fins de automação pessoal e produtividade (testes, jogos, tarefas repetitivas). Use com responsabilidade. O uso em plataformas que proíbem automação pode resultar em banimento de conta.

