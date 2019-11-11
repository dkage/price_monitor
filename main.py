from trackers.kabum_functions import *
from trackers.pichau_functions import *
from trackers.terabyte_functions import *
import flask


cpu = dict()
cpu['kabum'] = 102438  # Ryzen 5 3600
cpu['pichau'] = 'processador-amd-ryzen-5-3600-hexa-core-3-6ghz-4-2ghz-turbo-35mb-cache-am4-yd3600bbafbox'  # Ryzen 5 3600
cpu['terabyte'] = '11313/processador-amd-ryzen-5-3600-36ghz-42ghz-turbo-6-core-12-thread-cooler-wraith-stealth-am4'  # Ryzen 5 3600
# print(get_kabum(cpu['kabum']))
# print(get_pichau(cpu['pichau']))
print(get_terabyte(cpu['terabyte']))


taichi = 102175  # Ryzen 5 3600
mobo = dict()
mobo['terabyte'] = '8567/mouse-redragon-gamer-cobra-chroma-m711-7-botoes-programaveis-10000-dpi-rgb-preto'
# print(get_kabum(taichi))
print(get_terabyte(mobo['terabyte']))
cpu_2 = 102436  # Ryzen 5 3600
# print(get_kabum(cpu_2))

psu = dict()
psu['terabyte'] = '7903/fonte-corsair-cx550-cp-9020121-ww-550w-reais-atxeps-23-pfc-ativo'
print(get_terabyte(psu['terabyte']))
