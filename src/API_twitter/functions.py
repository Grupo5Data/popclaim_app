## importamos librerias
import re
from nltk.corpus import stopwords



## limpiamos los tweets de todos los signos de puntuación y pasamos todo a minúsculas
signos = re.compile("(\.)|(\;)|(\:)|(\!)|(\?)|(\¿)|(\@)|(\#)|(\,)|(\")|(\()|(\))|(\[)|(\])|(\{)|(\})|(\d+)")

def signs_tweets(tweet):
    return signos.sub('', tweet.lower())


## corregimos abreviaciones
def fix_abbr(tweet):
    '''Corrige abreviaciones'''
    if type(tweet) == list:
        words = tweet
    elif type(tweet) == str:
        words = tweet.split()
    else:
        raise TypeError('debe ser list o str')
    abbrevs = {'d': 'de',
               'x': 'por',
               'xa': 'para',
               'as': 'has',
               'q': 'que',
               'k': 'que',
               'dl': 'del',
               'xq': 'porqué',
               'dr': 'doctor',
               'dra': 'doctora',
               'sr': 'señor',
               'sra': 'señora',
               'm': 'me'}
    return " ".join([abbrevs[word] if word in abbrevs.keys() else word for word in words])


## eliminamos los LINKS de los tweets 
def remove_links(df):
    return " ".join(['{link}' if ('http') in word else word for word in df.split()])


# eliminamos STOPWORDS
spanish_stopwords = stopwords.words('spanish')
user_stop_words = ['RT','rt', 'un', 'uno', 'a', 'da', 'al', 'una', 'o', 'el', 'le',
                    'lo', 'los', '...', '..', '.', '.....', '....', '......','.......','que', 'es', '@']
stop_words = spanish_stopwords + user_stop_words

def remove_stopwords(df):
    return " ".join([word for word in df.split() if word not in stop_words])



## eliminamos las vocales repetidas 
def remove_repeated_vocals(data):
    '''Elimina vocales repetidas'''
    list_new_word = []

    for word in data.split(): #separa en palabras
        new_word = []
        pos = 0
        
        for letra in word: #separa cada palabra en letras
            if pos>0:
                if letra in ('a', 'e', 'i', 'o', 'u') and letra == new_word[pos-1]:
                    None
                else:
                    new_word.append(letra)
                    pos +=1
            else:
                new_word.append(letra)
                pos += 1
        else:
            list_new_word.append("".join(new_word))  
    return " ".join(list_new_word)



## normalizamos las risas
def normalize_laughts(data):
    '''Normaliza risas'''
    list_new_words = []
    for word in data.split(): #separamos en palabras
        count = 0
        vocals_dicc = {'a': 0, 'e': 0, 'i': 0, 'o':0, 'u':0}
        
        for letra in word:
            #print(word)
            if letra == 'j':
                count+=1
            if letra in vocals_dicc.keys():
                vocals_dicc[letra] += 1
        else:
            if count>3:
                dicc_risa = {'a': 'jaja', 'e': 'jeje', 'i': 'jiji', 'o': 'jojo', 'u': 'juju'}
                risa_type = max(vocals_dicc, key= lambda x: vocals_dicc[x]) #Indica si es a,e,i,o,u
                list_new_words.append(dicc_risa[risa_type])
            else:
                list_new_words.append(word)
    
    return " ".join(list_new_words)



# Función principal
def transform_tweets(df):
    """ Junta todas las funciones de limpieza """
    df = signs_tweets(df)
    df = fix_abbr(df)
    df = remove_links(df)
    df = remove_stopwords(df)
    df = remove_repeated_vocals(df)
    df = normalize_laughts(df)

    return df

