//! Dependency-free COSMOS synaptic state kernel.
//! This mirrors the Python LocalCNS update equation and is an engineering
//! interoperability primitive, not a medical or consciousness model.

pub const PHASE_STEP: f64 = 0.618_033_988_75;

#[derive(Debug, Clone, Copy, PartialEq)]
pub struct Feature {
    pub baseline_delta: f64,
    pub quality: f64,
}

impl Feature {
    pub fn new(baseline_delta: f64, quality: f64) -> Result<Self, &'static str> {
        if !baseline_delta.is_finite() || !quality.is_finite() {
            return Err("feature values must be finite");
        }
        if !(0.0..=1.0).contains(&quality) {
            return Err("quality must be in [0,1]");
        }
        Ok(Self { baseline_delta, quality })
    }
}

#[derive(Debug, Clone, PartialEq)]
pub struct Update {
    pub vector: Vec<f64>,
    pub revision: u64,
    pub confidence: f64,
}

#[derive(Debug, Clone)]
pub struct SynapseState {
    dimensions: usize,
    leak: f64,
    input_gain: f64,
    state: Vec<f64>,
    revision: u64,
}

impl SynapseState {
    pub fn new(dimensions: usize, leak: f64, input_gain: f64) -> Result<Self, &'static str> {
        if dimensions == 0 {
            return Err("dimensions must be positive");
        }
        if !leak.is_finite() || !(0.0..1.0).contains(&leak) {
            return Err("leak must be finite and in [0,1)");
        }
        if !input_gain.is_finite() || input_gain < 0.0 {
            return Err("input_gain must be finite and non-negative");
        }
        Ok(Self {
            dimensions,
            leak,
            input_gain,
            state: vec![0.0; dimensions],
            revision: 0,
        })
    }

    pub fn cosmos_12d() -> Self {
        Self::new(12, 0.88, 0.12).expect("constant configuration is valid")
    }

    pub fn vector(&self) -> &[f64] { &self.state }
    pub fn revision(&self) -> u64 { self.revision }

    pub fn update(&mut self, features: &[Feature], confidence: f64) -> Result<Update, &'static str> {
        if !confidence.is_finite() || !(0.0..=1.0).contains(&confidence) {
            return Err("confidence must be in [0,1]");
        }
        if features.is_empty() {
            self.revision += 1;
            return Ok(Update { vector: self.state.clone(), revision: self.revision, confidence: 0.0 });
        }
        let inputs: Vec<f64> = features.iter().map(|feature| feature.baseline_delta.tanh() * feature.quality).collect();
        let mut next = Vec::with_capacity(self.dimensions);
        for i in 0..self.dimensions {
            let source = inputs[i % inputs.len()];
            let phase = (((i + 1) as f64) * PHASE_STEP).sin();
            let value = self.leak * self.state[i] + self.input_gain * source * phase;
            next.push(value.clamp(-1.0, 1.0));
        }
        self.state = next;
        self.revision += 1;
        Ok(Update { vector: self.state.clone(), revision: self.revision, confidence })
    }
}

pub fn synaptic_step(previous_state: &[f64], features: &[Feature], leak: f64, input_gain: f64) -> Result<Vec<f64>, &'static str> {
    if previous_state.is_empty() { return Err("previous_state must not be empty"); }
    let mut engine = SynapseState::new(previous_state.len(), leak, input_gain)?;
    engine.state.copy_from_slice(previous_state);
    Ok(engine.update(features, 1.0)?.vector)
}
