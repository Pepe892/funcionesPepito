import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

############################################ LA FAMOSA MAKE QUANTILES ###########################################################

def Make_Quantiles(dataframe, n_divisions, variable_name, defaultname='FLAG_MALO', function='MEAN'):
    
    default = defaultname
    
    if(dataframe[variable_name].dtype == 'O' or dataframe[variable_name].dtype == 'S'):
        print('Error: Columna no es una variable numérica')
        return
    
    percent = 1./n_divisions
    x = dataframe[[variable_name, default]]
    
    percentile_ant = x[[variable_name]].quantile(percent)
    percentile = x[[variable_name]].quantile(percent*2)
    
    x.loc[:,variable_name+'_quant'] = np.select([ x[variable_name]>percentile_ant[0] ], [1],0)
    x.loc[:,variable_name+'_corte'] = np.select([ x[variable_name]>percentile_ant[0] ], 
                                                ['%.2f - %.2f'%(percentile_ant[0], percentile[0])], '<=%.2f'%percentile_ant[0])
    
#    for i in range(n_divisions-3):
#        percentile_ant = percentile
#        percentile = x[[variable_name]].quantile(percent*(i+3))
#        x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_quant'] = 2+i
#        x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_corte'] = '%.2f - %.2f'%(percentile_ant[0], percentile[0])
    
#    percentile_ant = percentile
#    x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_quant'] = n_divisions-1
#    x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_corte'] = '>%.2f'%(percentile_ant[0])

    for i in range(n_divisions-3):
        percentile_ant = percentile
        percentile = x[[variable_name]].quantile(percent*(i+3))
        x.loc[ :, variable_name+'_quant'] = np.where(( x[variable_name]>(percentile_ant[0]) ), 2+i, x[variable_name+'_quant'])
        x.loc[ :, variable_name+'_corte'] = np.where(( x[variable_name]>(percentile_ant[0]) ), '%.2f - %.2f'%(percentile_ant[0], percentile[0]), 
		x[variable_name+'_corte'])

    percentile_ant = percentile
	
    x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_quant'] = n_divisions-1
    x.loc[ ( x[variable_name]>(percentile_ant[0]) ), variable_name+'_corte'] = '>%.2f'%(percentile_ant[0])
    
    if(function=='MEAN'):
        x = x[[variable_name+'_quant', variable_name+'_corte', default]].groupby(
            [variable_name+'_quant', variable_name+'_corte']).mean()
    elif(function=='COUNT'):
        x = x[[variable_name+'_quant', variable_name+'_corte', default]].groupby(
            [variable_name+'_quant', variable_name+'_corte']).count()
    elif(function=='COUNT_NORM'):
        temp = x[[variable_name+'_quant', variable_name+'_corte', default]].groupby([variable_name+'_quant', variable_name+'_corte']).count()
        length = len(x)
        temp[default+'_countnorm'] = 1.*temp[default]/length 
		
        x = temp[[default+'_countnorm']]
		
    else:
        print ('Invalid function ... defaulting to mean function')
        x = x[[variable_name+'_quant', variable_name+'_corte', default]].groupby(
            [variable_name+'_quant', variable_name+'_corte']).mean()

    x = x.reset_index().drop(variable_name+'_quant', axis=1)
    x = x.set_index(variable_name+'_corte')
        
        
    return x
###################################### FUNCION DE INICIALIZACION DE LA BASE #####################################################

def inicializar_reniec(reniec):
#    reniec.loc[:,'RENTABASICA'] = reniec['RENTABASICA'].map(round)
    reniec = reniec.dropna(subset=['DEPARTAMENTO'])
    reniec.loc[:,'RUCCOMPANIA'] = reniec['RUCCOMPANIA'].map(str).apply(lambda x: x.zfill(8))
    reniec = reniec[(reniec['MES1']<1) | (reniec['MES1'].isna())]
    reniec = reniec.drop(['GBSM00', 'GBSM01', 'GBSM02', 'GBSM03', 'GBSM04',
       'GBSM05', 'GBSM06', 'GBSM07', 'GBSM08', 'GBSM09', 'GBSM10',
       'GBSM11', 'GBSM12', 'SUSPMORAM00',
       'SUSPMORAM01', 'SUSPMORAM02', 'SUSPMORAM03', 'SUSPMORAM04',
       'SUSPMORAM05', 'SUSPMORAM06', 'SUSPMORAM07', 'SUSPMORAM08',
       'SUSPMORAM09', 'SUSPMORAM10', 'SUSPMORAM11', 'SUSPMORAM12', 'CICLO', 
                          'FLAGDEFAULT', 'MANTIGCLIENTE', 'TIPO_DOC', 'DM_MAX', 'MES1', 'RENTABASICA'], axis=1)
    
