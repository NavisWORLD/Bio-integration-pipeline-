#include "cosmos_synapse/cosmos_synapse.hpp"
#include "cosmos_synapse/cosmos_synapse_c.h"
#include <array>
#include <cassert>
#include <cmath>
#include <cstdint>
int main() {
    constexpr std::array<double,12> golden={0.02891876766114646,-0.02220725520372799,0.04791912723131752,-0.01459072664788153,0.0025653072604511205,0.012620779875725187,-0.046233655674311015,0.0228828972723213,-0.032941984868177496,0.002413860648239461,0.024589940949515134,-0.02129692995842166};
    cosmos::synapse::State state; auto update=state.update({{0.5,0.9},{-0.25,0.8}},0.85); for(size_t i=0;i<golden.size();++i) assert(std::abs(update.vector[i]-golden[i])<1e-12);
    auto* c=cosmos_synapse_create(12,0.88,0.12); assert(c); double deltas[2]={0.5,-0.25}, qualities[2]={0.9,0.8}, out[12]={}; std::uint64_t revision=0; assert(cosmos_synapse_update(c,deltas,qualities,2,0.85,out,12,&revision)==0); assert(revision==1); for(size_t i=0;i<golden.size();++i) assert(std::abs(out[i]-golden[i])<1e-12); cosmos_synapse_destroy(c);
}
