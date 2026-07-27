# JOB-09 v0.3.2 Runtime Test Request

Please test only the existing-property computer path:

1. Disable older JOB-09 ZIPs and enable v0.3.2.
2. Reload the map or Career.
3. Use the normal Belasco service-property computer.
4. Connect the saved tow yard to the property.
5. Reopen the computer and confirm Tow Yard Management appears.
6. Confirm the vehicle uses `servicestationGarage`, remains owned with the same inventory ID, and is not offered a $5,000 same-property delivery with a 120-second delay.
7. Rename the tow yard and confirm the custom name persists.

Stop and preserve logs if a vehicle disappears, duplicates, loses ownership, changes inventory ID, or remains at an artificial `redfox_towshop_*` location after linking.
