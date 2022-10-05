import numpy as np
import pandas as pd
import xlrd as xl
pd.options.mode.chained_assignment = None


def Excel_Cleaner(DF):
    workingdata = DF.copy()
    # This is setting reference points to create a new data frame with only the columns that are needed.
    sampleID = workingdata[workingdata.columns[2]]
    RunID = workingdata[workingdata.columns[3]]
    Segment = workingdata[workingdata.columns[5]]
    ApparentVisc = workingdata[workingdata.columns[11]]
    slope = workingdata[workingdata.columns[12]]
    WRM = workingdata[workingdata.columns[15]]
    Temp = workingdata[workingdata.columns[6]]

    # Here a new data frame is created and all the new columns and rows are imported.
    newdf = pd.DataFrame()
    newdf['SampleID'] = sampleID
    value1 = 'Sample ID'
    newdf = newdf[newdf['SampleID'] != value1]
    newdf['Run_ID'] = RunID
    value2 = 'RunID'
    newdf = newdf[newdf['Run_ID'] != value2]
    newdf['Run_ID'] = newdf['Run_ID'].astype(str)
    newdf['Segment_'] = Segment
    value3 = 'Segment'
    newdf = newdf[newdf['Segment_'] != value3]
    newdf['Apparent Visc'] = ApparentVisc
    value4 = 'Apparent\nVisc, m-Pa-s'
    newdf = newdf[newdf['Apparent Visc'] != value4]
    newdf['Slope'] = slope
    value5 = 'Slope\nR² Fit'
    newdf = newdf[newdf['Slope'] != value5]
    newdf['WRM'] = WRM
    value6 = 'WRM\nR² Fit'
    newdf = newdf[newdf['WRM'] != value6]
    newdf['Temp'] = Temp
    newdf['Temp'] = newdf['Temp'].dropna()
    value = 'Chip\nTemp °C'
    newdf = newdf[newdf['Temp'] != value]

    # These lines clean the data by removing rows that have a slope of 0 or -1.
    newdf = newdf[newdf.Slope != 0]
    newdf = newdf[newdf.Slope != -1]

    # This line further cleans the data by removing the NaN values.
    newdf = newdf.dropna()

    
    
    newdf['Temp'] = newdf['Temp'].astype(float)

    # This rounds the temperature to make sure that runs at different temperatures are counted separately.
    newdf['Temp'] = newdf['Temp'].round(decimals=0)

    # This lines creates a unique name to parse through when doing statistical analysis.
    newdf['Sample_Run'] = newdf['SampleID'].astype(str) + "_run" + newdf['Run_ID'].astype(str) + "_Temp_" + newdf['Temp'].astype(str)
    return newdf

def DF_Stats(newdf):

    # Here dictionaries are created to store the values that are created to store values.
    averages = {}
    stdevs = {}
    runs = {}

    # These loops look for the unique identifier and performs calculations on all the lines but the first.
    for samplerun in newdf['Sample_Run'].unique():
        tempdf = newdf[newdf['Sample_Run'] == samplerun]
        average = tempdf['Apparent Visc'][1:].mean()
        averages[samplerun] = [average]
    for samplerun in newdf['Sample_Run'].unique():
        tempdf = newdf[newdf['Sample_Run'] == samplerun]
        stdev = tempdf['Apparent Visc'][1:].std()
        stdevs[samplerun] = [stdev]
    for samplerun in newdf['Sample_Run'].unique():
        tempdf = newdf[newdf['Sample_Run'] == samplerun]
        run = tempdf['Segment_'][1:].unique()
        run = np.count_nonzero(run)
        runs[samplerun] = [run]
    # These lines create new dataframes that hold the values that are collected in the loops above.
    average_df = pd.DataFrame.from_dict(averages, orient='index', columns=['Average Visc'])
    stdev_df = pd.DataFrame.from_dict(stdevs, orient='index', columns=['Standard Deviation'])
    segment_df = pd.DataFrame.from_dict(runs, orient='index', columns=['Number of Measurements'])

    # These lines round the decimals to the hundredths place.
    average_df = average_df.round(decimals=2)
    stdev_df = stdev_df.round(decimals=2)

    # These line create our final dataframe and saves the values in a new CSV.
    aggregate_df = pd.DataFrame()
    #aggregate_df['Average'] = average_df
    aggregate_df['Average'] = average_df['Average Visc']
    aggregate_df['St.Dev'] = stdev_df
    aggregate_df['# of measurements'] = segment_df
    aggregate_df = aggregate_df.dropna()
    return aggregate_df

def To_CSV(name, aggregate_df):
    aggregate_df.to_csv(name + '_Mean_Stdev_Count' + '.csv')


def Import_csv(path):
    data = pd.read_excel(path)
    #data = xl.open_workbook(path)
    return data





if __name__ == '__main__':
    control =int(input("Please enter the number correspondencing to selection choise \n 1: Perform calulation on File \n 2: Exit \n"))
    while (control == 1):
        path = input("Please enter file path here.\n")
        name = input("What do you want to name the file. \n")
        data = Import_csv(path)
        newdf = Excel_Cleaner(data)
        aggregate_df = DF_Stats(newdf)
        To_CSV(name, aggregate_df)
        print('Done')
        control = int(input("Please enter the number correspondencing to selection choise \n 1: Perform calulation on File \n 2: Exit \n"))
    if (control == 2):
        print("Thank you")

