"""help with address loction"""
from usaddress import parse

def find_field(parsed_result, field):
    """finds field"""
    for component in parsed_result:
        if component[1] == field:
            return component[0]
    return False

def get_street(full_address):
    """full address"""
    parsed = parse(full_address)
    street = find_field(parsed, 'StreetName')
    if street == False:
        return None
    else:
        return street

def get_zip(full_address):
    """gets zip code"""
    parsed = parse(full_address)
    zip = find_field(parsed, 'ZipCode')
    if zip == False:
        return None
    else:
        return zip

def get_state(full_address):
    """finds state"""
    parsed = parse(full_address)
    state = find_field(parsed, 'StateName')
    if state == False:
        return None
    else:
        return state

def get_num(full_address):
    """finds street address"""
    parsed = parse(full_address)
    number = find_field(parsed, 'AddressNumber')
    if number == False:
        return None
    else:
        return number
