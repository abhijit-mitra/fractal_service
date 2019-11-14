CREATE_TODO = [{
    'field_name': 'bucketName',
    'type': str,
}, {
    'field_name': 'name',
    'type': str,
}, {
    'field_name': 'done',
    'type': bool,
}, {
    'field_name': 'bucketId',
    'type': int,
    'required': False,
    'blank': (True,)
}]

UPDATE_TODO = [{
    'field_name': 'name',
    'type': str,
}, {
    'field_name': 'done',
    'type': bool,
    'required': False
}, {
    'field_name': 'bucketId',
    'type': int,
    'required': False,
    'blank': (True,)
}, {
    'field_name': 'bucketName',
    'type': str
}]
