import turtle
import time
import random

# Controla la velocidad del juego, es decir, cuánto tiempo espera entre cada actualización de la pantalla.
posponer = 0.1

# Marcador
score = 0
high_score = 0

# Configuración de la ventana
wn = turtle.Screen() # Crea la ventana donde se ejecutará el juego.
wn.title("Juego de Snake") # Configuran el título de la ventana.
wn.bgcolor("black") # Configuran el color de fondo.
wn.setup(width=600, height=600) # Define el tamaño de la ventana.
wn.tracer(0) # Desactiva la animación automática para que puedas controlarla manualmente con wn.update(). Esto es útil para evitar que el juego parpadee y mejorar el rendimiento.

# Cabeza de la serpiente
cabeza = turtle.Turtle() # Crea la cabeza de la serpiente como un objeto de tipo Turtle.
cabeza.speed(0) # Configuran la forma.
cabeza.shape("square") # Configuran la forma.
cabeza.color("white") # Configuran el color.
cabeza.penup() # Evita que la serpiente dibuje líneas al moverse (penup()).
cabeza.goto(0, 0) # Ubica la cabeza en el centro de la pantalla.
cabeza.direction = "stop" # Inicialmente, la serpiente no se mueve.

# Comida
comida = turtle.Turtle()
comida.speed(0) # Configuran la forma.
comida.shape("circle") # Configuran la forma.
comida.color("red") # Configuran el color.
comida.penup() # Evita que la serpiente dibuje líneas al moverse (penup()).
comida.goto(0, 100) # Ubica la comida en diferente lugares.

# Segmentos / cuerpo serpiente
segmentos = [] # Es una lista que almacena los segmentos del cuerpo de la serpiente. Al inicio está vacía, pero se van añadiendo segmentos a medida que la serpiente come.

# Texto
texto = turtle.Turtle() # Es un objeto Turtle que se usa para mostrar el marcador en la pantalla. Está configurado para no dibujar (penup()), ocultar la tortuga (hideturtle()), y mostrar texto en la parte superior de la pantalla.
texto.speed(0)
texto.color("white")
texto.penup()
texto.hideturtle()
texto.goto(0, 260)
texto.write("Score: 0       High Score: 0", align="center", font=("Courier", 24, "normal"))


# Funciones
# Estas funciones controlan la dirección en la que se mueve la serpiente, asegurándose de que no pueda ir en la dirección opuesta a su movimiento actual.
def arriba():
    if cabeza.direction != "down":
        cabeza.direction = "up"


def abajo():
    if cabeza.direction != "up":
        cabeza.direction = "down"


def izquierda():
    if cabeza.direction != "right":
        cabeza.direction = "left"


def derecha():
    if cabeza.direction != "left":
        cabeza.direction = "right"


# mov(): Actualiza la posición de la serpiente en función de su dirección. Utiliza las coordenadas actuales (xcor() y ycor()) y mueve la cabeza en incrementos de 20 unidades en la dirección correspondiente.
def mov():
    if cabeza.direction == "up":  # Arriba
        y = cabeza.ycor()
        cabeza.sety(y + 20)

    if cabeza.direction == "down":  # Abajo
        y = cabeza.ycor()
        cabeza.sety(y - 20)

    if cabeza.direction == "left":  # Izquierda
        x = cabeza.xcor()
        cabeza.setx(x - 20)

    if cabeza.direction == "right":  # Derecha
        x = cabeza.xcor()
        cabeza.setx(x + 20)


# Teclado
wn.listen() # Activa la escucha de eventos del teclado.
# onkeypress(función, tecla): Asigna las funciones de movimiento a las teclas de flecha del teclado.
wn.onkeypress(arriba, "Up")
wn.onkeypress(abajo, "Down")
wn.onkeypress(izquierda, "Left")
wn.onkeypress(derecha, "Right")

# Colisiones
while True: # Es un bucle infinito que mantiene el juego en funcionamiento.
    wn.update() # Actualiza la pantalla con los nuevos gráficos en cada iteración del bucle.

    # Colisiones bordes
    # Este bloque de código detecta si la cabeza de la serpiente toca los bordes de la ventana. Si es así, la serpiente se "resetea" al centro, y el juego vuelve a empezar con una puntuación de 0.
    if (cabeza.xcor() > 280 or cabeza.xcor() < -280 or cabeza.ycor() > 280 or cabeza.ycor() < -280):
        time.sleep(1)
        cabeza.goto(0, 0)
        cabeza.direction = "stop"

        # Esconder los segmentos
        for segmento in segmentos:
            segmento.goto(1000, 1000)

        # Limpiar lista de segmentos
        segmentos.clear()

        # Resetear marcador
        score = 0
        texto.clear()
        texto.write("Score: {}       High Score: {}".format(score, high_score),
                    align="center", font=("Courier", 24, "normal"))

    # Colisiones con la comida
    # Cuando la cabeza de la serpiente está lo suficientemente cerca de la comida (menos de 20 unidades), se genera una nueva comida en una posición aleatoria, se añade un nuevo segmento al cuerpo de la serpiente, y se actualiza el marcador.
    if cabeza.distance(comida) < 20:
        # Mover la comida a una posición aleatoria
        x = random.randint(-280, 280)
        y = random.randint(-280, 280)
        comida.goto(x, y)

        # Añadir un nuevo segmento
        nuevo_segmento = turtle.Turtle()
        nuevo_segmento.speed(0)
        nuevo_segmento.shape("square")
        nuevo_segmento.color("grey")
        nuevo_segmento.penup()
        segmentos.append(nuevo_segmento)

        # Aumentar marcador
        score += 10

        if score > high_score:
            high_score = score

        texto.clear()
        texto.write("Score: {}       High Score: {}".format(score, high_score),
                    align="center", font=("Courier", 24, "normal"))


    # Mover el cuerpo de la serpiente
    # Este código asegura que cada segmento del cuerpo de la serpiente siga a la cabeza de la serpiente. Los segmentos se mueven de atrás hacia adelante, con cada segmento tomando la posición del segmento que estaba delante de él.
    total_segmentos = len(segmentos)
    for index in range(total_segmentos - 1, 0, -1):
        x = segmentos[index - 1].xcor()
        y = segmentos[index - 1].ycor()
        segmentos[index].goto(x, y)

    if total_segmentos > 0:
        x = cabeza.xcor()
        y = cabeza.ycor()
        segmentos[0].goto(x, y)

    mov()

    # Colisiones con el cuerpo
    # Aquí, si la cabeza de la serpiente toca cualquier parte de su cuerpo, el juego se reinicia de manera similar a como lo hace cuando toca los bordes. La serpiente vuelve al centro y el cuerpo desaparece.
    for segmento in segmentos:
        if segmento.distance(cabeza) < 20:
            time.sleep(1)
            cabeza.goto(0, 0)
            cabeza.direction = "stop"

            # Esconder los segmentos
            for segmento in segmentos:
                segmento.goto(1000, 1000)

            # Limpiar lista de segmentos
            segmentos.clear()

            # Resetear marcador
            score = 0
            texto.clear()
            texto.write("Score: {}       High Score: {}".format(score, high_score),
                        align="center", font=("Courier", 24, "normal"))

    time.sleep(posponer)
