"""COSMOS Bio/CNS Integration Pipeline."""

from cosmos_bio_cns.adapters.base import BioAdapter
from cosmos_bio_cns.adapters.push import PushBioAdapter
from cosmos_bio_cns.baseline import RunningBaseline
from cosmos_bio_cns.cns import LocalCNS, OrganStatus
from cosmos_bio_cns.fusion import BioFusionEngine
from cosmos_bio_cns.models import BioFeature, BioObservation, CNSState, ConsentScope, FusionFrame, HeartbeatRecord
from cosmos_bio_cns.persistence import SQLiteEventStore
from cosmos_bio_cns.runtime import BioCNSRuntime
from cosmos_bio_cns.schema import load_schema
from cosmos_bio_cns.synapse import DEFAULT_DIMENSIONS, DEFAULT_INPUT_GAIN, DEFAULT_LEAK, PHASE_STEP, SynapticFeature, cosmos_12d_step, synaptic_step

__all__ = [
    "BioAdapter", "BioCNSRuntime", "BioFeature", "BioFusionEngine", "BioObservation", "PushBioAdapter",
    "CNSState", "ConsentScope", "FusionFrame", "HeartbeatRecord", "LocalCNS", "OrganStatus", "RunningBaseline",
    "SQLiteEventStore", "load_schema", "SynapticFeature", "synaptic_step", "cosmos_12d_step", "PHASE_STEP",
    "DEFAULT_DIMENSIONS", "DEFAULT_LEAK", "DEFAULT_INPUT_GAIN",
]

__version__ = "0.2.0"
