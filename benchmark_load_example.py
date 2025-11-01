from util.benchmark_parser import WorkerBenchmarkParser

def main(): 

    path = r"instances\Example_Instances_FJSSP-WF\Fattahi20.fjs"
    parser = WorkerBenchmarkParser()
    result = parser.parse_benchmark(path)
    print(result.durations())

    print(f"n_jobs: {result.n_jobs()}")
    print(f"n_machines: {result.n_machines()}")
    print(f"n_operations: {result.n_operations()}")
    print(f"get_workers_for_operation: {result.get_workers_for_operation(1)}")
    print(f"get_all_machines_for_all_operations: {result.get_all_machines_for_all_operations()}")
    print(f"get_workers_for_operation_on_machine: {result.get_workers_for_operation_on_machine(1, 1)}")
    print(f"is_possible: {result.is_possible(1,1,1)}")

if __name__ == "__main__":
    main()