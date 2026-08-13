from cosmos_bio_cns import BioCNSRuntime, SQLiteEventStore
from cosmos_bio_cns.adapters import DeterministicCardiacAdapter

store = SQLiteEventStore("demo.sqlite3")
runtime = BioCNSRuntime([DeterministicCardiacAdapter(subject_id="example")], store=store)
runtime.start()
try:
    for _ in range(10):
        frame, state = runtime.step()
        print(frame.frame_id, round(frame.confidence, 3), tuple(round(x, 4) for x in state.vector))
finally:
    runtime.stop()
    print("ledger valid:", store.verify())
    store.close()
