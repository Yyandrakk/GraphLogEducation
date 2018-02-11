import pandas as pd


def load(path):
    df = pd.read_csv(path)
    n_unicos = list(filter(lambda n: n != '-' and "Administrador" not in n,df['Nombre completo del usuario'].unique()))
    print (n_unicos)
    fil_arc = "Archivo:" in df['Contexto del evento']
    # fil_cues = "Cuestionario:" in df['Contexto del evento']
    # fil_arc_cues = df[fil_arc] or df[fil_cues]
    # #aux = df.loc[fil_arc_cues,'Contexto del evento']
    # aux=df['Contexto del evento'].where(lambda t: "Archivo:" in t or "Cuestionario:" in t).dropna()
    print (fil_arc)


if __name__ == '__main__':
    load("../media/user_1/logs_2017_18464_311_20171211-1635.csv")
