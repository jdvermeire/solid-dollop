import lxml
import requests
from bs4 import BeautifulSoup

# TODO add logging


## EXCEPTIONS ##
class DrugBankConnectionException(Exception):
    pass

class DrugBankParseException(Exception):
    pass


## MAIN CLASS ##
class DrugBank(object):
    """
    TODO add description
    """

    _URI = 'https://drugbank.ca'

    _DRUGS_PATH = 'drugs'


    def __init__(
        self,
        drugbank_id,
        *args,
        **kwargs,
    ):
        """
        Loads drug information from the DrugBank site

        Parameters
        ----------
        drugbank_id : str
            DrugBank ID string
        """
        self.id = drugbank_id

        # Ideally I would  break these into smaller, self-contained methods,
        #   but for simplicity sake, I'm keeping them in the init
        # TODO consider using a factory method instead of init. This would allow for greater flexibility and robustness
        resp = requests.get(f'{self._URI}/{self._DRUGS_PATH}/{self.id}')

        if resp.status_code != 200:
            raise DrugBankConnectionException(f'Connection to DrugBank failed with status code {resp.status_code}: {resp.reason}')

        soup = BeautifulSoup(resp.text, 'lxml')

        self.name, self.description = self.__class__._parse_meta(soup)

        self.smiles = self.__class__._parse_container(
            soup,
            "smiles",
            self.__class__._parse_smiles
        )

        targets = self.__class__._parse_container(
            soup,
            "targets",
            self.__class__._parse_targets
        )

        if targets is None:

            self.targets = None

        else:

            self.targets = [
                {
                    "gene_name": self.__class__._parse_container(
                        target,
                        "gene-name",
                        self.__class__._parse_target_gene_name
                    ),
                    "actions": self.__class__._parse_container(
                        target,
                        "actions",
                        self.__class__._parse_target_actions
                    )
                }
                for target
                in targets
            ]

        self.alt_ids = self.__class__._parse_container(
            soup,
            "external-links",
            self.__class__._parse_alt_ids
        )

    @staticmethod
    def _parse_meta(soup):
        """
        Parses name and description from a DrugBank drug page. Returns the values as a (name, description) tuple

        Parameters
        ----------
        soup : BeautifulSoup
            a DrugBank drug page as a BeautifulSoup object
        """

        return (
            soup.find("meta", attrs={"name": "dc.title"})["content"],
            soup.find("meta", attrs={"name": "description"})["content"]
        )

    # TODO when logging is added, log a warning or info if a container is not found. This is normal for some pages, but I want to log it to ensure that something expected isn't missed.
    @staticmethod
    def _parse_container(soup, container_id, fun):
        """
        Parses a "container" from a DrugBank drug page

        Parameters
        ----------
        soup : BeautifulSoup
            a DrugBank drug page as a BeautifulSoup object
        container_id : str
            the HTML attribute id for the container
        fun : function
            a function that parses the contents of the container
        """

        container = soup.find(id=container_id)

        if container is not None:

            return fun(container)


    @staticmethod
    def _parse_smiles(container):
        """
        Parses SMILES string from DrugBank page

        Parameters
        ----------
        container : BeautifulSoup
            the container that holds the SMILES string. Generally returned from _parse_container
        """

        return container.next_sibling.contents[0].string


    @staticmethod
    def _parse_targets(container):
        """
        Parses drug targets from a DrugBank drug page

        Parameters
        ----------
        container : BeautifulSoup
            the container that holds the targets. Generally returned from _parse_container
        """

        return container.find_all(class_="bond card")


    @staticmethod
    def _parse_target_gene_name(container):
        """
        Parses a drug target gene name from a DrugBank drug page target card

        Parameters
        ----------
        container : BeautifulSoup
            the container that holds the gene name. Generally returned from _parse_container
        """

        return container.next_sibling.string


    @staticmethod
    def _parse_target_actions(container):
        """
        Parses a list of drug target actions from a DrugBank drug page target card

        Parameters
        ----------
        container : BeautifulSoup
            the container that holds the target actions. Generally returned from _parse_container
        """

        return [
            action.string
            for action
            in container.next_sibling.find_all(class_="badge-action")
        ]


    @staticmethod
    def _parse_alt_ids(container):
        """
        Parses a list of alternative identifiers (external links) from a DrugBank drug page

        Parameters
        ----------
        container : BeautifulSoup
            the container that holds the alternative ids. Generally returned from _parse_container
        """

        return [
            {
                "alt_id_source_id": ext_link["id"],
                "alt_id_source_name": ext_link.string,
                "alt_id": ext_link.next_sibling.string,
                "alt_id_url": ext_link.next_sibling.a["href"],
            }
            for ext_link
            in container.next_sibling.dl.find_all("dt")
        ]


