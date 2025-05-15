#include "pico/stdlib.h"
#include "hardware/gpio.h"
#include "hardware/adc.h"
#include "pico/util/queue.h"

#include "pico/cyw43_arch.h"
#define LED_PIN CYW43_WL_GPIO_LED_PIN


/* Exemple d'utilisation d'un Raspberry Pi Pico W 
 * Lecture répétée de son convertisseur analogique 
 * numérique (ADC en anglais) intégré, à l'aide de 
 * timer précis 
 */

#define ADC_PIN 26
#define ADC_ID  0

int frequence = 5; // Hz 
int temps_acqu = 1;   // s


bool timer_callback([[maybe_unused]] repeating_timer_callback_t *rt) {
    uint16_t result = adc_read();
    printf("%d\n", result);

    return true; // Indique que le timer continue de se répeter
}



// Allume ou éteint la led sur le pico_w 
void pico_set_led(bool led_on) {
    cyw43_arch_gpio_put(LED_PIN, led_on);
}



int main() {
    /* Initialisation des différents systèmes */

    // Entrée et sortie du port série (USB)
    stdio_init_all();

    // Initialisation de la puce wifi qui gère la led
    int rc = cyw43_arch_init();
    hard_assert(rc == PICO_OK);

    // Convertisseur analogique-numérique intégré
    // Voir les pins ADC sur https://pico.pinout.xyz 
    adc_init();

    adc_gpio_init(ADC_PIN);
    adc_select_input(ADC_ID); // Le convertisseur possède 3 entrées 

    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(1000);
    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(1000);
    pico_set_led(true);

    // Timer qui se rappelle à une fréquence fixée
    repeating_timer_t timer;

    if (!add_repeating_timer_us(1000000 / frequence, (repeating_timer_callback_t) timer_callback, NULL, &timer)) {
        printf("ERREUR : Impossible de créer le timer\n");
        return 1;
    }

    /* L'allumage de la LED annonce le démarrage de l'acquisition */
    pico_set_led(true);

    sleep_until(2000);

    cancel_repeating_timer(&timer);

    return 0;
}
