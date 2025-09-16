import streamlit as st
import pandas as pd
from datetime import datetime, date
import os

# Importar o gerador de proposta
from gerador_proposta import gerar_proposta, EMPRESA_CONTRATADA, CLIENTE, SERVICOS, TERMOS

# Configuração da página
st.set_page_config(
    page_title="Gerador de Orçamento - GPM",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para interface moderna e limpa
st.markdown("""
<style>
    .main-header {
        text-align: center;
        background: linear-gradient(90deg, #3498db 0%, #2980b9 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .total-card {
        background: linear-gradient(135deg, #2ecc71 0%, #27ae60 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(46, 204, 113, 0.3);
    }
    .stButton>button {
        background: linear-gradient(45deg, #3498db, #2980b9);
        color: white;
        border-radius: 8px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 600;
        transition: all 0.3s;
        box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(52, 152, 219, 0.4);
    }
    .sidebar-logo {
        text-align: center;
        padding: 1rem;
        background: linear-gradient(135deg, #3498db, #2980b9);
        border-radius: 10px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 6px rgba(52, 152, 219, 0.3);
    }
</style>
""", unsafe_allow_html=True)

# Sidebar com informações da empresa e preview
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">
        <h3 style="color: white; margin: 0;">🏢 GPM DESENTUPIDORA</h3>
        <p style="color: #ecf0f1; margin: 0; font-size: 0.9rem;">Sistema de Orçamentos</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Logo se existir
    if os.path.exists("assets/gpm_desentupidora.png"):
        st.image("assets/gpm_desentupidora.png", width=250)
    
    st.markdown("### 📊 Resumo do Orçamento")
    
    # Inicializar dados no session_state
    if 'cliente_nome' not in st.session_state:
        st.session_state.cliente_nome = CLIENTE["nome"]
    # Inicializar serviços no session_state se não existir
    if 'servicos_lista' not in st.session_state:
        st.session_state.servicos_lista = [
            {
                "descricao": "",
                "tipo_medida": "metragem", 
                "quantidade": 0,
                "preco_unitario": 50.0
            }
        ]
    
    # Calcular total para o sidebar
    total_sidebar = 0
    for s in st.session_state.servicos_lista:
        if s["tipo_medida"] == "unitario":
            total_sidebar += s["quantidade"] * s["preco_unitario"]
        else:  # metragem
            total_sidebar += s["preco_unitario"]
    
    # Métricas no sidebar
    col1, col2 = st.columns(2)
    with col1:
        st.metric("📋 Serviços", len([s for s in st.session_state.servicos_lista if s.get("descricao", "").strip()]))
    with col2:
        st.metric("💰 Total", f"R$ {total_sidebar:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    st.markdown("---")
    
    # Preview rápido
    st.markdown("### 👁️ Preview Rápido")
    if st.session_state.cliente_nome:
        st.write(f"**Cliente:** {st.session_state.cliente_nome[:30]}{'...' if len(st.session_state.cliente_nome) > 30 else ''}")
    
    for i, servico in enumerate(st.session_state.servicos_lista[:3]):
        if servico.get("descricao", "").strip():
            if servico["tipo_medida"] == "unitario":
                valor = servico["quantidade"] * servico["preco_unitario"]
            else:  # metragem
                valor = servico["preco_unitario"]
            st.write(f"**{i+1}.** {servico['descricao'][:25]}{'...' if len(servico['descricao']) > 25 else ''}")
            st.write(f"   💰 R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    
    if len(st.session_state.servicos_lista) > 3:
        st.write(f"... e mais {len(st.session_state.servicos_lista) - 3} serviços")

# Cabeçalho principal
st.markdown("""
<div class="main-header">
    <h1 style="margin: 0; font-size: 2.5rem;">💰 Gerador de Orçamento Profissional</h1>
    <p style="margin: 0.5rem 0 0 0; font-size: 1.2rem; opacity: 0.9;">Sistema completo para criação de orçamentos personalizados</p>
</div>
""", unsafe_allow_html=True)

# Abas principais
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📋 Cliente", 
    "🏢 GPM Dados", 
    "💼 Serviços", 
    "⚙️ Configurações", 
    "👁️ Preview", 
    "📄 Gerar PDF"
])

# ==================== ABA 1: DADOS DO CLIENTE ====================
with tab1:
    st.markdown("## 📋 Informações do Cliente")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.session_state.cliente_nome = st.text_input(
            "Nome da Empresa Cliente *",
            value=st.session_state.cliente_nome,
            placeholder="Digite o nome completo da empresa",
            help="Campo obrigatório"
        )
        
        cliente_endereco = st.text_area(
            "Endereço Completo *",
            value=CLIENTE["endereco"],
            placeholder="Rua, número, bairro, cidade - UF",
            height=100,
            help="Endereço onde será realizado o serviço"
        )
    
    with col2:
        cliente_cnpj = st.text_input(
            "CNPJ/CPF",
            value=CLIENTE["cnpj"],
            placeholder="XX.XXX.XXX/XXXX-XX ou XXX.XXX.XXX-XX",
            help="CNPJ da empresa ou CPF da pessoa física"
        )
        
        cliente_cep = st.text_input(
            "CEP",
            value=CLIENTE["cep"],
            placeholder="XXXXX-XXX",
            help="CEP para localização"
        )
        
        cliente_contato = st.text_input(
            "Telefone/E-mail",
            placeholder="(61) 99999-9999 ou email@empresa.com",
            help="Contato para comunicação"
        )

# ==================== ABA 2: DADOS DA GPM ====================
with tab2:
    st.markdown("## 🏢 Dados da GPM Desentupidora")
    
    col1, col2 = st.columns(2)
    
    with col1:
        empresa_nome = st.text_input(
            "Razão Social:",
            value=EMPRESA_CONTRATADA["nome"],
            help="Nome completo da empresa"
        )
        
        empresa_nome_fantasia = st.text_input(
            "Nome Fantasia:",
            value=EMPRESA_CONTRATADA["nome_fantasia"],
            help="Nome fantasia que aparece no cabeçalho"
        )
        
        empresa_cnpj = st.text_input(
            "CNPJ:",
            value=EMPRESA_CONTRATADA["cnpj"],
            help="CNPJ da empresa"
        )
        
        empresa_endereco = st.text_area(
            "Endereço:",
            value=EMPRESA_CONTRATADA["endereco"],
            height=80,
            help="Endereço completo da empresa"
        )
        
        empresa_cidade = st.text_input(
            "Cidade/Estado:",
            value=EMPRESA_CONTRATADA["cidade"],
            help="Cidade e estado"
        )
    
    with col2:
        empresa_cep = st.text_input(
            "CEP:",
            value=EMPRESA_CONTRATADA["cep"],
            help="CEP da empresa"
        )
        
        empresa_telefones = st.text_input(
            "Telefones:",
            value=EMPRESA_CONTRATADA["telefones"],
            help="Telefones de contato"
        )
        
        empresa_email = st.text_input(
            "E-mail:",
            value=EMPRESA_CONTRATADA["email"],
            help="E-mail principal"
        )
        
        empresa_site = st.text_input(
            "Site:",
            value=EMPRESA_CONTRATADA["site"],
            help="Website da empresa"
        )
        
        empresa_inscricao = st.text_input(
            "Inscrição Estadual:",
            value=EMPRESA_CONTRATADA["inscricao_estadual"],
            help="Número da inscrição estadual"
        )
    
    st.info("💡 Estes dados aparecerão no PDF do orçamento como informações da empresa contratada.")

# ==================== ABA 3: SERVIÇOS ====================
with tab3:
    st.markdown("## 💼 Serviços e Valores")
    
    # Botões de ação
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1])
    
    with col1:
        if st.button("➕ Adicionar Serviço", type="secondary"):
            st.session_state.servicos_lista.append({"descricao": "", "tipo_medida": "metragem", "quantidade": 0, "preco_unitario": 50.0})
            st.rerun()
    
    with col2:
        if st.button("🗑️ Remover Último", type="secondary") and len(st.session_state.servicos_lista) > 1:
            st.session_state.servicos_lista.pop()
            st.rerun()
    
    with col3:
        if st.button("📋 Duplicar Último", type="secondary") and st.session_state.servicos_lista:
            ultimo_servico = st.session_state.servicos_lista[-1].copy()
            st.session_state.servicos_lista.append(ultimo_servico)
            st.rerun()
    
    with col4:
        if st.button("🧹 Limpar Tudo", type="secondary"):
            st.session_state.servicos_lista = [{"descricao": "", "tipo_medida": "metragem", "quantidade": 0, "preco_unitario": 50.0}]
            st.rerun()
    
    st.markdown("---")
    
    # Lista de serviços
    total_geral = 0
    
    for i, servico in enumerate(st.session_state.servicos_lista):
        st.markdown(f"### 🔧 Serviço {i+1}")
        
        # Descrição do serviço
        st.session_state.servicos_lista[i]["descricao"] = st.text_area(
            "Descrição detalhada do serviço:",
            value=servico["descricao"],
            key=f"desc_{i}",
            placeholder="Ex: Desentupimento e lavagem da rede de esgoto...",
            height=80
        )
        
        # Valores em colunas
        col1, col2, col3, col4, col5 = st.columns([1, 1, 1, 1, 1])
        
        with col1:
            st.session_state.servicos_lista[i]["tipo_medida"] = st.selectbox(
                "Tipo:",
                ["unitario", "metragem"],
                index=0 if servico["tipo_medida"] == "unitario" else 1,
                key=f"tipo_{i}",
                help="Unitário: quantidade × preço | Metragem: metros × valor total"
            )
        
        with col2:
            if servico["tipo_medida"] == "unitario":
                label_quantidade = "Quantidade:"
                help_quantidade = "Número de unidades"
            else:
                label_quantidade = "Metros:"
                help_quantidade = "Quantidade em metros lineares"
                
            st.session_state.servicos_lista[i]["quantidade"] = st.number_input(
                label_quantidade,
                min_value=0,
                value=servico["quantidade"],
                key=f"quantidade_{i}",
                help=help_quantidade
            )
        
        with col3:
            if servico["tipo_medida"] == "unitario":
                label_preco = "Preço unitário (R$):"
                help_preco = "Valor por unidade"
            else:
                label_preco = "Valor total (R$):"
                help_preco = "Valor total pelos metros"
                
            st.session_state.servicos_lista[i]["preco_unitario"] = st.number_input(
                label_preco,
                min_value=0.0,
                value=servico["preco_unitario"],
                format="%.2f",
                key=f"preco_{i}",
                help=help_preco
            )
        
        with col4:
            if servico["tipo_medida"] == "unitario":
                # Para unitário: quantidade × preço unitário
                preco_total = servico["quantidade"] * servico["preco_unitario"]
            else:
                # Para metragem: o valor já é o total
                preco_total = servico["preco_unitario"]
            
            total_geral += preco_total
            st.metric("💰 Total do Serviço", f"R$ {preco_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        
        with col5:
            if len(st.session_state.servicos_lista) > 1:
                if st.button(f"❌ Remover", key=f"remove_{i}", type="secondary"):
                    st.session_state.servicos_lista.pop(i)
                    st.rerun()
        
        st.divider()
    
    # Total geral destacado
    st.markdown(f'''
    <div class="total-card">
        <h2 style="margin: 0;">💰 VALOR TOTAL DO ORÇAMENTO</h2>
        <h1 style="margin: 0.5rem 0 0 0; font-size: 3rem;">R$ {total_geral:,.2f}</h1>
    </div>
    '''.replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

# ==================== ABA 4: CONFIGURAÇÕES ====================
with tab4:
    st.markdown("## ⚙️ Configurações do Orçamento")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📅 Data e Validade")
        
        data_proposta = st.date_input(
            "Data do orçamento:",
            value=date.today(),
            help="Data que aparecerá no documento"
        )
        
        validade_proposta = st.selectbox(
            "Validade do orçamento:",
            [
                "15 (quinze) dias consecutivos",
                "30 (trinta) dias consecutivos", 
                "45 (quarenta e cinco) dias consecutivos", 
                "60 (sessenta) dias consecutivos",
                "90 (noventa) dias consecutivos"
            ],
            index=1,
            help="Prazo de validade da proposta"
        )
        
        local_proposta = st.text_input(
            "Local da proposta:",
            value="Brasília - DF",
            help="Cidade onde será emitida a proposta"
        )
    
    with col2:
        st.markdown("### 💳 Condições de Pagamento")
        
        prazo_pagamento = st.selectbox(
            "Forma de pagamento:",
            [
                "À vista com desconto de 5%",
                "À vista",
                "Entrada + 2x no cartão",
                "Entrada + 3x no cartão", 
                "Entrada + 5x no boleto (a cada 15 dias)",
                "50% entrada + 50% na conclusão",
                "30% entrada + 70% na conclusão",
                "Parcelado em 6x no boleto"
            ],
            index=4,
            help="Condições de pagamento oferecidas"
        )
        
        prazo_entrega = st.selectbox(
            "Prazo de execução:",
            [
                "Imediato (até 24h)",
                "Até 2 dias úteis",
                "Até 5 dias úteis",
                "Conforme cronograma acordado",
                "A definir com o cliente"
            ],
            index=3,
            help="Prazo para execução dos serviços"
        )
        
        observacoes = st.text_area(
            "Observações adicionais:",
            placeholder="Informações extras para o orçamento...",
            help="Campo opcional para observações"
        )

# ==================== ABA 5: PREVIEW ====================
with tab5:
    st.markdown("## 👁️ Preview do Orçamento")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown("### 📋 Dados do Cliente")
        st.write(f"**Empresa:** {st.session_state.cliente_nome}")
        st.write(f"**CNPJ/CPF:** {cliente_cnpj}")
        st.write(f"**Endereço:** {cliente_endereco}")
        st.write(f"**CEP:** {cliente_cep}")
        
        st.markdown("### ⚙️ Configurações")
        st.write(f"**Data:** {data_proposta.strftime('%d/%m/%Y')}")
        st.write(f"**Local:** {local_proposta}")
        st.write(f"**Validade:** {validade_proposta}")
        st.write(f"**Pagamento:** {prazo_pagamento}")
        st.write(f"**Execução:** {prazo_entrega}")
    
    with col2:
        st.markdown("### 💼 Serviços Inclusos")
        
        servicos_validos = [s for s in st.session_state.servicos_lista if s.get("descricao", "").strip()]
        
        if servicos_validos:
            for i, servico in enumerate(servicos_validos):
                if servico["tipo_medida"] == "unitario":
                    valor_servico = servico["quantidade"] * servico["preco_unitario"]
                    display_calculo = f"{servico['quantidade']} un × R$ {servico['preco_unitario']:.2f}"
                else:  # metragem
                    valor_servico = servico["preco_unitario"]
                    display_calculo = f"{servico['quantidade']}m = R$ {servico['preco_unitario']:.2f}"
                
                st.write(f"**{i+1}.** {servico['descricao']}")
                st.write(f"   📏 {display_calculo} = **R$ {valor_servico:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
                st.write("---")
            
            # Calcular total preview com a nova lógica
            total_preview = 0
            for s in servicos_validos:
                if s["tipo_medida"] == "unitario":
                    total_preview += s["quantidade"] * s["preco_unitario"]
                else:  # metragem
                    total_preview += s["preco_unitario"]
            
            st.markdown(f"### 💰 **TOTAL: R$ {total_preview:,.2f}**".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            st.write("⚠️ Nenhum serviço adicionado ainda")

# ==================== ABA 6: GERAR PDF ====================
with tab6:
    st.markdown("## 📄 Gerar e Baixar Orçamento")
    
    # Validações
    servicos_validos = [s for s in st.session_state.servicos_lista if s.get("descricao", "").strip()]
    
    # Calcular total final com a nova lógica
    total_final = 0
    for s in servicos_validos:
        if s["tipo_medida"] == "unitario":
            total_final += s["quantidade"] * s["preco_unitario"]
        else:  # metragem
            total_final += s["preco_unitario"]
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Status do orçamento
        st.markdown("### ✅ Status do Orçamento")
        
        if st.session_state.cliente_nome.strip():
            st.success("✅ Nome do cliente preenchido")
        else:
            st.error("❌ Nome do cliente é obrigatório")
        
        if servicos_validos:
            st.success(f"✅ {len(servicos_validos)} serviço(s) adicionado(s)")
        else:
            st.error("❌ Adicione pelo menos um serviço")
        
        if total_final > 0:
            st.success(f"✅ Valor total: R$ {total_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        else:
            st.error("❌ O valor total deve ser maior que zero")
        
        # Botão principal
        pode_gerar = st.session_state.cliente_nome.strip() and servicos_validos and total_final > 0
        
        if st.button("🚀 GERAR ORÇAMENTO PDF", type="primary", disabled=not pode_gerar, use_container_width=True):
            if pode_gerar:
                # Atualizar dados globais
                import gerador_proposta
                
                gerador_proposta.CLIENTE = {
                    "nome": st.session_state.cliente_nome,
                    "cnpj": cliente_cnpj,
                    "endereco": cliente_endereco,
                    "cep": cliente_cep
                }
                
                # Atualizar dados da empresa com os valores editados
                gerador_proposta.EMPRESA_CONTRATADA = {
                    "nome": empresa_nome,
                    "nome_fantasia": empresa_nome_fantasia,
                    "cnpj": empresa_cnpj,
                    "endereco": empresa_endereco,
                    "cidade": empresa_cidade,
                    "cep": empresa_cep,
                    "site": empresa_site,
                    "telefones": empresa_telefones,
                    "inscricao_estadual": empresa_inscricao,
                    "email": empresa_email
                }
                
                gerador_proposta.SERVICOS = servicos_validos
                
                gerador_proposta.TERMOS = {
                    "prazo_entrega": prazo_entrega,
                    "prazo_pagamento": prazo_pagamento,
                    "validade_proposta": validade_proposta
                }
                
                # Converter data para texto em português
                meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho",
                        "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
                mes_nome = meses[data_proposta.month - 1]
                gerador_proposta.DATA_PROPOSTA = f"{data_proposta.day} de {mes_nome} de {data_proposta.year}"
                gerador_proposta.LOCAL_PROPOSTA = local_proposta
                
                try:
                    with st.spinner("Gerando orçamento..."):
                        gerador_proposta.gerar_proposta()
                    
                    st.success("🎉 Orçamento gerado com sucesso!")
                    
                    # Botão de download
                    if os.path.exists("proposta.pdf"):
                        with open("proposta.pdf", "rb") as file:
                            nome_arquivo = f"orcamento_{st.session_state.cliente_nome.replace(' ', '_').replace('/', '_')}_{data_proposta.strftime('%Y%m%d')}.pdf"
                            st.download_button(
                                label="⬇️ BAIXAR ORÇAMENTO PDF",
                                data=file.read(),
                                file_name=nome_arquivo,
                                mime="application/pdf",
                                type="primary",
                                use_container_width=True
                            )
                
                except Exception as e:
                    st.error(f"❌ Erro ao gerar orçamento: {str(e)}")
    
    with col2:
        st.markdown("### 📊 Resumo Final")
        st.markdown(f'<div class="preview-card">', unsafe_allow_html=True)
        st.metric("Cliente", st.session_state.cliente_nome[:20] + "..." if len(st.session_state.cliente_nome) > 20 else st.session_state.cliente_nome)
        st.metric("Serviços", len(servicos_validos))
        st.metric("Valor Total", f"R$ {total_final:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        st.metric("Data", data_proposta.strftime("%d/%m/%Y"))
        st.markdown('</div>', unsafe_allow_html=True)

# Rodapé
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 2rem; background: linear-gradient(90deg, #1f4e79 0%, #2980b9 100%); border-radius: 10px; color: white; margin-top: 2rem;'>
    <h3 style="margin: 0;">🏢 GPM DESENTUPIDORA</h3>
    <p style="margin: 0.5rem 0;">Sistema Profissional de Geração de Orçamentos</p>
    <p style="margin: 0; opacity: 0.8;">📞 (61) 4104-4143 | 📱 (61) 99242-3009 | 📧 contato@gpmdesentupidora.com.br</p>
</div>
""", unsafe_allow_html=True)