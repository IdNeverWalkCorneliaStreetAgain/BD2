import numpy as np
import pandas as pd

def mydataCleaning():
    
    print("*** Datacleaning Start ***")

    #Lettura dataset
    DF = pd.read_csv('dataset/Preprocessed_data.csv', skipinitialspace=True)

    #Drop delle colonne superflue o ridondanti
    TO_DROP = ['img_s','img_m','img_l','Summary','location','Language']
    DF.drop(TO_DROP, axis=1, inplace=True)

    #Impostiamo l'indice del DataFrame
    DF.set_index('isbn', inplace=True)
    
    #Conversione dei dati year_of_publication e age da float a int
    print("*** Cleaned-up Year of Publication ***")
    DF['year_of_publication'] = DF['year_of_publication'].astype(int)
    
    print("*** Cleaned-up Age ***")
    DF['age'] = DF['age'].astype(int)
    
    #Pulizia dei caratteri speciali,delle parentesi superflue e sostituzione valori non pertinenti alle categorie di dati
    print("*** Cleaned-up Category ***")
    DF['Category'] = DF['Category'].str.replace('[', '', regex=True)
    DF['Category'] = DF['Category'].str.replace(']', '', regex=True)
    DF['Category'] = DF['Category'].str.replace('\'', '', regex=True)
    DF['Category'] = DF['Category'].str.replace('9', 'Fiction', regex=True)

    print("*** Cleaned-up Title ***")
    DF['book_title'] = DF['book_title'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)
    
    print("*** Cleaned-up Author ***")
    DF['book_author'] = DF['book_author'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)
    
    print("*** Cleaned-up Publisher ***")
    DF['publisher'] = DF['publisher'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)
    
    print("*** Cleaned-up City ***")
    DF['city'] = DF['city'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)
    
    print("*** Cleaned-up State ***")
    DF['state'] = DF['state'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)
    
    print("*** Cleaned-up Country ***")
    DF['country'] = DF['country'].str.replace('[^a-zA-Z0-9\s\:\.\\(\\)]+', '',regex=True)

    #Creazione dataset pulito
    DF.to_csv('dataset/processed_data.csv', header='column_names')

    print("** Datacleaning END ***")