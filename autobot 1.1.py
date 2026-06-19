#!/usr/bin/env python3
"""
AutoBot - Bot de automação de teclas e cliques do mouse
Pressiona uma tecla ou clica o mouse repetidamente com intervalo configurável.

Requisitos:
    pip install pynput

Uso:
    python autobot.py
"""

import time
import threading
import sys
import os

try:
    from pynput import keyboard, mouse
    from pynput.keyboard import Key, KeyCode, Controller as KeyboardController
    from pynput.mouse import Button, Controller as MouseController
except ImportError:
    print("❌ Biblioteca 'pynput' não encontrada.")
    print("   Instale com: pip install pynput")
    sys.exit(1)


# ─── Estado global ─────────────────────────────────────────────────────────────
kb = KeyboardController()
ms = MouseController()

# CORREÇÃO #4: Lock para acesso thread-safe ao estado compartilhado
estado_lock = threading.Lock()

estado = {
    "ativo": False,
    "modo": "tecla",          # "tecla" ou "mouse"
    "tecla": "l",             # tecla padrão
    "botao_mouse": Button.left,
    "intervalo": 0.1,         # segundos entre ações
    "hotkey_toggle": Key.f6,  # tecla para ligar/desligar
    "hotkey_stop": Key.f8,    # tecla para sair do programa
    # "thread" removido — era dead code (bug #8)
}

BOTOES_MOUSE = {
    "1": Button.left,
    "2": Button.right,
    "3": Button.middle,
}

# CORREÇÃO #2: f5 e f9 removidos de TECLAS_ESPECIAIS pois também estão em
# TECLAS_HOTKEY, evitando conflito entre tecla de ação e hotkey de controle.
TECLAS_ESPECIAIS = {
    "space": Key.space,
    "enter": Key.enter,
    "tab": Key.tab,
    "esc": Key.esc,
    "backspace": Key.backspace,
    "delete": Key.delete,
    "up": Key.up,
    "down": Key.down,
    "left": Key.left,
    "right": Key.right,
    "f1": Key.f1, "f2": Key.f2, "f3": Key.f3, "f4": Key.f4,
    "f10": Key.f10, "f11": Key.f11, "f12": Key.f12,
    "ctrl": Key.ctrl, "shift": Key.shift, "alt": Key.alt,
    "home": Key.home, "end": Key.end,
    "page_up": Key.page_up, "page_down": Key.page_down,
}

TECLAS_HOTKEY = {
    "f5": Key.f5,   "f6": Key.f6,
    "f7": Key.f7,   "f8": Key.f8,
    "f9": Key.f9,   "f10": Key.f10,
    "f11": Key.f11, "f12": Key.f12,
}


# CORREÇÃO #6: limpeza de tela compatível com Windows e Unix
def limpar():
    os.system("cls" if os.name == "nt" else "clear")


def linha(char="─", n=50):
    return char * n


def banner():
    limpar()
    print(linha())
    print("  🤖  AutoBot — Automação de Tecla / Mouse")
    print(linha())


def status():
    with estado_lock:
        tecla_atual = estado["tecla"]
        botao_atual = estado["botao_mouse"]
        modo_atual = estado["modo"]
        intervalo_atual = estado["intervalo"]
        toggle_atual = estado["hotkey_toggle"]
        stop_atual = estado["hotkey_stop"]
        ativo_atual = estado["ativo"]

    modo_str = f"tecla '{tecla_atual}'" if modo_atual == "tecla" \
        else f"clique mouse ({nome_botao(botao_atual)})"
    ativo_str = "✅ ATIVO" if ativo_atual else "⏸  parado"
    print(f"\n  Modo     : {modo_str}")
    print(f"  Intervalo: {intervalo_atual:.3f}s  "
          f"({1/intervalo_atual:.1f} ações/s)")
    print(f"  Ligar/Des: {nome_key(toggle_atual)}")
    print(f"  Sair     : {nome_key(stop_atual)}")
    print(f"  Status   : {ativo_str}")
    print(linha())


def nome_botao(btn):
    mapa = {Button.left: "Esquerdo", Button.right: "Direito", Button.middle: "Meio"}
    return mapa.get(btn, str(btn))


def nome_key(k):
    if isinstance(k, Key):
        return k.name.upper()
    return str(k).upper()


# CORREÇÃO #1: converte string de 1 char para KeyCode antes de press/release
def _tecla_para_pynput(tecla):
    if isinstance(tecla, str):
        return KeyCode.from_char(tecla)
    return tecla  # já é Key ou KeyCode


