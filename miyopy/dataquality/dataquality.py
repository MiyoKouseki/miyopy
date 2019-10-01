
persons_data = [(1211817600,1211821696,'exv_seis',0,0,0,'NOT_CHECKED'),
                (1211821696,1211825792,'exv_seis',0,0,0,'NOT_CHECKED')]

import sqlite3
import numpy as np

''' DQflag database format

Channel(
    startgps unique, 
    endgps unique, 
    flag bit)

BitFlag:
    0 bit : "CHECK_BIT", If checked, bit rise to 1. Default bit drop to 0.
    1 bit : "LACK_OF_FILE", If lack, bit rise to 1. Default bit drop to 0.
    2 bit : "LACK_OF_DATA", If lack, bit rise to 1. Default bit drop to 0.
    3 bit : "GLITCH", If existing, bit rise to 1. Default bit drop to 0.
'''

CHECK_BIT    = 0b1    # 1
LACK_OF_FILE = 0b10   # 2
LACK_OF_DATA = 0b100  # 4
GLITCH       = 0b1000 # 8


class DataQuality(object):
    def __init__(self,dbname):
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()

    def check_db(self):
        with DataQuality('./dataquality/dqflag.db') as db:
            total      = db.ask('select startgps,endgps from EXV_SEIS')
            available  = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0')
            lackoffile = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=2')
            lackofdata = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=4')
            glitch     = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=8')
            use        = db.ask('select startgps,endgps from EXV_SEIS WHERE flag=0 ' +
                                'and startgps>={0} and endgps<={1}'.format(args.start,
                                                                           args.end))

        bad = len(total)-len(available)-len(lackoffile)-len(lackofdata)-len(glitch)
        if bad!=0:
            raise ValueError('SegmentList Error: Missmatch the number of segments.')
        
    def __enter__(self):
        print("Hello!")
        return self
    
    def __exit__(self, ex_type, ex_value, trace):
        self.conn.commit()
        self.conn.close()
        print('Close. Bye!')
        
    def bals(self):
        '''Initialize only TEST table
        '''
        # Find all tables and delete completely       
        ans = self.ask("select name from sqlite_master where type='table'")
        tables = list(np.array(ans).flatten())
        for name in tables:
            self.cursor.execute('drop table {0}'.format(name))
        self.cursor.execute('vacuum')
        # Make TEST table
        self.add_table('TEST')
        
    def add_table(self,name='TEST'):
        '''
        '''
        # Make new table
        self.cursor.execute('create table {0}('.format(name)+
                            'startgps unique, endgps unique, flag bit)')        
        # Insert TEST value        
        segments = zip(range(1211817600     ,1245372032+1,4096),
                       range(1211817600+4096,1245372032+1,4096))
        data = [(start,end,0) for start,end in segments]
        self.cursor.executemany("insert into {0} values (?,?,?)".format(name), data)

        
    def update_flag(self,name,start,end,flag,**kwargs):
        ''' Update flag
        '''
        override = kwargs.pop('override',False)
        off = kwargs.pop('off',False)
        check = kwargs.pop('check',False)
        # Check GPS time
        ans = self.ask('select startgps,endgps from {0} '\
                       'where startgps={1}'.format(name,start))            
        print ans[0]
        print (start,end)
        if not (start,end) == ans[0]:
            raise ValueError('({0},{1}) is wrong.'.format(start,end))
        
        # Read current flag
        now = self.get_flag(name,start,end,**kwargs)
        if override:
            now = flag
        else:
            if off:
                now -= now & flag # OFF
            else:
                now |= flag # ON
        if check:
            now |= CHECK_BIT
            
        # Update
        cmd = 'update {0} set flag = {1} where '.format(name,now) +\
              'startgps = {0}'.format(start,end)
        self.cursor.execute(cmd)
        
        
    def get_flag(self,name,start,end,**kwargs):
        '''
        '''
        ans = self.ask('select flag from {0} where startgps={1} '\
                       'and endgps={2}'.format(name,start,end))
        flag = ans[0][0]
        return flag

        
    def to_csv(self,rows,fname='tmp'):
        ''' Write down all data to csv file.
        '''
        import csv
        with open("{0}.csv".format(fname), "w") as f:
            writer = csv.writer(f)
            for row in rows:                
                writer.writerow(row)

    def to_txt(self,rows,fname='tmp'):
        ''' Write down all data to csv file.
        '''
        import csv
        with open("{0}.txt".format(fname), "w") as f:            
            for row in rows:
                print row
                f.write('{0} {1} {2}\n'.format(*row))
                

    def table_to_csv(self,name='TEST'):
        ''' Write down all data to csv file.
        '''
        import csv
        rows = self.ask('select * from {0}'.format(name))
        with open("DQflag_{0}.csv".format(name), "w") as f:
            writer = csv.writer(f)
            writer.writerow(['STARTGPSTIME','ENDGPSTIME','FLAG'])
            for row in rows:                
                writer.writerow(row)
                
                
    def ask(self,cmd):
        '''
        '''
        self.cursor.execute(cmd)        
        return self.cursor.fetchall()


def danger():
    #data = np.loadtxt('total.txt',dtype=np.int)    
    #data = np.loadtxt('nodata.txt',dtype=np.int)
    #data = np.loadtxt('lackofdata.txt',dtype=np.int)
    #data = np.loadtxt('glitch.txt',dtype=np.int)
    # with DataQuality() as db:
    #     for _,start,end,value in data:
    #         #db.update_flag('EXV_SEIS',start,end,0,override=True)            
    #         #db.update_flag('EXV_SEIS',start,end,LACK_OF_FILE)
    #         db.update_flag('EXV_SEIS',start,end,GLITCH)
    #     z = len(db.ask('select * from EXV_SEIS'))
    #     a = len(db.ask('select * from EXV_SEIS WHERE flag=0'))
    #     b = len(db.ask('select * from EXV_SEIS WHERE flag=2'))
    #     c = len(db.ask('select * from EXV_SEIS WHERE flag=4'))
    #     d = len(db.ask('select * from EXV_SEIS WHERE flag=8'))
    #     print z-a-b-c-d        
    pass





if __name__ == '__main__':
    #segments = np.loadtxt('newfound_lackofdata.txt',dtype=np.int)
    #print data
    #exit()
    with DataQuality() as db:
        #rows = db.ask('select * from EXV_SEIS WHERE flag=4')
        #for start,end in segments:
        #    db.update_flag('EXV_SEIS',start,end,LACK_OF_DATA)
        print db.ask('select startgps,endgps,flag from EXV_SEIS WHERE startgps=1213312640')
        #db.to_txt(rows)
