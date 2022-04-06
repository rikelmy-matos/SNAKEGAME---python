import random as rd

import pygame as pg


# criando objetos:
class Snake():
    # Fixo ao objeto
    cor = (0, 255, 0)
    # quantidade de pixels que irá ocupar == tamanho da Fruta
    tamanho = (10, 10)
    velocidade = 10  # 10 em 10 pixels
    tamanho_maximo = 49 * 49

    def __init__(self):
        # variável ao objeto
        # irá definir o formato da fruta == quadrado
        self.textura = pg.Surface(self.tamanho)
        self.textura.fill(self.cor)  # irá preencer a fruta com a cor

        # irá definir o corpo == cabeça(ponto inicial), corpo(ponto secundario) dentro de uma lista[]
        self.corpo = [(100, 100), (90, 100), (80, 100)]

        self.direcao = "direita"  # irá definir a direcao do objeto
        self.pontos = 0
        self.dificuldade = None

    def blit(self, screen):  # irá imprimir na tela o que desejo com o blit
        for posicao in self.corpo:
            screen.blit(self.textura, posicao)

    # Logica da movimentação

    def andar(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        # Para cada movimento esta criando uma nova cabeça
        if self.direcao == "direita":
            self.corpo.insert(0, (x + self.velocidade, y))
        elif self.direcao == "esquerda":
            self.corpo.insert(0, (x - self.velocidade, y))
        elif self.direcao == "cima":
            self.corpo.insert(0, (x, y - self.velocidade))
        elif self.direcao == "baixo":
            self.corpo.insert(0, (x, y + self.velocidade))

        # Para cada movimento esta cortando o rabo
        self.corpo.pop(-1)

    def direita(self):
        if self.direcao != "esquerda":
            self.direcao = "direita"

    def esquerda(self):
        if self.direcao != "direita":
            self.direcao = "esquerda"

    def cima(self):
        if self.direcao != "baixo":
            self.direcao = "cima"

    def baixo(self):
        if self.direcao != "cima":
            self.direcao = "baixo"

    def colisao_frutinha(self, frutinha):
        return self.corpo[0] == frutinha.posicao  # retornar True

    def comer(self, frutinha):
        self.corpo.append(0)  # irá incluir no corpo
        self.pontos += 1  # irá somar um ponto ao comer a fruta

        pg.display.set_caption(f"SNAKE GAME | SCORE: {self.pontos}")

    def colisao(self):
        cabeca = self.corpo[0]
        x = cabeca[0]
        y = cabeca[1]

        calda = self.corpo[1:]

        return x < 0 or y < 0 or x > 490 or y > 490 or cabeca in calda or len(self.corpo) > self.tamanho_maximo


class Fruta():
    cor = (255, 0, 0)
    tamanho = (10, 10)

    def __init__(self, cobrinha):
        self.textura = pg.Surface(self.tamanho)
        self.textura.fill(self.cor)
        self.posicao = Fruta.criar_posicao(cobrinha)

    @staticmethod
    def criar_posicao(cobrinha):
        # define os pixels == aleatorios inteiros
        # sempre vai ficar em uma grade de 10 pixels
        # 2D == x,y    3D == x,y,z
        x = rd.randint(0, 49) * 10
        y = rd.randint(0, 49) * 10

        if (x, y) in cobrinha.corpo:
            Fruta.criar_posicao(cobrinha)
        else:
            return x, y

    def blit(self, screen):  # irá imprimir na tela o que desejo com o blit
        screen.blit(self.textura, self.posicao)


def dificuldade(self):  # função / logica da dificuldade
    dificuldade = 10  # o valor é base referente ao FPS
    if self.pontos >= 0:  # se o objeto.pontos for maio/igual a 0
        # somar a pontuação a difuculdade e depois retornar nova variável
        dificuldade_jogo = dificuldade + self.pontos * 0.07
        return dificuldade_jogo


if __name__ == "__main__":
    pg.init()
    resolution = (500, 500)  # resolução com os pixels
    screen = pg.display.set_mode(resolution)  # tupla com os pixels
    pg.display.set_caption("SNAKE GAME by Rikelmy")
    clock = pg.time.Clock()  # irá definir o tempo de processamento
    coloracao = (0, 120, 50)  # até (255,255,255) == Red, Green, Blue

    cobrinha = Snake()
    frutinha = Fruta(cobrinha)

    while True:  # irá dar looping nos quadros == fps

        clock.tick(dificuldade(cobrinha))  # limitar os fps
        print(clock.get_fps())
        for event in pg.event.get():  # pegar cada evento dentro do loop
            if event.type == pg.QUIT:  # se o evento for de exit == sair
                exit()

            # irá chamar o evento de de movimento/logica dentro do objeto Snake
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RIGHT:
                    cobrinha.direita()
                    break
                elif event.key == pg.K_LEFT:
                    cobrinha.esquerda()
                    break
                elif event.key == pg.K_UP:
                    cobrinha.cima()
                    break
                elif event.key == pg.K_DOWN:
                    cobrinha.baixo()
                    break

        if cobrinha.colisao_frutinha(frutinha):  # se colidir com a frutinha
            cobrinha.comer(frutinha)
            frutinha = Fruta(cobrinha)  # irá substituir o objeto

        elif cobrinha.colisao():
            cobrinha = Snake()  # irá substituir o objeto
            frutinha = Fruta(cobrinha)  # irá substituir o objeto

        cobrinha.andar()
        screen.fill(coloracao)  # irá preencher a tela com a cor que deseja
        frutinha.blit(screen)
        cobrinha.blit(screen)
        pg.display.update()  # irá atualizar a tela
