import pyalveo
from pprint import pprint

# we need an alveo.config file, get one from the staging server to run these as tests
client = pyalveo.Client(configfile='examples/alveo.config')

meta = {
    "contribution_name": "HelloWorld2",
    "contribution_collection": "demotext",
    "contribution_text": "This is contribution description",
    "contribution_abstract": "This is contribution abstract"
}
result = client.create_contribution(meta)
#result = client.get_contribution('https://staging.alveo.edu.au/contrib/29')

pprint(result)

contrib_url = result['url']

itemurl = 'https://staging.alveo.edu.au/catalog/demotext/2006-05-28-19'
result = client.add_document(itemurl, 'testfile2.txt', metadata={}, content='hello world', contrib_id=result['id'])

pprint(result)

result = client.delete_contribution(contrib_url)

pprint(result)