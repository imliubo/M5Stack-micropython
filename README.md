[![CI badge](https://github.com/imliubo/M5Stack-micropython/workflows/esp32%20port/badge.svg)](https://github.com/imliubo/M5Stack-micropython/actions?query=branch%3Amaster+event%3Apush) [![Coverage badge](https://coveralls.io/repos/imliubo/M5Stack-micropython/badge.png?branch=master)](https://coveralls.io/r/imliubo/M5Stack-micropython?branch=master)

The MicroPython for M5Stack project
===================================
<p align="center">
  <img src="https://github.com/imliubo/M5Stack-micropython/blob/master/logo/micropython-core2-logo.png" alt="MicroPython Logo"/>
</p>
This is the MicroPython project, which aims to put an implementation
of Python 3.x on microcontrollers and small embedded systems.

You can find the official website at [micropython.org](http://www.micropython.org).

More detail about MicroPython project you can find at the original repository on [github](github.com/micropython.micropython).

[About M5Stack](https://m5stack.com/)
-------------------------------------
M5Stack is modular stackable product development toolkits based on **ESP32** (The world’s most popular Wi-Fi SoC, upgrade of ESP8266). The M5 ecosystem consists of main controller we call it “core”, the stackable modules and bases, grove compatible sensors we call it “units” and different applications for STEM, makers and industry IoT. M5Stack is committed to providing easy-to-develop and cost-effective IoT devices.

M5Stack main controller support list
------------------------------------
| Supported                                                        | Support status |
| ---------------------------------------------------------------- | :------------: |
| [Core2](https://docs.m5stack.com/#/en/core/core2)                |     alpha      |
| [Core](https://docs.m5stack.com/#/en/core/basic)                 |      not       |
| [Fire](https://docs.m5stack.com/#/en/core/fire)                  |      not       |
| [Core2 for AWS](https://docs.m5stack.com/#/en/core/core2_for_aws)|      not       |
| [M5Paper](https://docs.m5stack.com/#/en/core/m5paper)            |      not       |
| [CoreInk](https://docs.m5stack.com/#/en/core/coreink)            |      not       |
| [Stick-C](https://docs.m5stack.com/#/en/core/m5stickc)           |      not       |
| [Stick-C Plus](https://docs.m5stack.com/#/en/core/m5stickc_plus) |      not       |
| [ATOM Matrix](https://docs.m5stack.com/#/en/core/atom_matrix)    |      not       |
| [ATOM Lite](https://docs.m5stack.com/#/en/core/atom_lite)        |      not       |

- ``not`` not support yet(The basic functions of micropython can be used).
- ``alpha`` just start for support, have bugs and missing functionality. 
- ``beta`` it's under improvement time, have bugs or missing functionality.
- ``stable`` after testing, there are no obvious bugs, and it can be used normally.

How to build the firmware(not test yet)
---------------------------------------
```bash
$ git clone --recursive https://github.com/imliubo/M5Stack-micropython.git
$ git clone https://github.com/espressif/esp-idf.git && cd esp-idf
$ git checkout 4c81978a3e2220674a432a588292a4c860eef27b  # ESP-IDF V4 or ESP-IDF V3: 9e70825d1e1cbf7988cf36981774300066580ea7
$ git submodule update --init --recursive
$ ./install.sh  
$ export ESPIDF=$(pwd)  # It is recommended to record this path in bashrc
$ cd ./../M5Stack-micropython
$ cd mpy-cross
$ make
$ cd ./../ports/esp32
```

Create a new file in the esp32 directory called `makefile`
and add the following lines to that file:

```
ESPIDF := ${ESPIDF} 
BOARD := M5STACK_CORE2
PORT := /dev/ttyUSB0
CROSS_COMPILE := xtensa-esp32-elf-

include Makefile
```

Then to build MicroPython for the M5Stack(ESP32) run:
```bash
$ . ${ESPIDF}/export.sh  # This step is necessary
$ make submodules
$ make
```

If you are installing MicroPython to your module for the first time, or
after installing any other firmware, you should first erase the flash
completely:

```bash
$ make erase
```

To flash the MicroPython firmware to your ESP32 use:

```bash
$ make deploy
```

You can get a prompt via the serial port, via UART0, which is the same UART
that is used for programming the firmware.  The baudrate for the REPL is
115200 and you can use a command such as:

```bash
$ picocom -b 115200 /dev/ttyUSB0
```

Contributing
------------

MicroPython is an open-source project and welcomes contributions. To be
productive, please be sure to follow the
[Contributors' Guidelines](https://github.com/micropython/micropython/wiki/ContributorGuidelines)
and the [Code Conventions](https://github.com/micropython/micropython/blob/master/CODECONVENTIONS.md).
Note that MicroPython is licenced under the MIT license, and all contributions
should follow this license.