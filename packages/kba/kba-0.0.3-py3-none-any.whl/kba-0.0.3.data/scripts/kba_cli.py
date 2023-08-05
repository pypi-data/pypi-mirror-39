import click, time, os, pprint, pickle

from progress.spinner import Spinner as _Spinner

class Spinner(_Spinner):
    """
    A custom spinner class that clears its own message when finish is called.
    """
    phases = ['x', '|', '-', '+']
    def clearln(self):
        print('\r\x1b[K', end='', file=self.file)
    def finish(self):
        self.clearln()
        _Spinner.finish(self)

from kba.utils import AggregatorApi
from kba import ConceptsApi, StatementsApi, MetadataApi

aggregator = AggregatorApi()

STATE = 'cli_state.pickle'

def save(state:dict) -> None:
    with open(STATE, 'wb') as f:
        pickle.dump(state, f, protocol=pickle.HIGHEST_PROTOCOL)

def load() -> dict:
    with open(STATE, 'rb') as handle:
        return pickle.load(handle)

def join(thread, message='Waiting for response ', seconds=0.1):
    """
    Waits for thread to finish, and then returns result
    """
    spinner = Spinner(message)

    while not thread.ready():
        time.sleep(seconds)
        spinner.next()

    spinner.finish()

    return thread.get()

@click.group()
def cli():
    pass

@cli.command()
@click.option('--keywords', '-k', multiple=True, required=True, help='A list of keywords to use for a substring match')
@click.option('--categories', '-c', multiple=True)
@click.option('--beacons', '-b', multiple=True, type=list)
def concept(keywords, categories, beacons):
    """
    Initiates a concept query with the given search parameters
    """
    kwargs = {}
    if categories is not None:
        kwargs['categories'] = list(categories)
    if beacons is not None:
        kwargs['beacons'] = list(beacons)

    thread = ConceptsApi().post_concepts_query(keywords=keywords, **kwargs, async=True)

    response = join(thread, 'Waiting for response ')

    click.echo('Query ID:\t{}'.format(response.query_id))

    save({'query' : response.query_id, 'command' : 'concept'})

@cli.command()
@click.option('--source', '-s', type=str, multiple=True)
@click.option('--relation', '-r', type=str, multiple=True)
@click.option('--target', '-t', type=str, multiple=True)
@click.option('--keyword', '-k', type=str, multiple=True)
@click.option('--category', '-c', type=str, multiple=True)
@click.option('--beacon', '-b', type=int, multiple=True)
def statement(source, relation, target, keyword, category, beacon):
    """
    Initiates a statement query with the given search parameters
    """
    kwargs = {}
    if source is not None:
        kwargs['source'] = list(source)
    if relation is not None:
        kwargs['relations'] = list(relation)
    if target is not None:
        kwargs['target'] = list(target)
    if keyword is not None:
        kwargs['keywords'] = list(keyword)
    if category is not None:
        kwargs['categories'] = list(category)
    if beacon is not None:
        kwargs['beacons'] = list(beacon)

    thread = StatementsApi().post_statements_query(**kwargs, async=True)

    response = join(thread, 'Waiting for response ')

    click.echo('Query ID:\t{}'.format(response.query_id))

    save({'query' : response.query_id, 'command' : 'statement'})

@cli.command()
@click.option('--query', '-q', help='A query ID')
@click.option('--command', '-c', type=click.Choice(['concept', 'statement']), help='The command that produced the given query ID, to help us know which endpoint to use')
def ping(query, command):
    """
    Retrieves the status of a query (by default the last query)
    """
    state = load()

    if query is None:
        query = state['query']
        click.echo('Last query:\t{}'.format(query))
    else:
        click.echo('Query ID:\t{}'.format(query))

    if command is None:
        command = state['command']

    if command == 'concept':
        thread = ConceptsApi().get_concepts_query_status(query, async=True)
    elif command == 'statement':
        thread = StatementsApi().get_statements_query_status(query, async=True)
    else:
        raise Exception('Unknown command {}'.format(command))

    response = join(thread, 'Waiting for response ')

    statuses = response.status
    statuses.sort(key=lambda s: s.beacon)

    for status in statuses:
        if status.count is not None:
            click.echo('Beacon {} finished with {} records'.format(status.beacon, status.count))
        elif status.discovered is not None:
            click.echo('Beacon {} discovered {} records, processed {}'.format(status.beacon, status.discovered, status.processed))
        else:
            click.echo('Beacon {} has not yet returned'.format(status.beacon))

@cli.command()
@click.option('--query', '-q', help='A query ID')
@click.option('--command', '-c', type=click.Choice(['concept', 'statement']), help='The command that produced the given query ID, to help us know which endpoint to use')
@click.option('--out', '-o', type=click.Path(), help='If provided, the results of the query will be written to this file instead of sent to standard out')
@click.option('--page', type=int, default=1, help='The ordinal number of the page to get (1=first, 2=second, etc.)')
@click.option('--size', type=int, default=100, help='The size of page to get')
def dump(query, command, out, page, size):
    """
    Retrieves the results of a query (by default the last query)
    """
    state = load()

    if query is None:
        query = state['query']
        click.echo('Last query:\t{}'.format(query))
    else:
        click.echo('Query ID:\t{}'.format(query))

    if command is None:
        command = state['command']

    if command == 'concept':
        thread = ConceptsApi().get_concepts(query, page_number=page, page_size=size, async=True)
    elif command == 'statement':
        thread = StatementsApi().get_statements(query, page_number=page, page_size=size, async=True)
    else:
        raise Exception('Unknown command {}'.format(command))

    response = join(thread, 'Waiting for response ')

    if out is not None:
        with open(out, 'w+') as f:
            f.write(str(response))
            click.echo('Saved response to {}'.format(out))
    else:
        pprint.pprint(response)

@cli.command()
@click.option('--out', '-o', type=click.Path(), help='If provided, query results will be saved to the given file')
def predicates(out):
    """
    Retrieves all predicates
    """
    thread = MetadataApi().get_predicates(async=True)
    response = join(thread)

    if out is not None:
        with open(out, 'w+') as f:
            f.write(str(response))
            click.echo('Saved response to {}'.format(out))
    else:
        pprint.pprint(response)

@cli.command()
@click.option('--out', '-o', type=click.Path(), help='If provided, query results will be saved to the given file')
def kmap(out):
    """
    Retrieves the knowledge map
    """
    thread = MetadataApi().get_knowledge_map(async=True)
    response = join(thread)

    if out is not None:
        with open(out, 'w+') as f:
            f.write(str(response))
            click.echo('Saved response to {}'.format(out))
    else:
        pprint.pprint(response)

@cli.command()
@click.option('--out', '-o', type=click.Path(), help='If provided, query results will be saved to the given file')
def categories(out):
    """
    Retrieves all categories
    """
    thread = MetadataApi().get_concept_categories(async=True)
    response = join(thread)

    if out is not None:
        with open(out, 'w+') as f:
            f.write(str(response))
            click.echo('Saved response to {}'.format(out))
    else:
        pprint.pprint(response)

@cli.command()
@click.option('--out', '-o', type=click.Path(), help='If provided, query results will be saved to the given file')
def beacons(out):
    """
    Retrieves all beacons
    """
    thread = MetadataApi().get_beacons(async=True)
    response = join(thread)

    if out is not None:
        with open(out, 'w+') as f:
            f.write(str(response))
            click.echo('Saved response to {}'.format(out))
    else:
        pprint.pprint(response)
