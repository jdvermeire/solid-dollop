/**
 * Create a table for DrugBank drug alternative identifiers
 */

CREATE TABLE IF NOT EXISTS drugbank.drug_alt_ids (
  id            SERIAL NOT NULL,
  drug_id       INT NOT NULL,
  alt_source_id INT NOT NULL,
  alt_id        VARCHAR NOT NULL,
  alt_id_url    VARCHAR NOT NULL,
  created_ts    TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts   TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts    TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_drug_alt_ids_pk
    PRIMARY KEY (id)
)
;

CREATE INDEX IF NOT EXISTS idx_drug_alt_ids_drug_id
  ON drugbank.drug_alt_ids (drug_id)
;
CREATE INDEX IF NOT EXISTS idx_drug_alt_ids_alt_source_id
  ON drugbank.drug_alt_ids (alt_source_id)
;
