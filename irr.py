import sys, socket
from pprint import pprint

from App import Whois

timeout = 60
server = 'whois.radb.net'
asn = 7195
port = 43

try:
    # consultar as-set
    # separar objetos do tipo origin e do tipo as-set
    # refazer o processo até eliminar todos os as-sets
    
    # após ter apenas origins fazer consulta de rotas
    
    all_origins = list()
    

    irr_data = Whois('AS-EDGEUNO', ['AS-EDGEUNO'])
    print(irr_data.origins)

        
except (socket.timeout, socket.error) as e:

    print(e)