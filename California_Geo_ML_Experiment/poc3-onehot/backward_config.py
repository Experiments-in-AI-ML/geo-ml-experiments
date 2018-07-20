import pandas as pd
pd.options.mode.chained_assignment = None

df = pd.read_csv('forward_face.csv')
df_builder = pd.DataFrame()

df_builder['addr_number'] = (df.addr_number.apply(lambda x: int(x) if pd.notna(x) else x)).astype('object')

def get_addr_drctn(X):
    if (X['addr_drctn_XDir'] == 1.0):
        return 'E'
    if (X['addr_drctn_XDir'] == -1.0):
        return 'W'
    if (X['addr_drctn_YDir'] == 1.0):
        return 'N'
    if (X['addr_drctn_YDir'] == -1.0):
        return 'S'
    return ''

df_builder['addr_drctn'] = df[['addr_drctn_XDir', 'addr_drctn_YDir']].apply(lambda x: get_addr_drctn(x), axis=1)

def get_string_char(X, column_name, num_char, list_char):
    ret = ''
    for i in range(num_char):
        miss = True
        for char in list_char:
            new_column_name = ''
            if i < 10:
                new_column_name = column_name + '_0' + str(i) + '_' + char 
            else:
                new_column_name = column_name + '_' + str(i) + '_' + char
            if X[new_column_name] == 1.0:
                ret = ret + char
                miss = False
                break
        if miss:
            ret = ret + ' '
    return ret

letters_with_numbers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def get_string_distinct(X, column_name):
    list_index = X.index.tolist()
    for new_name in list_index:
        if ((column_name + ':') in new_name) and (X[new_name] == 1.0):
            return new_name.split(':')[-1]

#Read config from file
configs = pd.read_csv('config.csv')

#Extract with config
for i in range(len(configs)):
    config = configs.loc[i,:]
    #print 'Start extract ' + config['name']
    if config.type == 1:
        df_builder[config['name']] = df.apply(lambda x: get_string_distinct(x, config['name']), axis=1)
    else:
        list_char = letters
        if config.char_list == 1:
            list_char = letters_with_numbers
        df_builder[config['name']] = df.apply(lambda x: get_string_char(x, config['name'], config.num, list_char), axis=1)
        
df_builder['mapcol'] = df.mapcol.apply(lambda x: chr(x))

df_builder['mappage'] = (df.mappage.apply(lambda x: int(x) if pd.notna(x) else x)).astype('object')
df_builder['maprow'] = (df.maprow.apply(lambda x: int(x) if pd.notna(x) else x)).astype('object')

df_builder.to_csv('reverse.csv', index=False)


