# Database model for solid_dollop
from sqlalchemy import Column, Integer, String, DateTime, Sequence, event, DDL, Index
from sqlalchemy.sql import func
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base


# TODO create mixin for crud columns

Base = declarative_base()
Base.metadata.schema = "drugbank"
event.listen(
    Base.metadata,
    "before_create",
    DDL("CREATE SCHEMA IF NOT EXISTS drugbank")
)


class Drugs(Base):
    """

    """
    __tablename__ = 'drugs'

    id = Column(Integer, Sequence('drug_id_seq'), primary_key=True)
    drugbank_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    description = Column(String)
    smiles = Column(String)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))


class Genes(Base):
    """

    """
    __tablename__ = 'genes'

    id = Column(Integer, Sequence("gene_id_seq"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))


class Actions(Base):
    """

    """
    __tablename__ = 'actions'

    id = Column(Integer, Sequence("action_id_seq"), primary_key=True)
    name = Column(String, unique=True, nullable=False)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))


class AltSources(Base):
    """

    """
    __tablename__ = 'alt_sources'

    id = Column(Integer, Sequence("alt_source_id_seq"), primary_key=True)
    drugbank_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))


class DrugTargets(Base):
    """

    """
    __tablename__ = 'drug_targets'

    id = Column(Integer, Sequence("drug_target_id_seq"), primary_key=True)
    drug_id = Column(Integer, nullable=False, index=True)
    gene_id = Column(Integer, nullable=False, index=True)
    action_ids = Column(postgresql.ARRAY(Integer), nullable=False)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))


class DrugAltIds(Base):
    """

    """
    __tablename__ = 'drug_alt_ids'

    id = Column(Integer, Sequence("drug_alt_id_id_seq"), primary_key=True)
    drug_id = Column(Integer, nullable=False, index=True)
    alt_source_id = Column(Integer, nullable=False, index=True)
    alt_id = Column(String, nullable=False)
    alt_id_url = Column(String, nullable=False)
    created_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_ts = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    deleted_ts = Column(DateTime(timezone=True))
