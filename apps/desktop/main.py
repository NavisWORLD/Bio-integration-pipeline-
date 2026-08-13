from __future__ import annotations

import math
from pathlib import Path
import tkinter as tk
from tkinter import messagebox, ttk

from cosmos_bio_cns import BioCNSRuntime, BioObservation, ConsentScope, PushBioAdapter, SQLiteEventStore


APP_TITLE = "COSMOS Bio/CNS"


class CosmosDesktopApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title(APP_TITLE)
        root.geometry("860x620")
        root.minsize(760, 560)

        data_dir = Path.home() / ".cosmos_bio_cns"
        data_dir.mkdir(parents=True, exist_ok=True)
        self.store = SQLiteEventStore(data_dir / "events.sqlite3")
        self.adapter = PushBioAdapter()
        self.runtime = BioCNSRuntime([self.adapter], store=self.store, cosmos_id="cosmos-desktop")
        self.runtime.start()
        self.sequence = 0

        self.sensor = tk.StringVar(value="desktop")
        self.channel = tk.StringVar(value="heart_rate")
        self.value = tk.StringVar(value="72.0")
        self.unit = tk.StringVar(value="bpm")
        self.quality = tk.StringVar(value="0.98")
        self.subject = tk.StringVar(value="local-user")
        self.status = tk.StringVar(value="Ready. First accepted sample establishes the personal baseline.")
        self.state_text = tk.StringVar(value="No CNS state yet.")

        style = ttk.Style()
        if "clam" in style.theme_names():
            style.theme_use("clam")
        style.configure("Title.TLabel", font=("TkDefaultFont", 22, "bold"))
        style.configure("Sub.TLabel", font=("TkDefaultFont", 11))
        style.configure("Vector.TLabel", font=("TkFixedFont", 11))

        outer = ttk.Frame(root, padding=20)
        outer.pack(fill="both", expand=True)
        ttk.Label(outer, text="COSMOS Bio/CNS", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            outer,
            text="Local-first biosignal → baseline → fusion → 12D CNS → heartbeat ledger",
            style="Sub.TLabel",
        ).pack(anchor="w", pady=(2, 16))

        card = ttk.LabelFrame(outer, text="Observation", padding=14)
        card.pack(fill="x")
        fields = [
            ("Sensor", self.sensor),
            ("Channel", self.channel),
            ("Value", self.value),
            ("Unit", self.unit),
            ("Quality 0..1", self.quality),
            ("Subject", self.subject),
        ]
        for row, (label, variable) in enumerate(fields):
            ttk.Label(card, text=label).grid(row=row // 2, column=(row % 2) * 2, sticky="w", padx=(0, 8), pady=6)
            ttk.Entry(card, textvariable=variable, width=28).grid(
                row=row // 2,
                column=(row % 2) * 2 + 1,
                sticky="ew",
                padx=(0, 18),
                pady=6,
            )
        card.columnconfigure(1, weight=1)
        card.columnconfigure(3, weight=1)

        actions = ttk.Frame(outer)
        actions.pack(fill="x", pady=14)
        ttk.Button(actions, text="Process observation", command=self.process_observation).pack(side="left")
        ttk.Button(actions, text="Add demo heartbeat", command=self.add_demo_heartbeat).pack(side="left", padx=8)
        ttk.Button(actions, text="Verify ledger", command=self.verify_ledger).pack(side="left")

        result = ttk.LabelFrame(outer, text="Current local CNS state", padding=14)
        result.pack(fill="both", expand=True)
        ttk.Label(result, textvariable=self.state_text, style="Vector.TLabel", justify="left").pack(anchor="nw")
        ttk.Separator(outer).pack(fill="x", pady=(14, 8))
        ttk.Label(outer, textvariable=self.status, wraplength=800).pack(anchor="w")

        root.protocol("WM_DELETE_WINDOW", self.close)

    def _process(self, value: float) -> None:
        quality = float(self.quality.get())
        self.sequence += 1
        observation = BioObservation(
            sensor=self.sensor.get().strip() or "desktop",
            channel=self.channel.get().strip() or "value",
            value=value,
            unit=self.unit.get().strip() or "unitless",
            quality=quality,
            sequence=self.sequence,
            subject_id=self.subject.get().strip() or "anonymous",
            device_id="desktop-app",
            consent=ConsentScope(session_id="desktop-app", bio_processing=True, raw_retention=False),
        )
        self.adapter.push(observation)
        frame, state = self.runtime.step()
        vector = "\n".join(
            f"D{index + 1:02d}: {component:+0.6f}"
            for index, component in enumerate(state.vector)
        )
        self.state_text.set(
            f"Revision {state.revision}    confidence={state.confidence:.3f}\n"
            f"frame={frame.frame_id}\n\n{vector}"
        )
        self.status.set(
            f"Processed {observation.channel}={observation.value:g} {observation.unit}. "
            f"Ledger events: {self.store.count()} | hash chain valid: {self.store.verify()}"
        )

    def process_observation(self) -> None:
        try:
            self._process(float(self.value.get()))
        except Exception as exc:
            messagebox.showerror(APP_TITLE, str(exc))

    def add_demo_heartbeat(self) -> None:
        self.sensor.set("desktop-demo")
        self.channel.set("heart_rate")
        self.unit.set("bpm")
        self.quality.set("0.98")
        demo_value = 72.0 + 4.0 * math.sin((self.sequence + 1) / 2.0)
        self.value.set(f"{demo_value:.2f}")
        self.process_observation()

    def verify_ledger(self) -> None:
        valid = self.store.verify()
        messagebox.showinfo(APP_TITLE, f"Events: {self.store.count()}\nHash chain valid: {valid}")

    def close(self) -> None:
        try:
            self.runtime.stop()
        finally:
            self.store.close()
            self.root.destroy()


def main() -> None:
    root = tk.Tk()
    CosmosDesktopApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
