
from . import reader


reader_dic = {
    'gif':reader.gif,
    'kagra':reader.kagra,
    }

def get_reader(fmt,obj):
    print fmt
    return reader_dic[fmt]
