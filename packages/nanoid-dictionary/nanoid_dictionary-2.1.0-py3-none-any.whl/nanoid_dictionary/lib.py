import re

lookalikes = '1l0o'
lowercase = 'abcdefghijklmnopqrstuvwxyz'
numbers = '0123456789'
uppercase = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def match_all_unsafe_symbols(symbols):
    return '[%s]' % symbols


def prevent_misreadings(unsafe_chars, string):
    return re.sub(match_all_unsafe_symbols(unsafe_chars), '', string, flags=re.IGNORECASE)


alphabet_std = '_-' + numbers + lowercase + uppercase
human_alphabet = prevent_misreadings(lookalikes, alphabet_std)

if __name__ == '__main__':
    print(lookalikes),
    print(lowercase),
    print(numbers),
    print(uppercase),
    print(match_all_unsafe_symbols(lookalikes))
    print(prevent_misreadings(lookalikes, alphabet_std)),
    print(alphabet_std),
    print(human_alphabet)
