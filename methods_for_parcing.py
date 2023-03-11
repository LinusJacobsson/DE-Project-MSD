from pyspark import SparkContext


    #this function takes a sparcontext and a lyrics file and return an rdd with the format sonid,word1, word2, word3...
def parse_lyricsfile(sc, filepath:str):
    rdd = sc.textFile("filepath").map(lambda line: line.split(','))

    rdd = rdd.map(lambda line: (line[0], {int(x.split(':')[0]): int(x.split(':')[1]) for x in line[2:]}))


    rdd = rdd.map(lambda x: (x[0], {i: x[1].get(i, 0) for i in range(1, 5001)}))


    rdd = rdd.map(lambda x: [x[0] , tuple(x[1].values())])
    return rdd



#this function takes a sparcontext and a genera file and return an rdd with the format songid,generaid
#the generas are map to an int based on the number of diffrent generas in the file
def parcs_generafile(sc,filepath):
    rdd = sc.textFile("filpath").map(lambda line: line.split("\t"))

    generaindexes= rdd.map(lambda x: x[1]).distinct().zipWithIndex()
    rdd= rdd.map(lambda x: (x[1], x[0])).join(generaindexes).map(lambda x: [x[1][0], x[1][1]])

    return rdd

#this function takes a sparcontext  a lyrcis rdd and agenera rdd and return an rdd with the format [id,generaid,word1,word2,word3...]
def generate_combinedrdd(sc,lyricsrdd,generardd):
    rdd = lyricsrdd.join(generardd)
    rdd= rdd.map(lambda x: [x[0], x[1][1]]+ list(x[1][0]))


    return rdd



