CREATE_TODO = [{
    'field_name': 'bucket__name',
    'type': str,
}, {
    'field_name': 'name',
    'type': str,
}, {
    'field_name': 'bucket__id',
    'type': int,
    'required': False
}]

UPDATE_TODO = [{
    'field_name': 'id',
    'type': int,
}, {
    'field_name': 'name',
    'type': str,
}, {
    'field_name': 'bucket__id',
    'type': int,
    'required': False
}, {
    'field_name': 'bucket__name',
    'type': int
}]
