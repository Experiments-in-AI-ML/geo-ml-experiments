import sys
import pandas as pd
pd.options.mode.chained_assignment = None

df = pd.read_csv(sys.argv[1])
df_builder = pd.DataFrame()

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
configs = pd.read_csv(sys.argv[2])

#Extract with config
for i in range(len(configs)):
    config = configs.loc[i,:]
    #print 'Start extract ' + config['name']
    if config['type'] == 'cat':
        df_builder[config['name']] = df.apply(lambda x: get_string_distinct(x, config['name']), axis=1)
    else:
        list_char = letters
        if config['char_list'] == 'withNums':
            list_char = letters_with_numbers
        df_builder[config['name']] = df.apply(lambda x: get_string_char(x, config['name'], config['maxLength'], list_char), axis=1)
        
df_builder.to_csv(sys.argv[3], index=False)

