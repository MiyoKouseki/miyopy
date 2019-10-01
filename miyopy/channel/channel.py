
def get_seis_chname(start,end,place=['EXV'],axis=['X']):
    '''
    
    '''
    if place == 'all':
        place = ['EXV','EYV','IXV']
    if axis == 'all':
        axis = ['X','Y','Z']

    axis0 = {'X':'WE','Y':'NS','Z':'Z'}
    axis1 = {'X':'X','Y':'Y','Z':'Z'}
    axis2 = {'X':'EW','Y':'NS','Z':'UD'}
    place0 = {'EXV':'EX1','EYV':'EY1','IXV':'IX1'}
    place1 = {'EXV':'EXV','EYV':'EYV','IXV':'IXV'}

    if start > 1232755218:                          # 01/29 00:00 2019 - Today
        place = [place1[p] for p in place]
        axis = [axis2[a] for a in axis]
        fmt = 'K1:PEM-SEIS_{place}_GND_{axis}_IN1_DQ'
        # chname = ['K1:PEM-SEIS_EXV_GND_EW_IN1_DQ',
        #           'K1:PEM-SEIS_EXV_GND_NS_IN1_DQ',
        #           'K1:PEM-SEIS_EXV_GND_UD_IN1_DQ']
    elif 1227441618 < start and start < 1232701218: # 11/28 12:00 2018 - 01/28 09:00 2019
        place = [place1[p] for p in place]
        axis = [axis1[a] for a in axis]
        fmt = 'K1:PEM-{place}_GND_TR120Q_{axis}_IN1_DQ'
        # chname = ['K1:PEM-EXV_GND_TR120Q_X_IN1_DQ',
        #           'K1:PEM-EXV_GND_TR120Q_Y_IN1_DQ',
        #           'K1:PEM-EXV_GND_TR120Q_Z_IN1_DQ']
    elif 1216803618 < start and start < 1227438018: # 07/28 09:00 2018 - 11/28 11:00 2018
        place = [place1[p] for p in place]
        axis = [axis0[a] for a in axis]
        fmt = 'K1:PEM-{place}_SEIS_{axis}_SENSINF_IN1_DQ'
        # chname = ['K1:PEM-EXV_SEIS_WE_SENSINF_IN1_DQ',
        #           'K1:PEM-EXV_SEIS_NS_SENSINF_IN1_DQ',
        #           'K1:PEM-EXV_SEIS_Z_SENSINF_IN1_DQ']
    elif 1203897618 < start and start < 1216800000: # 03/01 00:00 2018 - 07/28 08:00 2018
        place = [place0[p] for p in place]
        axis = [axis0[a] for a in axis]
        fmt = 'K1:PEM-{place}_SEIS_{axis}_SENSINF_IN1_DQ'
        # chname = ['K1:PEM-EX1_SEIS_WE_SENSINF_IN1_DQ',
        #           'K1:PEM-EX1_SEIS_NS_SENSINF_IN1_DQ',
        #           'K1:PEM-EX1_SEIS_Z_SENSINF_IN1_DQ']
    else:
        return None

    chname = [fmt.format(place=p,axis=a) for a in axis for p in place]
    return chname

