#pragma once
#include <initguid.h>

/**
 * PhoneDock Common Definitions
 * Shared between the WinUI App and the Indirect Display Driver.
 */

// {789A5B3C-2D1E-4F0A-9B8C-7D6E5F4A3B2C}
DEFINE_GUID(GUID_DEVINTERFACE_PHONEDOCK_DISPLAY,
    0x789a5b3c, 0x2d1e, 0x4f0a, 0x9b, 0x8c, 0x7d, 0x6e, 0x5f, 0x4a, 0x3b, 0x2c);

// IOCTL for communicating with the virtual display driver
#define IOCTL_PHONEDOCK_UPDATE_MONITOR_CONFIG \
    CTL_CODE(FILE_DEVICE_UNKNOWN, 0x801, METHOD_BUFFERED, FILE_ANY_ACCESS)

#define IOCTL_PHONEDOCK_GET_FRAME \
    CTL_CODE(FILE_DEVICE_UNKNOWN, 0x802, METHOD_BUFFERED, FILE_ANY_ACCESS)

/**
 * PDP Protocol Version
 */
#define PDP_VERSION_MAJOR 0
#define PDP_VERSION_MINOR 1

/**
 * Standard PDP Port (if discovery fails)
 */
#define PDP_DEFAULT_PORT 45124
