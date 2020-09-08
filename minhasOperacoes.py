import matplotlib.pyplot as plt
import investpy as inv
import seaborn as sns
import pandas as pd
import numpy as np
import datetime
import os

from MoneyInvested import MoneyInvested
from loadData import loadPrice
from Operacao import Operacao

pd.set_option('display.max_rows', None)

'''
Nicholas de Almeida Pinto

version - 0.6   -> implementei a função de preço médio, também coloquei a coluna 'date' na classe Operacao 

later versions
- 0.5   -> arrumei o código, melhorei algumas funções e excluí as desnecessárias.
- 0.4.1 -> adicionei uma maneira de obter os dados das empresas via investing.com, é mostrado com as ações em carteira.
- 0.4   -> arrumei várias operações, os dados estão batendo com a corretora, com erro menor que 2 reais.
- 0.3.1 -> yahoo finances para valor das ações
- 0.2   -> criei funções para obter o valor total mostrado na corretora, utilizando os valores atuais das ações
- 0.1   -> created this program

to do
- criar outra classe para obter minhas operações de venda sem ficar bagunçado
- pensar em alguma forma de obter o custo médio das ações
'''

class minhasOperacoes:
    def __init__(self):
        self.vendas = Operacao('sold')
        self.compras = Operacao('purchased')
        self.proventos = Operacao('earnings')
        self.investido = MoneyInvested()
        self.carregarCotacao()

    def carregarCotacao(self):
        self.actualPrices = loadPrice(self.compras.getNames(add='.SA')).reset_index()
        self.actualPrices.columns = ['name', 'cotação']
        self.actualPrices['name'] = self.actualPrices['name'].str.replace('.SA', '', regex=False)

    def cumulativeValue(self): # obtêm os valores acumulados por dia das operações
        compact = np.array([[0.0,0.0]])
        cumulativeValue = np.array([[0.0,0.0]])
        for m in range(12):
            for d in range(31):
                dateExist = False
                try:
                    datetime.datetime(2020, m, d)
                    dateExist = True
                except:
                    dateExist = False
                if dateExist:
                    bought = self.compras.dayOperation(d, m)['total'].sum()
                    sold = self.vendas.dayOperation(d, m)['total'].sum()
                    invested = self.investido.dayOperation(d, m)['value'].sum()
                    if bought != 0 or sold != 0 or invested != 0:
                        compact = np.append(compact, [[datetime.datetime(2020,m,d), invested - bought + sold]], axis=0)
        for i in compact:
            cumulativeValue = np.append(cumulativeValue, [[i[0], cumulativeValue[-1, 1]+i[1]]], axis=0)
        cumulativeValue = np.delete(cumulativeValue, 0,0)
        cumulativeValue = np.delete(cumulativeValue, 0,0)
        return pd.DataFrame({'day':cumulativeValue[:,0], 'value':cumulativeValue[:,1]})

    def precoMedio(self, actual): # obtêm os valores acumulados por dia das operações
        vendas = self.vendas.getFull()
        compras = self.compras.getFull()
        vendas['qtd'] = vendas['qtd']*-1
        actual['preço médio'] = 0

        names = actual['name']

        full = pd.concat([compras, vendas]).sort_values(['date'])
        for name in list(names):
            full_name = full[full['name'] == name]
            qtd = 0
            value = 0
            for index, row in full_name.iterrows():
                if row['qtd']>0:
                    value = (value*qtd + row['value']*row['qtd'])/(qtd + row['qtd'])
                    qtd = qtd+row['qtd']
                elif row['qtd'] < 0:
                    qtd = qtd + row['qtd']
            actual.at[actual['name'] == name, 'preço médio'] = value
        
        return actual

    def get_IndividualPrice(self, name):
        return float(self.actualPrices[self.actualPrices['name'] == name]['cotação'])

    def actualPatrimon(self): # pega o pandas dataframe do diffCompras_Vendas e atualiza o valor total com o valor das ações atualmente
        actual = self.diffCompras_Vendas()
        actual['lucro'] = 0.0
        actual['preço atual'] = 0.0
        for index, row in  actual.iterrows():
            if row['qtd'] > 0:
                newTotal = row['qtd']*self.get_IndividualPrice(row['name'])
                profit   = row['total'] + row['qtd']*self.get_IndividualPrice(row['name'])
                # replaces
                actual['total'] = actual['total'].replace(row['total'], newTotal)
                actual.at[index, 'preço atual'] = 1.0*float(self.get_IndividualPrice(row['name']))
                actual.at[index, 'lucro'] = float(profit)
            else:
                actual.at[index, 'lucro'] = row['total']
        return actual

    def diffCompras_Vendas(self): # retorna um pandas dataframe com o nome/qtd/total das ações
        comprasCompact = self.compras.getCompact()
        vendasCompact = self.vendas.getCompact()

        vendasCompact['qtd'] = -1.0*vendasCompact['qtd']
        comprasCompact['total'] = -1.0*comprasCompact['total']
        
        dif = vendasCompact.set_index('name').add(comprasCompact.set_index('name'), fill_value=0).reset_index()
        return dif

    def adicionarInformacoesEmpresas(self, actual):
        ''' Esta função adiciona os dados de P/L, P/Pa e indice Graham, pode ser um dataframe geral: precisa somente do "name"'''
        actual['distribuição (%)'] = (actual['total'] / actual['total'].sum()) * 100
        actual['P/L'] = 0.0
        #actual['P/VP'] = 0.0
        #actual['Graham'] = 0.0
        os.system('cls')
        for index, row in actual.iterrows():
            try:
                print('Carregando informações de ' + row['name'])
                info = inv.get_stock_information(row['name'], 'brazil', as_json=True)
                #P_Vp = info['Shares Outstanding']*info['Prev. Close']/(float(info['Market Cap'])) 
                #Graham = P_Pa * info['P/E Ratio']
                actual.at[index, 'P/L'] = info['P/E Ratio']
                #actual.at[index, 'P/VP'] = P_Vp
                #actual.at[index, 'Graham'] = Graham
            except:
                pass
        return actual

    def AddInfo(self, addmoney): # Function get info of name / qtd / value / day / month
        name = 0
        qtd = 0
        if ~addmoney:
            name  = input('Nome da ação: ')
            qtd   = input('Quantidade: ')
        value = input('Valor: ')
        day   = input('Dia: ')
        month = input('Mes: ')
        case  = input('0 para cancelar')
        if case == '0':
            return
        return [name, qtd, value, day, month]

    def valorPatrimonioAtual(self): # retorna o valor total que tenho atualmente, é o número que a corretora deve mostrar
        actual = self.actualPatrimon()
        return self.investido.getTotal() + actual['lucro'].sum() + self.proventos.getFull()['total'].sum()

    def livreEmCorretora(self):
        return self.investido.getTotal() + self.vendas.getTotal() - self.compras.getTotal() + self.proventos.getTotal()

    def menu(self):
        while(1):
            os.system('cls')
            print('################################')
            print('Patrimônio atual: ' + '{0:.2f}'.format(self.valorPatrimonioAtual()))
            print('Lucro com vendas: ' + '{0:.2f}'.format(self.actualPatrimon()['lucro'].sum()))
            print('Proventos: ' + '{0:.2f}'.format(self.proventos.getFull()['total'].sum()))
            print('Em corretora: ' + '{0:.2f}'.format(self.livreEmCorretora()))
            print('################################\n')
            print('1-Adicionar operação')
            print('2-Mostrar tudo')
            print('3-Mostrar ações em carteira')
            print('4-Mostrar lucro com as ações')
            print('9-Recarregar cotação')
            opt = input('--> ')

            if opt == '1': # add info
                while(1):
                    os.system('cls')
                    addmoney = False
                    print('1-Compra')
                    print('2-Venda')
                    print('3-Proventos')
                    print('4-Adicionar capital')
                    _opt = input('--> ')
                    if _opt == '1':
                        self.compras.addInfo(self.AddInfo(addmoney))
                    elif _opt == '2':
                        self.vendas.addInfo(self.AddInfo(addmoney))
                    elif _opt == '3':
                        self.proventos.addInfo(self.AddInfo(addmoney))
                    elif _opt == '4':
                        addmoney = True
                        _addinfo = self.AddInfo(addmoney)
                        self.investido.addInfo(_addinfo[2],_addinfo[3],_addinfo[4])
                    else: 
                        break

            elif opt == '2': # mostrar tudo
                os.system('cls')
                print('Compras: ')
                print(self.compras.getFull())
                input()

                os.system('cls')
                print('Vendas: ')
                print(self.vendas.getFull())
                input()
                
                os.system('cls')
                print('Proventos: ')
                print(self.proventos.getFull())
                input()
                
                os.system('cls')
                print('Movimento de capital: ')
                print(self.investido.getFull())
                input()

            elif opt == '3': # ações em carteira
                acoes = self.actualPatrimon()
                acoes = self.adicionarInformacoesEmpresas(acoes[acoes['qtd'] > 0])
                acoes = self.precoMedio(acoes)
                acoes['lucro atual'] = (acoes['preço atual'] - acoes['preço médio'])*acoes['qtd']
                os.system('cls')
                print('Ações atualmente em carteira: ')
                print(acoes)
                print('Lucro atual: '+str(acoes['lucro atual'].sum()))
                input()

            elif opt == '4':
                os.system('cls')
                lucro = self.actualPatrimon()
                print(lucro[['name', 'qtd', 'lucro']])
                input()

            elif opt == '9':
                self.carregarCotacao()

            else:
                break

'''
acoes = minhasOperacoes()
acoes.menu()'''