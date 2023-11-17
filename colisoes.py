import numpy as np
import math 
import pygame 
import random
from pygame.locals import *
from sys import exit

pygame.init()


N_BOLAS = 10
largura = 1680
altura = 1024
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption('Colisões')



# Definição do objeto 'bola' #
class Bolas:
    def __init__(self) -> None:
        self.pos = [random.randint(50, largura - 50), random.randint(50, altura - 50)]
        self.velocidade = [random.randint(-10, 10), random.randint(-10, 10)]
        self.raio = random.randint(10, 50)
        self.massa = self.raio*(3/2)
        self.cor = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    def cria(self):
        pygame.draw.circle(tela, self.cor, (self.pos[0], self.pos[1]), self.raio)
        
#======================================================== Criar bolas e validá-las ===================================================================================#
bolas = []
for i in range(N_BOLAS):
    bolas.append(Bolas()) 
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
#====================================================================================================================================================================#                     
                    
clock = pygame.time.Clock() 
  
while True:
    
    clock.tick(30)
    tela.fill((115, 0, 155))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
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
            bolas.velocidade[1] *= -1
            
        elif bolas[i].pos[1] <= bolas[i].raio:
            bolas[i].pos[1] = bolas[i].raio
            bolas[i].velocidade[1] *= -1        
                

            
                   
    pygame.display.update()
                  