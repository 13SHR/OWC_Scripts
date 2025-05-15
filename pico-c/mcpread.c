/**
 * Copyright (c) 2020 Raspberry Pi (Trading) Ltd.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#include <boards/pico_w.h>
#include <hardware/gpio.h>
#include <stdio.h>
#include <string.h>
#include "pico/stdlib.h"
#include "pico/binary_info.h"
#include "pico/cyw43_arch.h"
#include "hardware/spi.h"

/* Example code to talk to a MCP3008 ADC converter.

   This is taking to simple approach of simply reading registers. It's perfectly
   possible to link up an interrupt line and set things up to read from the
   inbuilt FIFO to make it more useful.

   NOTE: Ensure the device is capable of being driven at 3.3v NOT 5v. The Pico
   GPIO (and therefore SPI) cannot be used at 5v.

   You will need to use a level shifter on the I2C lines if you want to run the
   board at 5v.

   Note: SPI devices can have a number of different naming schemes for pins. See
   the Wikipedia page at https://en.wikipedia.org/wiki/Serial_Peripheral_Interface
   for variations.
*/

#define LED_PIN CYW43_WL_GPIO_LED_PIN

#define PIN_MISO 8
#define PIN_CS   9
#define PIN_SCK  6
#define PIN_MOSI 7

#define SPI_PORT spi0
#define READ_BIT 0x80

static inline void cs_select() {
    asm volatile("nop \n nop \n nop");
    gpio_put(PIN_CS, 0);  // Active low
    asm volatile("nop \n nop \n nop");
}

static inline void cs_deselect() {
    asm volatile("nop \n nop \n nop");
    gpio_put(PIN_CS, 1);
    asm volatile("nop \n nop \n nop");
}


static void mcp3008_init() {
    // Two byte reset. First byte register, second byte data
    // There are a load more options to set up the device in different ways that could be added here
    uint8_t buf[] = {0x08};
    cs_select();
    spi_write_blocking(SPI_PORT, buf, 1);
    cs_deselect();
}

int read(uint8_t channel, bool differential) {
    /*
    uint8_t tx_buf[] = {
        0x01,   // see datasheet sec 6.1
        ((differential ? 0 : 1) << 7) | (channel << 4)
        };

    uint8_t rx_buf[3] = {0x00, 0x00, 0x00};

    cs_select();
    spi_write_read_blocking(SPI_PORT, tx_buf, rx_buf, 3);
    cs_deselect();

    return (((uint16_t)(rx_buf[1] & 0x07)) << 8) | rx_buf[2];
    */ 
    return gpio_get(15);
}


int main() {
    stdio_init_all();

    printf("Hello, MCP3008! Reading raw data from registers via SPI...\n");

    // This example will use SPI0 at 0.5MHz.
    spi_init(SPI_PORT, 1000 * 1000);
    gpio_set_function(PIN_MISO, GPIO_FUNC_SPI);
    gpio_set_function(PIN_SCK, GPIO_FUNC_SPI);
    gpio_set_function(PIN_MOSI, GPIO_FUNC_SPI);

    // Chip select is active-low, so we'll initialise it to a driven-high state
    gpio_init(PIN_CS);
    gpio_set_dir(PIN_CS, GPIO_OUT);
    gpio_put(PIN_CS, 1);
    gpio_set_dir(15, GPIO_IN);

    hard_assert(cyw43_arch_init() == PICO_OK);

    cyw43_arch_gpio_put(LED_PIN, true);
    sleep_ms(250);

    while (1) {
        int value = read(0, false);
        printf("%d\n", value);

        sleep_us(100);
    }
}
