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

int frequence = 5000; // Hz 
int temps_acqu = 1;   // s

queue_t file_adc;
const int TAILLE_FILE = 100;



bool timer_callback([[maybe_unused]] repeating_timer_callback_t *rt) {
    uint16_t result = adc_read();
    printf("I was called");

    if (!queue_try_add(&file_adc, &result)) {
        printf("WARNING : La file est pleine\n");
    }

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

    printf("Begin init\n");

    // Initialisation de la puce wifi qui gère la led
    int rc = cyw43_arch_init();
    hard_assert(rc == PICO_OK);

    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(500);
    printf("LED initiated\n");

    // Convertisseur analogique-numérique intégré
    // Voir les pins ADC sur https://pico.pinout.xyz 
    adc_init();

    adc_gpio_init(ADC_PIN);
    adc_select_input(ADC_ID); // Le convertisseur possède 3 entrées 

    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(500);
    printf("ADC initiated\n");

    // Timer qui se rappelle à une fréquence fixée
    repeating_timer_t timer;

    if (!add_repeating_timer_us(1000000 / frequence, (repeating_timer_callback_t) timer_callback, NULL, &timer)) {
        printf("ERREUR : Impossible de créer le timer\n");
        return 1;
    }

    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(500);
    printf("Timer initiated\n");

    // initialisation de la structure de données 
    queue_init(&file_adc, sizeof(uint16_t), TAILLE_FILE);
    
    /* L'allumage de la LED annonce le démarrage de l'acquisition */
    pico_set_led(true);
    sleep_ms(1000);
    pico_set_led(false);
    sleep_ms(500);
    printf("Sucessfull initialisation\n");


    temps_acqu *= frequence;
    for(; temps_acqu > 0; temps_acqu--) {
        printf("Trying remove\n");
        uint16_t valeur;
        queue_remove_blocking(&file_adc, &valeur);
        printf("%d\n", valeur);
    }

    cancel_repeating_timer(&timer);

    // Ignore les données restantes
    uint16_t v;
    while (queue_try_remove(&file_adc, &v));

    queue_free(&file_adc);

    return 0;
}
