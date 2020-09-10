/**
 * Create lookup table for DrugBank actions
 */

CREATE TABLE IF NOT EXISTS drugbank.actions (
  id          SERIAL NOT NULL,
  name        VARCHAR NOT NULL,
  created_ts  TIMESTAMPTZ NOT NULL DEFAULT now(),
  modified_ts TIMESTAMPTZ NOT NULL DEFAULT now(),
  deleted_ts  TIMESTAMPTZ NULL,

  CONSTRAINT drugbank_actions_pk
    PRIMARY KEY (id),
  CONSTRAINT uq_drugbank_actions_name
    UNIQUE (name)
)
;
