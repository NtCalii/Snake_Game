#importando biblioteca
import pygame
import random

#configuração inicial
pygame.init()
pygame.display.set_caption("Jogo da Cobrinha Python")
largura, altura = 600, 400
tela = pygame.display.set_mode((largura, altura))
relogio = pygame.time.Clock()

#cores RGB
preto = (0, 0, 0)
branco = (255, 255, 255)
verde = (0, 255, 0)
vermelho = (255, 0, 0)

#parametros cobrinha
tamanho_quadrado = 10
velocidade_jogo = 15

def gerar_comida():
    comida_x = round(random.randrange(0, largura - tamanho_quadrado) / 20.0) * 20.0
    comida_y = round(random.randrange(0, altura - tamanho_quadrado) / 20.0) * 20.0
    return comida_x, comida_y

def desenhar_comida(tamanho, comida_x, comida_y):
    pygame.draw.rect(tela, verde, [comida_x, comida_y, tamanho, tamanho])

def desenhar_cobra(tamanho, pixel):
    for pixels in pixel:
        pygame.draw.rect(tela, branco, [pixels[0], pixels[1], tamanho, tamanho])

def desenhar_pontuacao(pontuacao):
    fonte = pygame.font.SysFont("Helvetica", 30)
    texto = fonte.render(f"Pontuação: {pontuacao}", True, vermelho)
    tela.blit(texto, [5, 5])

def selecionar_velocidade(tecla):
    if tecla == pygame.K_DOWN:
        velocidade_x = 0
        velocidade_y = tamanho_quadrado
    elif tecla == pygame.K_UP:
        velocidade_x = 0
        velocidade_y = -tamanho_quadrado
    elif tecla == pygame.K_RIGHT:
        velocidade_x = tamanho_quadrado
        velocidade_y = 0
    elif tecla == pygame.K_LEFT:
        velocidade_x = -tamanho_quadrado
        velocidade_y = 0
    return velocidade_x, velocidade_y

def mensagem_game_over():
    fonte = pygame.font.SysFont("Helvetica", 35)
    texto = fonte.render("Game Over! R - Reiniciar | Q - Sair", True, vermelho)
    texto_retangulo = texto.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto, texto_retangulo)
    pygame.display.update()

    esperando_resposta = True
    while esperando_resposta:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_q:
                    pygame.quit()
                    quit()
                elif evento.key == pygame.K_r:
                    esperando_resposta = False
                    rodar_jogo()

#rodar o jogo
def rodar_jogo():
    fim_jogo = False
    x = largura / 2
    y = altura / 2
    velocidade_x = 0
    velocidade_y = 0
    tamanho_cobra = 1
    pixel = []
    comida_x, comida_y = gerar_comida()

    while not fim_jogo:
        tela.fill(preto)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                mensagem_game_over()
            elif evento.type == pygame.KEYDOWN:
                velocidade_x, velocidade_y = selecionar_velocidade(evento.key)

        # desenhar comida
        desenhar_comida(tamanho_quadrado, comida_x, comida_y)

        if x < 0  or x >= largura or y < 0 or y >= altura:
            mensagem_game_over()

        #atualiza a posição da cobra
        x += velocidade_x
        y += velocidade_y

        # desenhar cobra
        pixel.append([x, y])
        if len(pixel) > tamanho_cobra:
            del pixel[0]

        # se a cobra bateu no próprio corpo
        for pixels in pixel[:-1]:
            if pixels == [x, y]:
                mensagem_game_over()
        desenhar_cobra(tamanho_quadrado, pixel)

        #desenhar pontuação
        desenhar_pontuacao(tamanho_cobra - 1)

        # atualizar jogo
        pygame.display.update()

        #criar nova comida
        if x == comida_x and y == comida_y:
            tamanho_cobra += 1
            comida_x, comida_y = gerar_comida()

        relogio.tick(velocidade_jogo)

#iniciar o jogo
rodar_jogo()
