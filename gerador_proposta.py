"""
Gerador de Proposta Comercial em PDF
Biblioteca utilizada: reportlab
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import datetime
import locale
import os

# ================================================================================
# CONFIGURAÇÃO DOS DADOS - EDITE AQUI PARA PERSONALIZAR A PROPOSTA
# ================================================================================

# Dados da Empresa Contratada
EMPRESA_CONTRATADA = {
    "nome": "GPM COMÉRCIO, TRANSPORTE E LIMPEZA LTDA",
    "nome_fantasia": "GPM DESENTUPIDORA",
    "cnpj": "17.908.156/0001-78",
    "endereco": "Setor de Oficinas, quadra 1 conjunto 02 lote 17 - loja 1",
    "cidade": "Brasília - DF",
    "cep": "71262-110",
    "site": "www.gpmdesentupidora.com.br",
    "telefones": "(61) 4104-4143 / (61) 99242-3009",
    "inscricao_estadual": "0763965500104",
    "email": "contato@gpmdesentupidora.com.br"
}

# Dados do Cliente
CLIENTE = {
    "nome": "CAPITAL INDUSTRIA E COM DE PRODUTOS RECICLAVEIS LTDA",
    "cnpj": "06.096.335/0001-31",
    "endereco": "ST SCIA QUADRA 09 CONJUNTO 01 LOTE 01- BRASÍLIA -DF",
    "cep": "71250-810"
}

# Serviços da Proposta
SERVICOS = [
    {
        "descricao": "Desentupimento e lavagem da rede de esgoto. (início das caixas até final do muro)",
        "tipo_medida": "metragem",  # "metragem" ou "unidade"
        "quantidade": 260,
        "preco_unitario": 50.00
    },
    {
        "descricao": "Desentupimento e lavagem da rede de esgoto.(interno)",
        "tipo_medida": "metragem",
        "quantidade": 120,
        "preco_unitario": 50.00
    },
    {
        "descricao": "Limpeza de caixa de gordura",
        "tipo_medida": "unidade",
        "quantidade": 2,
        "preco_unitario": 150.00
    }
]

# Termos e Condições
TERMOS = {
    "prazo_pagamento": "Entrada +5x no boleto (a cada 15 dias)",
    "validade_proposta": "30 (trinta) dias consecutivos",
    "prazo_entrega": "Conforme cronograma acordado"
}

# Data da Proposta
DATA_PROPOSTA = "30 de outubro de 2024"
LOCAL_PROPOSTA = "Brasília - DF"

# ================================================================================
# FUNÇÕES AUXILIARES
# ================================================================================

def formatar_moeda(valor):
    """Formata valor para padrão brasileiro de moeda"""
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def criar_estilos():
    """Cria os estilos personalizados para o documento"""
    styles = getSampleStyleSheet()
    
    # Estilo para cabeçalho da empresa
    styles.add(ParagraphStyle(
        name='CabecalhoEmpresa',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=12,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para título do documento
    styles.add(ParagraphStyle(
        name='TituloDocumento',
        parent=styles['Heading2'],
        fontSize=16,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para seções
    styles.add(ParagraphStyle(
        name='TituloSecao',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    ))
    
    # Estilo para texto normal
    styles.add(ParagraphStyle(
        name='TextoNormal',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_LEFT,
        spaceAfter=4,
        fontName='Helvetica'
    ))
    
    # Estilo para texto centralizado
    styles.add(ParagraphStyle(
        name='TextoCentro',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.black,
        alignment=TA_CENTER,
        spaceAfter=4,
        fontName='Helvetica'
    ))
    
    return styles

def criar_tabela_servicos():
    """Cria a tabela de serviços e preços"""
    styles = criar_estilos()
    
    # Cabeçalho da tabela
    dados_tabela = [
        ['ESPECIFICAÇÃO DE SERVIÇO', 'Quantidade', 'Preço Unitário', 'Preço Total']
    ]
    
    # Adiciona os serviços
    total_geral = 0
    for servico in SERVICOS:
        if servico['tipo_medida'] == "unitario":
            quantidade_str = f"{servico['quantidade']} un"
            preco_unitario_str = formatar_moeda(servico['preco_unitario'])
            preco_total = servico['quantidade'] * servico['preco_unitario']
        else:  # metragem
            quantidade_str = f"{servico['quantidade']}m"
            preco_unitario_str = "Valor total"
            preco_total = servico['preco_unitario']
        
        preco_total_str = formatar_moeda(preco_total)
        total_geral += preco_total
        
        # Criar Paragraph para a descrição permitir quebra de linha
        descricao_paragraph = Paragraph(servico['descricao'], styles['TextoNormal'])
        
        dados_tabela.append([
            descricao_paragraph,
            quantidade_str,
            preco_unitario_str,
            preco_total_str
        ])
    
    # Linha de total
    dados_tabela.append([
        'TOTAL',
        '',
        '',
        formatar_moeda(total_geral)
    ])
    
    # Criar tabela com larguras definidas para permitir quebra de linha adequada
    tabela = Table(dados_tabela, colWidths=[10*cm, 2.5*cm, 2.5*cm, 3*cm])
    
    # Estilo da tabela
    estilo_tabela = TableStyle([
        # Cabeçalho
        ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        
        # Dados
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('FONTNAME', (0, 1), (-1, -2), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -2), 9),
        ('ALIGN', (1, 1), (-1, -1), 'CENTER'),
        ('ALIGN', (0, 1), (0, -2), 'LEFT'),
        ('VALIGN', (0, 1), (0, -2), 'TOP'),
        
        # Linha de total
        ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, -1), (-1, -1), 10),
        
        # Bordas
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        
        # Ajustar padding para melhor aparência
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ])
    
    tabela.setStyle(estilo_tabela)
    return tabela

def gerar_proposta():
    """Função principal para gerar o PDF da proposta"""
    # Criar documento com margens menores
    doc = SimpleDocTemplate(
        "proposta.pdf",
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1*cm,
        bottomMargin=1.5*cm
    )
    
    # Obter estilos
    styles = criar_estilos()
    
    # Lista para armazenar elementos do documento
    elementos = []
    
    # 1. Logo da Empresa (centralizada)
    caminho_logo = os.path.join("assets", "gpm_desentupidora.png")
    if os.path.exists(caminho_logo):
        logo = Image(caminho_logo, width=6*cm, height=3*cm)
        logo.hAlign = 'CENTER'
        elementos.append(logo)
        elementos.append(Spacer(1, 0.2*cm))
    else:
        # Se não encontrar a imagem, usa texto como fallback
        elementos.append(Paragraph(EMPRESA_CONTRATADA["nome_fantasia"], styles['CabecalhoEmpresa']))
        elementos.append(Spacer(1, 0.2*cm))
    
    # 2. Título do Documento
    elementos.append(Paragraph("ORÇAMENTO", styles['TituloDocumento']))
    elementos.append(Spacer(1, 0.2*cm))
    
    # 3. Dados do Cliente
    elementos.append(Paragraph("À Administração", styles['TituloSecao']))
    elementos.append(Paragraph(f"<b>Empresa:</b> {CLIENTE['nome']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>CNPJ/CPF:</b> {CLIENTE['cnpj']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>Endereço:</b> {CLIENTE['endereco']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>CEP:</b> {CLIENTE['cep']}", styles['TextoNormal']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # 4. Dados da Empresa Contratada
    elementos.append(Paragraph("Dados da Empresa Contratada", styles['TituloSecao']))
    elementos.append(Paragraph(f"<b>Empresa:</b> {EMPRESA_CONTRATADA['nome']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>Endereço:</b> {EMPRESA_CONTRATADA['endereco']}, {EMPRESA_CONTRATADA['cidade']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>CEP:</b> {EMPRESA_CONTRATADA['cep']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>CNPJ:</b> {EMPRESA_CONTRATADA['cnpj']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>Site:</b> {EMPRESA_CONTRATADA['site']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>Telefones:</b> {EMPRESA_CONTRATADA['telefones']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>Inscrição Estadual:</b> {EMPRESA_CONTRATADA['inscricao_estadual']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"<b>E-mail:</b> {EMPRESA_CONTRATADA['email']}", styles['TextoNormal']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # 5. Texto Introdutório
    texto_intro = """
    Prezados Senhores,<br/><br/>
    Temos a satisfação de apresentar nossa proposta comercial para os serviços de desentupimento, 
    conforme solicitação. Nossa empresa possui vasta experiência no mercado e está preparada para 
    atender suas necessidades com qualidade e pontualidade.
    """
    elementos.append(Paragraph(texto_intro, styles['TextoNormal']))
    elementos.append(Spacer(1, 0.3*cm))
    
    # 6. Tabela de Serviços
    elementos.append(Paragraph("Serviços e Preços", styles['TituloSecao']))
    elementos.append(criar_tabela_servicos())
    elementos.append(Spacer(1, 0.3*cm))
    
    # 7. Termos e Condições
    elementos.append(Paragraph("Termos e Condições", styles['TituloSecao']))
    elementos.append(Paragraph("• Os preços apresentados incluem todos os impostos e custos necessários para execução dos serviços.", styles['TextoNormal']))
    elementos.append(Paragraph(f"• <b>Prazo de Entrega:</b> {TERMOS['prazo_entrega']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"• <b>Prazo de Pagamento:</b> {TERMOS['prazo_pagamento']}", styles['TextoNormal']))
    elementos.append(Paragraph(f"• <b>Validade da Proposta:</b> {TERMOS['validade_proposta']}", styles['TextoNormal']))
    elementos.append(Spacer(1, 0.8*cm))
    
    # 8. Encerramento e Assinaturas
    elementos.append(Paragraph(f"{LOCAL_PROPOSTA}, {DATA_PROPOSTA}", styles['TextoCentro']))
    elementos.append(Spacer(1, 0.6*cm))
    
    # Criar tabela para as assinaturas lado a lado
    dados_assinaturas = [
        ["_" * 35, "_" * 35],
        ["Assinatura da Empresa", "Assinatura do Cliente"],
        [f"{EMPRESA_CONTRATADA['nome']}", ""],
        [f"CNPJ: {EMPRESA_CONTRATADA['cnpj']}", ""]
    ]
    
    tabela_assinaturas = Table(dados_assinaturas, colWidths=[9*cm, 9*cm])
    
    estilo_assinaturas = TableStyle([
        # Linha das assinaturas
        ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        
        # Labels das assinaturas
        ('ALIGN', (0, 1), (-1, 1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, 1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 1), (-1, 1), 10),
        
        # Dados da empresa
        ('ALIGN', (0, 2), (0, 3), 'CENTER'),
        ('FONTNAME', (0, 2), (0, 3), 'Helvetica'),
        ('FONTSIZE', (0, 2), (0, 3), 9),
        
        # Remover bordas
        ('GRID', (0, 0), (-1, -1), 0, colors.white),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        
        # Espaçamento
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ])
    
    tabela_assinaturas.setStyle(estilo_assinaturas)
    elementos.append(tabela_assinaturas)
    
    # Gerar PDF
    doc.build(elementos)
    print("Proposta gerada com sucesso! Arquivo: proposta.pdf")

# ================================================================================
# EXECUÇÃO
# ================================================================================

if __name__ == "__main__":
    gerar_proposta()