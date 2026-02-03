<style>
    .markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}
</style>
# Competition on Flexible Job Shop Scheduling Problems with Worker Flexibility under Uncertainty (FJSSP-WU Com)
---

## Overview
---
The competition on Flexible Job Shop Scheduling Problems with Worker Flexibility (FJSSP-W) under optional Uncertainty focuses on optimizing production schedules where workers can operate multiple machines but show different skill levels (i.e., processing times) across the tasks. This problem is highly relevant for manufacturing, logistics, and energy operations, where assigning flexible workers affects cost and lead time and where variability in processing rates increases scheduling complexity. The competition further addresses the impact of uncertainty in processing times. This reflects the variability of human workers' processing times to evaluate the robustness of algorithms under more realistic operational conditions. 

Although there are many different methods for solving FJSSP-W (e.g. Mathematical Programming, Constraint Programming, etc.), this competition is especially designed for meta-heuristics, such as Evolutionary Algorithms, Swarm Algorithms, or other nature- and physics-inspired methods. Such algorithms often show great results, especially for very complex problem instances. Since there are only a few comparable benchmark instances, such algorithms should demonstrate their capabilities in this competition and compare their performance. In this way, the research community can gain valuable insights into the performance and working principles of contemporary solvers for this class of problems. 

The competition provides 30 FJSSP-W benchmark instances with diverse problem characteristics, which rely on well-known FJSSP problem instances. An evaluation method for the FJSSP-W instances as well as a simulation environment for the uncertain scenarios is also specified and provided as Python code. The participants must address at least one of the two different scenarios of the competition, i.e. they may decide to choose the option with or without uncertainty influences on the processing times. The distinction broadens the scope of the competition by allowing existing solvers that were not directly developed for optimization under uncertainty to participate in the competition. 

## Competition Goals
---
For the first scenario of the competition, the main objective to minimize the makespan across the proposed FJSSP-W test problems. The makespan represents the total time required to complete all tasks in a schedule, i.e. the duration from the start of the first task to the completion of the last task. It represents a critical metric in scheduling because it directly impacts the overall efficiency and performance of a production process. For this reason, it is often the main criterion for a company.  

For the second scenario of the competition, the goal is to produce robust schedules towards stochastic processing times. The overall objective remains with the minimization of the makespan. However, the makespan should deteriorate as little as possible when tested subject to the uncertainty simulations. The provided simulation uses different probability distributions for each worker to emulate the fluctuating work performance expected from human workers. The respective parameters are provided by the testing environment and also need to be used for the evaluation of the final result.  

As companies are also interested in a balanced distribution of tasks across the workers, we will consider worker balance as a potential tie breaker in case two solvers return equal makespan values on one problem instance.  

By doing so, the competition provides a tool for evaluating and comparing scheduling algorithms tailored to FJSSP-W problems. It offers an opportunity to gain insights into the algorithms’ practical relevance in dynamic production environments, where balancing employee flexibility, machine utilization, and production time is essential.  

## Competition Rules
---

As the competition intends to focus on meta-heuristical solvers of the FJSSP-WF, each solver needs to be executed on each problem instance at least 10 times with a fixed function evaluation budget of 5,000,000. This way, the stochasticity of the solvers is accounted for. After exceeding the time or function evaluation limit, the best candidate solution found needs to be reported for all 10 individual algorithm runs. The feasibility of these final candidate solutions will be evaluated by the organization team after submission of the results.  

Notice that each evaluation of a solution's makespan is counted as a function evaluation. For scenario 2, this means that if multiple simulations are used to average the uncertainty in the objective function, multiple function evaluations must be counted. 

For scenario 2, the uncertainty parameters retrieved from the function provided by the environment cannot be changed. 

In addition, the results should be properly prepared according to the following sections and a detailed description of the participating algorithm, and its working principles should be available.  

Furthermore, we expect a minimum of novelty value from all submissions, be it the presentation of novel algorithmic ideas or the more detailed and dedicated benchmarking of an algorithm already presented on a few problem instances or real-world problems.  

## Submission process
---
### Solver 

The algorithmic source code as well as the algorithmic results need to be submitted to the organizers of the competition via Submission Issues in a prepared Github repository. 

