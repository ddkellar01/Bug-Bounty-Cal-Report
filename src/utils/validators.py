import re

def validate_cvss_vector(vector: str) -> bool:
    pattern = r"^CVSS:3\.1/AV:[NALP]/AC:[LH]/PR:[NLH]/UI:[NR]/S:[UC]/C:[HLN]/I:[HLN]/A:[HLN]$"
    return bool(re.match(pattern, vector))

def validate_eth_address(address: str) -> bool:
    pattern = r"^0x[a-fA-F0-9]{40}$"
    return bool(re.match(pattern, address))
