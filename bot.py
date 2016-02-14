# -*- coding: utf-8 -*-
# importamos el diccionario KEYS del archivo keys.py, esto lo hacemos por
# seguridad, para no tener las claves en el mismo archivo que ejecutamos,
# es una buena práctica
from keys import KEYS
# importamos la librería de tweepy
import tweepy
# creamos una variable 'authorization' y le damos el valor obtenido por la
# función de autenticación de tweepy
authorization = tweepy.OAuthHandler(
    KEYS['consumer_key'], KEYS['consumer_secret'])
# lo mismo para los tokens de acceso
authorization.set_access_token(KEYS['access_token'], KEYS['access_secret'])
# comprobamos que las claves son correctas y lo notificamos mediante 'print'
try:
    redirect_url = authorization.get_authorization_url()
    print 'Authorization obtained.'
except tweepy.TweepError:
    print 'Error! Failed to get request token.'
# iniciamos la aplicación con la autorización
api = tweepy.API(authorization)

# creamos un "array" de arrays, donde almacenamos la palabra/frase en la
# posición 0, la respuesta en la posición 1 y la imagen en la posición 2
# de cada array de BENDER (arrayinceptio 0.0)
BENDER = (
    ('cerveza', "Pues a tu salud, toma una de estas!", "benderbrau.png"),
    ('"romantico"', "No hay nada más romántico que regalar una Benderbrau!",
     "benderbrau.png"),
    # aquí podríamos poner más
)

# recorremos el array BENDER, es decir, creamos una variable array "frase"
# en la que vamos almacenando cada valor iterable de BENDER, esto quiere
# decir que frase primero contendrá el array 1 ('cerveza', "Pues a tu
# salud, toma una de estas!", "benderbrau.png"), luego el dos, etc
for frase in BENDER:
        # almacenamos en "query" la frase o palabra que queremos buscar, dado
        # que es un array que contiene ("frase", "respuesta", )
    query = frase[0]
    # creamos una lista con los tweets que encruentra la API tweepy, cada
    # elemento de la lista debe contener la frase que contamos, buscamos el
    # número de elementos que pongamos en "count" y seleccionamos el idioma a
    # busca con "lang", esto último sirve para agilizar la búsqueda
    tweet_list = api.search(q=query, count=5, lang="es")
    # creamos una variable para contar el número de tweets respondidos
    tweets_answered = 0
    # ahora, en la lista de tweets obtenidos por la API, los vamos
    # respondiendo uno a uno
    for tweet in tweet_list:
        # obtenemos el "@username" que suele aparecer en tweeter (nombre
        # público) para poder utilizarlo más adelante
        screen_name = tweet.user.screen_name

        # Para evitar responder a retweets, comprobamos que su estatus no es
        # retwiteado, que no tiene el comando 'RT @' o que no se nombra el
        # usuario a sí mismo (otra forma de retweet)
        if(hasattr(tweet, 'retweeted_status') or
                'RT @' in tweet.text or
                api.me().screen_name == screen_name):
            print "this is a retweet, let's try another one."
        # en el caso de que no sea un retweet procedemos con el else
        else:
                # creamos una variable 'message' en la que almacenamos ".@"+
                # nombre de usuario + mensaje (mensaje obtenido del array
                # frases descrito anteriormente)
            message = ".@{username} {message}".format(
                username=screen_name, message=frase[1])
            # creamos una variable "image_path" en la que guardamos la
            # dirección de la imagen que queremos adjuntar
            image_path = "{image_name}".format(image_name=frase[2])
            # mediante un try/catch respondemos el tweet, utilizamos el
            # try/catch para que en caso de error, por el motivo que sea,
            # seamos conscientes de el porqué ha pasado, así podremos saber qué
            # tenemos que retocar en el código
            try:
                # usamos la función "update_with_media" para responder con una
                # imagen "filename", un mensaje "status" y el id a quien
                # queremos mandar el mensaje "in_reply_to_status_id"
                api.update_with_media(
                    filename=image_path, status=message,
                    in_reply_to_status_id=tweet.id)
                # sumamos a la variable "tweets_answered" +1 para llevar la
                # cuenta de los tweets respondidos, dado que pese a que podemos
                # obtener todos los tweets que queramos, es probable que  no
                # queramos responderlos a todos para que no nos echen por spam.
                # Cierto que podríamos limitar el número de tweets obtenidos,
                # pero podría ser que muchos sean retweets y no respondamos
                # ninguno. Para asegurarnos de que siempre respondemos un
                # número concreto de tweets podríamos poner un 'go to' (super
                # chapuzero, mejor modificar el for tweet in tweet_list) para
                # que a menos que hayamos respondido los tweets que queremos,
                # el programa no deje de buscar tweets
                tweets_answered += 1
                # mostramos por pantalla el mensaje que hemos twiteado
                print '{tweets_answered} {query}'.format(
                    tweets_answered=tweets_answered,
                    query=query)

                print message
                # en el caso de que hayamos respondido el número de tweets que
                # queremos, nos salimos del "for tweet in..." y se finalizará
                # el programa
                if tweets_answered >= 2:
                    break
            except tweepy.TweepError as error:
                print error.message[0]['code']
                print error.message[0][0]['code']