In the style of the COCO BBOB benchmarking suite, we intend to accept submissions as Github issues. That is, the code, the data and optional additional materials can be made available in a clear and organized way.

### Data 

The algorithms are tested on the provided benchmark FJSSP-W instances. The instances are generated based on well-known benchmark problems for the FJSSP. 

For scenario 1, the submissions are ranked according to the makespan (duration of the start of the first operation to the end of the last operation) of the solution over all benchmark instances.  

If the makespan results in a tie, the workload balance for the workers is determined to break the tie. 

For scenario 2, the submissions are ranked according to the makespan obtained for the final solution over several simulation runs. The final solution is evaluated on 50 noisy simulation runs and the mean makespan resulting from these simulations is used for the comparison.  If the mean makespan results in a tie, the relation of the makespan of the original schedule to the mean makespan after the simulations is used as secondary criteria. 

For either scenario, if the secondary measurement still results in a tie, the required function evaluations to reach the best result are used. 

The submissions need to include 
<ul>
    <li>A CSV or JSON file containing one entry for every benchmark instance and each of the 10 individual algorithms runs on each instance </li>
    <ul>
        <li>an ordered list of all start times for all operations  </li>
        <li>an ordered list of all machine assignments for all operations </li>
        <li>an ordered list of all worker assignments for all operations </li>
        <li>the name of the benchmark instance </li>
        <li>number of function evaluations to achieve the best result</li>
        <li><b>For scenario 2 also:</b> the uncertainty parameters provided by the simulation environment</li>
    </ul>
    <li>a description of the algorithm (solver) </li>
    <li>the code of the solver </li>
    <li>a description of the used hardware </li>
    <li>Name, affiliation and emails of the participants </li>
</ul>
The lists are ordered according to the jobs of the benchmark instance (e.g. Job 1 Operation 1, Job 1 Operation 2, Job 2 Operation 1, Job 3 Operation 1, Job 3 Operation 2). 

The functions used to determine the makespan and workload balance are provided by the competition to make sure everyone uses the same metrics. The required simulation functions are also provided. 

In case there are any open questions about the submission process or format, you can contact: david.hutter@fhv.at

### Paper 

Each submission needs to be accompanied with a formal description of the solver applied that incorporates a proper algorithm description in pseudo code as well as the mandatory results requested for this specific competition. The authors are required to use a submission template prepared by the organizing team and made available in the submission repository in case the competition is accepted. 

Each competition entry is expected to report the working principles of the approach as well as the obtained results in form of a paper submitted in style of the conference requirements. 

