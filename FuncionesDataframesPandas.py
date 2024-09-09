# -*- coding: utf-8 -*-
"""
Created on Wed Jan 26 12:54:20 2022

@author: david
"""
#Antes de nada, importamos pandas y numpy para operar con dataframes.
import pandas as pd
import numpy as np

#Empezaremos creando los dataframes con los que vamos a operar a partir de los documentos de texto "movies.dat", "ratings.dat" y "users.dat"
moviesHeader = ["movie_id", "title", "genders"]
movies = pd.read_table("C:/ExamenRecuperacion/movies.dat", engine="python", sep="::", header= None, names = moviesHeader, encoding = "latin1")

ratingsHeader = ["user_id", "movie_id", "ratings", "timestamp"]
ratings = pd.read_table("C:/ExamenRecuperacion/ratings.dat", engine="python", sep="::", header= None, names = ratingsHeader, encoding = "latin1")

usersHeader = ["user_id", "gender", "age", "ocupation", "zip"]
users = pd.read_table("C:/ExamenRecuperacion/users.dat", engine="python", sep="::", header= None, names = usersHeader, encoding = "latin1")

#Una vez importados los documentos correctamente, procedemos a mergear los dataframes. En esta ocasión he realizado dos mergeos diferentes
#porque en uno de los ejercicios no utilizaremos los datos de "users.dat", y aunque sea ligeramente contraproducente en cuanto a escritura de
#código, aligerará un poco el tiempo de carga del dataframe al ejecutar esa opción.
userRatingsMoviesDF = pd.merge(pd.merge(ratings, users), movies)
ratingsMoviesDF = pd.merge(ratings, movies)

#Creamos el menú con los cuatro ejercicios y con la opción de salir para finalizar el programa, todo dentro de un bucle while para volver a 
#utilizar el programa las veces que se deseen.
#El valor que se le da a menú en un principio es indiferente siempre que no se escoja el 0 como valor inicial. En este caso le di un valor 10.
menu = 10 
while menu != 0:
    menu = int(input("¡Hola! Este es el menú de programas del examen de recuperación. Selecciona la opción que quieras elegir.\n \n \
    Las opciones son:\n \
    1. Rating medio de Star Wars por género.\n \
    2. Películas mejor valoradas.\n \
    3. Media de usuarios del género terror.\n \
    4. Actualización de datos (puntuación sobre 10).\n \
    0. Salir. \n \
    \nIntroduce el número para la operación que quieras realizar: "))

#Con distintos "if" y "elif", nos moveremos por las distintas opciones.
    if menu == 1:
#En cada uno de los ejercicios vamos a trabajr sobre una copia de seguridad, nunca sobre el DataFrame original.
        listaStarWars = userRatingsMoviesDF.copy()
#En este ejercicio utilizaremos "str.contains" para filtrar la información que queremos, "Star Wars", añadiendo todas las filas que contengan
#dichos caracteres a un nuevo DataFrame.
        filtered_df = listaStarWars[listaStarWars["title"].str.contains("STAR WARS", case=False)]
#Con una tabla pivotante utilizaremos la función "np.mean" sobre la columna "ratings" teniendo en cuenta y dividiendo entre géneros ("gender").
        starWarsPT = filtered_df.pivot_table(index=["movie_id", "title"], values=["ratings"], columns=["gender"], aggfunc=[np.mean])
#Creamos el archivo .css teniendo en cuenta el encabezado, elegimos separación y, aunque no sea necesario, ponemos el "encoding" correctamente
#por si en el futuro se fuese a ampliar el DataFrame y fuese necesario.
        starWarsPT.to_csv(r"C:/ExamenRecuperacion/Ejercicio1_DavidAlcazarSanchez.csv", sep=";", header=True, encoding = "latin1")
#Pintamos la tabla con la información solicitada, aunque solo los 10 primeros campos. Si se desea acceder al resto de información, se puede hacer
#fácilmente desde el explorador de variables o en el documento.css. Este sistema de muestra lo utilizaremos también en los demás ejercicios.
        print()    
        print ("El rating medio de Star Wars por género es:  \n%s" % starWarsPT[:10])
        #A lo largo del documento utilizaré varios prints vacíos para facilitar la lectura de datos en consola.
        print()  
        print()
    
    elif menu == 2:
