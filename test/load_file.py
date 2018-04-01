import pandas as pd

def load(path):
    dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')
    df = pd.read_csv(path,parse_dates=['Hora'], date_parser=dateparse, dayfirst=True)
    filter=df.apply(lambda fila: fila.iloc[1] != '-' and "Administrador" not in fila.iloc[1],axis=1)
    df=df[filter]

    # print(list(df['Contexto del evento'].unique()))
    #print(df)
    #n_unicos = list(df['Nombre completo del usuario'].unique()))
    # print (df['Nombre completo del usuario'].unique())
    # fil_arc = df[df['Contexto del evento'].str.contains("Archivo:")]
    # fil_cues =  df[df['Contexto del evento'].str.contains("Cuestionario:")]
    # fil_arc_cues = df[fil_arc] or df[fil_cues]
    # #aux = df.loc[fil_arc_cues,'Contexto del evento']
    # aux=df['Contexto del evento'].where(lambda t: "Archivo:" in t or "Cuestionario:" in t).dropna()
    # func = lambda s: s.split(':')[1].strip()auth_group_permissions
    # print(list(map(func,fil_arc['Contexto del evento'].unique())))
    # print(set(map(func, fil_cues['Contexto del evento'].unique())))
    times = pd.DatetimeIndex(df['Hora'])
    #print(df.groupby(pd.Grouper(key='Hora', freq='24H')).count())
    # aux=pd.DataFrame({'count': df.groupby(pd.Grouper(key='Hora', freq='D')).size()}).reset_index()
    # print(pd.DataFrame({'count' :df.groupby(pd.Grouper(key='Hora', freq='D')).size()}).reset_index())
    #aux = pd.DataFrame({'count':df.groupby([times.hour]).size()}).reset_index()
    #print(pd.DataFrame({'count':df.groupby([times.hour]).size()}).reset_index())
    #print(type(aux.iloc[0,0]))
    #for fila in pd.DataFrame({'count':df.groupby([times.hour]).size()}).reset_index().itertuples():
        #print(pd.to_datetime(fila.Hora, unit='h'))
    #print(pd.DataFrame({'count': df.groupby([pd.Grouper(key='Nombre completo del usuario'),pd.Grouper(key='Hora', freq='D')]).size()}).reset_index())
    #print( df.sort_values(by=['Nombre completo del usuario', 'Hora']))
    '''std_name = ''
    time_invertido = 0
    fecha_anterior = None
    umbral_sec= 5*60
    for fila in df.sort_values(by=['Nombre completo del usuario', 'Hora']).itertuples():
        if std_name != fila._2.strip():
            print("{0} time: {1}".format(std_name,time_invertido))
            std_name =  fila._2.strip()
            time_invertido = 0
        fecha = pd.to_datetime(fila.Hora, unit='s')
        if fecha_anterior != None and (fecha - fecha_anterior).seconds <umbral_sec:
            time_invertido += (fecha - fecha_anterior).seconds
        fecha_anterior=fecha
        '''

    for fila in df.loc[(df['Nombre completo del usuario'] == "Maria Muñoz Sanz") & df['Nombre evento'].isin(['Ha comenzado el intento','Intento enviado'])].sort_values(by=['Nombre completo del usuario','Contexto del evento','Hora']).itertuples():
        print('Name: {0}, Fecha: {1}, Contexto: {2}, Nombre evento: {3}'.format(fila._2,fila.Hora, fila._4,fila._6))








if __name__ == '__main__':
    load("../media/user_1/curso_Prueba/logs_2017_18464_311_20171211-1635.csv")
