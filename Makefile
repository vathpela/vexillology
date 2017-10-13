SRCS   := luxafor.c
HDRS   := luxafor.h
OBJS   := $(SRCS:.c=.o)

CC     ?= gcc
CFLAGS ?= -O2 -Wall -g
LIBS   ?=

# libusb is required
CFLAGS += $(shell pkg-config --cflags liblzma libudev libusb-1.0)
LIBS   += $(shell pkg-config --libs liblzma libudev libusb-1.0)

all: luxafor

luxafor: $(OBJS)
	$(CC) $(CFLAGS) $< -o $@ $(LIBS)

.c.o:
	$(CC) $(CFLAGS) $< -o $@ -c

clean:
	-rm -f $(OBJS) luxafor
