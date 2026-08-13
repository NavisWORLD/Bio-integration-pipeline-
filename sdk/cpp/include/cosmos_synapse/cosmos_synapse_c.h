#ifndef COSMOS_SYNAPSE_C_H
#define COSMOS_SYNAPSE_C_H
#include <stddef.h>
#include <stdint.h>
#ifdef __cplusplus
extern "C" {
#endif
typedef struct cosmos_synapse_handle cosmos_synapse_handle;
cosmos_synapse_handle* cosmos_synapse_create(size_t dimensions, double leak, double input_gain);
void cosmos_synapse_destroy(cosmos_synapse_handle* handle);
int cosmos_synapse_update(cosmos_synapse_handle* handle, const double* baseline_deltas, const double* qualities, size_t feature_count, double confidence, double* out_vector, size_t out_vector_length, uint64_t* out_revision);
size_t cosmos_synapse_dimensions(const cosmos_synapse_handle* handle);
#ifdef __cplusplus
}
#endif
#endif
