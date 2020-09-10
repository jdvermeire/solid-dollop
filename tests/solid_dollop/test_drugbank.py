import pytest
from bs4 import BeautifulSoup
from solid_dollop import DrugBank


def test_init():
    pass

def test_parse_meta():
    soup = BeautifulSoup('<meta name="dc.title" content="happy" /><meta name="description" content="the happy path" />', features="lxml")
    assert DrugBank._parse_meta(soup) == ("happy", "the happy path")

def test_parse_container():
    def test_fun(container):
        return container.string

    soup = BeautifulSoup('<dt id="happy">happy</dt>', features="lxml")
    assert DrugBank._parse_container(soup, "happy", test_fun) == "happy"

def test_parse_container_none():
    def test_fun(container):
        return container.string

    soup = BeautifulSoup('<dt id="sad">sad</dt>', features="lxml")
    assert DrugBank._parse_container(soup, "happy", test_fun) is None

def test_parse_smiles():
    soup = BeautifulSoup('<dt class="col-xl-2 col-md-3 col-sm-4" id="smiles">SMILES</dt><dd class="col-xl-10 col-md-9 col-sm-8"><div class="wrap">CC(=O)NC1=CC=C(O)C=C1</div></dd>', "lxml")
    smiles_container = soup.find(id="smiles")
    assert DrugBank._parse_smiles(smiles_container) == 'CC(=O)NC1=CC=C(O)C=C1'

def test_parse_targets():
    soup = BeautifulSoup(
        '<div id="targets"><div class="bond-list"><div class="bond card"></div><div class="bond card"></div><div class="bond card"></div></div></div>',
        features="lxml"
    )

    out = BeautifulSoup('<div class="bond card"></div>', features="lxml").div

    targets_container = soup.find(id="targets")
    assert DrugBank._parse_targets(targets_container) == [
        out,
        out,
        out,
    ]

def test_parse_target_gene_name():
    soup = BeautifulSoup(
        '<div class="bond card"><div class="card-body"><div class="row"><div><dl><dt id="gene-name">Gene Name</dt><dd>HAPPY</dd></dl></div></div></div></div>',
        features="lxml"
    )

    tgn_container = soup.find(id="gene-name")

    assert DrugBank._parse_target_gene_name(tgn_container) == 'HAPPY'

def test_parse_target_actions():
    soup = BeautifulSoup(
        '<dt class="col-md-5 col-sm-6" id="actions">Actions</dt><dd class="col-md-7 col-sm-6"><div class="badge badge-pill badge-action">Inhibitor</div></dd>',
        features="lxml"
    )

    action_container = soup.find(id="actions")

    assert DrugBank._parse_target_actions(action_container) == ['Inhibitor']

def test_parse_alt_ids():
    soup = BeautifulSoup(
        '<dt class="col-xl-2 col-md-3 col-sm-4" id="external-links">External Links</dt><dd class="col-xl-10 col-md-9 col-sm-8"><dl class="inner-dl"><dt class="col-md-4 col-sm-5" id="human-metabolome-database">Human Metabolome Database</dt><dd class="col-md-8 col-sm-7"><a target="_blank" rel="noopener" href="http://www.hmdb.ca/metabolites/HMDB0001859">HMDB0001859</a></dd><dt class="col-md-4 col-sm-5" id="wikipedia">Wikipedia</dt><dd class="col-md-8 col-sm-7"><a target="_blank" rel="noopener" href="http://en.wikipedia.org/wiki/Paracetamol">Paracetamol</a></dd></dl></dd>',
        features="lxml"
    )

    alt_ids_container = soup.find(id="external-links")

    assert DrugBank._parse_alt_ids(alt_ids_container) == [
        {
            "alt_id_source_id": "human-metabolome-database",
            "alt_id_source_name": "Human Metabolome Database",
            "alt_id": "HMDB0001859",
            "alt_id_url": "http://www.hmdb.ca/metabolites/HMDB0001859",
        },
        {
            "alt_id_source_id": "wikipedia",
            "alt_id_source_name": "Wikipedia",
            "alt_id": "Paracetamol",
            "alt_id_url": "http://en.wikipedia.org/wiki/Paracetamol",
        },
    ]


# TODO add mocks to conftest.py in order to test things that require requests
