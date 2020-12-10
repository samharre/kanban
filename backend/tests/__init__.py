def check_status_code_400(test, status_code, data):
    test.assertEqual(status_code, 400)
    test.assertFalse(data['success'])
    test.assertEqual(data['message'].lower(), 'bad request')


def check_status_code_404(test, status_code, data):
    test.assertEqual(status_code, 404)
    test.assertFalse(data['success'])
    test.assertEqual(data['message'].lower(), 'resource not found')


def check_status_code_405(test, status_code, data):
    test.assertEqual(status_code, 405)
    test.assertFalse(data['success'])
    test.assertEqual(data['message'].lower(), 'method not allowed')


def check_status_code_409(test, status_code, data):
    test.assertEqual(status_code, 409)
    test.assertFalse(data['success'])
    test.assertEqual(data['message'].lower(), 'duplicated found')


def check_status_code_422(test, status_code, data):
    test.assertEqual(status_code, 422)
    test.assertFalse(data['success'])
    test.assertEqual(data['message'].lower(), 'unprocessable')
