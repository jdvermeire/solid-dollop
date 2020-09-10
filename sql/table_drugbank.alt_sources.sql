/**
 * Create table for alternative (in relation to DrugBank) sites for drug information
 */

CREATE TABLE IF NOT EXISTS drugbank.alt_sources (
  id          SERIAL NOT NULL,
  drugbank_id VARCHAR NOT NULL,
  name        VARCHAR NOT NULL,
  created_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts  TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_alt_sources_pk
    PRIMARY KEY (id),
  CONSTRAINT uq_drugbank_alt_sources_drugbank_id
    UNIQUE (drugbank_id)
)
;
