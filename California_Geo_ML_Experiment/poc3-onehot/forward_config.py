
import pandas as pd
pd.options.mode.chained_assignment = None

#Onehot encopding functions

letters_with_numbers = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
          '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 
               'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def get_code(s, index, letter):
    if pd.isna(s):
        return 0.0
    if len(s) <= index:
        return 0.0
    else:
        if s[index].upper() == letter:
            return 1.0
        else:
            return 0.0



def get_endcode(df_builder, df, column_name, num_char, list_char, reverse = False):
    for i in range(num_char):
        for char in list_char:
            new_column_name = ''
            if i < 10:
                new_column_name = column_name + '_0' + str(i) + '_' + char 
            else:
                new_column_name = column_name + '_' + str(i) + '_' + char
            if reverse:
                df_builder[new_column_name] = df[column_name].apply(lambda x: 0.0 if pd.isna(x) 
                                                                    else get_code(str(x)[-num_char:], i, char))
            else:
                df_builder[new_column_name] = df[column_name].apply(lambda x: get_code(x, i, char))
                    

def get_endcode_distinct(df_builder, df, column_name):
    list_distinct = (df[column_name].value_counts()).index.tolist()
    for value in list_distinct:
        new_column_name = column_name + ':' + str(value)
        df_builder[new_column_name] = df[column_name].apply(lambda x: 1.0 if x==value else 0.0)

#Read data from source
df = pd.read_csv('input_v2.csv')

#get 10000 rows to test
#df = df[:10000]
df = df.drop(columns=['system_id', 'county']).drop_duplicates()

#make builder to extract data
df_builder = pd.DataFrame()

#Addr_number: Parse directly as a DOUBLE
df_builder['addr_number'] = df.addr_number.apply(lambda x: float(x) if str(x).isdigit() else None)

#Addr_drctn: split to two fields: YDir=North(1.0)/South(-1.0), XDir=East(1.0)/West(-1.0)
df_builder.loc[:, 'addr_drctn_XDir'] = df.addr_drctn.apply(lambda x: 1.0 if x == 'E' else (-1.0 if x == 'W' else 0.0))
df_builder.loc[:, 'addr_drctn_YDir'] = df.addr_drctn.apply(lambda x: 1.0 if x == 'N' else (-1.0 if x == 'S' else 0.0))

#Read config from file
configs = pd.read_csv('config.csv')

#Extract with config
for i in range(len(configs)):
    config = configs.loc[i,:]
    #print 'Start extract ' + config['name']
    if config.type == 1:
        get_endcode_distinct(df_builder, df, config['name'])
    else:
        list_char = letters
        if config.char_list == 1:
            list_char = letters_with_numbers
        last_character = False
        if config.last_character == 1:
            last_character = True
        get_endcode(df_builder, df, config['name'], config.num, list_char, last_character)

#Mapcol: convert the letter to its ASCII value
df_builder['mapcol'] = df.mapcol.apply(lambda x: 0 if pd.isna(x) else ord(x))

#Mappage: Parse directly as a DOUBLE
#Maprow: Parse directly as a DOUBLE
df_builder['mappage'] = df.mappage.apply(lambda x: float(x) if str(x).isdigit() else None)
df_builder['maprow'] = df.maprow.apply(lambda x: float(x) if str(x).isdigit() else None)

# Finish! Print to csv
df_builder.to_csv('forward_face.csv', index=False)

