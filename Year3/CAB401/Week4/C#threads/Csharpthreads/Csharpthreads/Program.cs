using System;
using System.Threading;
using System.Threading.Tasks;

namespace Csharpthreads
{
    class Program
    {
        //static public void start(object? threadId)
        //{
        //    Thread.Sleep(1000);
        //    Console.WriteLine("Hello from the thread" + threadId);
        //}
        //static void Main(string[] args)
        //{
        //    Console.WriteLine("Hello from main");
        //    var thread = new Thread(start);
        //    thread.IsBackground = true;
        //    thread.Start(42);

        //    thread.Join();
        //}

        const int N = 33;
        static void Main(string[] args)
        {

            for(int i =0; i <N; i++)
            {
                Parallel.For(0, N, i =>
                {
                    Console.WriteLine("Hello {0} thread = {1} core = {2}", i, Thread.CurrentThread.ManagedThreadId, Thread.GetCurrentProcessorId());
                });
                

            }
        }


    }
}
