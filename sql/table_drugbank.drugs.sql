/**
 * Create base table for drug information from DrugBank
 */

CREATE TABLE IF NOT EXISTS drugbank.drugs (
  id          SERIAL NOT NULL,
  drugbank_id VARCHAR NOT NULL,
  name        VARCHAR NOT NULL,
  description VARCHAR NULL,
  smiles      VARCHAR NULL,
  created_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts  TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_drugs_pk
    PRIMARY KEY (id),
  CONSTRAINT uq_drugbank_drugs_drugbank_id
    UNIQUE (drugbank_id)
)
;
