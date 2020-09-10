/**
 * Create lookup table for DrugBank genes
 */

CREATE TABLE IF NOT EXISTS drugbank.genes (
  id          SERIAL NOT NULL,
  name        VARCHAR NOT NULL,
  created_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts  TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_genes_pk
    PRIMARY KEY (id),
  CONSTRAINT uq_drugbank_genes_name
    UNIQUE (name)
)
;
