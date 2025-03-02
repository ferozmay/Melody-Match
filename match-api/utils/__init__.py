def parse_id(identifier):
    try:
        return int(identifier)
    except ValueError:
        return str(identifier)
