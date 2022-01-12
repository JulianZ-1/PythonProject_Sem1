using System;
using System.Numerics;
using System.Threading;
using System.Threading.Tasks;

namespace DigitalMusicAnalysis
{
    public class timefreq
    {
        const int NUM_THREADS = 4; 
        public float[][] timeFreqData;
        public int wSamp;
        public Complex[] twiddles;
        private int blockSize;
        private int N;
        public float[][] Y;
        public Complex[] newX;
        public float fftMax;

        public timefreq(float[] x, int windowSamp)
        {
            int ii;
            double pi = 3.14159265;
            Complex i = Complex.ImaginaryOne;
            this.wSamp = windowSamp;
            twiddles = new Complex[wSamp];
            for (ii = 0; ii < wSamp; ii++)
            {
                double a = 2 * pi * ii / (double)wSamp;
                twiddles[ii] = Complex.Pow(Complex.Exp(-i), (float)a);
            }


            //Parallel.For(0, wSamp, new ParallelOptions { MaxDegreeOfParallelism = NUM_THREADS }, ii =>
            // {
            //     double a = 2 * pi * ii / (double)wSamp;
            //     twiddles[ii] = Complex.Pow(Complex.Exp(-i), (float)a);
            // });



            timeFreqData = new float[wSamp/2][];

            int nearest = (int)Math.Ceiling((double)x.Length / (double)wSamp);
            nearest = nearest * wSamp;

            Complex[] compX = new Complex[nearest];
            //for (int kk = 0; kk < nearest; kk++)
            //{
            //    if (kk < x.Length)
            //    {
            //        compX[kk] = x[kk];
            //    }
            //    else
            //    {
            //        compX[kk] = Complex.Zero;
            //    }
            //}

            Parallel.For(0, nearest, new ParallelOptions { MaxDegreeOfParallelism = NUM_THREADS }, kk =>
             {
                 if (kk < x.Length)
                 {
                     compX[kk] = x[kk];
                 }
                 else
                 {
                     compX[kk] = Complex.Zero;
                 }
             });


            int cols = 2 * nearest /wSamp;

            //for (int jj = 0; jj < wSamp / 2; jj++)
            //{
            //    timeFreqData[jj] = new float[cols];
            //}

            Parallel.For(0, wSamp / 2, new ParallelOptions { MaxDegreeOfParallelism = NUM_THREADS }, jj =>
              {
                  timeFreqData[jj] = new float[cols];
              });

            timeFreqData = stft(compX, wSamp);
	
        }

        float[][] stft(Complex[] x, int wSamp)
        {
            int ii = 0;
            int jj = 0;
            int kk = 0;
            int ll = 0;
            N = x.Length;
            fftMax = 0;
            newX = x;
            
            Y = new float[wSamp / 2][];

            //for (ll = 0; ll < wSamp / 2; ll++)
            //{
            //    Y[ll] = new float[2 * (int)Math.Floor((double)N / (double)wSamp)];
            //}


            Parallel.For(0, wSamp / 2, new ParallelOptions { MaxDegreeOfParallelism = NUM_THREADS }, ll =>
            {
                Y[ll] = new float[2 * (int)Math.Floor((double)N / (double)wSamp)];
            });

            Thread[] stftThreads = new Thread[NUM_THREADS];

            for (int iii = 0; iii < NUM_THREADS; iii++)
            {
                stftThreads[iii] = new Thread(funstft);
                stftThreads[iii].Start(iii);
            }
            for (int iii = 0; iii < NUM_THREADS; iii++)
            {
                stftThreads[iii].Join();
            }


            //Complex[] temp = new Complex[wSamp];
            //Complex[] tempFFT = new Complex[wSamp];

            //for (ii = 0; ii < 2 * Math.Floor((double)N / (double)wSamp) - 1; ii++)
            //{

            //    for (jj = 0; jj < wSamp; jj++)
            //    {
            //        temp[jj] = x[ii * (wSamp / 2) + jj];
            //    }

            //    tempFFT = fft(temp);

            //    for (kk = 0; kk < wSamp / 2; kk++)
            //    {
            //        Y[kk][ii] = (float)Complex.Abs(tempFFT[kk]);

            //        if (Y[kk][ii] > fftMax)
            //        {
            //            fftMax = Y[kk][ii];
            //        }
            //    }


            //}

            //Thread[] stftThreads2 = new Thread[NUM_THREADS];

            //for (int iii = 0; iii < NUM_THREADS; iii++)
            //{
            //    stftThreads2[iii] = new Thread(funstft);
            //    stftThreads2[iii].Start(iii);
            //}
            //for (int iii = 0; iii < NUM_THREADS; iii++)
            //{
            //    stftThreads2[iii].Join();
            //}


            for (ii = 0; ii < 2 * Math.Floor((double)N / (double)wSamp) - 1; ii++)
            {
                for (kk = 0; kk < wSamp / 2; kk++)
                {
                    Y[kk][ii] /= fftMax;
                }
            }

            return Y;
        }

