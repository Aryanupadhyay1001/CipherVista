MITRE_MAP = {

    "ICMP Flood": {
        "id": "T1498",
        "name": "Network Denial of Service"
    },

    "UDP Flood": {
        "id": "T1498",
        "name": "Network Denial of Service"
    },

    "SYN Flood": {
        "id": "T1498",
        "name": "Network Denial of Service"
    },

    "Port Scan": {
        "id": "T1046",
        "name": "Network Service Discovery"
    },

    "Brute Force": {
        "id": "T1110",
        "name": "Brute Force"
    },

    "SQL Injection": {
        "id": "T1190",
        "name": "Exploit Public-Facing Application"
    }
}


def get_mitre(threat):

    return MITRE_MAP.get(
        threat,
        {
            "id": "-",
            "name": "Unknown"
        }
    )