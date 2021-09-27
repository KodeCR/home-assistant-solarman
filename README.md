# Home Assistant custom component for SolarMAN (IGEN Tech) solar inverter logger
Uses a local push connection by setting up a server listing for packages from the logger, parsing the data, and updating the relevant sensors.

Tested with a Trannergy solar inverter, but probably works with any inverter using a SolarMAN (IGEN Tech) logger.

## Setup
Configure with your Home Assistant machine's hostname or ip address and a port number of your choosing.
Browse to the (local) webpage of the solar inverter logger and point one of the entries under "Advanced" -> "Remote server" to the Home Assistant machine's hostname or ip address and selected port.


## Acknowlegements
Thanks to @rhmswink for figuring out how to parse the incoming data, as found here: https://github.com/rhmswink/omnik_monitor.
