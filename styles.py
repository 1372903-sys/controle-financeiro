import streamlit as st

def apply_styles():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Playfair+Display:wght@700&display=swap');
        
        /* Paleta de Prosperidade: 
           Verde Esmeralda: #2e7d32
           Dourado: #d4af37
           Azul Marinho: #1a237e
        */
        
        .main {
            background-color: transparent;
        }
        
        /* Título Sofisticado com Degradê de Prosperidade */
        .sophisticated-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 700;
            background: linear-gradient(45deg, #1a237e, #2e7d32, #d4af37);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-align: center;
            margin-top: 2rem;
            margin-bottom: 0.2rem;
            letter-spacing: -1px;
            line-height: 1.2;
        }
        
        .sophisticated-subtitle {
            font-family: 'Inter', sans-serif;
            font-size: 0.9rem;
            color: #2e7d32; /* Verde Prosperidade */
            text-align: center;
            margin-bottom: 3rem;
            text-transform: uppercase;
            letter-spacing: 5px;
            font-weight: 800;
        }
        
        /* Dark Mode Support */
        @media (prefers-color-scheme: dark) {
            .sophisticated-title {
                background: linear-gradient(45deg, #d4af37, #66bb6a, #ffffff);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
            }
            .sophisticated-subtitle {
                color: #d4af37; /* Dourado no Dark Mode */
            }
        }

        /* Cartões de Métricas Estilizados */
        div[data-testid="stMetric"] {
            background-color: rgba(46, 125, 50, 0.05); /* Fundo verde leve */
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(46, 125, 50, 0.1);
            border: 1px solid rgba(212, 175, 55, 0.3); /* Borda dourada sutil */
        }
        
        /* Botões de Prosperidade */
        .stButton>button {
            background: linear-gradient(45deg, #1a237e, #2e7d32) !important;
            color: white !important;
            border-radius: 10px;
            font-weight: 600;
            transition: all 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
            border: none !important;
        }
        
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(46, 125, 50, 0.3);
            background: linear-gradient(45deg, #2e7d32, #d4af37) !important;
        }

        /* Tabelas e Dataframes */
        .stDataFrame {
            border-radius: 15px;
            overflow: hidden;
            border: 1px solid rgba(46, 125, 50, 0.1);
        }

        /* Ajustes para Mobile */
        @media (max-width: 768px) {
            .sophisticated-title {
                font-size: 2.2rem;
            }
            .sophisticated-subtitle {
                font-size: 0.7rem;
                letter-spacing: 3px;
            }
        }
        </style>
    """, unsafe_allow_html=True)
