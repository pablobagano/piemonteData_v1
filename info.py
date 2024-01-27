bahia = 'Camaçari,Pindobaçu,Utinga,Seabra,Serrolândia,Iuiu,Salvador,Ibitiara,Saúde,Iaçu,VárzeaNova,Candeal,Capim Grosso,Ibotirama,A. Dourada,Sobradinho,Jacobina'.split(",")
bahia = sorted(bahia)
sergipe = 'Carira,Aracaju,São Cristóvão,N. Sª Da Glória,Neópolis,SimãoDias,Frei Paulo,Campo do Brito,Macambira'.split(",")
sergipe = sorted(sergipe) 
cidades = bahia + sergipe 
cidades = sorted(cidades)
lista_cidades = zip([i.lower() for i in cidades], cidades) 
