import numpy as np
from PIL import Image
import pandas as pd


def process_text():
    print("Inicio")

    lines = ""
    with open('bittorrent') as f:
        lines = f.readlines()

    i = 0#Comeca sem nada
    string = ''
    n = 0;
    lst = []
    count = 0
    x = 0;
    y = 0
    for each in lines:
        print("Linha arquivo: "+str(each))
        if i == 1:
            if "};" in each:
                print("Each: "+str(each))
                each = each.split(" };")
                print(str(each))
                print("Dentro do fim: "+str(each[0]))
                l = each[0].split(", ")
                print("Valor de L após split: "+str(l))
                print("Tamanho de L: "+str(len(l)))

                l[0] = str(l[0].split(" ")[0])
                print("Valor de L aposo formatado: "+str(l))

                for i in range(len(l)):
                    print("Arrumando...")
                    l[i] = str(l[i].split(" ")[0])

                print("Arrumada: "+str(l))

                acrescimo = 8 - len(l)
                print("Acrescimo: "+str(acrescimo))
                for i in range(acrescimo):
                    l.insert(len(l), "0xFF")

                print("L FINAL2: "+str(l))
                lst.append(l)
                count = count + 1
                x = x + 1
                create_image(lst,count,x)
                x = 0
                lst = []
                i = 0
                print("Continua...")

            else:
                #print(each)
                l = each.split(", ")
                print("Lista: "+str(l))
                print(str((l[8].split(", \n")[0])))
                l[8] = str((l[8].split(", \n")[0]))
                if l[8] == "\n":
                    #print("Ultimo e barra-n")
                    l.pop(8)
                #print(l)
                lst.append(l)
                #print(str(n+1) + " Line: "+str(string))
                n = n + 1
                x = x + 1
        if i == 0:
            if "{" in each:
                i = 1

def create_image(lst, n,x):

    print("Tamanho de X: "+str(x))

    #print(lst)
    #exit()

    #print(string)
    teste = np.asmatrix(lst)
    print(teste)
    #print(np.size(teste))
    #print(np.shape(teste))
    #print(teste[20,5])
    #print(int(teste[0,0],16))

    #if np.size(teste,1) > 169 and np.size(teste,1) <=196:
    #    print("Criar uma matriz 14 x 14")

    for i in range(x):
        for j in range(8):
            #print(str(teste[i,j]))
            teste[i,j] = int(teste[i,j],16)

    teste = teste.tolist()
    #print("Teste: "+str(teste))
    #print(teste[0][1])


    numeros = np.matrix(teste)
    numeros = numeros.astype(int)
    #print(numeros.shape)
    #print(numeros)

    dataFrame = pd.DataFrame(numeros)
    data = dataFrame.to_numpy()

    data = data.tolist()
    #print(data[0][7])

    for i in range(x):
        for j in range(8):
            data[i][j] = [data[i][j],data[i][j],data[i][j]]

    data = np.array(data)
    #print(data)


    img = Image.fromarray(data.astype('uint8'), 'RGB')
    size=n*8
    #arr = np.zeros((size,size,3))
    #arr[:,:,0] = [[255]*size]*size
    #arr[:,:,1] = [[255]*size]*size
    #arr[:,:,2] = [[0]*size]*size
    #img = Image.fromarray(arr.astype('uint8'), 'RGB')

    print("\nPronto pra salvar: " + str(n))
    img.save("bittorrent"+str(n)+".png")
    return

process_text()