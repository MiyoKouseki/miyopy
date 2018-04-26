#
#! coding:utf-8
import sys
import subprocess


def get_gpstime(events):
    '''イベントを指定して、そのイベントの期間を返す関数。    

    Return
    ------
    t0 : int
       開始時刻。GPS時刻。
    tlen : int
       期間。秒。
    '''
    try:
        event = sys.argv[1]
        t0, tlen = events[event]
        title = '../event/{0}'.format(event)
        cmd = 'mkdir -p {0}'.format(title)
        ret = subprocess.check_call( cmd.split(" ") )        
    except IndexError as e:
        print type(e),e
        print 'Please add event. ex, python main.py <EQname>'
        print '\n'.join(events.keys())
        print 'exit...'
        exit()
    except KeyError as e:
        print type(e),e
        print '{0} is not in events.'.format(e)
        print 'Please use argvs bellow;'
        print '\n'.join(events.keys())
        exit()
    return t0,tlen,title
