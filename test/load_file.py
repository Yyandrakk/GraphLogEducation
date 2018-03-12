import pandas as pd

def load(path):
    dateparse = lambda x: pd.datetime.strptime(x, '%d/%m/%Y %H:%M')
    df = pd.read_csv(path,parse_dates=['Hora'], date_parser=dateparse, dayfirst=True)
    filter=df.apply(lambda fila: fila.iloc[1] != '-' and "Administrador" not in fila.iloc[1],axis=1)
    df=df[filter]
    #print(df)
    #n_unicos = list(df['Nombre completo del usuario'].unique()))
    print (df['Nombre completo del usuario'].unique())
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

    for fila in pd.DataFrame({'count': df.groupby([pd.Grouper(key='Nombre completo del usuario'),times.hour]).size()}).reset_index().itertuples():
        print(fila._1)

if __name__ == '__main__':
    load("../media/user_1/logs_2017_18464_311_20171211-1635.csv")
