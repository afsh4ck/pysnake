import turtle
import time
import random


class SnakeGame:
    def __init__(self, width=800, height=800, color="#CEFF00"):
        """Inicializa los componentes del juego."""

        self._ancho = width
        self._alto = height

        # Inicializa el lienzo
        self.screen = turtle.Screen()
        self.screen.title('Videojuego Snake')
        self.screen.bgcolor(color)
        self.screen.setup(width=width, height=height)
        self.screen.tracer(0)

        # Inicializa la serpiente
        self.snake = turtle.Turtle()
        self.snake.speed(0)
        self.snake.shape('square')
        self.snake.color('black')
        self.snake.penup()
        self.snake.goto(0, 0)

        # Inicializa los segmentos de la serpiente
        self._segmentos = []
        self._segmentos.append(turtle.Turtle())
        self._segmentos[0].speed(0)
        self._segmentos[0].shape('square')
        self._segmentos[0].color('black')
        self._segmentos[0].penup()
        self._segmentos[0].goto(0, 0)

        # Inicializa la comida de la serpiente
        self.comida = turtle.Turtle()
        self.comida.speed(0)
        self.comida.shape('circle')
        self.comida.color('white')
        self.comida.penup()
        self.comida.goto(0, 100)

        # Inicializa el texto que se muestra en pantalla
        self.texto = turtle.Turtle()
        self.texto.speed(0)
        self.texto.penup()
        self.texto.color('black')
        self.texto.hideturtle()  # Método que oculta el puntero
        self.texto.goto(0, (height / 2) - 40)  # Posición arriba del todo

        # Atributos de la clase
        self._direccion = None
        self._delay = 0.1
        self._score = 0
        self._high_score = 0

        # Asociar movimientos a las teclas
        self.screen.listen()
        self.screen.onkeypress(self.arriba, 'w')
        self.screen.onkeypress(self.abajo, 's')
        self.screen.onkeypress(self.izquierda, 'a')
        self.screen.onkeypress(self.derecha, 'd')

        # Inicializar score
        self._print_score()

    def arriba(self):
        """Este método define el movimiento hacia arriba de la serpiente"""
        if self._direccion != 'abajo':
            self._direccion = 'arriba'

    def abajo(self):
        """Este método define el movimiento hacia abajo de la serpiente"""
        if self._direccion != 'arriba':
            self._direccion = 'abajo'

    def izquierda(self):
        """Este método define el movimiento hacia la izquierda de la serpiente"""
        if self._direccion != 'derecha':
            self._direccion = 'izquierda'

    def derecha(self):
        """Este método define el movimiento hacia la derecha de la serpiente"""
        if self._direccion != 'izquierda':
            self._direccion = 'derecha'

    def move(self):
        """Este método mueve y actualiza las coordenadas la serpiente"""
        if self._direccion == 'arriba':
            y = self.snake.ycor()
            self.snake.sety(y + 20)
        elif self._direccion == 'abajo':
            y = self.snake.ycor()
            self.snake.sety(y - 20)
        elif self._direccion == 'izquierda':
            x = self.snake.xcor()
            self.snake.setx(x - 20)
        elif self._direccion == 'derecha':
            x = self.snake.xcor()
            self.snake.setx(x + 20)

        # Verificar colisiones con el cuerpo de la serpiente
        for segmento in self._segmentos:
            if self.snake.distance(segmento) < 20:
                self.colision_cuerpo()

        # Mover los segmentos en reversa
        for i in range(len(self._segmentos) - 1, 0, -1):
            x = self._segmentos[i - 1].xcor()
            y = self._segmentos[i - 1].ycor()
            self._segmentos[i].goto(x, y)

        # Mover el primer segmento a la cabeza de la serpiente
        if len(self._segmentos) > 0:
            x = self.snake.xcor()
            y = self.snake.ycor()
            self._segmentos[0].goto(x, y)

    def play(self):
        """Este método hace que la serpiente avance constantemente y evalúa las colisiones"""
        while True:
            self.screen.update()
            self.colision_borde()
            self.colision_comida()
            time.sleep(self._delay)
            self.move()
        self.screen.mainloop()

    def colision_borde(self):
        """Este método evalúa las colisiones con el borde"""
        # Definimos los bordes del tablero
        bxcor = (self._ancho // 2) - 20
        bycor = (self._alto // 2) - 20

        if (
                self.snake.xcor() > bxcor
                or self.snake.xcor() < -bxcor
                or self.snake.ycor() > bycor
                or self.snake.ycor() < -bycor
        ):
            time.sleep(1)
            self.snake.goto(0, 0)
            self._direccion = None
            # Reiniciar el delay
            self._delay = 0.1
            # Actualizar puntuación máxima
            if self._score > self._high_score:
                self._high_score = self._score
            self._score = 0
            self._print_score()

            # Reiniciar el cuerpo de la serpiente con solo un segmento
            for segmento in self._segmentos:
                segmento.hideturtle()
            self._segmentos.clear()
            self._segmentos.append(turtle.Turtle())
            self._segmentos[0].speed(0)
            self._segmentos[0].shape('square')
            self._segmentos[0].color('black')
            self._segmentos[0].penup()
            self._segmentos[0].goto(0, 0)

    def colision_comida(self):
        """Este método hace distintas acciones al comer la comida"""
        if self.snake.distance(self.comida) < 20:
            # Mover la comida a un lugar aleatorio
            bxcor = (self._ancho // 2) - 20
            bycor = (self._alto // 2) - 20
            x = random.randint(-bxcor, bxcor)
            y = random.randint(-bycor, bycor)
            self.comida.goto(x, y)
            # Reducir el delay cada vez que come
            self._delay -= 0.001
            # Aumentar el score
            self._score += 10
            self._print_score()
            # Agregar un nuevo segmento
            self._agregar_segmento()

    def colision_cuerpo(self):
        """Este método evalua la colisión con el propio cuerpo de la serpiente"""
        time.sleep(1)
        self.snake.goto(0, 0)
        self._direccion = None
        # Reiniciar el delay
        self._delay = 0.1
        # Actualizar puntuación máxima
        if self._score > self._high_score:
            self._high_score = self._score
        self._score = 0
        self._print_score()
        # Reiniciar el cuerpo de la serpiente con solo un segmento
        for segmento in self._segmentos:
            segmento.hideturtle()
        self._segmentos.clear()
        self._segmentos.append(turtle.Turtle())
        self._segmentos[0].speed(0)
        self._segmentos[0].shape('square')
        self._segmentos[0].color('black')
        self._segmentos[0].penup()
        self._segmentos[0].goto(0, 0)

    def _agregar_segmento(self):
        segmento = turtle.Turtle()
        segmento.speed(0)
        segmento.shape('square')
        segmento.color('grey')
        segmento.penup()
        self._segmentos.append(segmento)

    def _print_score(self):
        self.texto.clear()
        self.texto.write('Puntos: {}   Record: {}'.format(self._score, self._high_score), align='center', font=('Courier', 24, 'normal'))

# Crear una instancia del juego
snake_game = SnakeGame()

# Iniciar el juego
snake_game.play()
