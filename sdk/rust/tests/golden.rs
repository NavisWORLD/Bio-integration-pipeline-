use cosmos_synapse::{Feature, SynapseState};

const GOLDEN: [f64; 12] = [
    0.02891876766114646,-0.02220725520372799,0.04791912723131752,-0.01459072664788153,
    0.0025653072604511205,0.012620779875725187,-0.046233655674311015,0.0228828972723213,
    -0.032941984868177496,0.002413860648239461,0.024589940949515134,-0.02129692995842166,
];

#[test]
fn matches_python_golden_vector() {
    let features = [Feature::new(0.5, 0.9).unwrap(), Feature::new(-0.25, 0.8).unwrap()];
    let mut engine = SynapseState::cosmos_12d();
    let update = engine.update(&features, 0.85).unwrap();
    assert_eq!(update.revision, 1);
    for (actual, expected) in update.vector.iter().zip(GOLDEN.iter()) {
        assert!((actual - expected).abs() < 1e-12, "{actual} != {expected}");
    }
}
