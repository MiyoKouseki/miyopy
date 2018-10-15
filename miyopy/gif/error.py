
class NoChannelNameError(Exception):
    def __init__(self,chname):
        self.chname = chname
        keys = [key for key in fname_fmt.keys() if self.chname in key]
        if len(keys)==0:
            keys = fname_fmt.keys()
        self.text = '\n Is it in these channel name?'
        keys.sort(reverse=False)
        for key in keys:
            self.text += '\n- '+key
            
    def __str__(self):
        return "Invalid channel name '{0};{1}'".format(self.chname,self.text)