#CORREGIMOS LOS CAMPSO QUE CAUSAN DUPLICADOS
                    
    indexes = reniec[['RUCCOMPANIA', 'PERIODO', 'CONTRATO']].drop_duplicates().index.tolist()
    reniec = reniec[reniec.index.isin(indexes)]
    
    reniec = reniec.groupby(['CODMES', 'SCORE', 'PERIODO', 'CONTRATO', 'CODUNICOCLI',
       'RUCCOMPANIA', 'COMPANIA', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
       'PRODUCTO', 'N_PLAN',
       'LOGINTIENDA', 'PRECIOPAGADO', 'CODSBS',
       'FLAG_MALO', 'DDATR1MSF_F', 'VAR721_F','VAR1009_F',
'VAR1004_F', 'VAR1006_F', 'VAR704_F', 'PRPNOR3MSF_F', 'VAR1010_F',
'CNTENR12MSF_F', 'VAR719_F', 'VAR1005_F', 'DDVNCOPRR1MSF_F', 'VAR1007_F']).max().reset_index()
    
#SUMAMOS LOS MEGAS PARA LAS ENTRADAS DUPLICADAS 

    reniec = reniec.groupby(['CODMES', 'SCORE', 'PERIODO', 'CONTRATO', 'CODUNICOCLI',
       'RUCCOMPANIA', 'COMPANIA', 'DEPARTAMENTO', 'PROVINCIA', 'DISTRITO',
       'PRODUCTO', 'N_PLAN',
       'LOGINTIENDA', 'PRECIOPAGADO', 'CODSBS',
       'FLAG_MALO', 'DDATR1MSF_F', 'VAR721_F','VAR1009_F',
'VAR1004_F', 'VAR1006_F', 'VAR704_F', 'PRPNOR3MSF_F', 'VAR1010_F',
'CNTENR12MSF_F', 'VAR719_F', 'VAR1005_F', 'DDVNCOPRR1MSF_F', 'VAR1007_F', 'RANKPROBSCORE']).sum().reset_index()

#NUMERO DE MESES CON INFO DE DATOS

    reniec.loc[:,'N_MESES_DATOS'] = (reniec['GBTM01']!=0).map(int)+(reniec['GBTM02']!=0).map(int)+(reniec['GBTM03']!=0).map(int)+(reniec['GBTM04']!=0).map(int)+(reniec['GBTM05']!=0).map(int)+(reniec['GBTM06']!=0).map(int)

    reniec = reniec[reniec['N_MESES_DATOS']>4]
    
    return reniec.drop(['COMPANIA', 'DEPARTAMENTO', 'PROVINCIA', 'N_PLAN', 
       'LOGINTIENDA', 'PRECIOPAGADO'], axis=1)

############################################ FUNCION GET FLAGS FACEBOOK #########################################################

def get_flags_facebook():
    print('Obteniendo los flags de Facebook')
    arr = []
    for i in range(3,13):
        temp_new = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/flags_2017'+str(i).zfill(2)+'_cruzado.csv')
        temp_new['PERIODO'] = 201700+i
        temp_new['RUCCOMPANIA'] = temp_new['RUCCOMPANIA'].map(str).apply( lambda x: x.zfill(8) )
        arr.append(temp_new)
    
    new = pd.concat(arr)
    print('FIN')
    return new.drop(['EDAD','CODSBS', 'SCOREBURO'], axis=1)

################################################## FUNCION GET INGRESOS #########################################################

