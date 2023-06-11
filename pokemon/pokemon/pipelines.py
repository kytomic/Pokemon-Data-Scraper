# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class PokemonPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        # Lowercase all the string
        lowercase_keys = ['name', 'japanese', 'types', 'species', 'evoform', 'evointo']
        for key in lowercase_keys:
            value = adapter.get(key)[0]
            if value is None:
                print('---------------------------------')
                print(key)
                print('---------------------------------')
            adapter[key] = value.lower()
        
        # Special Case: Lowercasing an array
        arr = []
        abilities = adapter.get('ability')[0]
        for ability in abilities:
            arr.append(ability.lower())
        adapter['ability'] = arr
        
        # Turn stat into a number
        integer_keys = ['hp', 'attack', 'defense', 'sp_atk', 'sp_def', 'speed', 'total']
        for key in integer_keys:
            value = adapter.get(key)[0]
            adapter[key] = int(value)
        
        return item
