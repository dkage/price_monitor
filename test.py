from functions import *
import configparser
import psycopg2.extras
import re
import json


products_dict = {
    'store_prices': {
        'pichau': {
            'cpu': {
                'product_name': 'Processador AMD Ryzen 5 3600 Hexa-Core 3.6GHz (4.2GHz Turbo) 35MB Cache AM4, 100-100000031BOX',
                'price': 'R$1.248,86',
                'price_cash': 'R$1.099,00'
            },
            'motherboard': {
                'product_name': 'Placa Mae AsRock X570 Taichi DDR4 Socket AM4 Chipset AMD X570',
                'price': 'R$2.498,83',
                'price_cash': 'R$2.198,97'
            },
            'royal': {
                'product_name': 'Memoria G.Skill Trident Z Royal 16GB (2x8) DDR4 3600MHz Prata, F4-3600C17D-16GTRS',
                'price': 'R$1.135,26',
                'price_cash': 'R$999,03'
            }
        },
        'kabum': {
            'cpu': {
                'product_name': 'Processador AMD Ryzen 5 3600 Cache 32MB 3.6GHz(4.2GHz Max Turbo) AM4, Sem Vídeo - 100-100000031BOX ',
                'price': 'R$1.294,00',
                'price_cash': 'R$1.099,90'
            },
            'motherboard': {
                'product_name': 'Placa-Mãe ASRock X570 Taichi, AMD AM4, ATX, DDR4 ',
                'price': 'R$2.665,76',
                'price_cash': 'R$2.265,90'
            },
            'royal': {
                'product_name': 'Memória G.Skill Trident Z Royal, 16GB (2x8GB), 3600Hz, DDR4, C18 - F4-3600C18D-16GTRS ',
                'price': 'SOLD OUT',
                'price_cash': 'SOLD OUT'
            }
        },
        'terabyte': {
            'cpu': {
                'product_name': 'Processador AMD Ryzen 5 3600 3.6GHz (4.2GHz Turbo), 6-Core 12-Thread, Cooler Wraith Stealth, AM4, 100-100000031BOX, S/ Video',
                'price_cash': 'R$ 979,00',
                'price': 'R$ 1.125,29',
                'installments': '12x'
            },
            'motherboard': {
                'price_cash': 'SOLD OUT',
                'price': 'SOLD OUT',
                'installments': 'SOLD OUT',
                'product_name': 'Placa Mãe ASRock X570 Taichi Wifi, Chipset X570, AMD AM4, ATX, DDR4'
            },
            'royal': {
                'product_name': 'Memória DDR4 G.Skill Trident Z Royal, 16GB (2X8GB) 3600MHz, F4-3600C18D-16GTRS',
                'price_cash': 'R$ 956,13',
                'price': 'R$ 1.099,00',
                'installments': '12x'
            }
        }
    },
    'product_keys': {
        'motherboard',
        'royal',
        'cpu'
    },
    'stores': ['pichau', 'kabum', 'terabyte']
}

products = get_products_array()


for product in products:
    pichau = get_pichau(product['link_pichau'])
    terabyte = get_terabyte(product['link_terabyte'])
    kabum = get_kabum(product['link_kabum'])
    print(terabyte)
    print(kabum)
    print(pichau)

