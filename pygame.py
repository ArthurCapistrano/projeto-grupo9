import pygame
import sys

# Comando padrão de inicialização do pygame
pygame.init()

# Setando as varíaveis de cada cor da coleta seletiva
GREY: (128, 128, 128) # Não Reciclável
GREEN: (0, 156, 59) # Vidro
BLUE = (0, 143, 210) # Papel
RED: (229, 36, 34) # Plástico
YELLOW: (255, 209, 0) # Metal
BROWN: (96, 56, 20) # Orgânico
WHITE = (255, 255, 255) # Lixo Hospitalar
BLACK = (0, 0, 0) # Madeira
ORANGE: (255, 255, 0) # Resíduos Perigosos

# Configurando o tamanho da janela que se abre para o jogo
WIDTH, HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h

# Criando a janela do jogo com o tamanho definido acima
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Alterando o nome da janela
pygame.display.set_caption("DigiTrash!")

# Fonte usada para textos no jogo
font = pygame.font.Font(None, 36)

# Função para perguntar ao professor quantos alunos estão participando
def get_num_alunos():
    screen.fill(WHITE)

    message_text = font.render("Olá Professor(a), quantos alunos participarão do jogo?", True, BLACK)
    message_rect = message_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    screen.blit(message_text, message_rect)

    input_box = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
    color_inactive = WHITE
    color_active = WHITE
    color = color_inactive
    aluno_text = ''
    active = False

    save_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 60, 100, 50)
    save_color_inactive = pygame.Color('lightgreen')
    save_color_active = pygame.Color('limegreen')
    save_color = save_color_inactive

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active = not active
                    color = color_active if active else color_inactive
                elif save_button.collidepoint(event.pos):
                    return int(aluno_text)

            if event.type == pygame.KEYDOWN:
                if active:
                    if event.key == pygame.K_RETURN:
                        return int(aluno_text)
                    elif event.key == pygame.K_BACKSPACE:
                        aluno_text = aluno_text[:-1]
                    else:
                        aluno_text += event.unicode

        txt_surface = font.render(aluno_text, True, BLACK)
        width = max(200, txt_surface.get_width() + 10)
        input_box.w = width

        pygame.draw.rect(screen, color, input_box, border_radius=15)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))

        pygame.draw.rect(screen, save_color, save_button, border_radius=15)
        save_text = font.render("Salvar", True, BLACK)
        save_rect = save_text.get_rect(center=save_button.center)
        screen.blit(save_text, save_rect)

        pygame.display.flip()

# Lista de questões, contendo dicionários para cada questão
questions = [
    # Primeira pergunta
    {
        "question": "Para lixeira Vermelha, qual lixo colocamos?",
        "options": ["a) Vidro", "b) Amarela", "c) Plástico", "d) Azul"],
        "correct_answer": "c",
    },
    # Segunda pergunta
    {
        "question": "Qual é o maior planeta do sistema solar?",
        "options": ["a) Marte", "b) Júpiter", "c) Vênus", "d) Urano"],
        "correct_answer": "b",
    },
]

# Função para exibir uma pergunta na tela
def display_question(question_data):
    # Escolhendo a cor de fundo
    screen.fill(WHITE)

    # Exibe a pergunta no centro da tela
    question_text = font.render(question_data["question"], True, BLACK)
    question_rect = question_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(question_text, question_rect)

    # Exibe as opções alinhadas uma ao lado da outra
    option_y = HEIGHT // 2
    for option in question_data["options"]:
        option_text = font.render(option, True, BLACK)
        option_rect = option_text.get_rect(left=100, top=option_y)
        screen.blit(option_text, option_rect)
        option_y += 50

# Loop principal do jogo
num_alunos = get_num_alunos()  # Obter o número de alunos do professor

players = []  # Lista de jogadores

for i in range(num_alunos):
    player = {
        "name": f"player" + str(i),
        "score": 0
    }
    players.append(player)

print("num_alunos: ", num_alunos)

pos = 0 # Qual player estaremos nos referindo
while num_alunos > 0:
    current_question = 0  # Reinicia o índice da pergunta
    score = 0  # Reinicia a pontuação

    # Loop de eventos pygame
    running = True
    while running and current_question < len(questions):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False  # Parar o jogo se o professor fechar a janela

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    chosen_option = "a"
                elif event.key == pygame.K_b:
                    chosen_option = "b"
                elif event.key == pygame.K_c:
                    chosen_option = "c"
                elif event.key == pygame.K_d:
                    chosen_option = "d"

                # Acessando a lista de perguntas indo na pergunta corrente e acessando a resposta correta
                if chosen_option == questions[current_question]["correct_answer"]:
                    score += 1

                current_question += 1  # Está mudando a pergunta que irá aparecer

        # Exibir a pergunta enquanto tiver perguntas a serem feitas
        if current_question < len(questions):
            display_question(questions[current_question])
            pygame.display.update()

    # Exibir e atualizar o score do jogador aqui, fora do loop de eventos
    print("------------")
    
    print(f'{players[pos]["name"]} fez:')
    print("Score: ", score)
    players[pos]["score"] += score
    
    pos += 1
    
    num_alunos -= 1  # Reduz o número de alunos a cada vez que as perguntas são respondidas

#Mostrando o score de cada jogador
screen.fill(WHITE) 
for i, player in enumerate(players):
    end_text = font.render(f"Pontuação final de {player['name']}: {player['score']}/{len(questions)}", True, BLACK)
    screen.blit(end_text, (250, 50 + i * 50))  #Ajusta a posição vertical para cada jogador a partir do i. Fará com que cada posição seja diferente.
    pygame.display.update() #As atualizações vão ser feitas imediatamente

# Colocando delay para ver a pontuação antes de pôr fim ao jogo
pygame.time.delay(3000)
    
pygame.quit()
sys.exit()