#pragma once

#include <algorithm>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <stdexcept>
#include <vector>

namespace cosmos::synapse {
inline constexpr double kPhaseStep = 0.61803398875;
struct Feature { double baseline_delta{}; double quality{}; };
struct Update { std::vector<double> vector; std::uint64_t revision{}; double confidence{}; };

class State {
public:
    State(std::size_t dimensions = 12, double leak = 0.88, double input_gain = 0.12)
        : dimensions_(dimensions), leak_(leak), input_gain_(input_gain), state_(dimensions, 0.0) {
        if (dimensions == 0) throw std::invalid_argument("dimensions must be positive");
        if (!std::isfinite(leak) || leak < 0.0 || leak >= 1.0) throw std::invalid_argument("leak must be in [0,1)");
        if (!std::isfinite(input_gain) || input_gain < 0.0) throw std::invalid_argument("input_gain must be non-negative");
    }
    Update update(const std::vector<Feature>& features, double confidence) {
        if (!std::isfinite(confidence) || confidence < 0.0 || confidence > 1.0) throw std::invalid_argument("confidence must be in [0,1]");
        for (const auto& feature : features) {
            if (!std::isfinite(feature.baseline_delta) || !std::isfinite(feature.quality) || feature.quality < 0.0 || feature.quality > 1.0) throw std::invalid_argument("invalid feature");
        }
        if (features.empty()) { ++revision_; return {state_, revision_, 0.0}; }
        std::vector<double> inputs; inputs.reserve(features.size());
        for (const auto& feature : features) inputs.push_back(std::tanh(feature.baseline_delta) * feature.quality);
        std::vector<double> next(dimensions_);
        for (std::size_t i = 0; i < dimensions_; ++i) {
            const double source = inputs[i % inputs.size()];
            const double phase = std::sin(static_cast<double>(i + 1) * kPhaseStep);
            const double value = leak_ * state_[i] + input_gain_ * source * phase;
            next[i] = std::clamp(value, -1.0, 1.0);
        }
        state_ = std::move(next); ++revision_; return {state_, revision_, confidence};
    }
    const std::vector<double>& vector() const noexcept { return state_; }
    std::uint64_t revision() const noexcept { return revision_; }
    std::size_t dimensions() const noexcept { return dimensions_; }
private:
    std::size_t dimensions_; double leak_; double input_gain_; std::vector<double> state_; std::uint64_t revision_{0};
};
} // namespace cosmos::synapse
