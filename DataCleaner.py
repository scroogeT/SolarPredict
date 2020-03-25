import pandas as pd
# from pandas import ExcelWriter
# from pandas import ExcelFile

raw_files = [
    {
        'file_name': 'Type1 Data.xlsx',
        'sheet_columns': [
            {
                'sheet_name': 'Type1 March_18',
                'cols': 'A,B,D,E,H,IN,IO,IR,IW,IX'
            },
            {
                'sheet_name': 'Type1 April_18',
                'cols': 'A,B,D,E,H,IU,IV,IR,IW,IX'
            },
            {
                'sheet_name': 'Type1 May_18',
                'cols': 'A,B,D,E,H,IN,IO,IR,IW,IX'
            },
            {
                'sheet_name': 'Type1 June_18',
                'cols': 'A,B,D,E,H,IU,IV,IY,IW,IX'
            },
            {
                'sheet_name': 'Type1 July_18',
                'cols': 'A,B,D,E,H,IN,IO,IR,IW,IX'
            },
            {
                'sheet_name': 'Type1 Aug_18',
                'cols': 'A,B,Q,R,U,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type1 Sep_18',
                'cols': 'A,B,Q,R,U,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type1 Nov_18',
                'cols': 'A,B,D,E,H,IN,IO,IR,IW,IX'
            },
        ]
    },
    {
        'file_name': 'Type2 Data.xlsx',
        'sheet_columns': [
            {
                'sheet_name': 'Type 2 March_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JI,JK'
            },
            {
                'sheet_name': 'Type 2 April_18',
                'cols': 'A,B,D,E,H,JH,JI,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 May_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 June_18',
                'cols': 'A,B,D,E,H,JH,JI,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 July_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 August_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 September_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 2 November_18',
                'cols': 'A,B,D,E,H,JA,JB,JE,JJ,JK'
            },
        ]
    },
    {
        'file_name': 'Type 4 Data.xlsx',
        'sheet_columns': [
            {
                'sheet_name': 'Type 4 March_18',
                'cols': 'B,C,GR,GS,GV,JI,JJ,JM,JK,JL'
            },
            {
                'sheet_name': 'Type 4 April_18',
                'cols': 'A,B,GQ,GR,GU,JA,JI,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 May_18',
                'cols': 'A,B,GQ,GR,GU,JH,JI,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 June_18',
                'cols': 'A,B,GQ,GR,GU,JA,JB,JE,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 July_18',
                'cols': 'A,B,GQ,GR,GU,JH,JI,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 August_18',
                'cols': 'A,B,GQ,GR,GU,JA,JB,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 September_18',
                'cols': 'A,B,GQ,GR,GU,JH,JI,JL,JJ,JK'
            },
            {
                'sheet_name': 'Type 4 December_18',
                'cols': 'A,B,GQ,GR,GU,JH,JI,JL,JJ,JK'
            },
        ]
    }
]
my_columns = ['Date', 'Time', 'SolIrr', 'DaySumIrr', 'TmpMod',
              'TmpAmb', 'Wind', 'Pac', 'Pdc', 'DaySum']

# Empty dataframe to contain all Readings
# master_readings = pd.DataFrame()
type_readings = pd.DataFrame()

for file in raw_files:
    for sheet in file['sheet_columns']:
        df = pd.read_excel(file['file_name'],
                           sheet_name=sheet['sheet_name'],
                           header=1,
                           usecols=sheet['cols'])
        # Clean-up column names
        df.columns = df.columns.str.replace('Pdc1', 'Pdc')
        df.columns = df.columns.str.replace('.1', '')
        df.columns = df.columns.str.replace('#', '')
        df.columns = df.columns.str.replace('5', '')

        print("Excel Sheet Columns: {} - {}".format(file['file_name'], sheet['sheet_name']))
        print(df.head())
        # re-order columns to be the same everywhere
        df = df[my_columns]

        print(df.head())

        if type_readings.empty:
            #master_readings = df.copy(deep=True)
            type_readings = df.copy(deep=True)
            print('First Run !!')
        else:
            #master_readings = master_readings.append(df, ignore_index=True, sort=True)
            type_readings = type_readings.append(df, ignore_index=True, sort=True)

        print('Global Readings: {}'.format(type_readings.shape))
        print(type_readings.tail())

    # Save Readings in one file
    type_readings.to_csv(path_or_buf='{}_flattened.csv'.format(file['file_name']), index=False)
    print("Excel File Columns: {}".format(file['file_name']))
    print(type_readings.head())
    # Clear readings for this type
    type_readings = type_readings.iloc[0:0]

#master_readings.to_csv(path_or_buf='flattened_data.csv', index=False)
#print("Flat data Columns")
#print(type_readings.head())