#Volvemos a crear una copia sobre la que trabajar.
        topRatings = ratingsMoviesDF.copy()
# Agrupamos por ID de película y título, y calculamos la media y el conteo.
        topRatings2 = topRatings.groupby(["movie_id", "title"]).agg(
            average_rating=('ratings', 'mean'),  # Calcula la media de ratings
            count_votes=('ratings', 'size')     # Cuenta el número de votos
        )

# Ordenamos las películas por la media de votos, de mayor a menor.
        topRatings2 = topRatings2.sort_values(by="average_rating", ascending=False)
#Creamos el documento csv...
        topRatings2.to_csv(r"C:/ExamenRecuperacion/Ejercicio2_DavidAlcazarSanchez.csv", sep=";", header=True, encoding = "latin1")
#...y pintamos la información en pantalla.
        print()
        print("Películas con la media de votos más alta: \n%s" % topRatings2[:10])
        print()
        print()
        
    elif menu == 3:
#De nuevo, creamos la copia sobre la que trabajar.
        horrorMedia = userRatingsMoviesDF.copy()
#Volvemos a filtrar, en este caso, la columna "genders" mediante "str.constains", buscando todos aquellos campos que contengan la cadena de
#caracteres "horror" para quedarnos con ellos.
        horrorMedia = horrorMedia[horrorMedia["genders"].str.contains("horror", case=False)]
#Aplicamos la función "mean" a la columna "age", haciendo la media de edad PARA CADA PELICULA. Todavía no hemos terminado el ejercicio.
        horrorMedia2 = horrorMedia.groupby(["title", "genders"])["age"].mean()
#Guardamos el DataFrame en un css...
        horrorMedia2.to_csv(r"C:/ExamenRecuperacion/Ejercicio3_DavidAlcazarSanchez.csv", sep=";", header=True, encoding = "latin1")
#...y, ahora sí, volvemos a aplicar la función "mean" al DataFrame, sacando finalmente por pantalla (con redondeo a un decimal)
#la información pedida, la media total de la edad de los espectadores del género de terror.
        mean_df = horrorMedia2.mean()
        print()
        print(f"La edad media de los usuarios más TERRORÍFICOS es {round(mean_df, 1)}")
        print()
        print()
        
    elif menu == 4:
#Al ser el DataFrame que generamos en este ejercicio el más grande de todos (hay que operar con el más de millon de filas del DataFrame bruto),
#me ha parecido una buena idea lanzar un mensaje de espera en pantalla. El tiempo que tarda en generarse el DataFrame "nuevaPuntuacion2" es 
#bastante extenso.
        print ("\n¡Por favor, ten un poco de paciencia! Esta operación tardará un poco en completarse.")
#Una vez más, la copia de seguridad.
        nuevaPuntuacion = userRatingsMoviesDF.copy()
#En este caso tenemos que cambiar la puntuación máxima de 5 a 10. Al ser el doble, simplemente multiplicaremos las puntuaciones ya existentes
#por 2, solventando este problema. Para ello utilizaremos una función lambda aplicada a "ratings", que he renombrado com "newAVG" simplemente
#para que aparezca un nombre que aplique a esa columna y sirva de guía para esa información.
        nuevaPuntuacion2 = nuevaPuntuacion.groupby(["movie_id", "title", "user_id"])["ratings"].agg(newAVG = lambda x : x*2)
#Creamos de nuevo el documento .csv.
        nuevaPuntuacion2.to_csv(r"C:/ExamenRecuperacion/Ejercicio4_DavidAlcazarSanchez.csv", sep=";", header=True, encoding = "latin1")
#Y finalmente pintamos la información solicitada.
        print()
        print("Se va a mostrar en pantalla las puntuaciones con el nuevo máximo de 10: \n%s" % nuevaPuntuacion2[:10])
        print()
        print()

#Un último "elif" para asegurarnos que el número elegido está dentro de los parámetros que podemos ofrecer.
    elif menu < 0 or menu > 4: 
       print("\n \nIntroduce un comando entre el 0 y el 4, por favor.")
       print()


#Finalmente, con else (el cual solo puede valer 0 dadas las condiciones anteriores), cerraremos el programa.     
else:
    print ("\nHas seleccionado la opción salir. ¡Hasta luego!")