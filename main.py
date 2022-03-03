from urllib.request import urlopen
from bs4 import BeautifulSoup
import pandas as pd


# 'https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/chevrolet/prisma/usado/_Loja_all_NoIndex_True'
response = urlopen('https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado/concessionaria/_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True?#applied_filter_id%3DITEM_CONDITION%26applied_filter_name%3DCondi%C3%A7%C3%A3o%26applied_filter_order%3D7%26applied_value_id%3D2230581%26applied_value_name%3DUsado%26applied_value_order%3D2%26applied_value_results%3D43556%26is_custom%3Dfalsee')
html = response.read().decode('utf-8')
soup = BeautifulSoup(html, 'html.parser')
anuncios = soup.find('section', {'class': 'ui-search-results'})
cont = 1
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

for i in range(1, numero_paginas):
    for dupla in grupos:
        carros = dupla.findAll('div', {'class':'ui-search-result__content-wrapper'})
        for carro in carros:
            print(f'Inserindo o carro numero {cont}:')
            preco = carro.find('span', {'class': 'price-tag-fraction'})
            km = carro.find('ul', {'class': 'ui-search-card-attributes'})
            descricao = carro.find('div', {'class': 'ui-search-item__group ui-search-item__group--title'})
            loja = carro.find('p', {
                'class': 'ui-search-official-store-label ui-search-item__group__element ui-search-color--GRAY'})
            local = carro.find('span', {'class': 'ui-search-item__group__element ui-search-item__location'}).getText()
            """print('Preco: ' + preco.get_text())
            print(f'Marca : {descricao.get_text().split()[0]}')
            nova = descricao.get_text().split()[2:]
            print(f'Nome: {descricao.get_text().split()[1]}')
            print(f'Modelo: {" ".join(nova)}')
            print('Km: ' + km.get_text().split()[0][4:])
            print('Ano: ' + km.get_text().split()[0][:4])
            print(f'Estado: {" ".join(local.split()[-2:])}')
            print(f'Regiao: {" ".join(local.split()[:-3])}')
            if loja is not None:
                print(f'Loja: {" ".join(loja.get_text().split()[2:])}')
            else:
                print('Loja: Vazio')"""

            lista_preco.append(preco.get_text())
            lista_marca.append(descricao.get_text().split()[0])
            lista_nome.append(descricao.get_text().split()[1])
            lista_modelo.append(" ".join(descricao.get_text().split()[2:]))
            lista_km.append(km.get_text().split()[0][4:])
            lista_ano.append( km.get_text().split()[0][:4])
            lista_estado.append(" ".join(local.split()[-2:]))
            lista_regiao.append(" ".join(local.split()[:-3]))
            if loja is not None:
                lista_loja.append(" ".join(loja.get_text().split()[2:]))
            else:
                lista_loja.append('Vazio')
            print('--------------------------------------------------------------------------------------------')
            cont += 1

    response = urlopen('https://lista.mercadolivre.com.br/veiculos/carros-caminhonetes/usado/concessionaria/_Desde_'+str(cont)+'_YearRange_2015-0_PriceRange_55000-90000_NoIndex_True')
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    anuncios = soup.find('section', {'class': 'ui-search-results'})

print('************************ Imprimindo o DataFrame: ************************')
data_frame = pd.DataFrame(data={'Preco':lista_preco, 'Marca':lista_marca, 'Nome':lista_nome, 'Modelo':lista_modelo,
                        'Km':lista_km, 'Ano':lista_ano, 'Estado':lista_estado, 'Regiao':lista_regiao, 'Loja':lista_loja})
print(data_frame)

print('************************ Salvando o DataFrame em csv e xlsx ************************')
data_frame.to_csv('baseDadosCarros.csv', sep=';')