def get_ingresos():
    print ('Obtenemos los ingresos de la base FB ...')
    arr = []
    for i in range(3,13):
        temp_new = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/ingreso_2017'+str(i).zfill(2)+'_cruzado.csv')
        arr.append(temp_new)
    for i in range(1,4):
        temp_new = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/ingreso_2018'+str(i).zfill(2)+'_cruzado.csv')
        arr.append(temp_new)
    
    new = pd.concat(arr)
    new['RUCCOMPANIA'] = new['RUCCOMPANIA'].map(str).apply(lambda x:x.zfill(8))
    print('FIN')
    return new.drop(['EDAD', 'CODSBS', 'CODDOC'], axis=1)

##################################################### FUNCION GET HISTORIAL #####################################################

def get_Historial_FB():
    print ('Armanado historial ...')
    start = 1
    end = 16
    historial_FB = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/flags_2017'+str(start).zfill(2)+'_cruzado.csv')
    print(historial_FB.columns.values)
    historial_FB = historial_FB[['RUCCOMPANIA', 'CODSBS', 'MODELOSCORE']]

    historial_FB.columns = ['RUCCOMPANIA', 'CODSBS', 'MODELOSCORE_%d'%start]
    for i in range(start+1,13):
        temp_new = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/flags_2017'+str(i).zfill(2)+'_cruzado.csv')
        temp_new = temp_new[['RUCCOMPANIA', 'MODELOSCORE']]
        temp_new.columns = ['RUCCOMPANIA', 'MODELOSCORE_%d'%i]
        historial_FB = pd.merge(historial_FB, temp_new, on='RUCCOMPANIA', how='outer')
    
    for i in range(13,end):
        temp_new = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Flags_NoBank/flags_2018'+str(i-12).zfill(2)+'_cruzado.csv')
        temp_new = temp_new[['RUCCOMPANIA', 'MODELOSCORE']]
        temp_new.columns = ['RUCCOMPANIA', 'MODELOSCORE_%d'%i]
        historial_FB = pd.merge(historial_FB, temp_new, on='RUCCOMPANIA', how='outer')
    
    historial_FB['RUCCOMPANIA'] = historial_FB['RUCCOMPANIA'].map(str).apply(lambda x: x.zfill(8))    
    historial_FB = historial_FB.set_index('RUCCOMPANIA')
    historial_FB = rellenar_historial_FB(historial_FB, start+1)
    historial_FB = create_mes_bancarizacion(historial_FB, start)
    print ('FIN')
    return historial_FB

#RELLENAMOS LOS MESES A LSO QUE LES FALTA MODELOSCORE
def rellenar_historial_FB(historial_FB, minimo):    
    #RELLENAMOS SANGUCHES 
    print ('Rellenando los vacíos ...')
    for n_sanguche in range(1,12):
        for i in range(minimo,16-n_sanguche):
            historial_FB['MODELOSCORE_%d'%i] = np.where( 
                ( ( historial_FB['MODELOSCORE_%d'%i].isna() ) & 
                 (historial_FB['MODELOSCORE_%d'%(i-1)]==historial_FB['MODELOSCORE_%d'%(i+n_sanguche)]) ) |
                ( ( historial_FB['MODELOSCORE_%d'%i].isna() ) & ( (historial_FB['MODELOSCORE_%d'%(i-1)]=='NON PREMIUM PROVINCIA')
                | (historial_FB['MODELOSCORE_%d'%(i-1)]=='NON PREMIUM LIMA O EN BLANCO') ) ), 
                historial_FB['MODELOSCORE_%d'%(i+n_sanguche)], 
                historial_FB['MODELOSCORE_%d'%(i)]
            )
    #RELLENAMOS LOS 'NO HIT' DE ADELANTE PARA ATRAS

    for i in range(minimo,16):
         historial_FB['MODELOSCORE_%d'%(14+minimo-i)] = np.where( ( historial_FB['MODELOSCORE_%d'%(14+minimo-i)].isna() ) & 
                                                  ( historial_FB['MODELOSCORE_%d'%(15+minimo-i)]=='HIT SIN INFORMACION/NO HIT' ), 
                                                 'HIT SIN INFORMACION/NO HIT', historial_FB['MODELOSCORE_%d'%(14+minimo-i)])            
    for i in range(minimo,16):
         historial_FB['MODELOSCORE_%d'%(i)] = np.where( ( historial_FB['MODELOSCORE_%d'%(i)].isna() ) & 
                                                  ( historial_FB['MODELOSCORE_%d'%(i-1)]=='HIT SIN INFORMACION/NO HIT' ), 
                                                 'HIT SIN INFORMACION/NO HIT', historial_FB['MODELOSCORE_%d'%(i)])
    print ('FIN')
    return historial_FB.drop(['CODSBS'], axis=1)