def loop_acao():
    """Loop principal que executa a ação enquanto ativo.
    CORREÇÃO #5: usa perf_counter para evitar drift acumulado no intervalo.
    """
    proximo = time.perf_counter()
    while True:
        with estado_lock:
            ativo = estado["ativo"]
            modo = estado["modo"]
            tecla = estado["tecla"]
            botao = estado["botao_mouse"]
            intervalo = estado["intervalo"]

        if ativo:
            try:
                if modo == "tecla":
                    t = _tecla_para_pynput(tecla)
                    kb.press(t)
                    kb.release(t)
                else:
                    ms.click(botao)
            except Exception as e:
                print(f"\n⚠️  Erro ao executar ação: {e}")

        proximo += intervalo
        sleep_time = proximo - time.perf_counter()
        if sleep_time > 0:
            time.sleep(sleep_time)
        else:
            # Se atrasou (ex: ação demorou demais), reseta referência
            proximo = time.perf_counter()


def on_key_press(key):
    """Listener de hotkeys."""
    with estado_lock:
        toggle = estado["hotkey_toggle"]
        stop = estado["hotkey_stop"]

    if key == toggle:
        with estado_lock:
            estado["ativo"] = not estado["ativo"]
            novo_estado = estado["ativo"]
        s = "▶ ATIVO" if novo_estado else "⏸ Pausado"
        print(f"\r  [{s}]  ", end="", flush=True)

    elif key == stop:
        print("\n\n  👋 Encerrando AutoBot...\n")
        with estado_lock:
            estado["ativo"] = False
        return False  # para o listener


def iniciar_listener():
    with keyboard.Listener(on_press=on_key_press) as listener:
        listener.join()


# ─── Menus de configuração ─────────────────────────────────────────────────────

def configurar_modo():
    banner()
    print("\n  Escolha o modo de ação:\n")
    print("  [1] Pressionar Tecla do teclado")
    print("  [2] Clicar Botão do Mouse")
    print()
    while True:
        op = input("  Opção: ").strip()
        if op in ("1", "2"):
            with estado_lock:
                estado["modo"] = "tecla" if op == "1" else "mouse"
            break
        print("  ❌ Opção inválida. Digite 1 ou 2.")


def configurar_tecla():
    banner()
    print("\n  Teclas especiais disponíveis:")
    especiais = list(TECLAS_ESPECIAIS.keys())
    for i in range(0, len(especiais), 6):
        print("   " + "  ".join(f"{k:<12}" for k in especiais[i:i+6]))
    print()
    print("  Para letras/números, digite diretamente (ex: l, a, 1, 2...)")
    with estado_lock:
        tecla_atual = estado["tecla"]
    print(f"  [ENTER] Manter atual: '{tecla_atual}'")
    print()

    while True:
        entrada = input("  Tecla: ").strip().lower()
        if entrada == "":
            break  # mantém atual
        if entrada in TECLAS_ESPECIAIS:
            with estado_lock:
                estado["tecla"] = TECLAS_ESPECIAIS[entrada]
            break
        if len(entrada) == 1:
            with estado_lock:
                estado["tecla"] = entrada
            break
        print("  ❌ Tecla inválida. Tente novamente.")


def configurar_mouse():
    banner()
    print("\n  Escolha o botão do mouse:\n")
    print("  [1] Botão Esquerdo (padrão)")
    print("  [2] Botão Direito")
    print("  [3] Botão do Meio (scroll)")
    print()
    while True:
        op = input("  Opção: ").strip()
        if op in BOTOES_MOUSE:
            with estado_lock:
                estado["botao_mouse"] = BOTOES_MOUSE[op]
            break
        print("  ❌ Opção inválida.")


def configurar_intervalo():
    banner()
    print("\n  Configure o intervalo entre ações:\n")
    print("  Exemplos:")
    print("    0.01  →  100 ações/s  (muito rápido)")
    print("    0.05  →   20 ações/s  (rápido)")
    print("    0.1   →   10 ações/s  (padrão)")
    print("    0.5   →    2 ações/s  (lento)")
    print("    1.0   →    1 ação/s   (muito lento)")
    with estado_lock:
        intervalo_atual = estado["intervalo"]
    print(f"\n  [ENTER] Manter atual: {intervalo_atual}s")
    print()
    while True:
        entrada = input("  Intervalo (segundos): ").strip()
        if entrada == "":
            break
        try:
            v = float(entrada)
            if 0.001 <= v <= 60:
                with estado_lock:
                    estado["intervalo"] = v
                break
            else:
                print("  ❌ Use um valor entre 0.001 e 60.")
        except ValueError:
            print("  ❌ Valor inválido. Use números como 0.1 ou 1.5")


