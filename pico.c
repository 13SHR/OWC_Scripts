#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

#include "pico/cyw43_arch.h"
#define LED_PIN CYW43_WL_GPIO_LED_PIN


#define ADC_PIN 26
#define ADC_ID  0

// Initialisation de la puce wifi
// Nécessaire pour utiliser la led
int pico_led_init(void) {
    return cyw43_arch_init();
}

// Allume ou éteint la led sur le pico 
void pico_set_led(bool led_on) {
    cyw43_arch_gpio_put(LED_PIN, led_on);
}

// Retourne la valeur lue par le capteur sur le pin gpio 15
int read() {
    return gpio_get(15);
}

int main() {
    /* Initialisation des différents systèmes */

    // Entrée et sortie du port série (USB)
    stdio_init_all();

    // LED sur la carte
    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);

    // Signal lumineux pour indiquer que la lecture va commencer
    pico_set_led(true);
    sleep_ms(250);

    // Boucle principale de fonctionnement
    while (1) {
        printf("%d\n", read());
        sleep_us(1000);  // Attend 1000 µs
    }

    return 0;
}
