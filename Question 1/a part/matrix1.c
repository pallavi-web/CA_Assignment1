#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 4096

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


// Version 1: Simple [i,j,k]
void matmul_simple_ijk(double **A, double **B, double **C, int n) {
    for (int i = 0; i < n; i++)
        for (int j = 0; j < n; j++) {
            A[i][j] = 0.0;
            for (int k = 0; k < n; k++)
                A[i][j] += B[i][k] * C[k][j];
        }
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

    // Simple [i,j,k]
    printf("Running matmul_simple_ijk ...\n");
    start = get_time();
    matmul_simple_ijk(A, B, C, N);
    end = get_time();
    printf("Time (simple [i,j,k]): %f seconds\n", end - start);

    free_matrix(A, N);
    free_matrix(B, N);
    free_matrix(C, N);

    return 0;
}
