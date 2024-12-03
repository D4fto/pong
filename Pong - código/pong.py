import pygame
from pygame.locals import *
from random import randrange
import time
import os
from sys import exit

pygame.init()#inicializa o pyggame
#region criando variáveis
#geralmente quando ver uma váriavel terminada em p é que ela guarda  um valor padrão
tamx, tamy=pygame.display.get_desktop_sizes()[0]#tamx = largura da tela, tamy = largura da tela
scg = (tamy/1080+tamx/1920)/2#faz uma proporção entre o tamanho da tela original do jogo(1920x1080) e o tamanho atual da tela (tamx x tamy), sempre que aparecer algo*scg é só para proporcionalo
mus1 = ylin = pontos2 = pontos1 = yy = x = tempo = tem = m = 0#define varias coisas pra 0
exe = debug = menu = False
tempo2 = time.time()#variável para  o cronometro
multiplayer2 = multiplayer = True
som = pygame.mixer.Sound('arquivos/som.wav')#define o som de quicar da bola
som2 = pygame.mixer.Sound('arquivos/ponto.wav')#define o som de qfazer pontos
cor_bola = [255,255,255]
speed_playersp = speed_players = speed_lim = round(35 * scg) 
lim = 15*scg#tamanho das bordas
acel2 = acel = 1.001#aceleração
volume_som = volume_musica = 1
speed_bolay = speed_bolax = speed_bolap = speed_bola = round(10 * scg)
largura = 25 * scg#largura dos jogadores
altura = altura2 = round(150 * scg)
loc_inic_cir = [tamx/2,tamy/2]#localização inicial da bola
loc_temp_cir = loc_inic_cir[:]#localização temporaria da bola
tela = pygame.display.set_mode((tamx,tamy))#define a tela, que é a superfície onde tudo sera mostrado
pygame.display.set_caption("Pong")#define o nome da janela
pygame.display.set_icon(pygame.image.load("arquivos/pong_icon.png"))#define o ícone da janela
fps = 100
clock = pygame.time.Clock()#comando para definir fps
y2 = y1 = tamy/2#localizações dos jogadores
rect2 = pygame.draw.rect(tela,(255,255,255),(0,0,largura,altura2))#joagador da direita
rect1 = pygame.draw.rect(tela,(255,255,255),(0,0,largura,altura))#joagador da esquerda
pygame.mixer_music.set_volume(volume_musica)#define o volume da música 
pygame.mixer.Sound.set_volume(som,volume_som)#define o volume do efeito sonoro 
pasta_musicas = os.listdir("arquivos/musica/")#faz a lista das músicas na pasta das músicas
musica = pygame.mixer.music.load(f"arquivos/musica/{pasta_musicas[mus1]}")#define a música inicial
pygame.mixer.music.play(-1)#faz a música tocar em loop
pygame.mouse.set_visible(True)#deixa o mouse invisivel
# point = pygame.image.load("arquivos/point.png").convert_alpha() ignora
# point = pygame.transform.scale(point,(32,32)) ignora
# point_rect = point.get_rect() ignora

#region jogo da vida

matriz = []
for linha in range(54):
    matriz.append([])
    for _ in range(96):
        matriz[linha].append(0)
game = False
delay = 0

#endregion



#endregion
#region criando funções
def fonte(tam):#função fonte, entrada tamanho
    return pygame.font.Font('arquivos/Minecrafter.Reg.ttf',tam)#retorna a fonte do minecraft no tamanho pedido