#CREAMOS VARIABLE "MES BANCARIZACION"
def create_mes_bancarizacion(historial_FB, start, end=15):
    print ('Creando la variable "MES_BANCARIZACION ...')
    lista = [ (historial_FB['MODELOSCORE_%d'%i]=='HIT SIN INFORMACION/NO HIT') & 
                                        ((historial_FB['MODELOSCORE_%d'%(i+1)]!='HIT SIN INFORMACION/NO HIT') &
                                         ~(historial_FB['MODELOSCORE_%d'%(i+1)].isna())) for i in range(start,end) ]

    historial_FB['MES_BANCARIZACION'] = np.select(lista, range(start+1, end+1), 0)
    print ('FIN')
    return historial_FB

######################################## FUNCION PARA OBTENER LAS LLAMADAS Y LOS NODOS ##########################################

def get_llamadas_nodos(reniec):
#JALAMOS LAS VARIABLES DE LLAMADAS

    llamadas_1 = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Llamadas_Entel_1.csv')
    llamadas_2 = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Llamadas_Entel_2.csv')

    llamadas = pd.concat([llamadas_1, llamadas_2]).drop('TIPO_DOC', axis=1)
    llamadas = llamadas[ ~(llamadas['RUCCOMPANIA'].map(str).map(len)>8) ].drop(['FLAGDEFAULT'], axis=1)
    llamadas['RUCCOMPANIA'] = llamadas['RUCCOMPANIA'].map(str).apply(lambda x: x.zfill(8))  #HACEMOS EL DNI UN INTEGER

    llamadas['RATIO_MINS'] = np.where(llamadas['MIN_ENTRANTES']==0, 0,llamadas['MIN_SALIENTE']/llamadas['MIN_ENTRANTES'])

    llamadas['RATIO_LLAMADAS'] = np.where(llamadas['LLAM_ENTRANTES']==0, 0,llamadas['LLAM_SALIENTES']/llamadas['LLAM_ENTRANTES'])

    llamadas['MINS_POR_LLAMADA_E'] = np.where(llamadas['LLAM_ENTRANTES']==0, 0,llamadas['MIN_ENTRANTES']/llamadas['LLAM_ENTRANTES'])

    llamadas['MINS_POR_LLAMADA_S'] = np.where(llamadas['LLAM_SALIENTES']==0, 0,llamadas['MIN_SALIENTE']/llamadas['LLAM_SALIENTES'])

    llamadas = llamadas.groupby(['CONTRATO', 'PERIODO', 'RUCCOMPANIA']).max().reset_index()

    print(len(llamadas[['CONTRATO', 'PERIODO', 'RUCCOMPANIA']]))

#UNIMOS LAS VARIABLES DE LLAMADAS

    base_miner = pd.merge(reniec, llamadas, on=['RUCCOMPANIA', 'CONTRATO', 'PERIODO'], how='inner')

#CREAMOS LA NUEVA VARIABLE DE NODOS
    nodos_mean = base_miner['NODOS'].mean()
    base_miner['NODOS_2'] = (base_miner['NODOS']-nodos_mean)*(base_miner['NODOS']-nodos_mean)

    print (len(base_miner))
    print (len(reniec))
    
    return base_miner

################################################### CREATE MODEL VARIABLE #######################################################

