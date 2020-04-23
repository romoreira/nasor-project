import numpy as np
from PIL import Image
import pandas as pd


def process_text():

    lines = ""
    with open('rawdata') as f:
        lines = f.readlines()

    i = 0#Comeca sem nada
    string = ''
    n = 0;
    lst = []
    count = 0
    for each in lines:
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
                print("L FINAL2: "+str(l))
                lst.append(l)
                count = count + 1
                create_image(lst,count)
                i = 0
            else:
                #print(each)
                l = each.split(", ")
                #print(str((l[7].split(",\n")[0])))
                print(l)
                l[7] = str((l[7].split(", \n")[0]))
                print(l)
                lst.append(l)
                #print(str(n+1) + " Line: "+str(string))
                n = n + 1
        if i == 0:
            if "Packet" in each:
                i = 1

def create_image(lst, n):

    #print(lst)
    exit()

    #print(string)
    teste = np.asmatrix(lst)
    #print(teste)
    print(np.size(teste))
    print(np.shape(teste))
    #print(teste[20,5])
    print(int(teste[0,0],16))

    #if np.size(teste,1) > 169 and np.size(teste,1) <=196:
    #    print("Criar uma matriz 14 x 14")

    for i in range(22):
        for j in range(8):
            teste[i,j] = int(teste[i,j],16)

    teste = teste.tolist()
    print("Teste: "+str(teste))
    #print(teste[0][1])


    numeros = np.matrix(teste)
    numeros = numeros.astype(int)
    #print(numeros.shape)
    #print(numeros)

    dataFrame = pd.DataFrame(numeros)
    data = dataFrame.to_numpy()

    data = data.tolist()
    print(data[0][7])

    for i in range(22):
        for j in range(8):
            data[i][j] = [data[i][j],data[i][j],data[i][j]]

    data = np.array(data)
    print(data)


    img = Image.fromarray(data.astype('uint8'), 'RGB')
    size=176
    #arr = np.zeros((size,size,3))
    #arr[:,:,0] = [[255]*size]*size
    #arr[:,:,1] = [[255]*size]*size
    #arr[:,:,2] = [[0]*size]*size
    #img = Image.fromarray(arr.astype('uint8'), 'RGB')

    #img.save("foto.png")

    print("\nPronto pra salvar: "+str(n))



# lst = []
#
# for each in lines:
#     print(each)
#     if "Packet" not in each:
#         values = each.split(",")
#         for hex in values:
#             if hex != str("\n"):
#                 #print("HEX: "+str(hex))
#                 l = [hex.strip()]
#                 lst.append(l)
# list_2 = []
# #print(lst)
#
# for elem in lst:
#     #print(elem)
#     list_aux = [[int(elem[0],0),int(elem[0],0),int(elem[0],0)]]
#     list_2.append(list_aux)
#
# data = np.array(list_2)
# print(data)
#
# img = Image.fromarray(data.astype('uint8'), 'RGB')
#
# size=241
#
# arr = np.zeros((size,size,3))
#
# arr[:,:,0] = [[255]*size]*size
# arr[:,:,1] = [[255]*size]*size
# arr[:,:,2] = [[0]*size]*size
#
# #img = Image.fromarray(arr.astype('uint8'), 'RGB')
# #img.save("foto.png")

process_text()