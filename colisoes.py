import numpy as np
import math 
import pygame 
import random
from pygame.locals import *
from pygame import mixer
from sys import exit

pygame.init()
pygame.mixer.init()
sound = mixer.Sound('boop.wav')

CR = 1
N_BOLAS = 10
branco = (255, 255, 255)
preto = (0, 0, 0)
fonte = pygame.font.SysFont('arial', 12)
largura = 1920
altura = 1080
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Simulador de colisões')

# Definição do objeto 'bola' #
class Bolas:
    def __init__(self) -> None:
        self.pos = [random.randint(50, largura - 50), random.randint(50, altura - 50)]
        self.velocidade = [random.randint(-10, 10), random.randint(-10, 10)]
        self.raio = random.randint(10, 50)
        self.massa = self.raio*(1/2)
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def cria(self):
        pygame.draw.circle(tela, self.cor, (self.pos[0], self.pos[1]), self.raio)

def calculaDistancia(pos1, pos2):
    return np.linalg.norm(np.subtract(pos1, pos2))

def calculaProjecao(v, vetor_diretor):
    return (np.multiply(vetor_diretor, np.divide(np.dot(v, vetor_diretor), np.linalg.norm(vetor_diretor)**2 )))

def mudaPosicao(dist, raio1, raio2):
    return 0.5*(dist - raio1 - raio2)
       
# ======================================================== Criar bolas e validá-las =================================================================================== #
bolas = []
for i in range(N_BOLAS):
    bolas.append(Bolas()) # Adiciona uma bola na lista de bolas
    recriar = False
    for j in range(i+1, len(bolas)):
        if (math.hypot(bolas[i].pos[0] - bolas[j].pos[0], bolas[i].pos[1] - bolas[j].pos[1]) #Cria bolas e testa se elas possuem sobreposição, caso tenham,
            <= (bolas[i].raio + bolas[j].raio)):                                             #o próximo bloco de comandos as recria e testa novamente.
            recriar = True
    while recriar:
        recriar = False
        bolas[i] = Bolas()
        for k in range(i+1, len(bolas)):
            if (math.hypot(bolas[i].pos[0] - bolas[k].pos[0], bolas[i].pos[1] - bolas[k].pos[1])
            <= (bolas[i].raio + bolas[k].raio)):
                recriar = True
# ==================================================================================================================================================================== #                     
                    
clock = pygame.time.Clock() 
  
while True:
    
    # ============ #
    clock.tick(30)
    tela.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
    # ============ #        
    
    # == Imprime as energias cinéticas na tela == #
    kx = 0
    ky = 0
    k = 0
    for i in range(len(bolas)):
        kx += np.divide(np.multiply(bolas[i].massa, np.multiply(bolas[i].velocidade[0], bolas[i].velocidade[0])), 2)
        ky += np.divide(np.multiply(bolas[i].massa, np.multiply(bolas[i].velocidade[1], bolas[i].velocidade[1])), 2)
    kx = round(kx, 3)
    ky = round(ky, 3)
    k = round(np.add(kx, ky), 3)
    
    textoX = fonte.render(f'Kx = {kx}', True, branco, preto)
    textoRectX = textoX.get_rect()
    textoRectX.center = (largura // 2, altura // 2 - 20)

    textoY = fonte.render(f'Ky = {ky}', True, branco, preto)
    textoRectY = textoY.get_rect()
    textoRectY.center = (largura // 2, altura // 2)
    
    textoK = fonte.render (f'K = {k}', True, branco, preto)
    textoRectK = textoK.get_rect()
    textoRectK.center = (largura // 2, altura // 2 + 20)

    tela.blit(textoX, textoRectX)
    tela.blit(textoY, textoRectY)
    tela.blit(textoK, textoRectK)
    # =========================================== #
           
    # Atualiza as posições conforme as velocidades #        
    for i in range(len(bolas)):
        bolas[i].cria()
        bolas[i].pos[0] += bolas[i].velocidade[0]
        bolas[i].pos[1] += bolas[i].velocidade[1]
    # ============================================ #
    
    # Colisões com as paredes #
    for i in range(len(bolas)):
        if bolas[i].pos[0] >= largura - bolas[i].raio:
            bolas[i].pos[0] = largura - bolas[i].raio 
            bolas[i].velocidade[0] *= -1
            
        elif bolas[i].pos[0] <= bolas[i].raio:
            bolas[i].pos[0] = bolas[i].raio
            bolas[i].velocidade[0] *= -1
            
        if bolas[i].pos[1] >= altura - bolas[i].raio:
            bolas[i].pos[1] = altura - bolas[i].raio
            bolas[i].velocidade[1] *= -1
            
        elif bolas[i].pos[1] <= bolas[i].raio:
            bolas[i].pos[1] = bolas[i].raio
            bolas[i].velocidade[1] *= -1
            
    # Colisões entre as bolas #        
        for j in range(i+1, len(bolas)):
            dist = calculaDistancia(bolas[i].pos, bolas[j].pos)
            if dist <= (bolas[i].raio + bolas[j].raio):
                
                # ===== Muda a posicao das bolas para que ======= #
                # ===== elas não entrem umas nas outras ========= #
                fatorDeMudanca = mudaPosicao(dist, bolas[i].raio, bolas[j].raio)
                
                bolas[i].pos[0] -= fatorDeMudanca * (bolas[i].pos[0] - bolas[j].pos[0])/dist
                bolas[i].pos[1] -= fatorDeMudanca * (bolas[i].pos[1] - bolas[j].pos[1])/dist
                
                bolas[j].pos[0] += fatorDeMudanca * (bolas[i].pos[0] - bolas[j].pos[0])/dist
                bolas[j].pos[1] += fatorDeMudanca * (bolas[i].pos[1] - bolas[j].pos[1])/dist
                mixer.Sound.play(sound)
                
                # ========= Colide as bolas ========= #
                vetor_diretor = np.subtract(bolas[i].pos, bolas[j].pos)
                
                vetor_v1 = bolas[i].velocidade
                proj_v1 = calculaProjecao(vetor_v1, vetor_diretor)
                v1_perpendicular = np.subtract(vetor_v1, proj_v1) #Informações da bola 1.
                momento_1 = np.multiply(bolas[i].massa, vetor_v1)
                
                vetor_v2 = bolas[j].velocidade
                proj_v2 = calculaProjecao(vetor_v2, vetor_diretor) 
                v2_perpendicular = np.subtract(vetor_v2, proj_v2)  #Informações da bola 2.
                momento_2 = np.multiply(bolas[j].massa, vetor_v2)
                
                vcm = np.divide((np.add(momento_1, momento_2)), (bolas[i].massa + bolas[j].massa))
                vcm = calculaProjecao(vcm, vetor_diretor) #Calcula velocidade do centro de massa no sentido da colisão.
                
                proj_v1 = np.subtract(np.multiply(1+CR, vcm), np.multiply(CR, proj_v1)) # V = (1+Cr)Vcm - V1*Cr
                proj_v2 = np.subtract(np.multiply(1+CR, vcm), np.multiply(CR, proj_v2))
                
                vetor_v1 = np.add(proj_v1, v1_perpendicular) #Soma os vetores.
                vetor_v2 = np.add(proj_v2, v2_perpendicular)
                
                bolas[i].velocidade = vetor_v1 #Atualiza os vetores após a colisão.
                bolas[j].velocidade = vetor_v2 
                
                bolas[i].cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                bolas[j].cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))    
                # ==================================== #               
    pygame.display.update()
                  