#arquivo com as funções utilizadas para tratar os dados

import pandas as pd

def nick(data):
    nick = []
    for i in range(len(data)):
        div = 1 + 0.08*float(data['Cres. Rec (5a)'][i]) - 2*data['Endividamento'][i] - 0.1*data['Rec. Endividamento'][i]
        if div == 0:
            print('div = 0')
            div = 1
        nick.append(data['Graham'][i]/div)
    return nick

def basics(data):
    '''Função que gera os índices básicos e fracionados para calculos avançados.
    Também calcula o índice Graham'''
    data['Valor Contábil'] = data['Patrim. Líq']/data['Nro. Ações']
    data['Valorização'] = data['Cotação']/data['Valor Contábil']
    data['Endividamento'] = data['Dív. Líquida']/data['Patrim. Líq']
    data['Rec. Endividamento'] = data['Dív. Líquida']/data['Lucro Líquido']
    data['Graham'] = data['Valorização']*data['P/L']
    data['Nick'] = nick(data)
    data['Movimentações'] = data['Vol $ méd (2m)']/data['Cotação']/data['Nro. Ações']
    return data

def printBest(data):
    '''Função que mostra as melhores ações, baseado nos indices Graham e Nick'''

    print('\n\nMelhores cotacoes')
    count = 0
    for i in range(len(data)):
        if data['Graham'][i] > 0 and data['Graham'][i]<22.5 and data['Nick'][i]>0 and data['Nick'][i]<30 and float(data['P/L'][i]) > 0 and float(data['Patrim. Líq'][i]) > 0 and float(data['Lucro Líquido'][i]) > 0:
            print('Papel: ' + data['Papel'][i] + 
            ' - Cotação: ' + str('{:7.2f}'.format(data['Cotação'][i])) + 
            ' - P/L: ' + str('{:7.2f}'.format(data['P/L'][i])) +
            ' - Graham: '  + str('{:7.2f}'.format(data['Graham'][i])) + 
            ' - Nick: '    + str('{:7.2f}'.format(data['Nick'][i])))
            count = count + 1
    print('Foram listadas: ' + str(count) + ' empresas de ' + str(len(data)))

def myInvestment(data, path):
    '''Função que mostra os índices graham, nick e cotação dos papeis que tenho em carteira'''

    print('\n\nMinhas cotacoes')
    r = open(path+'/pref/myInvestments.txt', 'r')

    select = ['Papel', 'Cotação', 'Graham', 'Nick']
    df = pd.DataFrame(columns=select)

    for token in r:
        df = pd.concat([df, data.loc[data['Papel']==token[0:5]][select]])
    r.close()

    for i in df.index:
        print('Papel: ' + data['Papel'][i] + 
        ' - Cotação: ' + str('{:7.2f}'.format(data['Cotação'][i])) + 
        ' - P/L: '     + str('{:7.2f}'.format(data['P/L'][i])) + 
        ' - Graham: '  + str('{:7.2f}'.format(data['Graham'][i])) + 
        ' - Nick: '    + str('{:7.2f}'.format(data['Nick'][i])))


def report(data):
    count_P_L = 0
    count_Pl = 0
    count_Lucro = 0
    count_Endivi = 0
    for i in range(len(data)):
        if data['P/L'][i] < 0:
            count_P_L = count_P_L+1
        if data['Patrim. Líq'][i] < 0:
            count_Pl = count_Pl+1
        if data['Lucro Líquido'][i] < 0:
            count_Lucro = count_Lucro+1
        if data['Endividamento'][i] < 0:
            count_Endivi = count_Endivi+1

    print('Número de empresas com os seguintes índices menores que 0.0:')
    print(' - '+str(count_P_L)+' P/L')
    print(' - '+str(count_Pl)+' Patrimônio líquido')
    print(' - '+str(count_Lucro)+' Lucro líquido')
    print(' - '+str(count_Endivi)+' Endividamento')

def search(data):
    while(1):
        choice = input('Token escolhido: ')
        if choice == '':
            break
        else:
            temp = data.loc[data['Papel']==choice]
            pd.set_option('display.max_columns', None)
            if len(temp) > 0:
                print(temp)
            else: 
                print('Token não encontrado')

def graphics(data):
    import matplotlib.pyplot as plt

    y = 'Valorização'

    plt.subplot(221)
    x = 'Nro. Ações'
    plt.loglog(data[x], data[y], '*')
    plt.xlabel(x)
    plt.ylabel(y)
    
    plt.subplot(222)
    x = 'P/L'
    plt.loglog(data[x], data[y], '*')
    plt.xlabel(x)
    plt.ylabel(y)

    plt.subplot(223)
    x='Giro Ativos'
    plt.loglog(data[x], data[y], '*')
    plt.xlabel(x)
    plt.ylabel(y)

    plt.subplot(224)
    x='Div. Yield'
    plt.loglog(data[x], data[y], '*')
    plt.xlabel(x)
    plt.ylabel(y)

    plt.show()

def pairplot(data):
    lista = ['Graham', 'Cotação', 'Cres. Rec (5a)', 'Endividamento', 'Valor Contábil']

    #t = data.loc[data['Cres. Rec (5a)'] == data['Cres. Rec (5a)'].max()]['Papel']
    #print(t)

    temp = data[lista]
    temp = temp.drop([197], axis=0)
    import seaborn as sns
    import matplotlib.pyplot as plt
    sns.pairplot(temp)
    plt.show()

def threeD(data):
    import matplotlib.pyplot as plt
    ax = plt.axes(projection='3d')
    ax.scatter3D(data['P/L'], data['Nro. Ações'], data['Valorização'])
    plt.show()