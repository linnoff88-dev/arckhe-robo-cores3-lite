// Copie este arquivo para "segredos.h" (na mesma pasta) e preencha.
// O "segredos.h" está no .gitignore: nunca vai para o repositório.
#pragma once

#define WIFI_NOME      "nome-da-sua-rede"
#define WIFI_SENHA     "senha-da-sua-rede"

// Cérebro: 1 = servidor local (opção B, padrão). 2 = API direta (opção A, só depois da autorização do Nei).
#define CEREBRO        1

// Opção B: endereço do servidor local na rede de casa (a máquina onde roda servidor/servidor.py).
#define SERVIDOR_URL   "http://192.168.0.10:8770"

// O mesmo valor de ROBO_TOKEN do servidor/.env
#define ROBO_TOKEN     "troque-por-um-texto-longo"

// Opção A (F3): fica vazio até o Nei autorizar o serviço e a finalidade.
#define API_CHAVE      ""
