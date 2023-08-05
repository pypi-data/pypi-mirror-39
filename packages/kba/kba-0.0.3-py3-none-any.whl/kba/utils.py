from kba import ConceptsApi
from kba import StatementsApi

from kba.api_client import ApiClient
from kba.configuration import Configuration

from typing import List

import click, time, itertools

class Query(object):
    def __init__(self, query, api, status_fn, get_fn):
        self.query = query
        self.api = api
        self.status_fn = status_fn
        self.get_fn = get_fn

    @property
    def id(self):
        return self.query.query_id

    @property
    def keywords(self):
        return self.query.keywords

    @property
    def categories(self):
        return self.query.categories

    def status(self, beacons:list=None):
        if beacons is not None:
            return self.status_fn(self.id, beacons=beacons)
        else:
            return self.status_fn(self.id)

    def get(self):
        return self.get_fn(self.id)

    def wait(self, seconds=3):
        unfinished = [s.beacon for s in self.status().status]

        while unfinished != []:

            with click.progressbar(itertools.repeat(None), label='Waiting for beacons to return...') as bar:
                for _ in bar:
                    for status in self.status().status:
                        is_ready = status.discovered is not None or status.count is not None
                        if is_ready and status.beacon in unfinished:
                            unfinished.remove(status.beacon)
                            break
                    else:
                        time.sleep(seconds)
                        continue
                    break

            if status.discovered is not None:
                with click.progressbar(range(status.discovered), label='Processing beacon {}'.format(status.beacon)) as bar:
                    prev_processed = 0
                    for _ in bar:
                        new_status = next(s for s in self.status().status if s.beacon == status.beacon)
                        bar.update(new_status.processed - prev_processed)
                        prev_processed = new_status.processed

                        if new_status.processed != new_status.discovered:
                            time.sleep(seconds)

        data = self.get()

        if data == []:
            click.echo('No records discovered for {}'.format(self.id))
        else:
            return data






class AggregatorApi(object):
    def __init__(self, host=None):
        self.concepts_api = ConceptsApi()
        self.statements_api = StatementsApi()

        if host is not None:
            self.concepts_api.api_client.configuration.host = host
            self.statements_api.api_client.configuration.host = host

    def build_concept_query(self, keywords:List[str], categories:List[str]=None, beacons:List[int]=None):
        kwargs = {}

        if categories is not None:
            kwargs['categories'] = categories

        if beacons is not None:
            kwargs['beacons'] = beacons

        q = self.concepts_api.post_concepts_query(keywords=keywords, **kwargs)

        return Query(
            q,
            self.concepts_api,
            self.concepts_api.get_concepts_query_status,
            self.concepts_api.get_concepts,
        )
