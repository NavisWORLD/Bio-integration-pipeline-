import Foundation

public let cosmosPhaseStep = 0.61803398875

public struct SynapticFeature: Sendable {
    public let baselineDelta: Double
    public let quality: Double

    public init(baselineDelta: Double, quality: Double) throws {
        guard baselineDelta.isFinite, quality.isFinite, (0.0...1.0).contains(quality) else {
            throw SynapseError.invalidFeature
        }
        self.baselineDelta = baselineDelta
        self.quality = quality
    }
}

public struct SynapticUpdate: Sendable {
    public let vector: [Double]
    public let revision: UInt64
    public let confidence: Double
}

public enum SynapseError: Error {
    case invalidConfiguration
    case invalidFeature
    case invalidConfidence
}

public final class SynapseState: @unchecked Sendable {
    private let leak: Double
    private let inputGain: Double
    private var vector: [Double]
    public private(set) var revision: UInt64 = 0

    public init(dimensions: Int = 12, leak: Double = 0.88, inputGain: Double = 0.12) throws {
        guard dimensions > 0, leak.isFinite, leak >= 0.0, leak < 1.0, inputGain.isFinite, inputGain >= 0.0 else {
            throw SynapseError.invalidConfiguration
        }
        self.leak = leak
        self.inputGain = inputGain
        self.vector = Array(repeating: 0.0, count: dimensions)
    }

    public func update(features: [SynapticFeature], confidence: Double = 1.0) throws -> SynapticUpdate {
        guard confidence.isFinite, (0.0...1.0).contains(confidence) else {
            throw SynapseError.invalidConfidence
        }
        revision += 1
        guard !features.isEmpty else {
            return SynapticUpdate(vector: vector, revision: revision, confidence: 0.0)
        }
        let inputs = features.map { tanh($0.baselineDelta) * $0.quality }
        var next = Array(repeating: 0.0, count: vector.count)
        for i in next.indices {
            let phase = sin(Double(i + 1) * cosmosPhaseStep)
            let value = leak * vector[i] + inputGain * inputs[i % inputs.count] * phase
            next[i] = min(1.0, max(-1.0, value))
        }
        vector = next
        return SynapticUpdate(vector: next, revision: revision, confidence: confidence)
    }
}
