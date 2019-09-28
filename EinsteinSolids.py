import math;
from decimal import Decimal;
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt;
from prettytable import PrettyTable

class MultiplicityData:
    def __new__(cls, *args, **kwargs):
        print( "Creating Instance");
        instance = super(MultiplicityData, cls).__new__(cls, *args, **kwargs);
        return instance;

    def __init__(self):
        self.MultiplicityOfA_arr = []
        self.MultiplicityOfB_arr = []
        self.EnergyInA_arr = []
        self.EnergyInB_arr = []
        self.TotalMultiplicity_arr = []

    MultiplicityOfA_arr = []
    MultiplicityOfB_arr = []
    EnergyInA_arr = []
    EnergyInB_arr = []
    TotalMultiplicity_arr = []

def GetEnergyPermutations(count):
    permutations = [i for i in range(count+1)];
    return permutations;

def GetMultiplicityForOneEnergyState(qa, qb, Na, Nb):
    MultiplicityOfA = (math.factorial(qa + Na -1)/(math.factorial(qa)*math.factorial(Na - 1)));
    MultiplicityOfB = (math.factorial(qb + Nb -1)/(math.factorial(qb)*math.factorial(Nb - 1)));
    MultiplicityTotal = MultiplicityOfA * MultiplicityOfB;
    return (MultiplicityOfA, MultiplicityOfB, MultiplicityTotal);

def GetTotalMultiplicityOfAllStates(MultiplicityTotal):
    return sum(MultiplicityTotal);

def ConvertToScientificNotation(number):
    return '%.2E' % Decimal(number);

def GetMultiplicityData(qArr, Na, Nb):
    mData = MultiplicityData();
    SolidA_TotalMuliplicityVsEnergy = [];
    MultiplicityOfA = [];
    MultiplicityOfB = [];
    EnergyInA = [];
    EnergyInB = [];
    for state in qArr:
        energyInSolidA = state;
        energyInSolidB = len(qArr) - 1 - state;
        data = GetMultiplicityForOneEnergyState(energyInSolidA, energyInSolidB, Na, Nb);
        mData.MultiplicityOfA_arr.append(data[0]);
        mData.MultiplicityOfB_arr.append(data[1]);
        mData.EnergyInA_arr.append(energyInSolidA);
        mData.EnergyInB_arr.append(energyInSolidB);
        mData.TotalMultiplicity_arr.append(data[2]);
    
    return mData;

def DisplayBarChart(mData, plotName):
    x_data = [];
    y_data = [];
    xAxisIsToWide = len(mData.EnergyInA_arr) > 75;
    if (xAxisIsToWide):
        x_data = mData.EnergyInA_arr[90:171];
        y_data = mData.TotalMultiplicity_arr[90:171];
    else:
        x_data = mData.EnergyInA_arr;
        y_data = mData.TotalMultiplicity_arr;

    y_pos = np.arange(len(x_data))
    plt.bar(y_pos, y_data, align='center', alpha=0.5);
    if (xAxisIsToWide):
        plt.xticks(y_pos, x_data, rotation=70);
    else:
        plt.xticks(y_pos, x_data);
    plt.ylabel('Multiplicity');
    plt.xlabel('Energy (AU)');
    plt.title('Problem ' + plotName + ' Solid A Total Multiplicity vs Energy');

    manager = plt.get_current_fig_manager();
    manager.resize(*manager.window.maxsize());

    plt.show();
    #plt.savefig(plotName + '_BarChart.png', bbox_inches='tight', pad_inches=0);

def DisplayTable(mData, plotName):
    formatted_MultiplicityOfA_arr = GetDataInScientificNotation(mData.MultiplicityOfA_arr);
    formatted_MultiplicityOfB_arr = GetDataInScientificNotation(mData.MultiplicityOfB_arr);
    formatted_TotalMultiplicity_arr = GetDataInScientificNotation(mData.TotalMultiplicity_arr);
    t = PrettyTable([])
    t.add_column('Energy in Solid A', mData.EnergyInA_arr);
    t.add_column('Multiplicity Of Solid A', formatted_MultiplicityOfA_arr);
    t.add_column('Energy in Solid B', mData.EnergyInB_arr);
    t.add_column('Multiplicity Of Solid A', formatted_MultiplicityOfB_arr);
    t.add_column('Total Multiplicity', formatted_TotalMultiplicity_arr);

    t.align["Energy in Solid A"] = "r";
    t.align["Multiplicity Of Solid A"] = "l";
    t.align["Energy in Solid A"] = "r";
    t.align["Multiplicity Of Solid A"] = "l";
    t.align["Total Multiplicity"] = "l";
    SaveTableToDisk(t, plotName);
    #print(tableAsString)

def GetDataInScientificNotation(data):
    formattedData = [];
    for value in data:
        formattedData.append('{:.2e}'.format(int(value)));
    return formattedData;

def SaveTableToDisk(table, plotName):
    f = open(plotName + '_table.txt', 'w');
    f.write(str(table));
    f.close();

def ListStateAndProbabilities(mData, problemNumber):
    maxState = max(mData.TotalMultiplicity_arr);
    minState = min(mData.TotalMultiplicity_arr);
    TotalMultiplicity = sum(mData.TotalMultiplicity_arr);
    maxProbability = (maxState/TotalMultiplicity)*100;
    minProbability = (minState/TotalMultiplicity)*100;
    maxProbabilityEnergyStateInA = mData.EnergyInA_arr[mData.TotalMultiplicity_arr.index(maxState)];
    minProbabilityEnergyStateInA = mData.EnergyInA_arr[mData.TotalMultiplicity_arr.index(minState)];

    print('This is for problem number ' + problemNumber);
    print('The most probable state is when A has : ' + str(maxProbabilityEnergyStateInA) + ' units of energy '
        'and the probability of this happening is ' + str("{0:.2f}".format(maxProbability)) + '%');
    print('The least probable state is when A has : ' + str(minProbabilityEnergyStateInA) + ' units of energy '
        'and the probability of this happening is ' + str("{0:.2f}".format(minProbability)) + '%');
    print('');

def EinsteinSolids(q, solidA, solidB, plotName):
    energyArr = GetEnergyPermutations(q);
    mData = GetMultiplicityData(energyArr, solidA, solidB);
    #print(SolidA_MultiplicityVsEnergy[0][0]);
    DisplayTable(mData, plotName);
    ListStateAndProbabilities(mData, plotName);
    #DisplayBarChart(mData, plotName);
    #print(SolidA_MultiplicityVsEnergy[0][1]);


EinsteinSolids(200, 200, 100, '2.10');
EinsteinSolids(6, 3, 3, '2.9a');
EinsteinSolids(6, 6, 4, '2.9b');

input1 = input();
