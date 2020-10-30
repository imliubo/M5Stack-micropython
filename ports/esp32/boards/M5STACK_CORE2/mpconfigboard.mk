SDKCONFIG += boards/sdkconfig.base
SDKCONFIG += boards/sdkconfig.spiram

FROZEN_MANIFEST ?= $(BOARD_DIR)/manifest.py

PART_SRC = partitions-16MiB.csv

LV_CFLAGS=-DLV_COLOR_DEPTH=16 -DLV_COLOR_16_SWAP=1