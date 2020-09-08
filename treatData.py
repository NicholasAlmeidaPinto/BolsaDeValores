from functions import * #arquivo com as funções utilizadas 
from machineLearn import *

path = 'C:/Users/nicho/Documents/9. Projetos/2. Bolsa de Valores'

data = pd.read_csv(path+'/data/df.txt', sep='\t\t', engine='python')
data = data.dropna(how='all', axis='columns')

data = basics(data)
data = data.fillna(0)
import numpy as np
data = data.replace(np.inf, 0)

while(1):
    a = input('\n\n1-Mostrar melhores acoes.'+
                '\n2-Mostrar minhas acoes.'+
                '\n3-Relatório'+
                '\n4-Investigar acao'+
                '\n5-Machine Learn'+
                '\n9-Gráficos.'+
                '\n--> ')
    if a == '1':
        printBest(data)
    elif a == '2':
        myInvestment(data, path)
    elif a == '3':
        report(data)
    elif a == '4':
        search(data)
    elif a == '5':
        print('GPR: ')
        ml_GPR(data)
        print('SVM: ')
        ml_SVM(data)
    elif a == '9':
        graphics(data)
        #pairplot(data)
    else:
        break