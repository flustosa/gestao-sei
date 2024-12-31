import requests
import datetime
import xml.etree.ElementTree as ElTree


def parse_response(response, sucesso, sigla_sistema, token, unidade, processo, url, andamento):
    """Validação anterior ao lançamento do andamento no processo. WebService retorna '1' para sucesso.
    Qualquer outro valor deve ser considerado algum tipo de erro e envia a mensagem de volta para a função de origem"""
    resultado = ElTree.fromstring(response.text)
    try:
        msg_erro = "\n Erro: " + resultado[0][0][1].text
        erro = 1
        return msg_erro, erro
    except:
        resultado_parse = resultado[0][0][0].text
        if resultado_parse == "1":
            lancar_andamento(sigla_sistema, token, unidade, processo, url, andamento)
            erro = 0
            return sucesso, erro

def bloquear_processo(sigla_sistema, token, unidade, processo, url, motivo, usuario):
    sucesso = f"\n Processo {processo} bloqueado com sucesso!"
    andamento = f"Motivo do bloqueio: {motivo}. Usuario: {usuario}"
    payload = f"""<?xml version=\"1.0\" encoding=\"utf-8\"?>\n
    <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\n
        <soap:Body>\n
            <bloquearProcesso>\n
                <SiglaSistema>{sigla_sistema}</SiglaSistema>\n
                <IdentificacaoServico>{token}</IdentificacaoServico>\n
                <IdUnidade>{unidade}</IdUnidade>\n
                <ProtocoloProcedimento>{processo}</ProtocoloProcedimento>\n
            </bloquearProcesso>\n
        </soap:Body>\n
    </soap:Envelope>"""
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8',
        'SOAPAction': 'SeiAction'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    resultado = parse_response(response, sucesso, sigla_sistema, token, unidade, processo, url, andamento)
    return resultado


def desbloquear_processo(sigla_sistema, token, unidade, processo, url, motivo, usuario):
    sucesso = f"\n Processo {processo} desbloqueado com sucesso!"
    andamento = f"Motivo do desbloqueio: {motivo}. Usuario: {usuario}"
    payload = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
    <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\
        <soap:Body>\
            <desbloquearProcesso>\
                <SiglaSistema>{sigla_sistema}</SiglaSistema>\
                <IdentificacaoServico>{token}</IdentificacaoServico>\
                <IdUnidade>{unidade}</IdUnidade>\
                <ProtocoloProcedimento>{processo}</ProtocoloProcedimento>\
            </desbloquearProcesso>\
        </soap:Body>\
    </soap:Envelope>"""
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8',
        'SOAPAction': 'SeiAction'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    resultado = parse_response(response, sucesso, sigla_sistema, token, unidade, processo, url, andamento)
    return resultado

#FIXME: O encode padrão do SEI é ISO-8859-1. Em testes com o Tkinter essa configuração do XML funcionou.
# Na configuração atual está ignorando os erros de encoding para evitar falha, mas não manda caracteres Latin-1.
def lancar_andamento(sigla_sistema, token, unidade, processo, url, andamento):
    """Lança andamento nos processos. Gera log das operações apenas para fins gerenciais, para que seja possível
    verificar o total de operações na aplicação, pois o SEI gera logs na Auditoria para fins de controle."""
    id_andamento = '65'
    sucesso = f"\n Lançamento enviado no processo {processo} com sucesso!"
    andamento_encode = andamento.encode("iso-8859-1")
    andamento_decode = andamento_encode.decode("utf_8", errors="ignore")

    payload = f"""<?xml version=\"1.0\" encoding=\"UTF-8\"?>\
    <soap:Envelope xmlns:soap=\"http://schemas.xmlsoap.org/soap/envelope/\">\
        <soap:Body>\
            <lancarAndamento>\
                <SiglaSistema>{sigla_sistema}</SiglaSistema>\
                <IdentificacaoServico>{token}</IdentificacaoServico>\
                <IdUnidade>{unidade}</IdUnidade>\
                <ProtocoloProcedimento>{processo}</ProtocoloProcedimento>\
                <IdTarefa>{id_andamento}</IdTarefa>\
                <IdTarefaModulo></IdTarefaModulo>\
                    <Atributos>\
                        <AtributoAndamento>\
                            <Nome>DESCRICAO</Nome>\
                            <Valor>{andamento_decode}</Valor>\
                        </AtributoAndamento>\
                    </Atributos>\
            </lancarAndamento>\
        </soap:Body>\
    </soap:Envelope>"""
    headers = {
        'Content-Type': 'text/xml; charset=UTF-8',
        'SOAPAction': 'SeiAction'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    time = str(datetime.datetime.now())
    f = open("wslog.txt", "a")
    f.write(time + '\n' + "Status code: " + str(response.status_code) + '\n' + "Response content: " + '\n' + str(
        response.content.decode("utf_8",
                                errors="ignore")) + '\n' + "Ambiente: " + url + "************************" + '\n')
    f.close()

    if response.status_code == 500:
        return response.status_code
    else:
        return sucesso
