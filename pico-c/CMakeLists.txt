cmake_minimum_required(VERSION 3.13)

include(pico_sdk_import.cmake)
include(pico_extras_import_optional.cmake)

project(test_project C CXX ASM)
set(CMAKE_C_STANDARD 11)
set(CMAKE_CXX_STANDARD 17)
pico_sdk_init()

add_executable(test 
    test.c 
)

pico_add_extra_outputs(test)
pico_enable_stdio_uart(test 1)
pico_enable_stdio_usb(test 1)

target_link_libraries(test pico_stdlib)
target_link_libraries(test pico_cyw43_arch_none)
target_link_libraries(test pico_stdlib hardware_adc)


add_executable(adc 
    adc.c 
)

pico_add_extra_outputs(adc)
pico_enable_stdio_uart(adc 1)
pico_enable_stdio_usb(adc 1)

target_link_libraries(adc pico_stdlib)
target_link_libraries(adc pico_cyw43_arch_none)
target_link_libraries(adc pico_stdlib hardware_adc)

add_executable(nqadc 
    adc-noqueue.c 
)

pico_add_extra_outputs(nqadc)
pico_enable_stdio_uart(nqadc 1)
pico_enable_stdio_usb(nqadc 1)

target_link_libraries(nqadc pico_stdlib)
target_link_libraries(nqadc pico_cyw43_arch_none)
target_link_libraries(nqadc pico_stdlib hardware_adc)


add_executable(mcp3008_spi
        mcpread.c
        )

# pull in common dependencies and additional spi hardware support
target_link_libraries(mcp3008_spi pico_stdlib hardware_spi)
target_link_libraries(mcp3008_spi pico_stdlib)
target_link_libraries(mcp3008_spi pico_cyw43_arch_none)
target_link_libraries(mcp3008_spi pico_stdlib hardware_adc)

# create map/bin/hex file etc.
pico_add_extra_outputs(mcp3008_spi)
pico_enable_stdio_usb(mcp3008_spi 1)
pico_enable_stdio_uart(mcp3008_spi 1)
