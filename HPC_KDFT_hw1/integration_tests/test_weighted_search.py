import gzip

from pytest import fixture

from test_util import (
    mktemp_path, wait_concrete_service,
    force_remove, force_remove_container, force_remove_volume,
    force_remove_image,
    docker_run, docker_build, docker_cp, docker_volume_create,
    text_to_lines,
)


@fixture(scope='module')
def weighted_search_container():
    docker_build('Dockerfile.concrete_python', 'concrete-python-image')
    docker_build('Dockerfile.weighted_search', 'weighted-search-image')
    docker_build('Dockerfile.search_client', 'search-client-image')

    docker_volume_create('index')
    docker_run(
        'concrete-python-image', 'sleep', 'infinity',
        d=True, v=('index', '/mnt/index'), name='index-copy')
    index_path = mktemp_path('.gz')
    with gzip.open(index_path, 'w') as f:
        f.write('''\
sweet	savory	sour	a	b	c	d	e	f	g	h	i	j	k
banana	0.3	0:3
orange	0.2	0:3	1:1	2:1
zucchini	0.3	0:2	1:6
tomato	0.4	1:4
squid	0.2	3:5	4:2	5:1	6:6	7:7	8:10	9:9	10:12	11:8	12:13	13:3
'''.encode('utf-8'))
    docker_cp(
        index_path, ('index-copy', '/mnt/index/index.gz'))
    force_remove(index_path)
    force_remove_container('index-copy')

    docker_run(
        'weighted-search-image',
        d=True, v=('index', '/mnt/index'), name='weighted-search')
    wait_concrete_service('weighted-search', 'Search')

    yield 'weighted-search'

    force_remove_container('weighted-search')
    force_remove_container('index-copy')
    force_remove_volume('index')
    force_remove_image('search-client-image')
    force_remove_image('weighted-search-image')
    force_remove_image('concrete-python-image')


def test_weighted_search_one_term_no_hits(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '10', 'avocado',
        rm=True, network=('container', weighted_search_container))
    assert set(text_to_lines(output)).issubset(
        ['sweet', 'savory', 'sour'] + list('abcdefghijk'))
    assert len(set(text_to_lines(output))) == 0


def test_weighted_search_one_term_one_hit(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '10', 'banana',
        rm=True, network=('container', weighted_search_container))
    assert text_to_lines(output)[:1] == ['sweet']
    assert len(set(text_to_lines(output))) == 1


def test_weighted_search_one_term_two_hits(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '10', 'zucchini',
        rm=True, network=('container', weighted_search_container))
    assert text_to_lines(output)[:2] == ['savory', 'sweet']
    assert len(set(text_to_lines(output))) == 2


def test_weighted_search_one_term_eleven_hits(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '11', 'squid',
        rm=True, network=('container', weighted_search_container))
    assert text_to_lines(output) == list('jhfgiedakbc')
    assert len(set(text_to_lines(output))) == 11


def test_weighted_search_two_terms_two_hits(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '10', 'banana', 'tomato',
        rm=True, network=('container', weighted_search_container))
    assert text_to_lines(output)[:2] == ['savory', 'sweet']
    assert len(set(text_to_lines(output))) == 2


def test_weighted_search_two_terms_three_hits(weighted_search_container):
    output = docker_run(
        'search-client-image', '-k', '10', 'orange', 'zucchini',
        rm=True, network=('container', weighted_search_container))
    assert text_to_lines(output)[:3] == ['savory', 'sweet', 'sour']
    assert len(set(text_to_lines(output))) == 3


def test_weighted_search_two_terms_three_hits_zero_k(weighted_search_container):
    output = docker_run(
            'search-client-image', '-k', '0', 'orange', 'zucchini',
            rm=True, network=('container', weighted_search_container))
    assert output == ""


def test_weighted_search_two_terms_three_hits_one_k(weighted_search_container):
    output = docker_run(
            'search-client-image', '-k', '1', 'orange', 'zucchini',
            rm=True, network=('container', weighted_search_container))
    assert output == ['savory'] or ['sweet'] or ['sour']
