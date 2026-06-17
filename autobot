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

try:
    from pynput import keyboard, mouse
    from pynput.keyboard import Key, Controller as KeyboardController
    from pynput.mouse import Button, Controller as MouseController
except ImportError:
    print("❌ Biblioteca 'pynput' não encontrada.")
    print("   Instale com: pip install pynput")
    sys.exit(1)


# ─── Estado global ─────────────────────────────────────────────────────────────
kb = KeyboardController()
ms = MouseController()

estado = {
    "ativo": False,
    "modo": "tecla",          # "tecla" ou "mouse"
    "tecla": "l",             # tecla padrão
    "botao_mouse": Button.left,
    "intervalo": 0.1,         # segundos entre ações
    "hotkey_toggle": Key.f6,  # tecla para ligar/desligar
    "hotkey_stop": Key.f8,    # tecla para sair do programa
    "thread": None,
}

BOTOES_MOUSE = {
    "1": Button.left,
    "2": Button.right,
    "3": Button.middle,
}

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
    "f5": Key.f5, "f9": Key.f9, "f10": Key.f10,
    "f11": Key.f11, "f12": Key.f12,
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


def limpar():
    print("\033[2J\033[H", end="")  # limpa tela cross-platform


def linha(char="─", n=50):
    return char * n


def banner():
    limpar()
    print(linha())
    print("  🤖  AutoBot — Automação de Tecla / Mouse")
    print(linha())


def status():
    modo_str = f"tecla '{estado['tecla']}'" if estado["modo"] == "tecla" \
        else f"clique mouse ({nome_botao(estado['botao_mouse'])})"
    ativo_str = "✅ ATIVO" if estado["ativo"] else "⏸  parado"
    print(f"\n  Modo     : {modo_str}")
    print(f"  Intervalo: {estado['intervalo']:.3f}s  "
          f"({1/estado['intervalo']:.1f} ações/s)")
    print(f"  Ligar/Des: {nome_key(estado['hotkey_toggle'])}")
    print(f"  Sair     : {nome_key(estado['hotkey_stop'])}")
    print(f"  Status   : {ativo_str}")
    print(linha())


def nome_botao(btn):
    mapa = {Button.left: "Esquerdo", Button.right: "Direito", Button.middle: "Meio"}
    return mapa.get(btn, str(btn))


def nome_key(k):
    if isinstance(k, Key):
        return k.name.upper()
    return str(k).upper()


def loop_acao():
    """Loop principal que executa a ação enquanto ativo."""
    while True:
        if estado["ativo"]:
            try:
                if estado["modo"] == "tecla":
                    kb.press(estado["tecla"])
                    kb.release(estado["tecla"])
                else:
                    ms.click(estado["botao_mouse"])
            except Exception as e:
                print(f"\n⚠️  Erro ao executar ação: {e}")
        time.sleep(estado["intervalo"])


def on_key_press(key):
    """Listener de hotkeys."""
    if key == estado["hotkey_toggle"]:
        estado["ativo"] = not estado["ativo"]
        s = "▶ ATIVO" if estado["ativo"] else "⏸ Pausado"
        print(f"\r  [{s}]  ", end="", flush=True)

    elif key == estado["hotkey_stop"]:
        print("\n\n  👋 Encerrando AutoBot...\n")
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
    print(f"  [ENTER] Manter atual: '{estado['tecla']}'")
    print()

    while True:
        entrada = input("  Tecla: ").strip().lower()
        if entrada == "":
            break  # mantém atual
        if entrada in TECLAS_ESPECIAIS:
            estado["tecla"] = TECLAS_ESPECIAIS[entrada]
            break
        if len(entrada) == 1:
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
    print(f"\n  [ENTER] Manter atual: {estado['intervalo']}s")
    print()
    while True:
        entrada = input("  Intervalo (segundos): ").strip()
        if entrada == "":
            break
        try:
            v = float(entrada)
            if 0.001 <= v <= 60:
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
    print(f"  Hotkey de ligar/desligar atual: {nome_key(estado['hotkey_toggle'])}")
    print(f"  Hotkey de sair atual          : {nome_key(estado['hotkey_stop'])}")
    print()

    entrada = input("  Nova hotkey de ligar/desligar [ENTER p/ manter]: ").strip().lower()
    if entrada in TECLAS_HOTKEY:
        estado["hotkey_toggle"] = TECLAS_HOTKEY[entrada]
    elif entrada:
        print("  ⚠️  Tecla não reconhecida, mantendo atual.")

    entrada = input("  Nova hotkey de sair          [ENTER p/ manter]: ").strip().lower()
    if entrada in TECLAS_HOTKEY:
        estado["hotkey_stop"] = TECLAS_HOTKEY[entrada]
    elif entrada:
        print("  ⚠️  Tecla não reconhecida, mantendo atual.")


def menu_principal():
    while True:
        banner()
        status()
        print("\n  O que deseja configurar?\n")
        print("  [1] Modo (tecla / mouse)")
        if estado["modo"] == "tecla":
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
            if estado["modo"] == "tecla":
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

    # Inicia o loop de ação em thread separada (daemon → morre com o programa)
    t = threading.Thread(target=loop_acao, daemon=True)
    t.start()
    estado["thread"] = t

    print(f"\n  ⏳ O bot começa PAUSADO.")
    print(f"  Pressione  {nome_key(estado['hotkey_toggle'])}  para ligar/desligar.")
    print(f"  Pressione  {nome_key(estado['hotkey_stop'])}  para sair.\n")
    print(linha("─", 50))
    print()

    # Listener de hotkeys (bloqueia até F8)
    iniciar_listener()

    # Voltou do listener → para o bot e volta ao menu
    estado["ativo"] = False
    print("\n  Voltando ao menu...\n")
    time.sleep(1)


# ─── Ponto de entrada ──────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("\n  Verificando dependências...", end=" ")
    print("OK ✅\n")
    time.sleep(0.5)
    menu_principal()
