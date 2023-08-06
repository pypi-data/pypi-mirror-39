"""Readers and writers for various formats.

They will be plugged together by autoconv module

"""


import csv
from rofetta.utils import as_asp_value
try:
    import clyngor
except ImportError:
    clyngor = None

SLF_HEADERS = {'lattice', 'objects', 'attributes', 'relation'}


def read_cxt(lines:iter):
    """Yield, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - (object, bools)

    """
    assert next(lines) == 'B\n', 'expects a B'
    assert next(lines) == '\n', 'expects empty line'
    nb_obj, nb_att = map(int, (next(lines), next(lines)))
    yield nb_obj
    yield nb_att
    assert next(lines) == '\n', 'expects empty line'
    objects = tuple(next(lines).strip() for _ in range(nb_obj))
    attributes = tuple(next(lines).strip() for _ in range(nb_att))
    assert nb_obj == len(objects)
    assert nb_att == len(attributes)
    yield objects
    yield attributes
    for object, properties in zip(objects, lines):
        properties = properties.strip()  # remove the line terminator
        assert len(properties) == len(attributes)
        yield object, tuple(char.lower() == 'x' for char in properties)


def write_cxt(reader:callable) -> iter:
    """Yield cxt lines knowing that reader will return, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - booleans relations

    """
    yield 'B\n'
    nb_obj, nb_att = next(reader), next(reader)
    yield str(nb_obj)
    yield str(nb_att) + '\n'
    for object in next(reader):
        yield str(object)
    for attribute in next(reader):
        yield str(attribute)
    for _, props in reader:
        yield ''.join('X' if hold else '.' for hold in props)


def read_slf(lines:str):
    """Yield, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - (object, bools)

    """
    for line in lines:
        if line.startswith('['):
            header = line.strip('[]\n').lower()
            assert header in SLF_HEADERS, header
            if header == 'lattice':
                nb_obj, nb_att = map(int, (next(lines), next(lines)))
                yield nb_obj
                yield nb_att
            elif header == 'objects':
                objects = tuple(next(lines).strip() for _ in range(nb_obj))
                yield objects
            elif header == 'attributes':
                attributes = tuple(next(lines).strip() for _ in range(nb_att))
                yield attributes
            elif header == 'relation':
                for object, line in zip(objects, lines):
                    yield object, tuple(bool(int(attr)) for attr in line.strip().split())
            else:
                raise ValueError("Header {} is not handled".format(header))


def write_slf(reader:callable) -> iter:
    """Yield slf lines knowing that reader will return, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - booleans relations

    """
    nb_obj, nb_att = next(reader), next(reader)
    yield '[Lattice]'
    yield str(nb_obj)
    yield str(nb_att)
    yield '[Objects]'
    for object in next(reader):
        yield str(object)
    yield '[Attributes]'
    for attribute in next(reader):
        yield str(attribute)
    yield '[relation]'
    for _, props in reader:
        yield ' '.join(('1' if hold else '0') for hold in props)


def read_csv(lines:iter):
    """Yield, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - (object, bools)

    """
    reader = csv.reader(lines, delimiter=',')
    header = next(reader)
    attributes = header[1:]
    while attributes[-1] == '':  attributes = attributes[:-1]
    print('READCSV ATTRIBUTES:', len(attributes), attributes)
    objects = tuple(l for l in reader if l)
    yield len(objects)
    yield len(attributes)
    yield tuple(name for name, *_ in objects)
    yield attributes
    for name, *marks in objects:
        marks = tuple(mark not in {' ', ''} for _, mark in zip(attributes, marks))
        print('READCSV MARK:', marks)
        yield name, marks


def write_csv(reader:callable) -> iter:
    """Yield csv lines knowing that reader will provide, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - booleans relations

    """
    nb_obj, nb_att = next(reader), next(reader)
    objects = next(reader)
    attributes = next(reader)
    assert nb_obj == len(objects)
    assert nb_att == len(attributes)
    print('WRITECSV OBJ:', objects)
    print('WRITECSV ATT:', attributes)
    yield ',' + ','.join(attributes)
    for object, holds in reader:
        print(holds)
        print(attributes)
        assert len(holds) == len(attributes)
        yield object + ',' + ','.join('X' if hold else '' for hold in holds)


def read_lp(lines:iter):
    """Yield, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - (object, bools)

    """
    lines = '\n'.join(lines)
    objects, attributes, relations = set(), set(), {}
    for answer in clyngor.solve(inline=lines).by_predicate.careful_parsing.int_not_parsed:
        for args in answer.get('rel', ()):
            if len(args) == 2:
                obj, att = args
                obj = obj[1:-1] if obj[0] == obj[-1] == '"' else obj
                att = att[1:-1] if att[0] == att[-1] == '"' else att
                objects.add(obj)
                attributes.add(att)
                relations.setdefault(obj, set()).add(att)
    objects = tuple(sorted(tuple(objects)))
    attributes = tuple(sorted(tuple(attributes)))
    yield len(objects)
    yield len(attributes)
    yield objects
    yield attributes
    for object in objects:
        hold = relations[object]
        yield object, tuple(attr in hold for attr in attributes)

if not clyngor:  # can't be used without it
    del read_lp


def write_lp(reader:callable) -> iter:
    """Yield ASP lines knowing that reader will provide, in that order:

    - number of objects
    - number of attributes
    - tuple of objects
    - tuple of attributes
    - for each object:
        - booleans relations

    """
    nb_obj, nb_att = next(reader), next(reader)
    objects = next(reader)
    attributes = next(reader)
    for object, holds in reader:
        for attr, hold in zip(attributes, holds):
            if hold:
                yield f'rel({as_asp_value(object)},{as_asp_value(attr)}).'
