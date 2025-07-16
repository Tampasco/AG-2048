import random

def simular_jogo_mock(individuo: list[str]) -> tuple[int, int]:
    maior_tile = random.choice([64, 128, 256, 512])
    movimentos_validos = random.randint(len(individuo) // 2, len(individuo))
    
    return (maior_tile, movimentos_validos)