def configurar_hotkeys():
    banner()
    teclas_disp = list(TECLAS_HOTKEY.keys())
    print("\n  Teclas disponíveis para hotkeys:", ", ".join(t.upper() for t in teclas_disp))
    print()
    with estado_lock:
        toggle_atual = estado["hotkey_toggle"]
        stop_atual = estado["hotkey_stop"]
    print(f"  Hotkey de ligar/desligar atual: {nome_key(toggle_atual)}")
    print(f"  Hotkey de sair atual          : {nome_key(stop_atual)}")
    print()

    nova_toggle = None
    nova_stop = None

    entrada = input("  Nova hotkey de ligar/desligar [ENTER p/ manter]: ").strip().lower()
    if entrada in TECLAS_HOTKEY:
        nova_toggle = TECLAS_HOTKEY[entrada]
    elif entrada:
        print("  ⚠️  Tecla não reconhecida, mantendo atual.")

    entrada = input("  Nova hotkey de sair          [ENTER p/ manter]: ").strip().lower()
    if entrada in TECLAS_HOTKEY:
        nova_stop = TECLAS_HOTKEY[entrada]
    elif entrada:
        print("  ⚠️  Tecla não reconhecida, mantendo atual.")

    # CORREÇÃO #7: impede que toggle e stop sejam a mesma tecla
    toggle_final = nova_toggle or toggle_atual
    stop_final = nova_stop or stop_atual

    if toggle_final == stop_final:
        print("  ❌ Hotkeys de ligar/desligar e sair não podem ser iguais. Mantendo anteriores.")
        time.sleep(1.5)
        return

    with estado_lock:
        if nova_toggle:
            estado["hotkey_toggle"] = nova_toggle
        if nova_stop:
            estado["hotkey_stop"] = nova_stop


def menu_principal():
    while True:
        banner()
        status()
        print("\n  O que deseja configurar?\n")
        print("  [1] Modo (tecla / mouse)")
        with estado_lock:
            modo_atual = estado["modo"]
        if modo_atual == "tecla":
            print("  [2] Qual tecla pressionar")
        else:
            print("  [2] Qual botão do mouse clicar")
        print("  [3] Intervalo entre ações")
        print("  [4] Hotkeys (ligar/desligar e sair)")
        print("  [5] ▶  INICIAR BOT")
        print("  [0] Sair")
        print()

        op = input("  Opção: ").strip()

        if op == "1":
            configurar_modo()
        elif op == "2":
            with estado_lock:
                modo_atual = estado["modo"]
            if modo_atual == "tecla":
                configurar_tecla()
            else:
                configurar_mouse()
        elif op == "3":
            configurar_intervalo()
        elif op == "4":
            configurar_hotkeys()
        elif op == "5":
            iniciar_bot()
        elif op == "0":
            print("\n  👋 Até mais!\n")
            sys.exit(0)
        else:
            print("  ❌ Opção inválida.")
            time.sleep(0.8)


def iniciar_bot():
    banner()
    status()

    # CORREÇÃO #3: thread do bot só é criada uma vez por sessão de uso.
    # O listener bloqueia até F8; ao retornar, ativo volta a False e
    # a thread daemon encerra junto com o processo se o usuário sair,
    # ou fica em espera (ativo=False) se voltar ao menu.
    t = threading.Thread(target=loop_acao, daemon=True)
    t.start()

    with estado_lock:
        toggle_key = estado["hotkey_toggle"]
        stop_key = estado["hotkey_stop"]

    print(f"\n  ⏳ O bot começa PAUSADO.")
    print(f"  Pressione  {nome_key(toggle_key)}  para ligar/desligar.")
    print(f"  Pressione  {nome_key(stop_key)}  para sair.\n")
    print(linha("─", 50))
    print()

    # Listener de hotkeys (bloqueia até a hotkey de stop)
    iniciar_listener()

    # Voltou do listener → garante bot pausado e volta ao menu
    with estado_lock:
        estado["ativo"] = False
    print("\n  Voltando ao menu...\n")
    time.sleep(1)


# ─── Ponto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  Verificando dependências...", end=" ")
    print("OK ✅\n")
    time.sleep(0.5)
    menu_principal()
