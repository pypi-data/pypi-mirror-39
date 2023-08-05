'''

'''

def table2docs0(df, keys, columns = [], modifiers = {}):
    if not columns:
        columns = keys
    modifiers = {
                  key : ( lambda x, modify=modifiers[key] : modify(x) ) if key in modifiers.keys() 
                        else ( lambda x : x ) for key in keys 
                }
    return [
             { key : modifiers[key](value) for key, value in zip(keys, values) }

             for values in zip(*[df.to_dict('list')[column] for column in columns])
           ]

def table2docs(df, keys=None, columns = [], modifiers = {}):

    def parse_column(column):
        if isinstance(column, list):
            return column
        return [column]

    def get_column_values(df_dict, column_list):
        if len(column_list) == 1:
            return df_dict[column_list[0]]
        return zip(*[df_dict[column] for column in column_list])

    if keys is None:
        keys = list(df.columns)

    if not columns:
        columns = keys
    columns = [ parse_column(column) for column in columns ]
    modifiers = {
                  key : ( lambda x, modify=modifiers[key] : modify(x) ) if key in modifiers.keys() 
                        else ( lambda x : x ) for key in keys
                }
    df_dict = df.to_dict('list')
    return [
             { key : modifiers[key](value) for key, value in zip(keys, values) }

             for values in zip( *[get_column_values(df_dict, column) for column in columns] )
           ]
