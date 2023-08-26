import re

a = "Game 1: Ghost Chat"

b, c = ''.join(''.join(a.split('Game ')).split(" Chat")).split(' ')
b = b.strip(':')
print(b, c, sep='\n')