from cosmos_bio_cns import BioCNSRuntime, BioObservation
from cosmos_bio_cns.adapters import PushBioAdapter

adapter = PushBioAdapter()
runtime = BioCNSRuntime([adapter])
runtime.start()
try:
    adapter.extend([
        BioObservation(sensor="watch", channel="heart_rate", value=74.2, unit="bpm", quality=0.97),
        BioObservation(sensor="phone", channel="motion_energy", value=0.31, unit="normalized", quality=0.94),
        BioObservation(sensor="audio", channel="rms", value=0.18, unit="normalized", quality=0.90),
        BioObservation(sensor="camera", channel="luminance", value=0.64, unit="normalized", quality=0.88),
    ])
    frame, state = runtime.step()
    print("accepted features:", len(frame.features))
    print("confidence:", frame.confidence)
    print("12D state:", state.vector)
finally:
    runtime.stop()
