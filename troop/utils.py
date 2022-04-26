import configparser

def choose_constant(type):
    config = configparser.ConfigParser()
    with open("arctic_fox_tribes/config.ini") as f:
        config.read_file(f)
        section = type.upper()
        return dict(config.items(section))

def get_value(type, name_of_value):
    return choose_constant(type)[name_of_value]

def count_troop_property(troop, initial_value, level_up_value):
    return float(get_value(troop.type.get_type_display(),
        initial_value))+float((troop.type.level-1)*float
    (get_value(troop.type.get_type_display(), level_up_value)))
