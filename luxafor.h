/*
 * luxafor.h
 * Luxafor USB LED
 */

/* Luxafor device IDs */
#define LUXAFOR_VENDOR_ID 0x04D8
#define LUXAFOR_PRODUCT_ID 0xF372

/* Commands */
enum {
    CMD_COLOR,        /* set one color by code (below) */
    CMD_RGB,          /* set color by RGB value        */
    CMD_FADE,         /* change color with a fade      */
    CMD_STROBE,       /* simulate a strobe light       */
    CMD_WAVE          /* simulate flag waving          */
};

/* CMD_COLOR color codes */
#define LUXAFOR_RED 'R'
#define LUXAFOR_GREEN 'G'
#define LUXAFOR_BLUE 'B'
#define LUXAFOR_CYAN 'C'
#define LUXAFOR_MAGENTA 'M'
#define LUXAFOR_YELLOW 'Y'
#define LUXAFOR_WHITE 'W'
#define LUXAFOR_BLACK 'O'

/* Side codes for CMD_RGB, CMD_FADE, CMD_STROBE, and CMD_WAVE */
#define BOTH_SIDES 0xFF
#define SIDE_A 0x41
#define SIDE_B 0x42

/* Individual LED ID codes for CMD_RGB, CMD_FADE, and CMD_STROBE */
#define LED1 0x01
#define LED2 0x02
#define LED3 0x03
#define LED4 0x04
#define LED5 0x05
#define LED6 0x06

/* Wave types for CMD_WAVE */
enum {
    WAVE_NULL,        /* unused                          */
    WAVE_TYPE_1,      /* half LED 2, LED 3, half LED 4   */
    WAVE_TYPE_2,      /* half LED 1, LED 2-4, half LED 5 */
    WAVE_TYPE_3,      /* WAVE_TYPE_1 w/ blue off         */
    WAVE_TYPE_4,      /* WAVE_TYPE_2 w/ blue off         */
    WAVE_TYPE_5       /* ???                             */
};
