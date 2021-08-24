#include <stdio.h>
#include <Windows.h>
#include <assert.h>
#include <chrono>
using namespace std::chrono;

const int THREADS = 32;
HANDLE handles[THREADS];
HANDLE mylock;
long long N;
double* A;
double totalSequential, totalParallel, totalParallelWithLock;

high_resolution_clock::time_point startTime;

void StartTiming() {
	startTime = high_resolution_clock::now();
}

double StopTiming() {
	duration<double> duration = high_resolution_clock::now() - startTime;
	return duration.count();
}

DWORD WINAPI sumNaive(LPVOID lpThreadParameter) {
	int threadId = (int)lpThreadParameter;
	long long blockSize = (N + THREADS - 1) / THREADS;
	long long start = threadId + blockSize;
	long long end = min(start + blockSize, N);
	for (long long  i = start; i < end; i++)
		totalParallel += A[i];
	return 0;
}

DWORD WINAPI sumWithlock(LPVOID lpThreadParameter) {
	int threadId = (int)lpThreadParameter;
	long long blockSize = (N + THREADS - 1) / THREADS;
	long long start = threadId + blockSize;
	long long end = min(start + blockSize, N);
	for (lonWWg long i = start; i < end; i++)
	{
		// get the lock here
		WaitForSingleObject(mylock, INFINITE);
		totalParallelWithLock += A[i];
		// let go of the lock here
		ReleaseMutex(mylock);

	}
	return 0;
}


int main(int argc, char* argv[]) {

	mylock = CreateMutexA(0, FALSE, "MyLock");

	for (N = 10; true; N * 10)
	{
		printf("N = %lld\n", N);

		A = new double[N];

		for (long long i = 0; i < N; i++)
			A[i] = 1.0;

		StartTiming();

		totalSequential = 0;
		for (long long i = 0; i < N; i++)
			totalSequential += A[i];

		double sequentialTime = StopTiming();

		printf("Sequential total %f, %f seconds\n", totalSequential, sequentialTime);
		//---------------------------------------------------------------------------------

		StartTiming();
		totalParallel = 0;
		for (int t = 0; t < THREADS; t++)
			handles[t] = CreateThread(0, 0, sumNaive, (void*)t, 0, 0);
		WaitForMultipleObjects(THREADS, handles, true, INFINITY);

		double parallelTime = StopTiming();

		printf("Parallel total %f, %.7f seconds\n", totalParallel, parallelTime);

		//---------------------------------------------------------------------------------

		StartTiming();
		totalParallelWithLock = 0;
		for (int t = 0; t < THREADS; t++)
			handles[t] = CreateThread(0, 0, sumWithlock, (void*)t, 0, 0);
		WaitForMultipleObjects(THREADS, handles, true, INFINITY);

		double totalParallelWithLock = StopTiming();

		printf("ParallelWithLock total %f, %.7f seconds\n", totalParallelWithLock, parallelTime);
		delete[] A;
	}

	return 0;
}