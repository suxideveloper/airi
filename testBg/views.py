from django.shortcuts import render

# Create your views here.
def kurish( request):

    return render(request, 'testBg/index.html')

class TestClass:

    def __init__(self) -> None:
        self.name = "Suxrob"
        self.age = 21


def test(request):
    test_instance = TestClass()
    context = {
        'key': 'value',
        'key1': 123,
        'talaba': test_instance,
        'key2': False,
        'key3': 12.34,
        'key4': [1, 2, 3, 4, 5],
        'key5': {'a': 1, 'b': 2, 'c': 3},
        'key6': None,
        'key7': (1, 2, 3),
        'key8': {1, 2, 3},
        'key9': b'byte string',
        'key10': bytearray(b'byte array'),
        'key11': frozenset([1, 2, 3]),
        'key12': complex(1, 2),
        'key13': range(5),
        'key14': memoryview(b'hello'),
        'key15': True,
        'key16': lambda x: x * 2,
        'key17': Exception('An error occurred'),
        'key18': iter([1, 2, 3]),
        'key19': slice(1, 5, 2),
        'key20': property(lambda self: 'property value'),
    }
    return render(request, 'testBg/test.html', context)