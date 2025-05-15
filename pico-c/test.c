#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"

#include "pico/cyw43_arch.h"
#define LED_PIN CYW43_WL_GPIO_LED_PIN


#define ADC_PIN 26
#define ADC_ID  0

// Initialisation de la puce wifi qui gère la led
int pico_led_init(void) {
    return cyw43_arch_init();
}

// Allume ou éteint la led sur le pico 
void pico_set_led(bool led_on) {
    cyw43_arch_gpio_put(LED_PIN, led_on);
}

int main() {
    /* Initialisation des différents systèmes */

    // Entrée et sortie du port série (USB)
    stdio_init_all();

    // LED sur la carte
    int rc = pico_led_init();
    hard_assert(rc == PICO_OK);

    // Convertisseur analogique-numérique intégré
    // Voir https://pico.pinout.xyz
    adc_init();

    adc_gpio_init(ADC_PIN);
    adc_select_input(ADC_ID); // Le convertisseur possède 3 entrées 

    // constante pour multiplier la lecteur afin d'obtenir un nombre entre 0 et 1 (théoriquement)
    // const float conversion_factor = 3.3f / (1 << 12);
    
    // Signal lumineux pour indiquer que la lecture est en cours
    printf("Reading sample to check fonctionnality...\n");
    uint16_t result = adc_read();
    printf("Reading successful");
    pico_set_led(true);
    sleep_ms(250);

    // Boucle principale de fonctionnement
    while (1) {
        result = adc_read();
        printf("%d\n", result);
        sleep_ms(1); // En pratique nécessaire pour permettre au convertisseur de traiter l'entrée analogique (théoriquement on ne devrait pas avoir besoin)
    }

    return 0;
}
