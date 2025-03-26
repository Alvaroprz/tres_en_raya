import pygame as pg

CROSS = 'X'
C_CROSS = (200, 200, 50)
W_CROSS = 12

CIRCLE = 'O'
C_CIRCLE = (50,50,200)
W_CIRCLE = 8

EMPTY = ''

FPS = 30

WINDOW = (450, 520)
C_BACKGROUND = (0, 0, 0)
BOARD_SIZE = 400
MARGIN = 25
PADDING = 10

C_LINES = (180, 180, 180)
W_LINES = 3

C_TEXT = (255, 255, 255)
TEXT_SIZE = 50

class TresEnRaya:

  def __init__(self):
    self.turno = CROSS
    self.game_over = False
    self.winner = None
    self.reset()
    pg.init()
    self.screen = pg.display.set_mode(WINDOW)
    pg.display.set_caption('Tres en raya')
    self.clock = pg.time.Clock()
    font_name = pg.font.get_default_font()
    self.font = pg.font.SysFont(font_name, TEXT_SIZE)

  def draw_message(self, text):
    img = self.font.render(text, True, C_TEXT, C_BACKGROUND)
    text_rect = img.get_rect(center=(WINDOW[0]//2, WINDOW[1]-TEXT_SIZE))
    self.screen.blit(img, text_rect)

  def draw_status(self):
    if self.game_over == True:
      if self.winner is not None:
        self.draw_message(f'¡Ha ganado {self.winner}!')
      else:
        self.draw_message('¡Empate!')
    else:
      self.draw_message(f'Turno para {self.turno}')

  def draw_o(self, pos):
    cell_size = BOARD_SIZE // 3
    radius = cell_size // 2 - PADDING

    col = pos % 3
    row = pos // 3

    x = MARGIN + cell_size // 2 + cell_size * col
    y = MARGIN + cell_size // 2 + cell_size * row
    pg.draw.circle(self.screen, C_CIRCLE, (x, y), radius, W_CIRCLE)

  def draw_x(self, pos):
    cell_size = BOARD_SIZE // 3
    col = pos % 3
    row = pos // 3

    x1 = MARGIN + PADDING * 2 + cell_size * col
    y1 = MARGIN + PADDING * 2 + cell_size * row
    x2 = MARGIN + cell_size - PADDING * 2 + cell_size * col
    y2 = MARGIN + cell_size - PADDING * 2 + cell_size * row
    pg.draw.line(self.screen, C_CROSS, (x1, y1), (x2, y2), W_CROSS)

    temp = x1
    x1 = x2
    x2 = temp
    pg.draw.line(self.screen, C_CROSS, (x1, y1), (x2, y2), W_CROSS)



  def draw_lines(self):
    cell_size = BOARD_SIZE // 3

    x1 = MARGIN + cell_size
    y1 = MARGIN
    x2 = x1
    y2 = y1 + BOARD_SIZE
    pg.draw.line(self.screen, C_LINES, (x1, y1), (x2, y2), W_LINES)

    x1 = x1 + cell_size
    x2 = x1
    pg.draw.line(self.screen, C_LINES, (x1, y1), (x2, y2), W_LINES)

    x1 = MARGIN
    x2 = MARGIN + BOARD_SIZE
    y1 = MARGIN + cell_size
    y2 = y1
    pg.draw.line(self.screen, C_LINES, (x1, y1), (x2, y2), W_LINES)

    y1 = y1 + cell_size
    y2 = y1
    pg.draw.line(self.screen, C_LINES, (x1, y1), (x2, y2), W_LINES)

  def play(self):
    playing = True

    while playing:
      self.clock.tick(FPS)

      for event in pg.event.get():
        if event.type == pg.QUIT:
          playing = False
        if event.type == pg.KEYDOWN:
          tecla = event.unicode
          if tecla in ('1', '2', '3', '4', '5', '6', '7', '8', '9'):
            num = int(tecla) - 1
            col = num % 3
            fila = 2 - num // 3
            pos = fila * 3 + col
            self.make_move(pos)
          if event.key == pg.K_r:
            self.reset()

      self.screen.fill(C_BACKGROUND)
      self.draw_lines()
      self.draw_board()
      self.draw_status()
      pg.display.flip()

    pg.quit()
    

  def draw_board(self):
    for i in range(len(self.tablero)):
      if self.tablero[i] == CROSS:
        self.draw_x(i)
      elif self.tablero[i] == CIRCLE:
        self.draw_o(i)

  def make_move(self, pos:int):
    assert 0 <= pos <= 8
    if self.game_over == False and self.tablero[pos] == EMPTY:
      self.tablero[pos] = self.turno
      self.check_winner()
      self.next_turn()

  def next_turn(self):
    if self.turno == CROSS:
      self.turno = CIRCLE
    else:
      self.turno = CROSS

  def reset(self):
    self.tablero = [EMPTY for i in range(9)]
    self.game_over = False
    if self.winner:
      self.turno = self.winner
    self.winner = None

  def draw_board_old(self):
    for i in range(9):
      if i % 3 == 0:
        print()
      valor = self.tablero[i]
      if valor == '':
        valor = ' '
      print(valor, end=' ')
    print()

  def check_winner(self):
    combos = [
      [0, 1, 2], [3, 4, 5], [6, 7, 8], # filas
      [0, 3, 6], [1, 4, 7], [2, 5, 8], # cols
      [0, 4, 8], [2, 4, 6]
    ]
    for combo in combos:
      if self.tablero[combo[0]] == self.tablero[combo[1]] == self.tablero[combo[2]] and self.tablero[combo[0]] != '':
        self.winner = self.turno
        print('Ha gando el jugador', self.winner)
        self.game_over = True
        return
      
    if EMPTY not in self.tablero:
      self.game_over = True