import scrapy

# Define uma spider do Scrapy para coletar dados
class MercadolivreSpider(scrapy.Spider):
    name = "mercadolivre" # Nome da spider
    start_urls = ["https://lista.mercadolivre.com.br/tenis-corrida-feminino"] # URL inicial
    page_count = 1 # Conta o número de páginas já visitadas
    max_pages = 10 # Limita o número de páginas a serem processadas

    def parse(self, response):
         # Seleciona os produtos na página atual
        products = response.css('div.ui-search-result__content')
        
        # Para cada produto encontrado, extrai os dados desejados
        for product in products:
            prices = product.css('span.andes-money-amount__fraction::text').getall() # Valores inteiros dos preços
            cents = product.css('span.andes-money-amount__cents::text').getall() # Centavos dos preços

            # Retorna os dados do produto como um dicionário
            yield {
                'brand': product.css('span.ui-search-item__brand-discoverability.ui-search-item__group__element::text').get(), # Marca do produto
                'name': product.css('h2.ui-search-item__title::text').get(), # Nome do produto
                'old_price_reais': prices[0] if len(prices) > 0 else None, # Parte inteira do preço antigo
                'old_price_centavos': cents[0] if len(cents) > 0 else None, # Centavos do preço antigo
                'new_price_reais': prices[1] if len(prices) > 1 else None, # Parte inteira do preço novo
                'new_price_centavos': cents[1] if len(cents) > 1 else None, # Centavos do preço novo
                'reviews_rating_number': product.css('span.ui-search-reviews__rating-number::text').get(), # Avaliação média
                'reviews_amount': product.css('span.ui-search-reviews__amount::text').get() # Quantidade de avaliações
            }
            
        # Verifica se deve continuar para a próxima página    
        if self.page_count < self.max_pages:
            next_page = response.css('li.andes-pagination__button.andes-pagination__button--next a::attr(href)').get() # Link da próxima página
            if next_page:
                self.page_count += 1 # Atualiza o contador de páginas
                yield scrapy.Request(url=next_page, callback=self.parse) # Faz uma nova requisição para a próxima página

