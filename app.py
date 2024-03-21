import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.io as pio

st.set_page_config(page_title='Violencia Sexual', layout='wide')

df = pd.read_csv('Violencia_Intrafamiliar.csv', low_memory=False, sep=',')
df_modificable = df.copy()

df_modificable.DEPARTAMENTO = df_modificable.DEPARTAMENTO.str.capitalize()
df_modificable.MUNICIPIO = df_modificable.MUNICIPIO.str.capitalize()
df_modificable.rename(columns={'ARMAS MEDIOS': 'Armas'}, inplace=True)
df_modificable.Armas = df_modificable.Armas.str.title()
df_modificable.GENERO = df_modificable.GENERO.str.capitalize()
df_modificable.rename(columns={'GRUPO ETARIO': 'Etario'}, inplace=True)
df_modificable.Etario = df_modificable.Etario.str.title()

df_modificable['DEPARTAMENTO'] = df_modificable['DEPARTAMENTO'].astype('object')
departamento = list(df_modificable['DEPARTAMENTO'].unique())

def municipios(departamento):
    municipios_departamentos = df_modificable[df_modificable['DEPARTAMENTO'] == departamento]['MUNICIPIO'].unique()
    return municipios_departamentos
    

pio.templates.default = 'plotly_white'

# COMIENZA EL DASHBOARD
    
st.header('Violencia Sexual Colombia 2022', divider='rainbow')


departamento_seleccionado = st.selectbox('Seleccione Departamento', departamento, index=None, placeholder='Departamento')
selec_municipios = st.multiselect('Municipio', options=municipios(departamento_seleccionado), placeholder='Municipios')

if departamento_seleccionado != None:
    df_modificable = df_modificable[df_modificable['DEPARTAMENTO'] == departamento_seleccionado]
if len(selec_municipios) > 0 :
    df_modificable = df_modificable[df_modificable['MUNICIPIO'].isin(selec_municipios)]

st.metric('Registros', len(df_modificable))

c1,c2 = st.columns([75,25], gap='small')

with c1:
    departamento_group = df_modificable.groupby(['MUNICIPIO']).agg({
        'CANTIDAD':'count'
    })   
    fig = px.bar(
        departamento_group,
    )
    
    fig.update_layout(title='Cantidad de casos por Municipio')
    fig.update_xaxes(title='Municipio')
    fig.update_yaxes(title='Cantidad')
    fig.update_layout(showlegend=False)
    
    st.plotly_chart(fig)
    
with c2:
    st.dataframe(departamento_group)

st.divider()

c3, c4 = st.columns([50,50], gap='medium')

with c3:    
    Etarios = df_modificable.groupby('Etario').count()
    Etarios = Etarios.reset_index()
        
    fig = px.pie(
            Etarios,
            values ='CANTIDAD',
            names='Etario',
            title='Cantidad de casos por Grupos Etarios'
        )
        
    fig.update_layout(legend_title='Grupo Etario', legend_title_side='left')
    fig.update_layout(width=500, height=500)
        
    st.plotly_chart(fig)

with c4:  
    genero = df_modificable.groupby('GENERO').count()
    genero = genero.reset_index()
        
    fig = px.bar(
            genero,
            x='GENERO',
            y='CANTIDAD',
            color='GENERO',
            title='Cantidad de casos por Generos'
        )

    fig.update_layout(width=500, height=500)
    fig.update_xaxes(title='Genero')
    fig.update_yaxes(title='Cantidad')
    fig.update_layout(showlegend=False)
    st.plotly_chart(fig)
    
st.divider()

col5 = st.columns([100], gap='small')

armas_group = df_modificable.groupby(['Armas']).count()
armas_group = armas_group.reset_index()

fig = px.bar(
    armas_group,
    x='Armas',
    y='CANTIDAD',
    color='Armas',
    title='Cantidad de abusus por Tipo de Armas'
)

fig.update_xaxes(title='Armas')
fig.update_yaxes(title='Cantidad')
fig.update_layout(showlegend=False)
st.plotly_chart(fig)