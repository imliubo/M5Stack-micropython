SDKCONFIG += boards/sdkconfig.base
SDKCONFIG += boards/sdkconfig.spiram

FROZEN_MANIFEST ?= $(BOARD_DIR)/manifest.py

PART_SRC = partitions-16MiB.csv

# LVGL CONFIG
CONFIG_LVGL_ENABLE=y