#include "cosmos_synapse/cosmos_synapse_c.h"
#include "cosmos_synapse/cosmos_synapse.hpp"
#include <vector>
struct cosmos_synapse_handle { cosmos::synapse::State state; explicit cosmos_synapse_handle(size_t d, double l, double g): state(d,l,g) {} };
extern "C" cosmos_synapse_handle* cosmos_synapse_create(size_t d, double l, double g) { try { return new cosmos_synapse_handle(d,l,g); } catch (...) { return nullptr; } }
extern "C" void cosmos_synapse_destroy(cosmos_synapse_handle* h) { delete h; }
extern "C" size_t cosmos_synapse_dimensions(const cosmos_synapse_handle* h) { return h ? h->state.dimensions() : 0; }
extern "C" int cosmos_synapse_update(cosmos_synapse_handle* h, const double* deltas, const double* qualities, size_t count, double confidence, double* out, size_t out_len, uint64_t* revision) {
    if (!h || !out || !revision) return 1; if (out_len < h->state.dimensions()) return 2; if (count > 0 && (!deltas || !qualities)) return 3;
    try { std::vector<cosmos::synapse::Feature> features; features.reserve(count); for (size_t i=0;i<count;++i) features.push_back({deltas[i],qualities[i]}); auto update=h->state.update(features,confidence); for(size_t i=0;i<update.vector.size();++i) out[i]=update.vector[i]; *revision=update.revision; return 0; } catch (...) { return 4; }
}
