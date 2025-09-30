#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4096
#define TILE_SIZE 64  // example tile size, adjust based on cache and experiment

double **allocate_matrix(int n) {
    double **mat = (double **)malloc(n * sizeof(double *));
    for (int i = 0; i < n; i++) {
        mat[i] = (double *)malloc(n * sizeof(double));
    }
    return mat;
}

void free_matrix(double **mat, int n) {
    for (int i = 0; i < n; i++) {
        free(mat[i]);
    }
    free(mat);
}

void initialize_matrix(double **mat, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++)
            mat[i][j] = (double)(i + j);
}


// Version 4: Tiled [k,i,j]
void matmul_tiled_kij(double **A, double **B, double **C, int n, int tile) {
    for (int i = 0; i < n; i += tile)
        for (int j = 0; j < n; j += tile)
            for (int ii = i; ii < i + tile && ii < n; ii++)
                for (int jj = j; jj < j + tile && jj < n; jj++)
                    A[ii][jj] = 0.0;

    for (int k = 0; k < n; k += tile)
        for (int i = 0; i < n; i += tile)
            for (int j = 0; j < n; j += tile)
                for (int kk = k; kk < k + tile && kk < n; kk++)
                    for (int ii = i; ii < i + tile && ii < n; ii++)
                        for (int jj = j; jj < j + tile && jj < n; jj++)
                            A[ii][jj] += B[ii][kk] * C[kk][jj];
}

double get_time() {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return ts.tv_sec + ts.tv_nsec * 1e-9;
}

int main() {
    printf("Allocating matrices...\n");
    double **A = allocate_matrix(N);
    double **B = allocate_matrix(N);
    double **C = allocate_matrix(N);

    printf("Initializing matrices...\n");
    initialize_matrix(B, N);
    initialize_matrix(C, N);

    double start, end;

    // Tiled [k,i,j]
    printf("Running matmul_tiled_kij ...\n");
    start = get_time();
    matmul_tiled_kij(A, B, C, N, TILE_SIZE);
    end = get_time();
    printf("Time (tiled [k,i,j]): %f seconds\n", end - start);

    free_matrix(A, N);
    free_matrix(B, N);
    free_matrix(C, N);

    return 0;
}
