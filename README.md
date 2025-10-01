README.txt

HPCA Assignment 1
	-by Nikhil Tayade & Pallavi Chauhan
	-nikhiltayade@iisc.ac.in & pallavi2@iisc.ac.in
	-25952 & 26144
	
Description:
This project involves performance analysis and benchmarking of matrix multiplication and BFS graph traversal algorithms on an 11th Gen Intel Core i5-11500 CPU system using Linux. It uses hardware performance counters for detailed measurement of cache/memory bandwidth, FLOPS, IPC, and CPI stacks. The project incorporates LIKWID microbenchmarks and perf tools to characterize hardware-software interaction.

System Setup:
- Linux OS with required tools: gcc, perf, likwid, cmake, git, python, Jupyter Notebook
- Hardware: 11th Gen Intel Core i5-11500, Linux

Installation:
1. Update packages:
   sudo apt update
2. Install dependencies:
   sudo apt install cmake g++ git
3. Clone BFS benchmark repo:
   git clone https://github.com/sbeamer/gapbs.git
   git clone https://github.com/passlab/NeoRodinia
4. Build GAP BFS binaries:
   cd gapbs
   make
5. Optionally, run tests:
   make test

Memory Bandwidth Microbenchmarks (LIKWID):
- Run load_avx benchmark for different cache sizes:
  likwid-bench -t load_avx -w S0:1GB:1 		---> DRAM Cache Bandwidth
  likwid-bench -t load_avx -w S0:6MB:1 		---> L3 Cache Bandwidth
  likwid-bench -t load_avx -w S0:256kB:1 	---> L2 Cache Bandwidth
  likwid-bench -t load_avx -w S0:32kB:1		---> L1 Cache Bandwidth

Matrix Multiplication:
- Compile variants:
  gcc -O2 -march=native -o matrix1op matrix1.c
  gcc -O2 -march=native -o matrix2op matrix2.c
  gcc -O2 -march=native -o matrix3op matrix3.c
  gcc -O2 -march=native -o matrix4op matrix4.c
- Execute with perf stats:
  taskset -c 0 perf stat -e cache-references,cache-misses,
  fp_arith_inst_retired.scalar_double,... ./matrixYop 		
  
  ---->Y = [1(for Simple_ijk),2(for Simple_kij),3(for Tiled_ijk),4(for Tiled_kij)]

- To plot the roofline model, Run the below command:
  python3 rooflineplot1.py


GAPBS BFS:
- Run BFS on graph:
  ./bfs -g 25 -n 1
- Measure performance counters:
	perf stat -e cpu-cycles -e instructions -e cache-references -e cache-misses 
	-e L1-dcache-loads -e L1-dcache-load-misses -e L1-dcache-stores -e L1-dcache-store-misses 
	-e l2_rqsts.demand_data_rd_hit -e l2_rqsts.demand_data_rd_miss -e LLC-loads 
	-e LLC-load-misses -e LLC-stores -e LLC-store-misses -e dTLB-loads -e dTLB-load-misses 
	-e branch-loads -e branch-load-misses ./bfs -g 25 -n 1


For CPI Stack Programs
1. GAPBS BFS with 2^22 vertices
2. Rodinia BFS with 20 million vertices

- Navigate to the following directory Question 2\gap bfs benchmark\gapbs\src:
- Run the below command to get the data for Question 2 with GAPBS BFS:
	sudo perf stat -e L1-dcache-loads,L1-dcache-load-misses, 
    l2_rqsts.demand_data_rd_hit,l2_rqsts.demand_data_rd_miss,
    LLC-load-misses,LLC-loads,dTLB-loads,dTLB-load-misses, 
    iTLB-load-misses,branch-instructions,branch-misses,cpu-cycles,
    instructions -I 10 -o perf_raw.txt -- ./bfs -g 22 -n 20
	
- For GAPBS, Navigate to the following directory: Question 2\gap bfs benchmark
	
- To get IPC Plot, run the following command:
	python3 bfs_gap_IPC_Plot

- To get CPI Stack, run the following in Jupyter Notebook:
	Question 2\gap bfs benchmark\Linear_regression_CPI_Plot.ipynb

- For Rodinia, Navigate to the following directory: Question 2\rodinia bfs benchmark
	
- For Rodinia, we need bfs graph generator, which is in Question 2\rodinia bfs benchmark\NeoRodinia\bfs\inputgen
	.\graphgen 20000000 -o graph20M.txt

- Run the below command to get the data for Question 2 with Rodinia BFS:
    sudo perf stat -e L1-dcache-loads,L1-dcache-load-misses,
    l2_rqsts.demand_data_rd_hit,l2_rqsts.demand_data_rd_miss,
    LLC-load-misses,LLC-loads,dTLB-loads,dTLB-load-misses,
    iTLB-load-misses,branch-instructions,branch-misses,
    cpu-cycles,instructions -I 10 -o data2.txt -- 
    ./bfs_omp_CPU_P3_clang_O1_exec graph20M.txt	
	
- To clean the data obtained above in data2.txt file:
	python3 DataClean.py

- To get IPC Plot, run the following command:
	python3 IPC_Plot

- To get CPI Stack, run the following in Jupyter Notebook:
	Question 2\rodinia bfs benchmark\Linear_regression_CPI_Plot.ipynb




System Inspection:
- View hardware info:
  lshw

Notes:
- Use taskset or affinity setting to pin workloads on specific cores for performance consistency.
- LIKWID benchmarks measure bandwidth at DRAM and cache levels.
- Performance counters provide insights into cache misses, FLOPS, branch misses, and influence composite metrics like IPC and CPI stack.
- This workflow supports building roofline models and detailed microarchitectural analysis.

Contact:
For questions or contributions, please contact the project owner- pallavi2@iisc.ac.in
