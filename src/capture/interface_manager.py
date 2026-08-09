from scapy.all import IFACES


class InterfaceManager:

    @staticmethod
    def get_interfaces():

        interfaces = []

        ignore = [
            "WAN Miniport",
            "Microsoft Wi-Fi Direct",
            "Bluetooth",
            "VirtualBox",
            "Loopback"
        ]

        for iface in IFACES.values():

            description = iface.description

            if any(x in description for x in ignore):
                continue

            interfaces.append(
                {
                    "name": iface.name,
                    "description": description
                }
            )

        return interfaces