def create_modelvariable(miner):
    miner['MODEL'] = miner['PRODUCTO'].apply(
    lambda x: x.upper()).apply(
    lambda x: x.replace('J5', 'GALAXYJ5')).apply(
    lambda x: x.replace('NEGRO', '')).apply(
    lambda x: x.replace('BLACK', '')).apply(
    lambda x: x.replace('BROWN', '')).apply(
    lambda x: x.replace('OSCURO', '')).apply(
    lambda x: x.replace('BLANCO', '')).apply(
    lambda x: x.replace('GRIS', '')).apply(
    lambda x: x.replace('GREY', '')).apply(
    lambda x: x.replace('BLUE', '')).apply(
    lambda x: x.replace('AZUL', '')).apply(
    lambda x: x.replace('VIOLETA', '')).apply(
    lambda x: x.replace('PLATA', '')).apply(
    lambda x: x.replace('DORADO', '')).apply(
    lambda x: x.replace('GOLD', '')).apply(
    lambda x: x.replace('SILVER', '')).apply(
    lambda x: x.replace('CORAL', '')).apply(
    lambda x: x.replace('(', '')).apply(
    lambda x: x.replace(')', '')).apply(
    lambda x: x.replace('SPACE', '')).apply(
    lambda x: x.replace('8GB', '')).apply(
    lambda x: x.replace('16GB', '')).apply(
    lambda x: x.replace('32GB', '')).apply(
    lambda x: x.replace('64GB', '')).apply(
    lambda x: x.replace('256GB', '')).apply(
    lambda x: x.replace('8G', '')).apply(
    lambda x: x.replace('16G', '')).apply(
    lambda x: x.replace('64G', '')).apply(
    lambda x: x.replace('256G', '')).apply(
    lambda x: x.replace('ESPACIAL', '')).apply(
    lambda x: x.replace('TITAN', '')).apply(
    lambda x: x.replace('SAMSUNG GALAXY', 'SAMSUNG')).apply(
    lambda x: x.replace('SAMSUNG', 'GALAXY')).apply(
    lambda x: x.replace('LG', '')).apply(
    lambda x: x.replace('SAM', '')).apply(
    lambda x: x.replace('NEO', '')).apply(
    lambda x: x.replace('HUAWEI', '')).apply(
    lambda x: x.replace('SMRT', '')).apply(
    lambda x: x.replace(' ', '')).apply(
    lambda x: x.replace('P9LITE2017', 'P9LITE')).apply(
    lambda x: x.replace('MOTOG4GENPLAY', 'MOTOG4PLAY')).apply(
    lambda x: x.replace('MOTOG4GEN', 'MOTOG4')).apply(
    lambda x: x.split('PLUS')[0])
    return miner

def create_megasvariable(miner):
    miner.loc[:,'GBT_mean'] = (
        miner['GBTM01']+miner['GBTM02']+miner['GBTM06']+
        miner['GBTM03']+miner['GBTM04']+miner['GBTM05']
        )/(miner['N_MESES_DATOS'])

    miner.loc[:,'GBT_var'] = (
        (miner['GBTM01']-miner['GBT_mean'])*(miner['GBTM01']-miner['GBT_mean'])+
        (miner['GBTM02']-miner['GBT_mean'])*(miner['GBTM02']-miner['GBT_mean'])+
        (miner['GBTM03']-miner['GBT_mean'])*(miner['GBTM03']-miner['GBT_mean'])+
        (miner['GBTM04']-miner['GBT_mean'])*(miner['GBTM04']-miner['GBT_mean'])+
        (miner['GBTM05']-miner['GBT_mean'])*(miner['GBTM05']-miner['GBT_mean'])+
        (miner['GBTM06']-miner['GBT_mean'])*(miner['GBTM06']-miner['GBT_mean'])
        )/(miner['N_MESES_DATOS'])
    
    miner['GBT_var_mean'] = miner['GBT_var']/miner['GBT_mean']
    
    miner.dropna(subset=['GBT_var_mean'])
    
    miner.dropna(subset=['GBTM00', 'GBTM01', 'GBTM02', 'GBTM03', 'GBTM04', 'GBTM05'])
    return miner.drop(['GBTM00', 'GBTM01', 'GBTM02', 'GBTM03', 'GBTM04', 'GBTM05', 'GBTM06', 'GBTM07', 'GBTM08',
       'GBTM09', 'GBTM10', 'GBTM11', 'GBTM12'], axis=1)

################################################### FILTROS FINALES #############################################################

def filtros_finales(miner_fb):
    miner = miner_fb.dropna(subset=['FLAG_MALO']).drop_duplicates()
    
