#include <stdio.h>
#include <Windows.h>
#include <assert.h>
#include <chrono>


int NUM_THREADS = 16;

long long N = 1500;


double** A, ** B, ** C;

//create thread
DWORD WINAPI MultiplyMutiply(LPVOID IpThreadParameter)
{	
	int threadID = (int)IpThreadParameter;
	int itemsPerThread = (N + NUM_THREADS-1) / NUM_THREADS;
	int startIndex = itemsPerThread * threadID;
	int endIndex = min(startIndex + itemsPerThread, N);


	for (int i = startIndex; i < endIndex; i++)
	{
		for (int j = 0; j < N; j++) {
			double total = 0;
			for (int k = 0; k < N; k++)
			{
				total += A[i][k] * B[i][k];
			}
			C[i][j] = total;
		}
	}
	

	
	return 0;

}


// In the main funciton, hadel = type and wait till that handel is done and then return 0;
int main(int argc, char* argv[])
{


	A = new double* [N];
	B = new double* [N];
	C = new double* [N];

	srand(42);

	for (int z = 0; z < N; z++)
	{
		A[z] = new double[N];
		B[z] = new double[N];
		C[z] = new double[N];
		for (int j = 0; j < N; j++)
		{
			A[z][j] = rand();
			B[z][j] = rand();
		}
	}
	auto start_time = std::chrono::high_resolution_clock::now();

	HANDLE* handles = new HANDLE[NUM_THREADS];

	for (int i = 0; i < NUM_THREADS; i++)
	{
		handles[i] = CreateThread(NULL, 0, MultiplyMutiply, (LPVOID)i, 0, NULL);
	}

	WaitForMultipleObjects(NUM_THREADS, handles, TRUE, INFINITE);




	auto end_time = std::chrono::high_resolution_clock::now();
	std::chrono::duration<double> duration = end_time - start_time;
	printf("%f seconds \n", duration.count());



	//printf("Hello world\n");

	////for (int i = 0; i < N; i++)
	////{
	////	printf("some computation %d\n", i);
	////}

	//


	return 0;


}