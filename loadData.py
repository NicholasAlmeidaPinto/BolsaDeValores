def loadData(token, path, index, other):
    '''Função para ler os dados das empresas no site fundamentus.com.br'''
    import requests
    from bs4 import BeautifulSoup

    #load link
    link = 'https://www.fundamentus.com.br/detalhes.php?papel=' + token
    req = requests.get(link)

    #test if it exists
    if req.status_code != 200:
        print(token[0:5] + ': Fail! - Page not found')        

    soup = BeautifulSoup(req.content, 'html.parser')

    all = index+other

    #save and treat data
    info = []
    data = soup.findAll('span', attrs={'class':'txt'})
    if len(data) == 0:
        failFile = open(path+'/errors/FailOpen.txt', 'a')
        failFile.write(token + '\n')
        failFile.close()
        print(token + ': Fail! - Not found!')
        return 0

    for a in data:
        if a.text not in all:
            temp = a.text
            temp = temp.replace('\n          ', '')
            temp = temp.replace('.', '')
            temp = temp.replace('%', '')
            temp = temp.replace(',', '.')
            if temp == '-':
                temp = '0'
            info.append(temp)
    if len(info) != len(index):
        failFile = open(path+'/errors/FailSize.txt', 'a')
        failFile.write(token + '\n')
        failFile.close()
        print(token[0:5]+': Size error: index: '+str(len(index))+'/ data: '+str(len(info)))
        return 0
    return info

def loadPrice(tokens):
    import pandas_datareader.data as web
    import yfinance as yf
    yf.pdr_override()
    print('Carregando cotações')
    return web.get_data_yahoo(tokens)['Adj Close'].iloc[-1]