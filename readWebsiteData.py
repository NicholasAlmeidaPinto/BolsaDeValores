from loadData import loadData

path = 'C:/Users/nicho/Documents/9. Projetos/2. Bolsa de Valores'

#Trash 
index = ['Papel', 'Cotação', 'Tipo', 'Data últ cot', 'Empresa', 'Min 52 sem',
        'Setor', 'Max 52 sem', 'Subsetor', 'Vol $ méd (2m)', 'Valor de mercado', 
        'Últ balanço processado', 'Valor da firma', 'Nro. Ações',  'P/L', 'LPA', 
        'P/VP', 'VPA', 'P/EBIT','Marg. Bruta',  'PSR', 'Marg. EBIT', 'P/Ativos', 
        'Marg. Líquida', 'P/Cap. Giro', 'EBIT / Ativo', 'P/Ativ Circ Liq', 'ROIC',  
        'Div. Yield',  'ROE',  'EV / EBITDA', 'Liquidez Corr',  'EV / EBIT', 
        'Div Br/ Patrim', 'Cres. Rec (5a)', 'Giro Ativos',  'Ativo', 'Dív. Bruta', 
        'Disponibilidades', 'Dív. Líquida', 'Ativo Circulante', 'Patrim. Líq',  
        'Receita Líquida', 'Receita Líquida', 'EBIT', 'EBIT', 'Lucro Líquido', 'Lucro Líquido']

bank  = ['Cart. de Crédito', 'Result Int Financ', 'Rec Serviços']
other = ['Oscilações', 'Indicadores fundamentalistas', 'Dia','Mês','30 dias','12 meses',
        '2020','2019','2018', '2017','2016','2015','Dados Balanço Patrimonial',
        'Dados demonstrativos de resultados', 'Últimos 12 meses', 'Últimos 3 meses', '']
        
print('\n\n###################################')
print('############## START ##############')
print('###################################\n\n')

#head in txt
f = open(path+'/data/df.txt','w')
for i in index:
    f.write(i+'\t\t')
f.close()

#take all tokens
tokens = []
r = open(path+'/tokens/tokens.txt', 'r')
for token in r:
    tokens.append(token)
r.close()
#set([x for x in tokens if tokens.count(x) > 1])
count = 1

for token in tokens:
    #function to load website data
    data = loadData(token[0:5], path, index, other)

    if (data != 0):
        print(str(count) + ' out of ' + str(len(tokens)) + ' - ' + token[0:5]+': Success!')
        f = open(path+'/data/df.txt','a')

        #save data in txt
        f.write('\n'+data[0])
        for i in data[1:]:
            f.write('\t\t'+i)
        f.close()
    count = count + 1

print('\n\n###################################')
print('############### END ###############')
print('###################################\n\n')