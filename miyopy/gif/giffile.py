#
#! coding:utf-8

from ..time import to_JSTdatetime

def path_to_file(gps,prefix='/Users/miyo/Dropbox/KagraData/gif/'):
    '''ファイルがある場所を調べる関数
    
    Parameter
    ---------
    gpstime: int
    開始時刻。GPS時間で指定。
    tlen: int
    長さ。秒で指定。
    chname:str
    チャンネル名。fname_fmtで指定されている名前を指定。
    prefix: str
    GIFデータが保存されているローカルディレクトリ。
    '''
    
    assert (gps%60)==18,'{0}%60={1}'.format(gps,gps%60)
    date = to_JSTdatetime(gps)
    date_str = date.strftime('%Y/%m/%d/%H/%y%m%d%H%M')
    try:
        self.fname = fname_fmt[self.chname].replace('<filename>',date_str)
        path_to_file = prefix[:-1] + self.fname    
    except KeyError as e:
        print type(e),e
        for key in fname_fmt.keys():
            print key
        exit()
    return path_to_file            