        public Complex[] fft(Complex[] x, int L, Complex[] td)
        {
            int ii = 0;
            int kk = 0;
            int N = x.Length;

            Complex[] Y = new Complex[N];

            // NEED TO MEMSET TO ZERO?

            if (N == 1)
            {
                Y[0] = x[0];
            }
            else{

                Complex[] E = new Complex[N/2];
                Complex[] O = new Complex[N/2];
                Complex[] even = new Complex[N/2];
                Complex[] odd = new Complex[N/2];

                for (ii = 0; ii < N; ii++)
                {

                    if (ii % 2 == 0)
                    {
                        even[ii / 2] = x[ii];
                    }
                    if (ii % 2 == 1)
                    {
                        odd[(ii - 1) / 2] = x[ii];
                    }
                }

                E = fft(even,L,td);
                O = fft(odd,L,td);

                for (kk = 0; kk < N; kk++)
                {
                    Y[kk] = E[(kk % (N / 2))] + O[(kk % (N / 2))] * td[kk * (L / N)];
                }
            }

           return Y;
        }
        public void funstft(object Id)
        {
            int threadId = (int)Id;
            blockSize = (2 * (int)Math.Floor(N / (double)wSamp) - 1) / NUM_THREADS;
            int blockSize2 = 2 * (int)Math.Floor(N / (double)wSamp) - 1;
            int start = threadId * blockSize;
            int finish = Math.Min(start + blockSize, blockSize2);

            Complex[] temp = new Complex[wSamp];
            Complex[] tempFFT = new Complex[wSamp];

            for (int ii = start; ii < finish; ii++)
            {

                for (int jj = 0; jj < wSamp; jj++)
                {
                    temp[jj] = newX[ii * (wSamp / 2) + jj];
                }

                tempFFT = fft(temp,wSamp, twiddles);

                for (int kk = 0; kk < wSamp / 2; kk++)
                {
                    Y[kk][ii] = (float)Complex.Abs(tempFFT[kk]);

                    if (Y[kk][ii] > fftMax)
                    {
                        fftMax = Y[kk][ii];
                    }
                }    

            }
        }

        //dont use failed
        //public void funstft2(object Id2) 
        //{
        //    int threadId = (int)Id2;
        //    blockSize = (2 * (int)Math.Floor(N / (double)wSamp) - 1) / NUM_THREADS;
        //    int blockSize2 = (2 * (int)Math.Floor(N / (double)wSamp) - 1);
        //    int start = threadId * blockSize;
        //    int finish = Math.Min(start + blockSize, blockSize2);
        //    for (int ii = start; ii < finish; ii++)
        //    {
        //        for (int kk = 0; kk < wSamp / 2; kk++)
        //        {
        //            Y[kk][ii] /= fftMax;
        //        }
        //    }


        //}

    }
}
