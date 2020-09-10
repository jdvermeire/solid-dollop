/**
 * Create table for all gene targets and actions for a given drug
 */

CREATE TABLE IF NOT EXISTS drugbank.drug_targets (
  id          SERIAL NOT NULL,
  drug_id     INT NOT NULL,
  gene_id     INT NOT NULL,
  -- move action_ids to a separate table?
  action_ids  INT[] NOT NULL,
  created_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts  TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_drug_targets_pk
    PRIMARY KEY (id)
)
;

CREATE INDEX IF NOT EXISTS idx_drug_targets_drug_id
  ON drugbank.drug_targets (drug_id)
;
CREATE INDEX IF NOT EXISTS idx_drug_targets_gene_id
  ON drugbank.drug_targets (gene_id)
;
