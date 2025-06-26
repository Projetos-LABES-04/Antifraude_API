_____________________________________________________________________________________________________________________________________________________________________________________________________________________
SOBRE O PROJETO:
 -
 Projeto Antifraude
  O projeto está estruturado da seguinte forma:

## OBJETIVO:
 -
Desenvolver um sistema antifraude capaz de identificar transações financeiras suspeitas e mapear comportamentos típicos de contas bancárias com base no histórico de transações, permitindo detectar possíveis anomalias em tempo real. O projeto adota uma abordagem que combina o mapeamento do comportamento padrão por conta com um módulo de inferência inteligente, responsável por identificar desvios em relação ao padrão esperado e classificar o risco de cada transação.

 ESCOPO:
-
As transações representam movimentações realizadas por clientes, como saques, transferências e pagamentos. A análise dessas transações permite identificar perfis de comportamento e detectar possíveis desvios com base em padrões históricos.

 INTRODUÇÃO:
-
A aplicação combina técnicas de aprendizado não supervisionado (Autoencoder + KMeans), regras heurísticas e modelos supervisionados (XGBoost) para identificar comportamentos anômalos em transações financeiras. O objetivo é apoiar a equipe de controle na identificação rápida de possíveis fraudes em contas bancárias. Toda a solução foi construída em Python, com uma API desenvolvida em FastAPI, integração com MongoDB e uma interface de visualização criada em Angular, proporcionando uma experiência completa de análise, monitoramento e gestão de alertas.

 BASE DE DADOS:
 -
As bases de dados utilizadas foram construídas com transações sintéticas de múltiplas contas, contendo atributos como:
transacao_id, cliente_id, conta_id, data, valor, tipo, mesma_titularidade, entre outros.
Além disso, foram adicionadas variáveis derivadas como faixa horária, fim de semana, cluster de comportamento, erro de reconstrução, entre outros.


 TECNOLOGIAS UTILIZADAS:
-
Backend: Python, FastAPI, Pydantic

Machine Learning: TensorFlow (Autoencoder), Scikit-learn (KMeans, ANOVA, GLM)

Frontend: React, Axios

Hospedagem: Render, Vercel

Banco de Dados: MongoDB

 ESTRUTURA DO PROJETO:
-

antifraude_api/
│
├── app/
│   ├── main.py                     
│   ├── config.py                    
│   ├── database/
│   │   ├── mongodb.py             
│   │   └── schemas/                 
│   ├── models/
│   │   ├── transacao.py            
│   │   ├── conta.py                
│   │   ├── cliente.py             
│   │   └── notificacao.py         
│   ├── routes/
│   │   ├── transacoes.py            
│   │   ├── contas.py                
│   │   ├── notificacoes.py          
│   │   ├── dashboard.py             
│   │   └── auth.py                  
│   ├── services/
│   │   ├── inferencia_comportamento.py  
│   │   ├── inferencia_anomalia.py       
│   │   └── notificacoes.py              
│   ├── utils/
│   │   ├── pre_processamento.py         
│   │   ├── auth_utils.py                
│   │   └── logger.py                    
│   └── tests/
│       ├── test_transacoes.py           
│       ├── test_dashboard.py            
│       └── conftest.py                 
│
├── modelos/                              
│   ├── scaler.pkl
│   ├── modelo_autoencoder.keras
│   ├── kmeans_auto.pkl
│   ├── modelo_xgboost.pkl
│   └── ...
│
├── .env                                  
├── requirements.txt                      
├── README.md                             
├── Procfile                              
└── start.sh 


•comando inicialização uvicorn:
   uvicorn app.main:app --reload

 CONCLUSÃO:
 -
O sistema antifraude entrega uma solução robusta, baseada em inteligência artificial, para análise de transações bancárias. Ele permite detectar rapidamente desvios comportamentais por conta e classificar o nível de suspeita com justificativas interpretáveis. A ferramenta visa fortalecer a segurança operacional e apoiar investigações da equipe de controle.
_____________________________________________________________________________________________________________________________________________________________________________________________________________________
