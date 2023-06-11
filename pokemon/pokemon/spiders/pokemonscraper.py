import scrapy
from pokemon.items import PokemonItem

class PokemonscraperSpider(scrapy.Spider):
    name = "pokemonscraper"
    allowed_domains = ["pokemon.fandom.com"]
    start_urls = ["https://pokemon.fandom.com/wiki/List_of_Pok%C3%A9mon"]
    
    custom_settings = {
        'FEEDS': { 'pokemonList.csv': { 'format': 'csv',}}
    }

    def parse(self, response):
        table = response.css('table.wikitable tbody tr')
        for pokemon in table:
            pokemonInfo = pokemon.css('td')
            
            # Check if the row of the table is header
            if len(pokemonInfo) == 0:
                continue
            
            next_page_url = 'https://pokemon.fandom.com/' + pokemonInfo[2].css('a').attrib['href']
            yield response.follow(next_page_url, callback=self.parse_pokemon_page)

        print('---- END ----')

    def parse_pokemon_page(self, response):
        pokemon = PokemonItem()
        
        pokemonInfo = response.css('div.wds-tab__content.wds-is-current')
        statRows = response.css('table.roundy tr')
        statRows.pop(0)

        pokemon['img_url'] = pokemonInfo.css('img.pi-image-thumbnail').attrib['src'],
        pokemon['name'] = pokemonInfo.xpath("//h2[@data-source='name']/text()").get(),
        pokemon['japanese'] = pokemonInfo.xpath("//h2[@data-source='ja_name']/text()").get(),
        pokemon['types'] = pokemonInfo.css('div.pi-item.pi-data.pi-item-spacing.pi-border-color div.pi-data-value.pi-font a').attrib['title'].split(' ')[0],
        pokemon['species'] = pokemonInfo.xpath("//div[@data-source='species']/div[@class='pi-data-value pi-font']/text()").get(),
        pokemon['ability'] = self.retrievingAbilities(response),    
        pokemon['evoform'] = pokemonInfo.xpath("//div[@data-source='evofrom']/div").css('div ::text').get(),
        pokemon['evointo'] = pokemonInfo.xpath("//div[@data-source='evointo']/div").css('div ::text').get(),
        pokemon['hp'] = statRows[0].css('td')[1].css('td ::text').get(),
        pokemon['attack'] = statRows[1].css('td')[1].css('td ::text').get(),
        pokemon['defense'] = statRows[2].css('td')[1].css('td ::text').get(),
        pokemon['sp_atk'] = statRows[3].css('td')[1].css('td ::text').get(),
        pokemon['sp_def'] = statRows[4].css('td')[1].css('td ::text').get(),
        pokemon['speed'] = statRows[5].css('td')[1].css('td ::text').get(),
        pokemon['total'] = statRows[6].css('td')[1].css('b ::text').get()
        

        yield pokemon
    
    def retrievingAbilities(self, response):
        abilityInfo = response.xpath("//div[@data-source='ability']/div[@class='pi-data-value pi-font']/a")
        arr = []
        for ability in abilityInfo:
            arr.append(ability.css('a ::text').get())
        return arr