import solid_dollop
from sqlalchemy import create_engine
from sqlalchemy.sql import select, insert
import os

# TODO add logging

from dotenv import load_dotenv
load_dotenv()

# setup db
DB_HOST = os.getenv("SOLID_DOLLOP_DB_HOST")
DB_PORT = os.getenv("SOLID_DOLLOP_DB_PORT")
DB_USER = os.getenv("SOLID_DOLLOP_DB_USER")
DB_PASS = os.getenv("SOLID_DOLLOP_DB_PASS")
DB_BASE = os.getenv("SOLID_DOLLOP_DB_BASE")

engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_BASE}')

solid_dollop.Base.metadata.create_all(engine)

# I don't know why I did this. I could have just imported them this way
# TODO clean this up
drugs = solid_dollop.Drugs
genes = solid_dollop.Genes
actions = solid_dollop.Actions
drug_targets = solid_dollop.DrugTargets
alt_sources = solid_dollop.AltSources
drug_alt_ids = solid_dollop.DrugAltIds


drug_list = [
    "DB00619",
    "DB01048",
    "DB14093",
    "DB00173",
    "DB00734",
    "DB00218",
    "DB05196",
    "DB09095",
    "DB01053",
    "DB00274",
]

with engine.connect() as conn:

    # TODO move all the select and insert sections into defined methods. That will clean up this code a lot and make it easier to debug in the future

    for drug in drug_list:
        db_drug = solid_dollop.DrugBank(drug)

        # base-level drug information
        drug_id_query = select([drugs.id]).\
            where(drugs.drugbank_id == drug)

        drug_id_result = conn.execute(drug_id_query)

        if not drug_id_result.rowcount:

            drug_insert = insert(drugs).\
                values(
                    drugbank_id=drug,
                    name=db_drug.name,
                    description=db_drug.description,
                    smiles=db_drug.smiles
                ).returning(drugs.id)

            drug_id_result = conn.execute(drug_insert)

        drug_id = drug_id_result.fetchone()[0]

        ## Drug Targets
        if db_drug.targets is not None:
            for target in db_drug.targets:

                ## Gene Target

                gene_name = target.get("gene_name")

                if gene_name is not None:

                    gene_id_query = select([genes.id]).\
                        where(genes.name == gene_name)

                    gene_id_result = conn.execute(gene_id_query)

                    if not gene_id_result.rowcount:

                        gene_insert = insert(genes).\
                            values(name=gene_name).\
                            returning(genes.id)

                        gene_id_result = conn.execute(gene_insert)

                    gene_id = gene_id_result.fetchone()[0]

                else:

                    gene_id = -1

                ## Actions

                action_ids = []

                # TODO batch this, instead of one at a time
                actions_list = target.get("actions")

                if actions_list is not None:
                    for action_name in target.get("actions"):

                        action_id_query = select([actions.id]).\
                            where(actions.name == action_name)

                        action_id_result = conn.execute(action_id_query)

                        if not action_id_result.rowcount:

                            action_insert = insert(actions).\
                                values(name=action_name).\
                                returning(actions.id)

                            action_id_result = conn.execute(action_insert)

                        action_id = action_id_result.fetchone()[0]
                        action_ids.append(action_id)


                ## Drug Target

                # check if the drug target already exists
                drug_target_query = select([drug_targets.id]).\
                    where(drug_targets.drug_id == drug_id).\
                    where(drug_targets.gene_id == gene_id).\
                    where(drug_targets.action_ids == action_ids)

                drug_target_result = conn.execute(drug_target_query)

                if not drug_target_result.rowcount:

                    drug_target_insert = insert(drug_targets).\
                        values(
                            drug_id=drug_id,
                            gene_id=gene_id,
                            action_ids=action_ids
                        )

                    drug_target_insert_result = conn.execute(drug_target_insert)
                    # TODO error handling

        ## Drug Alt Ids

        for alt_id in db_drug.alt_ids:

            ## Alt Sources

            alt_source_drugbank_id = alt_id.get("alt_id_source_id")
            alt_source_name = alt_id.get("alt_id_source_name")

            if alt_source_drugbank_id is None:
                raise Exception()

            if alt_source_name is None:
                raise Exception()

            alt_source_id_query = select([alt_sources.id]).\
                where(alt_sources.drugbank_id == alt_source_drugbank_id)

            alt_source_id_result = conn.execute(alt_source_id_query)

            if not alt_source_id_result.rowcount:

                alt_source_insert = insert(alt_sources).\
                    values(
                        drugbank_id=alt_source_drugbank_id,
                        name=alt_source_name
                    ).returning(alt_sources.id)

                alt_source_id_result = conn.execute(alt_source_insert)

            alt_source_id = alt_source_id_result.fetchone()[0]

            ## Drug Alt Id

            alt_id_query = select([drug_alt_ids.id]).\
                where(drug_alt_ids.drug_id == drug_id).\
                where(drug_alt_ids.alt_source_id == alt_source_id)

            alt_id_result = conn.execute(alt_id_query)

            if not alt_id_result.rowcount:

                alt_id_insert = insert(drug_alt_ids).\
                    values(
                        drug_id=drug_id,
                        alt_source_id=alt_source_id,
                        alt_id=alt_id.get("alt_id"),
                        alt_id_url=alt_id.get("alt_id_url")
                    )

                alt_id_insert_result = conn.execute(alt_id_insert)
                # TODO error handling