def printa(fonte,x,espaco,yo,local,cor,tela,palavras):#fonte = fonte que será usada, x = localização x do texto, espaco = espaçamento entre as linhas, yo = y original, local = localização que sera definida(centro,topo esquerda,topo direita) ex:topoesquerda=(x,y), cor = cor, tela = tela onde vai ficar o texto, palavras = lista de palvras ou frases que serão escritas na tela
    y=0#basicamente o numero de linhas
    espaco*=scg#proporciona o espaçamento
    yo*=scg#proporciona o y original
    for a in palavras:#percorre a lista de palavras
        msgm = fonte.render(a,False,cor,(0,0,0))#renderiza o texto na cor escolhida com fundo preto
        if local == 'center':#se a localização for o centro
            msgm_rect = msgm.get_rect(center = [x,yo+espaco*y])#basicamente define o centro do texto
        if local == 'topleft':#se a localização for o topo esquerdo
            msgm_rect = msgm.get_rect(topleft = [x,yo+espaco*y])#basicamente define o topo esquerdo do texto
        if local == 'topright':#se a localização for o topo direito
            msgm_rect = msgm.get_rect(topright = [x,yo+espaco*y])#basicamente define o topo direito do texto
        tela.blit(msgm,msgm_rect)#desenha na tela a mensaggem na localização escolhida
        y+=1#pula a linha
