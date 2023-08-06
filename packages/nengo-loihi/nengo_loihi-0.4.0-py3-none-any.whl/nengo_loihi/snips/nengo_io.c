#include <stdlib.h>
#include <string.h>
#include "nengo_io.h"

#define N_OUTPUTS 13
#define N_ERRORS 0
#define MAX_ERROR_LEN 0

int guard_io(runState *s) {
    return 1;
}

void nengo_io(runState *s) {
    NeuronCore *core786 = NEURON_PTR((CoreId){ .id=786 });
    NeuronCore *core787 = NEURON_PTR((CoreId){ .id=787 });
    CoreId coreId;
    int inChannel = getChannelID("nengo_io_h2c");
    int outChannel = getChannelID("nengo_io_c2h");
    int32_t count[1];
    int32_t spike[2];
    int32_t error_info[2];
    int32_t error_data[MAX_ERROR_LEN];
    int32_t error_index;
    int32_t output[N_OUTPUTS];

    if (inChannel == -1 || outChannel == -1) {
        printf("Got an invalid channel ID\n");
        return;
    }

    if (s->time % 100 == 0) {
        printf("time %d\n", s->time);
    }

    readChannel(inChannel, count, 1);
    // printf("count %d\n", count[0]);

    for (int i=0; i < count[0]; i++) {
        readChannel(inChannel, spike, 2);
        // printf("send spike %d.%d\n", spike[0], spike[1]);
        coreId = (CoreId) { .id=spike[0] };
        nx_send_discrete_spike(s->time, coreId, spike[1]);
    }

    // Communicate with learning snip
    s->userData[0] = N_ERRORS;
    error_index = 1;
    for (int i=0; i < N_ERRORS; i++) {
        readChannel(inChannel, error_info, 2);
        readChannel(inChannel, error_data, error_info[1]);
        s->userData[error_index] = error_info[0];
        s->userData[error_index + 1] = error_info[1];
        for (int j=0; j < error_info[1]; j++) {
            s->userData[error_index + 2 + j] = error_data[j];
        }
        error_index += 2 + error_info[1];
    }

    output[0] = s->time;
    output[1] = core786->cx_state[0].V;
    output[2] = core786->cx_state[1].V;
    output[3] = core786->cx_state[2].V;
    output[4] = core786->cx_state[3].V;
    output[5] = core786->cx_state[4].V;
    output[6] = core786->cx_state[5].V;
    output[7] = core787->cx_state[0].V;
    output[8] = core787->cx_state[1].V;
    output[9] = core787->cx_state[2].V;
    output[10] = core787->cx_state[3].V;
    output[11] = core787->cx_state[4].V;
    output[12] = core787->cx_state[5].V;

    writeChannel(outChannel, output, N_OUTPUTS);
}
