#!/bin/bash
modprobe libcomposite
# mouse
cd /sys/kernel/config/usb_gadget/
mkdir -p g2
cd g2
echo 0x1d6b > idVendor # Linux Foundation
echo 0x0104 > idProduct # Multifunction Composite Gadget
echo 0x0100 > bcdDevice # v1.0.0
echo 0x0200 > bcdUSB # USB2
mkdir -p strings/0x409
echo "fedcba9876543210" > strings/0x409/serialnumber
echo "Tobias Girstmair" > strings/0x409/manufacturer
echo "iSticktoit.net USB Device" > strings/0x409/product
mkdir -p configs/c.1/strings/0x409
echo "Config 2: ECM network" > configs/c.1/strings/0x409/configuration
echo 250 > configs/c.1/MaxPower


# Add functions here
mkdir -p functions/hid.usb0
echo 1 > functions/hid.usb0/protocol
echo 1 > functions/hid.usb0/subclass
echo 3 > functions/hid.usb0/report_length
D=$(mktemp)
echo -ne \\x05\\x01 >> "$D"      # USAGE_PAGE (Generic Desktop)
echo -ne \\x09\\x02 >> "$D"      # USAGE (Mouse)
echo -ne \\xA1\\x01 >> "$D"      # COLLECTION (Application)
echo -ne \\x09\\x01 >> "$D"      #  USAGE (Pointer)
echo -ne \\xA1\\x00 >> "$D"      #   COLLECTION (Application)
echo -ne \\x05\\x09 >> "$D"      #    USAGE_PAGE (Button)
echo -ne \\x19\\x01 >> "$D"      #    USAGE_MINIMUM (Button 1)
echo -ne \\x29\\x03 >> "$D"      #    USAGE_MAXIMUM (Button 3)
echo -ne \\x15\\x00 >> "$D"      #    LOGICAL_MINIMUM (0)
echo -ne \\x25\\x01 >> "$D"      #    LOGICAL_MAXIMUM (1)
echo -ne \\x95\\x03 >> "$D"      #    REPORT_COUNT (3)
echo -ne \\x75\\x01 >> "$D"      #    REPORT_SIZE (1)
echo -ne \\x81\\x02 >> "$D"      #    INPUT (Data,Var,Abs)
echo -ne \\x95\\x01 >> "$D"      #    REPORT_COUNT (1)
echo -ne \\x75\\x05 >> "$D"      #    REPORT_SIZE (5)
echo -ne \\x81\\x03 >> "$D"      #    INPUT (Data,Var,Abs)
echo -ne \\x05\\x01 >> "$D"      #    USAGE_PAGE (Generic Desktop)
echo -ne \\x09\\x30 >> "$D"      #    USAGE (X)
echo -ne \\x09\\x31 >> "$D"      #    USAGE (Y)
echo -ne \\x15\\x81 >> "$D"      #    LOGICAL_MINIMUM (-127)
echo -ne \\x25\\x7F >> "$D"      #    LOGICAL_MAXIMUM (127)
echo -ne \\x75\\x08 >> "$D"      #    REPORT_SIZE (8)
echo -ne \\x95\\x02 >> "$D"      #    REPORT_COUNT (2)
echo -ne \\x81\\x06 >> "$D"      #    INPUT (Data,Var,Abs)
echo -ne \\x09\\x38 >> "$D"      #    USAGE (wheel)
echo -ne \\x15\\x81 >> "$D"      #    LOGICAL_MINIMUM (-127)
echo -ne \\x25\\x7F >> "$D"      #    LOGICAL_MAXIMUM (127)
echo -ne \\x75\\x08 >> "$D"      #    REPORT_SIZE (8)
echo -ne \\x95\\x01 >> "$D"      #    REPORT_COUNT (1)
echo -ne \\x81\\x06 >> "$D"      #    INPUT (Data,Var,Rel)
echo -ne \\xC0 >> "$D"           #   END_COLLECTION
echo -ne \\xC0 >> "$D"           # END_COLLECTION
cp "$D" "functions/hid.usb0/report_desc"
ln -s functions/hid.usb0 configs/c.1/

ls /sys/class/udc > UDC