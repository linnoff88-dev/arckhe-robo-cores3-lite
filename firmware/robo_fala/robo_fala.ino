// robo-cores3-lite: esqueleto. Só confere a placa: mostra a PSRAM pela serial.
// A CoreS3 Lite não tem LED de usuário; tela, som e câmera entram na F2 (M5Unified + M5GFX) e na F4 (esp_camera).
//
// Compilar (na raiz do repo):
//   arduino-cli compile --fqbn esp32:esp32:m5stack_cores3 firmware/robo_fala
// A placa m5stack_cores3 liga a PSRAM em modo QSPI por padrão. Se a serial mostrar PSRAM 0 na Lite,
// testar --fqbn esp32:esp32:m5stack_cores3:PSRAM=opi (DEFINICAO.md, seção 12).

#include <Arduino.h>

void setup() {
  Serial.begin(115200);
  delay(1500);
  Serial.printf("robo-cores3-lite esqueleto | PSRAM: %u bytes | heap livre: %u bytes\n",
                (unsigned)ESP.getPsramSize(), (unsigned)ESP.getFreeHeap());
  if (ESP.getPsramSize() == 0) {
    Serial.println("ERRO: PSRAM em 0. Testar PSRAM=opi (veja firmware/README.md).");
  }
}

void loop() {
  Serial.printf("vivo | %lu s\n", millis() / 1000);
  delay(5000);
}
