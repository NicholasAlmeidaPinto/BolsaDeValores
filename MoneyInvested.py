''' Classe para organizar as operações de venda, compra ou dividendos. '''

'''esta classe lê os arquivos, retorna um pandas.dataframe e pode fazer algumas operações'''

''' VARIÁVEIS:
- data -> pd dataframe, columns: name / qtd / value / day / month / total
'''

import pandas as pd

PATH = 'C:/Users/nicho/Documents/9. Projetos/2. Bolsa de Valores/data/'

class MoneyInvested:
    def __init__(self):
        self.read()

    def addInfo(self, value, day, month):
        f = open(PATH+'moneyInvested.txt', 'a')
        f.write('\n'+value+'\t'+day+'\t'+month)
        f.close()
        self.read()

    def read(self):
        self.data = pd.read_csv(PATH+'moneyInvested.txt', sep='\t', header=0)

    def getFull(self):
        return self.data

    def getCompact(self):
        return self.data.groupby(['day', 'month'], as_index=False)['value'].sum()

    def dayOperation(self, day, month):
        ''' Esta função retorna o valor total de cada empresa realizadas no dia/mes passado como argumento'''
        dayOperation = self.data.loc[(self.data['day'] == day) & (self.data['month'] == month)]
        return dayOperation.sum()

    def getTotal(self):
        return self.data['value'].sum()