#FILTROS FINALES
    if (len(miner)>10000 and 'GBT_var' in miner.columns.values):
        limit_var = miner['GBT_var'].quantile(0.99)
        limit_mean = miner['GBT_mean'].quantile(0.99)
        lower_limit_var = miner['GBT_var'].quantile(0.0)
        lower_limit_mean = miner['GBT_mean'].quantile(0.00)
        
        print (limit_var)
        print (limit_mean)
        miner_6 = miner[(miner['GBT_var']<limit_var) & (miner['GBT_var']>lower_limit_var) &
                        (miner['GBT_mean']<limit_mean) & (miner['GBT_mean']>lower_limit_mean)
                       ]
    else:
        miner_6 = miner.copy()
    
    #JUNTAMOS LOS DISTRITOS CON POCA POBLACION
    
    a = miner_6[['DISTRITO', 'FLAG_MALO']].groupby('DISTRITO').count().reset_index()

    #LIMITS
    limit1=40
    limit2=100
    limit3=200

    less_50 = a[a['FLAG_MALO']<limit1]['DISTRITO']
    greater_50 = a[(a['FLAG_MALO']>=limit1) & (a['FLAG_MALO']<limit2)]['DISTRITO']
    greater_100 = a[(a['FLAG_MALO']>=limit2) & (a['FLAG_MALO']<limit3)]['DISTRITO']

    miner_6.loc[:,'DISTRITO2'] = np.select([miner_6['DISTRITO'].isin(less_50), 
                                      miner_6['DISTRITO'].isin(greater_50), 
                                      miner_6['DISTRITO'].isin(greater_100)
                                     ],
                                     ['Otros_1', 'Otros_2', 'Otros_3'
                                     ], miner_6['DISTRITO'])
    
    miner_6.loc[:,'DISTRITO3'] = np.select([miner_6['DISTRITO2'].isin(['SANTIAGO DE SURCO', 
                                                        'MIRAFLORES', 'SAN ISIDRO', 
                                                        'LA MOLINA', 'SAN BORJA']),
                               miner_6['DISTRITO2'].isin(['INDEPENDENCIA', 'VENTANILLA', 'VILLA MARIA DEL TRIUNFO', 'CALLAO',
                                                        'VILLA EL SALVADOR', 
                                                        'PIURA', 'SAN JUAN DE MIRAFLORES',
                                                       'LA VICTORIA', 'LURIGANCHO'
                                                       ])], [
    'DISTRITO_TOP', 'DISTRITO_RIESGOSO'], miner_6['DISTRITO2'])

    miner_6.loc[:,'DISTRITO_TOP'] = np.where(miner_6['DISTRITO3']=='DISTRITO_TOP', 1, 0)
    miner_6.loc[:,'DISTRITO_RIESGOSO'] = np.where(miner_6['DISTRITO3']=='DISTRITO_RIESGOSO', 1, 0)
    
    #CREAMOS EL FLAG DE BANCARIZADO
    
    miner_6.loc[:,'BANCARIZADO'] = np.where(miner_6['MODELOSCORE']=='HIT SIN INFORMACION/NO HIT', 0, 1)
      
    #ELIMINAMOS LAS VARIABLES DE LLAMADAS Y DATOS QUE SON REDUNDANTES
    
    for var in ['MIN_ENTRANTES', 'MIN_SALIENTE', 'LLAM_ENTRANTES', 'LLAM_SALIENTES', 
                            'RATIO_LLAMADAS', 'MINS_POR_LLAMADA_E', 'MINS_POR_LLAMADA_S', 'GBT_var']:
        if (var in miner_6.columns.values):
            miner_6 = miner_6.drop(var, axis=1)
    
    #AÑADIMOS CAMPOS DE RENIEC QUE FALTAN
    reniec = pd.read_csv('C:/Users/b35884/Desktop/Bases Entel/Entel_final_reniec.csv')
    reniec = reniec[['RUCCOMPANIA', 'EDAD', 'ESTADOCIVILTITULAR', 'GENERO']].drop_duplicates()
    reniec.loc[:,'RUCCOMPANIA'] = reniec['RUCCOMPANIA'].map(str).apply(lambda x:x.zfill(8))
    miner_6 = pd.merge(miner_6, reniec, on=['RUCCOMPANIA'], how='left')
    
    faltantes_reniec = reniec
    return miner_6