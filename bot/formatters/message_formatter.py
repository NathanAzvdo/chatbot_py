class MessageFormatter:
    def format_cotation(self, informacoes, template_parts):
        template = (
            template_parts["inicio"] +
            template_parts["compra"] +
            template_parts["venda"] +
            template_parts["alta"] +
            template_parts["baixa"] +
            template_parts["fim"]
        )
        return template.format(
            nome=informacoes["nome"],
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"]
        )

    def format_conversion(self, informacoes, valor, template_parts):
        template = (
            template_parts["inicio"] +
            template_parts["valor"] +
            template_parts["compra"] +
            template_parts["venda"] +
            template_parts["alta"] +
            template_parts["baixa"] +
            template_parts["fim"]
        )
        return template.format(
            nome=informacoes["nome"],
            conv=valor,
            bid=informacoes["bid"],
            ask=informacoes["ask"],
            alta=informacoes["alta"],
            baixa=informacoes["baixa"]
        )

class ConversionCalculator:
    def calcular(self, cotacao, valor):
        try:
            venda = float(cotacao["ask"])
            return float(valor) * venda
        except Exception as e:
            print(f"Erro ao calcular conversão: {e}")
            return None
