class MessageFormatter:
    def format_cotation(self, informacoes, template):
        return template.format(
            nome=informacoes["nome"],
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"]
        )

    def format_conversion(self, informacoes, valor, template):
        return template.format(
            nome=informacoes["nome"],
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"],
            conv=valor
        )

class ConversionCalculator:
    def calcular(self, cotacao, valor):
        try:
            venda = float(cotacao["ask"])
            return float(valor) * venda
        except Exception as e:
            print(f"Erro ao calcular conversão: {e}")
            return None
