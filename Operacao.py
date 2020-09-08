''' Classe para organizar as operações de venda, compra ou dividendos. '''

'''esta classe lê os arquivos, retorna um pandas.dataframe e pode fazer algumas operações'''

''' VARIÁVEIS:
- option -> string with the name of file: purchased, earnings or sold
- data -> pd dataframe, columns: name / qtd / value / day / month / year / total / date
'''

from datetime import datetime
import pandas as pd

PATH = 'C:/Users/nicho/Documents/9. Projetos/2. Bolsa de Valores/data/'

class Operacao:
    def __init__(self, option):
        self.option = option
        self.read()

    def addInfo(self, arg):
        name = arg[0]
        qtd = arg[1]
        value = arg[2]
        day = arg[3]
        month = arg[4]
        f = open(PATH+self.option+'.txt', 'a')
        f.write('\n'+name+'\t'+qtd+'\t'+value+'\t'+day+'\t'+month)
        f.close()
        self.read()

    def read(self):
        self.data = pd.read_csv(PATH+self.option+'.txt', sep='\t', header=0)
        self.data['year'] = 2020
        self.data['total'] = self.data['qtd']*self.data['value']
        self.data['date'] = pd.to_datetime(self.data[['year', 'month', 'day']])

    def getFull(self):
        return self.data

    def getCompact(self):
        compact = ['qtd', 'total']
        return self.data.groupby(['name'], as_index=False)[compact].sum()

    def getNames(self, add=''):
        names = self.getCompact()['name'] + add
        return names.tolist()

    def getTotal(self):
        return self.data['total'].sum()

    def dayOperation(self, day, month):
        ''' Esta função retorna o valor total de cada empresa realizadas no dia/mes passado como argumento'''
        dayOperation = self.data.loc[(self.data['day'] == day) & (self.data['month'] == month)]
        return dayOperation.groupby(['name'], as_index=False)['total'].sum()
