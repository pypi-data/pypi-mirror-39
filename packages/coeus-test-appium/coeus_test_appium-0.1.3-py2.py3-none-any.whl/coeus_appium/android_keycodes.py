class AndroidKeyCodes:
    BACK = 4

    ZERO = 7
    ONE = 8
    TWO = 9
    THREE = 10
    FOUR = 11
    FIVE = 12
    SIX = 13
    SEVEN = 14
    EIGHT = 15
    NINE = 16

    A = 29
    B = 30
    C = 31
    D = 32
    E = 33
    F = 34
    G = 35
    H = 36
    I = 37
    J = 38
    K = 39
    L = 40
    M = 41
    N = 42
    O = 43
    P = 44
    Q = 45
    R = 46
    S = 47
    T = 48
    U = 49
    V = 50
    W = 51
    X = 52
    Y = 53
    Z = 54

    ENTER = 66

    AT = 77

    mappings = {
        '0': ZERO,
        '1': ONE,
        '2': TWO,
        '3': THREE,
        '4': FOUR,
        '5': FIVE,
        '6': SIX,
        '7': SEVEN,
        '8': EIGHT,
        '9': NINE,
        'a': A,
        'b': B,
        'c': C,
        'd': D,
        'e': E,
        'f': F,
        'g': G,
        'h': H,
        'i': I,
        'j': J,
        'k': K,
        'l': L,
        'm': M,
        'n': N,
        'o': O,
        'p': P,
        'q': Q,
        'r': R,
        's': S,
        't': T,
        'u': U,
        'v': V,
        'w': W,
        'x': X,
        'y': Y,
        'z': Z
    }

    @staticmethod
    def get_keycode_for_char(char):
        if char in AndroidKeyCodes.mappings:
            return AndroidKeyCodes.mappings[char]

        raise Exception("Char {0} not found in mappings for keycodes.".format(char))