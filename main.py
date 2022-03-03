import os.path
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd



# https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True?#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D7%26applied_value_id%3D2230581%26applied_value_name%3DUsado%26applied_value_order%3D2%26applied_value_results%3D43556%26is_custom%3Dfalsee
url_sp = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-sao-paulo/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True'
url_mg = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-minas-gerais/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True'
url_rj = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-rio-de-janeiro/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True'
url_sc = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-santa-catarina/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True'
url_pr = 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-parana/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True'

cont = 1

response = urlopen(url_rj)
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
anuncios = soup.find('section', {'class': 'ui-search-results'})
grupos = anuncios.findAll('ol', class_='ui-search-layout ui-search-layout--grid')
num = anuncios.find('li', {'class': 'andes-pagination__page-count'})

numero_paginas = int(num.get_text().split()[-1])
print(numero_paginas)

lista_preco = []
lista_marca = []
lista_nome = []
lista_modelo = []
lista_km = []
lista_ano = []
lista_estado = []
lista_regiao = []
lista_loja = []

for i in range(1, numero_paginas + 1):
    anuncios = soup.find('section', {'class': 'ui-search-results'})
    grupos = anuncios.findAll('ol', class_='ui-search-layout ui-search-layout--grid')
    for dupla in grupos:
        carros = dupla.findAll('div', {'class':'ui-search-result__content-wrapper'})
        for carro in carros:
            print(f'Inserindo o carro numero {cont}:')
            preco = carro.find('span', {'class': 'price-tag-fraction'})
            km = carro.find('ul', {'class': 'ui-search-card-attributes'})
            descricao = carro.find('div', {'class': 'ui-search-item__group ui-search-item__group--title'})
            loja = carro.find('p', {
                'class': 'ui-search-official-store-label ui-search-item__group__element ui-search-color--GRAY'})
            local = carro.find('span', {'class': 'ui-search-item__group__element ui-search-item__location'})

            """
            teste
            print('Preco: ' + preco.get_text())
            print(f'Marca : {descricao.get_text().split()[0]}')
            nova = descricao.get_text().split()[2:]
            print(f'Nome: {descricao.get_text().split()[1]}')
            print(f'Modelo: {" ".join(nova)}')
            print('Km: ' + km.get_text().split()[0][4:])
            print('Ano: ' + km.get_text().split()[0][:4])
            print(f'Estado: RJ')
            print(f'Região: {" ".join(local.get_text().split())}')
            if loja is not None:
                print(f'Loja: {" ".join(loja.get_text().split()[2:])}')
            else:
                print('Loja: Vazio')"""
            lista_preco.append(preco.get_text())
            lista_marca.append(descricao.get_text().split()[0])
            lista_nome.append(descricao.get_text().split()[1])
            lista_modelo.append(" ".join(descricao.get_text().split()[2:]))
            lista_km.append(km.get_text().split()[0][4:])
            lista_ano.append(km.get_text().split()[0][:4])
            lista_estado.append("RJ")
            lista_regiao.append(" ".join(local.get_text().split()))
            if loja is not None:
                lista_loja.append(" ".join(loja.get_text().split()[2:]))
            else:
                lista_loja.append('Vazio')
            print('--------------------------------------------------------------------------------------------')
            cont += 1
    print(cont)
    response = urlopen('https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado-em-rio-de-janeiro/concessionaria/_Desde_'+str(cont)+'_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True')
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')


print('************************ Imprimindo o DataFrame: ************************')
data_frame = pd.DataFrame(data={'Preco':lista_preco, 'Marca':lista_marca, 'Nome':lista_nome, 'Modelo':lista_modelo,
                        'Km':lista_km, 'Ano':lista_ano, 'Estado':lista_estado, 'Regiao':lista_regiao, 'Loja':lista_loja})
print(data_frame)
data_frame.to_csv('baseDadosCarrosRJ.csv', sep=';')
print('************************ Salvando o DataFrame em csv e xlsx ************************')


"""
Para verificar se arquivo existe na pasta 
if(os.path.isfile('baseDadosCarros.csv')):
    print('está')

    with open('baseDadosCarros.csv', 'w', newline='') as saida:
        data_frame.to_csv('baseDadosCarros.csv', sep=';')
else:
    data_frame.to_csv('baseDadosCarros.csv', sep=';')
"""

