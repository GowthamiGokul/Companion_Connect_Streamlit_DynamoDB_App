import pandas as pd
import glob
df=pd.read_csv('animal-data-1.csv')

def printDtypes():
    return df.dtypes
def nullSum():
    return df.isnull().sum()

def getUnique(df):
    df=df.dropna()
    df.drop_duplicates(inplace=True,subset=['id'])
    df=df.reset_index(drop=True)
    if not 'animal_shelter.csv' in glob.glob('*.csv'):
        df.to_csv('animal_shelter.csv',index=False)
    else:return df



def create_files():
    animals=df[['sheltercode','identichipnumber','animalname',
            'speciesname','basecolour','animalage','sexname']]

    animals.to_csv('animals.csv',index=False)


    species=df['speciesname']
    breeds=df['breedname']
    intake=df[['intakedate','intakereason','istransfer']]
    movements=df[['movementdate','movementtype','istrial','returndate','returnedreason']]
    deceased=df[['deceaseddate','deceasedreason','diedoffshelter','puttosleep','isdoa']]
    location=df['location']

    species.to_csv('species.csv',index=False)
    breeds.to_csv('breeds.csv',index=False)
    intake.to_csv('intake.csv',index=False)
    movements.to_csv('movements.csv',index=False)
    deceased.to_csv('deceased.csv',index=False)
    location.to_csv('location.csv',index=False)



def loadShelter():
    as1=pd.read_csv('animal_shelter.csv')
    as1[['breedname','speciesname']]
    as1['species']=as1['speciesname'].map({'Cat':1,'Dog':2})
    mapp=zip(as1['species'].values,as1['breedname'].values)
    return tuple(mapp)

def loadIntake():
    intake=pd.read_csv('intake.csv')
    intake['animal_id']=[i for i in range(1,82)]
    intake['intakedate']=pd.to_datetime(intake['intakedate'])
    intake['intakedate']=intake['intakedate'].dt.strftime('%Y-%m-%d')
    intake.to_csv('intake.csv',index=False)


    intake=pd.read_csv('intake.csv')
    intake
    mapp=zip(intake['intakedate'].values,intake['istransfer'].values,intake['animal_id'].values,
            intake['intakereason'].values)


    return tuple(mapp)


def loadMove():
    move=pd.read_csv('movements.csv')
    move['animal_id']=[i for i in range(1,82)]
    move['movementdate']=pd.to_datetime(move['movementdate'])
    move['movementdate']=move['movementdate'].dt.strftime('%Y-%m-%d')

    move['returndate']=pd.to_datetime(move['returndate'])
    move['returndate']=move['returndate'].dt.strftime('%Y-%m-%d')
    mapp=zip(move['animal_id'].values,move['movementdate'].values,move['movementtype'].values,
            move['istrial'].values,move['returndate'].values,move['returnedreason'].values)

    return tuple(mapp)


def loadDec():
    deceased=pd.read_csv('deceased.csv')
    deceased['animal_id']=[i for i in range(1,82)]
    deceased['deceaseddate']=pd.to_datetime(deceased['deceaseddate'])
    deceased['deceaseddate']=deceased['deceaseddate'].dt.strftime('%Y-%m-%d')


    mapp=zip(deceased['animal_id'].values,deceased['deceaseddate'].values,deceased['deceasedreason'].values,
            deceased['diedoffshelter'].values,deceased['puttosleep'].values,deceased['isdoa'].values)
    
    return tuple(mapp)



def loadLoc():
    loc=pd.read_csv('location.csv')
    loc['animal_id']=[i for i in range(1,82)]

    mapp=zip(loc['animal_id'].values,loc['location'].values)
    print(tuple(mapp))