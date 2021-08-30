#include <stdio.h>
#include <stdlib.h>
#include <chrono>
#include <omp.h>


#define N 2000

int main(int argc, char* argv[])
{
	double* A = new double[N * N];
	double* B = new double[N * N];
	double* C = new double[N * N];

	srand(42);

	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++) {
			A[i * N + j] = rand();
			B[i * N + j] = rand();
		}
	}

	omp_set_num_threads(8);

	auto start_time = std::chrono::high_resolution_clock::now();

#pragma omp parallel for
	for (int i = 0; i < N; i++)
	{
		for (int j = 0; j < N; j++) {
			C[i * N + j] = 0;
		}
	}

#define BLOCK_SIZE  10
#pragma omp parallel for
	for (int ii = 0; ii < N; ii+= BLOCK_SIZE)
	{
		for (int jj = 0; jj < N; jj+= BLOCK_SIZE) {
			for (int kk = 0; kk < N; kk+= BLOCK_SIZE)
			{
				for (int i = ii; i < ii+ BLOCK_SIZE; i++)
				{
					for (int j = jj; j < jj+ BLOCK_SIZE; j++) {
						for (int k = kk; k < kk + BLOCK_SIZE; k++)
						{
							C[i * N + j] += A[i * N + k] * B[k + j * N];

						}
					}
				}
			}
		}
	}
	auto finish_time = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duration = finish_time - start_time;
	printf("%f seconds\n", duration.count());

	return 0;
}
