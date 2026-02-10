from pynput import mouse, keyboard

mouse_ctrl = mouse.Controller()
kb_ctrl = keyboard.Controller()

STEP = 20

def mover_mouse(direcao):
    x, y = mouse_ctrl.position

    if direcao == "UP":
        mouse_ctrl.position = (x, y - STEP)
    elif direcao == "DOWN":
        mouse_ctrl.position = (x, y + STEP)
    elif direcao == "LEFT":
        mouse_ctrl.position = (x - STEP, y)
    elif direcao == "RIGHT":
        mouse_ctrl.position = (x + STEP, y)

def clicar(botao="LEFT"):
    if botao == "LEFT":
        mouse_ctrl.click(mouse.Button.left)
    elif botao == "RIGHT":
        mouse_ctrl.click(mouse.Button.right)

def pressionar_tecla(tecla):
    kb_ctrl.press(tecla)
    kb_ctrl.release(tecla)