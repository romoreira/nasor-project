import numpy as np
from PIL import Image
import pandas as pd


def process_text():

    lines = ""
    with open('slice-2') as f:
        lines = f.readlines()

    i = 0#Comeca sem nada
    string = ''
    n = 0;
    lst = []
    count = 0
    for each in lines:
        print("Linha arquivo: "+str(each))
        if i == 1:
            if "};" in each:
                each = each.split("};")
                #print("Dentro do fim: "+str(each[0]))
                l = each[0].split(", ")
                #print(l[3].split(" ")[0])
                l[0] = str(l[0].split(" ")[0])
                l[1] = str(l[1].split(" ")[0])
                l[2] = str(l[3].split(" ")[0])
                l[3] = str(l[3].split(" ")[0])
                l.insert(len(l),"0xFF")
                l.insert(len(l), "0xFF")
                l.insert(len(l), "0xFF")
                l.insert(len(l), "0xFF")
                #print("L FINAL2: "+str(l))
                lst.append(l)
                count = count + 1
                create_image(lst,count)
                lst = []
                i = 0
                print("Continua...")
            else:
                #print(each)
                l = each.split(", ")
                #print(l)
                #print(str((l[7].split(",\n")[0])))
                l[7] = str((l[7].split(",\n")[0]))
                if l[8] == "\n":
                    #print("Ultimo e barra-n")
                    l.pop(8)
                #print(l)
                lst.append(l)
                #print(str(n+1) + " Line: "+str(string))
                n = n + 1
        if i == 0:
            if "Packet" in each:
                i = 1

def create_image(lst, n):

    #print(lst)
    #exit()

    #print(string)
    teste = np.asmatrix(lst)
    #print(teste)
    #print(np.size(teste))
    #print(np.shape(teste))
    #print(teste[20,5])
    #print(int(teste[0,0],16))

    #if np.size(teste,1) > 169 and np.size(teste,1) <=196:
    #    print("Criar uma matriz 14 x 14")

    for i in range(22):
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

    for i in range(22):
        for j in range(8):
            data[i][j] = [data[i][j],data[i][j],data[i][j]]

    data = np.array(data)
    #print(data)


    img = Image.fromarray(data.astype('uint8'), 'RGB')
    size=176
    #arr = np.zeros((size,size,3))
    #arr[:,:,0] = [[255]*size]*size
    #arr[:,:,1] = [[255]*size]*size
    #arr[:,:,2] = [[0]*size]*size
    #img = Image.fromarray(arr.astype('uint8'), 'RGB')

    print("\nPronto pra salvar: " + str(n))
    img.save("slice_2-"+str(n)+".png")
    return

process_text()