/*
 * luxafor.c
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <libusb.h>
#include <errno.h>
#include "luxafor.h"

struct libusb_device_handle *get_luxafor(void) {
    int count = 0;
    struct libusb_device_handle *handle = NULL;
    struct libusb_device **devs = NULL;

    count = libusb_get_device_list(NULL, &devs);
    if (count <= 0) {
        fprintf(stderr, "Error enumerating devices\n");
        return NULL;
    }

    handle = libusb_open_device_with_vid_pid(NULL, LUXAFOR_VENDOR_ID, LUXAFOR_PRODUCT_ID);
    libusb_free_device_list(devs, 1);
    return handle;
}

int main(int argc, char **argv) {
    int e = 0;
    struct libusb_device_handle *handle = NULL;

    /* bring up the USB userspace stack */
    errno = 0;
    if (libusb_init(NULL) < 0) {
        fprintf(stderr, "Can't open libusb: %s\n", strerror(errno));
        return EXIT_FAILURE;
    }

    /* Find the device.  Note that a common failure here is permissions. */
    errno = 0;
    if ((handle = get_luxafor()) == NULL) {
        fprintf(stderr, "Unable to find a Luxafor device: %s\n", strerror(errno));
        libusb_exit(NULL);
        return EXIT_FAILURE;
    }

    /* Set the device to unconfigured state. */
    if ((e = libusb_set_configuration(handle, -1)) != 0) {
        fprintf(stderr, "Unable to set device configuration: %s\n", libusb_error_name(e));
        libusb_close(handle);
        libusb_exit(NULL);
        return EXIT_FAILURE;
    }





/* XXX */

/*

0) Parse config files and read in profiles.
       a) /etc/luxafor.conf
       b) ~/.luxaforrc
1) Loop over command line options and process each section.
       a) A function for each option.
       b) A function to exec profiles?
       c) A help/usage screen.
2) Create a help screen and man page.
3) Man page for the config file or put that in main man page?
4) Config file examples.

 */













    /* We're done, clean up. */
    libusb_close(handle);
    libusb_exit(NULL);

    return EXIT_SUCCESS;
}