#endregion
#region loop principal(reinicia a cada frame)
while True: 
    clock.tick(fps) #define o fps
    
    #region loop que identifica as ações do usuário
    for event in pygame.event.get():#for que passa por todas as ações que o usuário fez naquele frame
        if event.type == pygame.QUIT:#identifica se o usuário clickou no x de sair
                exit()#termina o programa
        #region identifica se uma tecla foi pressionada
        if event.type == pygame.KEYDOWN:#identifica se alguma tecla foi pressionada
            if event.key == K_SPACE:#se a tecla(key) do evento(event) for a barra de espaço
                if not(exe):#se não tiver executando(acontecendo uma rodada)
                    exe=True#começa a executar
                    if randrange(0,2) == 1:#sorteia um número(0 ou 1) e se for 1 entra no if
                        speed_bolax*=-1#faz a bola começar para a direção horizontal oposta a que estava
                    if randrange(0,2) == 1:#sorteia um número(0 ou 1) e se for 1 entra no if
                        speed_bolay*=-1#faz a bola começar para a direção vertical oposta a que estava
            if event.key == K_m and not(exe):#se a tecla(key) do evento(event) for 'm' e não tiver executando(acontecendo uma rodada)
                if multiplayer:#se o jogador a direita não for um bot
                    multiplayer=False#jogador da direita vira um bot
                else:#se o jogador da direita for um bot
                    multiplayer=True#jogador da direita vira um jogador normal(player) controlado pelo usuário
            if event.key == K_p:#se a tecla(key) do evento(event) for 'p'
                if multiplayer2 and not(exe):#se o jogador a esquerda não for um bot e não tiver executando(acontecendo uma rodada)
                    multiplayer2=False#jogador da esquerda vira um bot
                else:#se o jogador da esquerda for um bot
                    multiplayer2=True#jogador da esquerda vira um jogador normal(player) controlado pelo usuário
            if event.key == K_v:
                if game:
                    game=False
                else:
                    game=True

            if event.key == K_ESCAPE:#se a tecla(key) do evento(event) for 'Esc'
                exit()#termina o programa
            if event.key == K_F1:#se a tecla(key) do evento(event) for 'F1'
                if debug:#se o debug estiver ativo
                    debug = False#desativa o debug
                else:#se o debug estiver desativado
                    debug = True#ativa o debug
            if event.key == K_F2:#se a tecla(key) do evento(event) for 'F2'
                mus1+=1#pula para a próxima música da pasta de músicas
                if mus1 == len(pasta_musicas):#se o indíce da música estiver fora do tamanho da lista de músicas
                    mus1=0#volta pra primeira música
                musica = pygame.mixer.music.load(f"arquivos/musica/{pasta_musicas[mus1]}")#carrega a nova música
                pygame.mixer.music.play(-1)#começa a tocar a música em loop
            if event.key == K_r and not(exe):#se a tecla(key) do evento(event) for 'r' e não tiver executando(acontecendo uma rodada)
                pontos1=0#reseta os pontos do jogador da esquerda
                pontos2=0#reseta os pontos do jogador da direita
            if event.key == K_c:#se a tecla(key) do evento(event) for 'c'
                if menu:#se já tiver no menu
                    menu = False#sai do menu 
                else:#se não tiver no menu
                    menu = True#entra no menu
        #endregion
    #endregion
    #region menu
    if menu:#se estiver no menu
        clock.tick(10)#fps fica em 10
        tela.fill((0,0,0))#preenche a tela de preto(todo frame a tela é preenchida de novo como uma forma de 'apagar' o que estava desenhado na tela anteriormente)
        if pygame.key.get_pressed()[K_e] and volume_musica<1:#se a tecla 'e' estiver pressionada e o volume da musica for menor que 1(no caso 1 seria 100%)
            volume_musica+=0.01#adiciona 0.01 no volume da música(adiciona 1%)
            pygame.mixer_music.set_volume(volume_musica)#aplica o novo volume da musica
        if pygame.key.get_pressed()[K_q] and volume_musica>0:#se a tecla 'q' estiver pressionada e o volume da musica for maior que 0
            volume_musica-=0.01#Tira 0.01 no volume da música(tira 1%)
            pygame.mixer_music.set_volume(volume_musica)#aplica o novo volume da musica
        if pygame.key.get_pressed()[K_d] and volume_som<1:#se a tecla 'd' estiver pressionada e o volume dos efeitos sonoros for menor que 1(no caso 1 seria 100%)
            volume_som+=0.01#adiciona 0.01 no volume dos efeitos sonoros(adiciona 1%)
            pygame.mixer.Sound.set_volume(som,volume_som)#aplica o novo volume para o efeito sonoro de quicar a bola
            pygame.mixer.Sound.set_volume(som2,volume_som)#aplica o novo volume para o efeito sonoro de fazer um ponto
        if pygame.key.get_pressed()[K_a] and volume_som>0:#se a tecla 'q' estiver pressionada e o volume dos efeitos sonoros for maior que 0
            volume_som-=0.01#Tira 0.01 no volume dos efeitos sonoros(tira 1%)
            pygame.mixer.Sound.set_volume(som,volume_som)#aplica o novo volume para o efeito sonoro de quicar a bola
            pygame.mixer.Sound.set_volume(som2,volume_som)#aplica o novo volume para o efeito sonoro de fazer um ponto
        printa(fonte(int(50*scg)),tamx/2,50,50,'center',(150,255,150),tela,['p para player1 virar bot','m para player2 virar bot','r para resetar pontos','f2 para trocar a musica','f1 para debug','esc para sair',f'musica  q {int(volume_musica*100)} e',f'efeitos sonoros  a {int(volume_som*100)} d','','debug layout','','Limite velocida bola 1 2','aceleracao bola 3 4','velocida bola padrao 5 6','velocida player 7 8','tamanho player1 9 0','tamanho player2 menos igual','fps f g','','c para sair do menu'])
        tela.blit(fonte(int(40*scg)).render(("v para jogo da vida"), False,(255,255,255),(0,0,0)),(25,25))
        #a linha acima mostra na tela tudo que ta nos cochetes centralizado com um espaçamento de 50
        tempo2 = time.time() - tempo#fazer o cronometro que aparece quando se está jogando um player vs o bot da direita ficar sem atualizar no menu
    #endregion
    #region não menu
    else:
        clock.tick(fps)#seta o fps do jogo
        tela.fill((0,0,0))#preenche a tela de preto(todo frame a tela é preenchida de novo como uma forma de 'apagar' o que estava desenhado na tela anteriormente)
        if game:
            if exe:
                for linha in range(len(matriz)):
                    for coluna in range(len(matriz[linha])):
                        if matriz[linha][coluna]:
                            pygame.draw.rect(tela,(255,255,0),(20*coluna,20*linha,20,20))
            for a in range(1,54):
                pygame.draw.line(tela,(150,150,150),(0,20*a),(1920,20*a),1)
            for a in range(1,96):
                pygame.draw.line(tela,(150,150,150),(20*a,0),(20*a,1080),1)
        #region mostra a listra do meio da tela
        while ylin<tamy:
            pygame.draw.rect(tela,(255,255,255),(tamx/2-10*scg/2,ylin,10*scg,tamy/27))
            ylin+=2*(tamy/27)
        ylin=0
        #endregion
        
            
        printa(fonte(int(100*scg)),tamx/2-25,0,lim+25,'topright',(255,255,255),tela,[str(pontos1)])#mostra na tela os pontos do joagdor da esquerda na cor branca
        printa(fonte(int(100*scg)),tamx/2+25,0,lim+25,'topleft',(255,255,255),tela,[str(pontos2)])#mostra na tela os pontos do joagdor da direita na cor branca
        lim3=pygame.draw.rect(tela,(255,255,255),(0,0,tamx,lim))#borda de cima
        lim4=pygame.draw.rect(tela,(255,255,255),(0,tamy-lim,tamx,lim))#borda de baixo
        #region executando(acontecendo uma rodada)
        if exe:
            #region jogador esquerda
            
            if multiplayer2:#se o jogador da esquerda for um player
                if pygame.key.get_pressed()[K_w] and not(rect1.colliderect(lim3)):#se a tecla 'k' estiver pressionada e o jogador não estiver colidindo com a borda de cima
                    y1-=speed_players-round(10*scg)#a posição y do jogador sobe a (velocidade dos player - 10) pixels
                elif rect1.colliderect(lim3) and not(pygame.key.get_pressed()[K_s]):#sistema pra o jogador não bugar com a borda
                    y1=lim+altura/2-2#sistema pra o jogador não bugar com a borda
                if pygame.key.get_pressed()[K_s] and not(rect1.colliderect(lim4)):#se a tecla 'k' estiver pressionada e o jogador não estiver colidindo com a borda de baixo
                    y1+=speed_players-round(10*scg)#a posição y do jogador desce a (velocidade dos player - 10) pixels
                elif rect1.colliderect(lim4) and not(pygame.key.get_pressed()[K_w]):#sistema pra o jogador não bugar com a borda
                    y1=tamy-lim-altura/2+1#sistema pra o jogador não bugar com a borda
                if tempo > tem and m == 0:#se o tempo atual do cronometro for maior do que o melhor tempo e o jogador não foi um bot na rodada
                    tem = tempo#melhor tempo = tempo atual
            else:#se o jogador for um bot
                if y1 < bola.center[1] and not(rect1.colliderect(lim4)):#se a posição y do centro da bola for maior que o centro y do player e não tiver colidindo com a borda de cima
                    if multiplayer:#se o player da direita for um player
                        y1+=speed_players-round(2*scg)#a posição y do jogador desce a (velocidade dos player - 2) pixels(deixa o bot 'vencivel')
                    else:#se o player da direita for um bot
                        y1+=speed_players#a posição y do jogador desce a (velocidade dos player) pixels(deixa o bot invencivel)
                elif rect1.colliderect(lim4) and not(y1 > bola.center[1]):#sistema pra o jogador não bugar com a borda
                    y1=tamy-lim-altura/2+1#sistema pra o jogador não bugar com a borda
                if y1 > bola.center[1] and not(rect1.colliderect(lim3)):#se a posição y do centro da bola for menor que o centro y do player e não tiver colidindo com a borda de baixo
                    if multiplayer:#se o player da direita for um player
                        y1-=speed_players-round(2*scg)#a posição y do jogador sobe a (velocidade dos player - 2) pixels(deixa o bot 'vencivel')
                    else:#se o player da direita for um bot
                        y1-=speed_players#a posição y do jogador sobe a (velocidade dos player) pixels(deixa o bot invencivel)
                elif rect1.colliderect(lim3) and not(y1 < bola.center[1]):#sistema pra o jogador não bugar com a borda
                    y1=lim+altura/2-1#sistema pra o jogador não bugar com a borda
                m=1#grava que o jogador da esquerda já foi um bot na rodada
            #endregion
            #region jogador direita
            if multiplayer:#se o jogador da direita for um player
                if pygame.key.get_pressed()[K_UP] and not(rect2.colliderect(lim3)):#se a setinha pra cima estiver pressionada e o jogador não estiver colidindo com a borda de cima
                    y2-=speed_players-round(10*scg)#a posição y do jogador sobe a (velocidade dos player - 10) pixels
                elif rect2.colliderect(lim3) and not(pygame.key.get_pressed()[K_DOWN]):#sistema pra o jogador não bugar com a borda
                    y2=lim+altura2/2-1#sistema pra o jogador não bugar com a borda
                if pygame.key.get_pressed()[K_DOWN] and not(rect2.colliderect(lim4)):#se a setinha pra baixo estiver pressionada e o jogador não estiver colidindo com a borda de baixo
                    y2+=speed_players-round(10*scg)#a posição y do jogador desce a (velocidade dos player - 10) pixels
                elif rect2.colliderect(lim4) and not(pygame.key.get_pressed()[K_UP]):#sistema pra o jogador não bugar com a borda
                    y2=tamy-lim-altura2/2+1#sistema pra o jogador não bugar com a borda
            else:#se o jogador for um bot
                if y2 < bola.center[1] and not(rect2.colliderect(lim4)):#se a posição y do centro da bola for maior que o centro y do player e não tiver colidindo com a borda de cima
                    y2+=speed_players#a posição y do jogador desce a (velocidade dos player) pixels(deixa o bot invencivel)
                elif rect2.colliderect(lim4) and not(y2 > bola.center[1]):#sistema pra o jogador não bugar com a borda
                    y2=tamy-lim-altura2/2+1#sistema pra o jogador não bugar com a borda
                if y2 > bola.center[1] and not(rect2.colliderect(lim3)):#se a posição y do centro da bola for menor que o centro y do player e não tiver colidindo com a borda de baixo
                    y2-=speed_players#a posição y do jogador sobe a (velocidade dos player) pixels(deixa o bot invencivel)
                elif rect2.colliderect(lim3) and not(y2 < bola.center[1]):#sistema pra o jogador não bugar com a borda
                    y2=lim+altura2/2-1#sistema pra o jogador não bugar com a borda
                tempo = time.time() - tempo2#atualiza o cornometro atual
                tempo = round(tempo,2)#arredonda o tempo do cronometro
                tempo1 = fonte(int(50*scg)).render(str(tempo)+' s',0,(255,255,255))#renderiza o texto do cronometro
                tela.blit(tempo1, (25, 25+lim))#mostra o cornometro a 25 pixels na horizontal e 25+o tamanho da borda pra baixo
            #endregion
            printa(fonte(int(50*scg)),tamx-int(25*scg),0,25+lim,'topright',(255,255,255),tela,[f'{tem} s'])#mostra na tela o melhor tempo
            rect1.center=(largura,y1)#define a posição do centro do jogador da esquerda
            rect2.center=(tamx-largura,y2)#define a posição do centro do jogador da direita
            bola = pygame.draw.circle(tela,cor_bola,loc_temp_cir,15*scg)#desenha a bola

            if x == 0:#sistema de esperar 5 frames após a colisão
                if bola.colliderect(rect1) or bola.colliderect(rect2):#se a bola colidir com qualquer jogador
                    som.play()#toca o som de quicar
                    speed_bolax*=-1 #a velocidade horizontal da bola inverte
                    cor_bola = [randrange(0,256),randrange(0,256),randrange(0,256)]#cor da bola muda pra uma aleatória
                    x = 5#sistema de esperar 5 frames após a colisão
            else:#sistema de esperar 5 frames após a colisão
                x -= 1#sistema de esperar 5 frames após a colisão
            if yy == 0:#sistema de esperar 5 frames após a colisão
                if bola.colliderect(lim4) or bola.colliderect(lim3):#se a bola colidir com a borda de cima ou de baixo
                    speed_bolay*=-1#a velocidade vertical da bola inverte
                    som.play()#toca o som de quicar
                    cor_bola = [randrange(0,256),randrange(0,256),randrange(0,256)]#cor da bola muda pra uma aleatória
                    yy=5#sistema de esperar 5 frames após a colisão
            else:#sistema de esperar 5 frames após a colisão
                yy -= 1#sistema de esperar 5 frames após a colisão
            if not(speed_bola>speed_lim):#se a velocidade da bola não for maior que o limite de velocidade
                speed_bola *= acel#velocidade da bola é multiplicada pela aceleração
                speed_bolax = speed_bola*speed_bolax/abs(speed_bolax)#atualiza a velocidade horizontal da bola
                speed_bolay = speed_bola*speed_bolay/abs(speed_bolay) #atualiza a velocidade vertical da bola
            loc_temp_cir[0]+=speed_bolax#localização temporaria horizontal da bola é adicionada a velocidade horizontal
            loc_temp_cir[1]+=speed_bolay#localização temporaria vertical da bola é adicionada a velocidade vertical
            if 15*scg>loc_temp_cir[0]+100 or 15*scg>tamx-loc_temp_cir[0]+100:#verifica se a bola saiu da tela
                if 15*scg>loc_temp_cir[0]:#se a bola saiu na esquerda
                    pontos2+=1#adiciona 1 na pontuação do joagador da direita 
                else:#se a bola saiu na direita
                    pontos1+=1#adiciona 1 na pontuação do joagador da esquerddda 
                som2.play()#toca o som de fazer ponto
                loc_temp_cir = loc_inic_cir[:]#reinicia a localização da bola
                speed_bola = speed_bolap#velocidade da bola fica padrão
                y1 = tamy/2#y do jogador da esquerda fica no meio da tela
                y2 = tamy/2#y do jogador da direita fica no meio da tela
                
                if game:
                    matriz = []
                    for linha in range(54):
                        matriz.append([])
                        for _ in range(96):
                            matriz[linha].append(0)
                exe=False#rodada acaba
            acel = acel2#atualiza o valor dda aceleração
            
        #endregion
        #region não estiver acontecendo uma rodada
        else:
            tempo2=time.time()#sistema pro cronometro
            m=0
            tempo = time.time() - tempo2#atualiza o cornometro atual
            pygame.draw.rect(tela,(255,255,255),rect1)#desenha na tela o jogador da esquerda
            pygame.draw.rect(tela,(255,255,255),rect2)#desenha na tela o jogador da direita
            speed_players = speed_playersp#a velocidade dos players vai pra velocidade padrão
            speed_bola = speed_bolap#velocidade da bola vai pra velocidade padrão
            bola = pygame.draw.circle(tela,(255,255,255),loc_temp_cir,15*scg)#mostra a bola no centro
            rect1.center=(largura,tamy/2)#manda o jogador da esquerda pra sua posição incial
            rect2.center=(tamx-largura,tamy/2)#manda o jogador da direita pra sua posição incial
            printa(fonte(int(50*scg)),tamx-int(25*scg),0,25+lim,'topright',(255,255,255),tela,[f'{tem} s'])#mostrana tela o melhor tempo
            printa(fonte(int(50*scg)),tamx/2,100,200,'center',(150,255,150),tela,["Pressione espaco para iniciar",'Aperte c para comandos'])#mostra na tela os textos em cochetes
        #endregion
        rect1[3]=altura#define a altura do jogador da esquerda
        rect2[3]=altura2#define a altura do jogador da direita
        rect1[2]=largura#define a largura do jogador da esquerda
        rect2[2]=largura#define a largura do jogador da direita
        if multiplayer:#se o jogador da direita for um player
            pygame.draw.rect(tela,(255,255,255),rect2)#desenha o jogador da direita branco
        else:#se o jogador da direita for um bot
            pygame.draw.rect(tela,(255,0,0),rect2)#desenha o jogador da direita vermelho
        if multiplayer2:#se o jogador da esquerda for um player
            pygame.draw.rect(tela,(255,255,255),rect1)#desenha o jogador da esquerda branco
        else:#se o jogador da esquerda for um bot
            pygame.draw.rect(tela,(0,255,0),rect1)#desenha o jogador da esquerda verde
        vivostotal=0
        for linha in matriz:
            for individuo in linha:
                if individuo:
                    vivostotal+=1

        if bola.centerx>-1 and bola.centerx<1921 and bola.centery>-1 and bola.centery<1081:
            if vivostotal<600:
                
                for a in range(-1,2):
                    for i in range(-1,2):
                        if (bola.centery/20)+a>53 or int(bola.centerx/20)+i>95:
                            continue
                        matriz[int(bola.centery/20)+a][int(bola.centerx/20)+i]=randrange(2)
            else:
                for a in range(-1,2):
                    for i in range(-1,2):
                        if (bola.centery/20)+a>53 or int(bola.centerx/20)+i>95:
                            continue
                        matriz[int(bola.centery/20)+a][int(bola.centerx/20)+i]=0
        if game:
            
            if delay == 0:
                matriz_copia = []
                for i in range(len(matriz)):
                    matriz_copia.append([])
                    matriz_copia[i] = matriz[i][:]
                for linha in range(len(matriz_copia)):
                    for coluna in range(len(matriz_copia[linha])):
                        vivos = 0
                        for a in range(-1,2):
                            for i in range(-1,2):
                                if coluna+i>95:
                                    continue
                                if linha+a>53:
                                    continue
                                if matriz_copia[linha+a][coluna+i]:
                                    vivos+=1
                        if matriz_copia[linha][coluna]:
                            vivos-=1
                        if vivos==3:
                            matriz[linha][coluna]=1
                        if vivos<2 or vivos>3:
                            matriz[linha][coluna]=0
                            
                delay=5
            else:
                delay-=1
                    
                
        #region debug
        if debug:
            if pygame.key.get_pressed()[K_1]:#se a tecla 1 estiver sendo pressionada
                speed_lim += 1
            if pygame.key.get_pressed()[K_2]:#se a tecla 2 estiver sendo pressionada
                speed_lim -= 1
            if pygame.key.get_pressed()[K_3]:#se a tecla 3 estiver sendo pressionada
                acel2 += 0.0001
            if pygame.key.get_pressed()[K_4]:#se a tecla 4 estiver sendo pressionada
                acel2 -= 0.0001
            if pygame.key.get_pressed()[K_5]:#se a tecla 5 estiver sendo pressionada
                speed_bolap += 1
            if pygame.key.get_pressed()[K_6]:#se a tecla 6 estiver sendo pressionada
                speed_bolap -= 1
            if pygame.key.get_pressed()[K_7]:#se a tecla 7 estiver sendo pressionada
                speed_playersp += 1
            if pygame.key.get_pressed()[K_8]:#se a tecla 8 estiver sendo pressionada
                speed_playersp -= 1
            if pygame.key.get_pressed()[K_9]:#se a tecla 9 estiver sendo pressionada
                altura += 1
            if pygame.key.get_pressed()[K_0]:#se a tecla 0 estiver sendo pressionada
                altura -= 1
            if pygame.key.get_pressed()[K_MINUS]:#se a tecla - estiver sendo pressionada
                altura2 += 1
            if pygame.key.get_pressed()[K_EQUALS]:#se a tecla = estiver sendo pressionada
                altura2 -= 1
            if pygame.key.get_pressed()[K_LEFT]:#se a setinha esquerda estiver sendo pressionada
                largura += 1
                lim+=1
            if pygame.key.get_pressed()[K_RIGHT]:#se a setinha direita estiver sendo pressionada
                largura -= 1
                lim-=1
            if pygame.key.get_pressed()[K_f]:#se a tecla f estiver sendo pressionada
                fps += 1
            if pygame.key.get_pressed()[K_g]:#se a tecla g estiver sendo pressionada
                fps -= 1
            printa(fonte(int(50*scg)),25,50,25,'topleft',(150,255,150),tela,[str(speed_lim),str(acel2),str(speed_bolap),str(speed_players),str(altura),str(altura2),str(fps)])
            #a linha acima desenha tudo o que tá entre cochetes
            

    #endregion
    #endregion
    # point_rect.center=pygame.mouse.get_pos() ignora
    # tela.blit(point,point_rect) ignora
    pygame.display.flip()#atualiza a tela
#endregion