import pytest

from ..datatype import GifData

class TestClass(object):
    def test_1(self):
        a = 1
        b = 1
        assert a == b
        

    def test_2(self):
        chname = 'CALC_STRAIN'
        start = '2019 Jan 04 00:00:00 JST'
        end = '2019 Jan 04 00:00:00 JST'
        data = GifData.findfiles(chname,start,end)
        

if __name__ == '__main__':
    pytest.main()        
