from serviceworker import leftpad

print leftpad.left_pad('foo', 5)

print leftpad.left_pad('foobar', 6)

print leftpad.left_pad('toolong', 2)

print leftpad.left_pad(1, 2, '0')

print leftpad.left_pad(17, 5, 0)
