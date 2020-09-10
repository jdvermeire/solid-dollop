import pytest
from bs4 import BeautifulSoup
from solid_dollop import DrugBank


def test_init():
    pass

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
    targets_container = soup.find(id="targets")
    assert DrugBank._parse_targets(targets_container) == [
        '<div class="bond card"></div>',
        '<div class="bond card"></div>',
        '<div class="bond card"></div>',
    ]

def test_parse_target_gene_name():
    pass

def test_parse_target_actions():
    pass

def test_parse_alt_ids():
    pass