## Evaluation
---
The submissions are primarily evaluated by the makespans of their resulting schedules.  All 10 independent runs of each participating algorithm are ranked on every single problem instance. The overall score of an algorithm on a single instance will be defined as the sum of all obtained ranks of the algorithm runs. This way we identify a ranking score on each instance and take into account the stochasticity of the solvers (algorithms that provide solution with very diverse quality are expected to achieve worse ranks than algorithms that consistently provide similar quality solutions). This is in line with other competitions (https://www.minizinc.org/challenge/) that on the different instances. The total rank of an algorithm will then be determined as the sum over all problem instances.  

The two scenarios of the competition are scored independently to allow participants to choose to only work on one of the issues. 

In the case of a tie on an instance with another submission, the workload balance of the schedules is considered as the secondary metric for comparison. For the second scenario, the ratio of the simulated makespan to the original makespan is considered to measure the deterioration of the schedule under uncertainty. If the secondary comparison still results in a draw (e.g. if the exact same solution was found), the number of function evaluations required to achieve the solution is used as the final comparison metric. 

The submitted solutions are expected to be feasible solutions. However, due to the possibility of different encodings used for the problem, there is no algorithm provided to test the feasibility of the created solutions during the optimization process. For this reason, we will leave the feasibility check to the participants. Yet, since the submission format of the solutions is mandatory and fixed, submitted solutions can be tested for feasibility by the team of organizers prior to the acceptance of the submission. If anything is unclear, we will get in touch with the participants. 

Additional analysis of the performance of the individual algorithms on different subsets of the problem instances and specific problem characteristics will be conducted and presented but do not influence the rankings of the competition. 

## Usage Example of the provided environment
---
### Scenario 1 FJSSP-W
```python
# This is an example solution of the Fattahi20 FJSSP-W instance
s = [0, 201, 341, 503, 198, 397, 610, 727, 0, 61, 244, 341, 0, 79, 470, 701, 79, 316, 760, 997, 603, 765, 886, 994, 93, 250, 397, 994, 224, 485, 779, 1008, 593, 760, 963, 1010, 0, 224, 455, 634, 457, 596, 836, 874, 61, 389, 596, 779]
m = [2, 6, 4, 7, 0, 1, 5, 4, 1, 6, 4, 7, 0, 4, 3, 5, 0, 6, 1, 7, 3, 2, 4, 3, 2, 2, 6, 4, 3, 4, 6, 6, 1, 3, 6, 5, 3, 5, 5, 7, 1, 2, 4, 5, 1, 2, 6, 7]
w = [0, 9, 2, 5, 11, 0, 10, 6, 1, 8, 2, 6, 7, 10, 0, 5, 9, 3, 8, 5, 8, 4, 11, 9, 3, 8, 11, 4, 7, 1, 9, 2, 7, 1, 8, 8, 5, 1, 4, 0, 3, 9, 6, 7, 4, 9, 11, 3]
bpath = r'instances/Example_Instances_FJSSP-WF'
from util.benchmark_parser import WorkerBenchmarkParser
parser = WorkerBenchmarkParser()
encoding = parser.parse_benchmark(bpath + '/' + 'Fattahi20.fjs')
instance = {
    's': s,
    'm': m,
    'w': w,
    'd': encoding.durations(),
    'js': encoding.job_sequence()
}

import util.evaluation as evaluation
# Calculate the makespan of the provided solution
makespan = evaluation.makespan(start_times, machines, workers, encoding.durations())
# Calculate the workload balance for the workers if required
worker_balance = evaluation.workload_balance(m, w, encoding.durations())
```

### Scenario 2: FJSSP-W under uncertainty
```python
# This is an example solution of the Fattahi20 FJSSP-W instance
s = [0, 201, 341, 503, 198, 397, 610, 727, 0, 61, 244, 341, 0, 79, 470, 701, 79, 316, 760, 997, 603, 765, 886, 994, 93, 250, 397, 994, 224, 485, 779, 1008, 593, 760, 963, 1010, 0, 224, 455, 634, 457, 596, 836, 874, 61, 389, 596, 779]
m = [2, 6, 4, 7, 0, 1, 5, 4, 1, 6, 4, 7, 0, 4, 3, 5, 0, 6, 1, 7, 3, 2, 4, 3, 2, 2, 6, 4, 3, 4, 6, 6, 1, 3, 6, 5, 3, 5, 5, 7, 1, 2, 4, 5, 1, 2, 6, 7]
w = [0, 9, 2, 5, 11, 0, 10, 6, 1, 8, 2, 6, 7, 10, 0, 5, 9, 3, 8, 5, 8, 4, 11, 9, 3, 8, 11, 4, 7, 1, 9, 2, 7, 1, 8, 8, 5, 1, 4, 0, 3, 9, 6, 7, 4, 9, 11, 3]
bpath = r'instances/Example_Instances_FJSSP-WF'
from util.benchmark_parser import WorkerBenchmarkParser
parser = WorkerBenchmarkParser()
encoding = parser.parse_benchmark(bpath + '/' + 'Fattahi20.fjs')
instance = {
    's': s,
    'm': m,
    'w': w,
    'd': encoding.durations(),
    'js': encoding.job_sequence()
}

# The implemented graph class requires the ending times for the simulations
e = [instance['s'][i]+instance['d'][i][instance['m'][i]][instance['w'][i]] for i in range(len(instance['s']))]
instance['e'] = e

# The Graph class expects the starting times 's', the ending times 'e', the machine assignments 'm', the worker assignments 'w', and the job sequence 'js'. 
# The optional parameter 'leftshift' : bool = False disables possible leftshifts (if the probability distribution allows for faster operation finished instead of only delays, the graph can compensate by adjusting the operations to an earlier starting time.)
# The optional parameter 'buffers' : list[float] = [] allows to add planned buffer times if they are part of the optimization process. The buffer times here are given as a percentage of the operations duration. If buffer times are given, the vector needs to have the same
# length as the sequence vector.
g = Graph(instance['s'], e, instance['m'], instance['w'], instance['js'])

n_workers = max(w)+1
from util.uncertainty import create_uncertainty_vector
# The function create_uncertainty_vector has 2 optional parameters
# The optional parameter 'factor' : float = 10.0 determines the ratio of alpha and beta for the used beta distribution beta = alpha * factor
# The default value 10.0 creates distributions that favor many smaller deviations and only few large delays caused by the workers
# The optional parameter 'offset' : float = 1.0 can be used to enforce an offset for the processing times, where e.g. offset = 1.1 would cause all processing times
# to be at least 10% longer than the original processing times
uncertainty_parameters = create_uncertainty_vector(n_workers)

# This example shows how the Graph class is used to run multiple simulations to gather multiple results to account for the random nature of the uncertainties
results = []
n_simulations = 50
for i in range(n_simulations):
    g = Graph(instance['s'], e, instance['m'], instance['w'], instance['js'])
    # Note that while the environment offers other types of uncertainties, the competition only
    # uses the uncertainties attached to the processing times.
    g.simulate(instance['d'], uncertainty_parameters, processing_times=True)
    results.append(float(max(g.e)))


import statistics
robust_makespan = statistics.mean(results)
robust_makespan_stdev = statistics.stdev(results)
R = robust_makespan/max(e)

# NOTE: as a shorthand for the above execution of the simulations, alternatively one can use, which returns the same metrics and the collection of the simulation results
results, robust_makespan, robust_makespan_stdev, R = run_n_simulations(instance['s'], e, instance['m'], instance['w'], instance['js'], instance['d'], uncertainty_parameters, n_simulations, processing_times=True)

print(f'Original Makespan: {max(e)} | Robust Makespan: {robust_makespan:.4f} - {robust_makespan_stdev:.4f} | Original-Robust Relation: {R:.4f}')
```

## Organizers
<b>Michael Hellwig</b> is a Senior Scientist at the Information Systems Research Center at Vorarlberg University of Applied Sciences in Dornbirn (Austria) and a lecturer in Business Mathematics and Statistics at the University of Liechtenstein. He studied Mathematics at the Technical University of Dortmund and received his doctorate in Theoretical Computer Science from the University of Ulm in 2017. During his post-doc period, he concentrated on the development and the theoretical analysis of Evolution Strategies in noisy and constrained search spaces. In connection with this, he has also dealt intensively with benchmarking aspects and contributed to the development of systematic test instances. Since 2021, he has been director of the Josef Ressel Centre for Robust Decision Making, which focuses on the application of Computational Intelligence methods for data-driven decision support in companies. In this context, he currently deals with the topic of worker flexibility and uncertainty in scheduling problems, among other topics. 

 <b>David Hutter</b> is a PhD student at the Josef Ressel Centre for Robust Decision Making at Vorarlberg Universitiy of Applied Sciences in Dornbirn (Austria) and the Department of Computer Sciences at the University of Innsbruck (Austria). He received his master’s degree in Computer Science from Vorarlberg University of Applied Sciences in Dornbirn (Austria). Currently, he mainly works on production scheduling problems, including the flexible job shop scheduling problem (FJSSP), the FJSSP with worker flexibility and the FJSSP with respect to different types of uncertainties. 
 
<b>Thomas Steinberger</b> is a is a Senior Scientist at the Information Systems Research Center at Vorarlberg University of Applied Sciences in Dornbirn (Austria) and a lecturer on Mathematics and Statistics at Vorarlberg University of Applied Sciences. He studied Mathematics at the University of Vienna and received his doctorate in Mathematics in 1997. His current research focusses on MIP and CP formulations of scheduling problems and on applications of neural networks to image classification problems. 

## Acknowledgements
The financial support by the Austrian Federal Ministry of Labour and Economy, the National Foundation for Research, Technology and Development, the Christian Doppler Research Association is gratefully acknowledged.
