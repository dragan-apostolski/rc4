"""
Автор: Драган Апостолски

Користење:

За генерирање на клуч од b бајти и иницијален клуч k, се повикува функцијата generate_key_stream(k, b). k мора да биде
во bytes објект. Пример:

    init_key = b'0102030405'
    key_len = 40
    key = generate_key_stream(init_key, key_len)

По генерирање на клуч, може да се шифрира текст со истиот клуч. Текст што ќе се шифрира исто така мора да биде во bytes
објект. За шифрирање на текст plain_text со клуч key, се повикува функцијата encrypt(plain_text, key). Пример:

    plain_text = b'00000000000000000000000000000000'
    cipher_text = encrypt(plain_text, key)

Шифрираниот текст во cipher_text е исто така во форма на bytes објект. Истиот текст, со истиот клуч може да се дешифрира
со повик до функцијата decrypt на следниов начин:

    original_text = decrypt(cipher_text, key)
"""


class StateVector:
    """Оваа класа го опишува векторот на состојба - s, кој во секое време содржи пермутација на сите 8-битни броеви во
    опсегот [0 - 255]"""

    def __init__(self, initial_key):
        """Во конструкторот на векторот на состојба се пополнува идентичната пермутација на s, се креира помошен вектор
        t - ги содржи вредностите на иницијалниот клуч, и се прави првичната пермутација на s, која зависи од
        вредностите на иницијалниот клуч

        :param initial_key низа од бајти со вредности на почетниот клуч
        """
        self.key_length = len(initial_key)
        self.s = list(range(256))  # identity permutation
        self.t = [initial_key[i % self.key_length] for i in range(256)]
        self.__permutate_state_vector__()

    def __permutate_state_vector__(self):
        """Во оваа функција се прави првичната пермутација на векторот на состојба - s. Бидејќи единствената операција е
        swap, резултатот е повторно пермутација.
        """
        j = 0
        for i in range(256):
            j = (j + self.s[i] + self.t[i]) % 256
            self.s[i], self.s[j] = self.s[j], self.s[i]

    def swap(self, i, j):
        """Ги заменува вредностите од s на позициите i и j"""
        self.s[i], self.s[j] = self.s[j], self.s[i]

    def __getitem__(self, item):
        return self.s[item]


def generate_key_stream(initial_key, length):
    """Оваа функција генерира клуч со должина length, врз основа на иницијалниот клуч initial_key. Прво се иницијализира
    објект од класата StateVector, кој што ќе биде енкапсулација на векторот на состојба s. Вредностите (бајтите) за
    клучот се случајно избрани вредности од векторот на состојба, а по секоја избрана вредност за клучот се врши нова
    пермутација на s со повик на функцијата swap

    :param initial_key bytes објект кој ги содржи бајтите на иницијалниот клуч
    :param length должина на клучот кој ќе биде вратен
    :return низа со должина length, која ги содржи вредностите на клучот во форма на броеви од опсегот [0 - 255]
    """
    state_vector = StateVector(initial_key)
    key = []
    i = j = 0
    for k in range(length):
        i = (i + 1) % 256
        j = (j + state_vector[i]) % 256
        state_vector.swap(i, j)
        key.append(state_vector[(state_vector[i] + state_vector[j]) % 256])
    return key


def encrypt(plain_text, key):
    """Примитивата encrypt служи за енкриптирање на текстот даден во plain_text со клуч key.
     Клучот треба да биде генериран со помош на функцијата generate_key_stream.

     :param plain_text текстот (во bytes објект) што треба да биде шифриран
     :param key клучот кој ќе се употреби во шифрирањето
     :return bytes објект кој го содржи шифрираниот текст
     """
    key_length = len(key)
    ciphered_text = bytearray(plain_text)
    for i in range(len(plain_text)):
        enc = ((plain_text[i] + key[i % key_length]) % 256)
        ciphered_text[i] = enc
    return bytes(ciphered_text)


def decrypt(ciphered_text, key):
    """Примитивата decrypt служи за дешифрирање на шифрираниот текст ciphered_text со клуч key.

    :param ciphered_text шифрираниот текст во форма на bytes објект
    :param key клучот за дешифрирање
    :return дешифриран текст во форма на bytes објект
    """
    original = bytearray(ciphered_text)
    key_len = len(key)
    for i in range(len(ciphered_text)):
        dec = ((ciphered_text[i] - key[i % key_len]) % 256)
        original[i] = dec
    return bytes(original)