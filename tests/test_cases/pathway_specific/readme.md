# Causal Pathway Test Suite
This folder contains input_message files developed such that each file tests the particular causal pathway that they are named for.

## Input/Output Expectations
For each input message, the following is an exhaustive list of the expected outcomes from thinkpudding and esteemer.

### Goal Approach CPtest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |GLU03   | Goal Approach     | 50 (goal)     | Approach Goal          |
| Acceptable      |GLU03   | Social Approach   | 100 (50th)    | Approach Peer Average  |
| Acceptable      |GLU03   | Social Approach   | 100 (75th)    | Approach Top 25 peer Benchmark  |
| Acceptable      |GLU03   | Social Approach   | 100 (90th)    | Approach Top 10 Peer Benchmark  |
| Acceptable      |GLU03   | Improving         | n/a           | Performance Improving  |
| Acceptable      |GLU03   | Improving         | n/a           | Congrats Improved Performance  |
| Acceptable      |GLU03   | Social Worse      | 100 (90th)    | Not Top Performer|
| Acceptable      |GLU03   | Unknown           | 100 (50th)    | Opportunity to Improve Peer Average|
| Acceptable      |GLU03   | Unknown           | 50 (goal)     | Opportunity to Improve Goal|

### Goal Gain CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |TOC01   | Goal Gain         | 90 (goal)     | Reached Goal   |
| Acceptable      |TOC01   | Improving         | n/a           | Performance Improving |
| Acceptable      |TOC01   | Improving         | n/a           | Congrats Improved Performance |
| Acceptable      |TOC01   | Social Better     | 1 (90th)     | Top Performer         |
| Acceptable      |TOC01   | Social Better     | 1 (75th)     | In Top 25%     |
| Acceptable      |TOC01   | Unknown           | 1 (90th)     | Consistently High Performance |

### Goal Loss CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |ABX01   | Goal Loss         | 90 (goal)     | Drop Below Goal |
| Acceptable      |ABX01   | Worsening         | n/a           | Getting Worse  |
| Acceptable      |ABX01   | Worsening         | n/a           | Performance Dropped |
| Acceptable      |ABX01   | Social Worse      | 99 (90th)     | Not Top Performer|
| Acceptable      |ABX01   | Unknown           | 99 (50th)    | Opportunity to Improve Peer Average|
| Acceptable      |ABX01   | Unknown           | 90 (goal)     | Opportunity to Improve Goal|

### Improving CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |GLU12   | Improving         | n/a           | Performance Improving |
| Selected        |GLU12   | Improving         | n/a           | Congrats Improved Performance |
| Acceptable      |GLU12   | Social Worse      | 99 (90th)     | Not Top Performer|
| Acceptable      |GLU12   | Unknown           | 99 (50th)     | Opportunity to Improve Peer Average|
| Acceptable      |GLU12   | Unknown           | 99 (goal)     | Opportunity to Improve Goal|
| Acceptable      |GLU12   | Goal Approach     | 99 (goal)     | Approach Goal          |
| Acceptable      |GLU12   | Social Approach   | 99 (50th)    | Approach Peer Average  |
| Acceptable      |GLU12   | Social Approach   | 99 (75th)    | Approach Top 25 peer Benchmark  |
| Acceptable      |GLU12   | Social Approach   | 99 (90th)    | Approach Top 10 Peer Benchmark  |

### Social Approach CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |TOC02   | Social Approach   | 50 (50th)     | Approach Peer Average |
| Acceptable      |TOC02   | Social Approach   | 100 (75th)    | Approach Top 25 peer Benchmark  |
| Acceptable      |TOC02   | Social Approach   | 100 (90th)    | Approach Top 10 Peer Benchmark  |
| Acceptable      |TOC02   | Unknown           | 50 (50th)     | Opportunity to Improve Peer Average|
| Acceptable      |TOC02   | Unknown           | 100 (goal)    | Opportunity to Improve Goal|
| Acceptable      |TOC02   | Improving         | n/a           | Performance Improving |
| Acceptable      |TOC02   | Improving         | n/a           | Congrats Improved Performance |
| Acceptable      |TOC02   | Social Worse      | 100 (90th)    | Not Top Performer|

### Social Better CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |SUS04   | Social Better     | 96 (90th)     | Top Performer |
| Acceptable      |SUS04   | Social Better     | 1 (75th)      | In Top 25%    |
| Acceptable      |SUS04   | Unknown           | 96 (90th)     | Consistently High Performance |

### Social Gain CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |TOC01   | Social Gain       | 50 (50th)     | Achieved Peer Average   |
| Acceptable      |TOC01   | Improving         | n/a           | Performance Improving |
| Acceptable      |TOC01   | Improving         | n/a           | Congrats Improved Performance |
| Acceptable      |TOC01   | Unknown           | 99 (goal)     | Opportunity to Improve Goal|
| Acceptable      |TOC01   | Goal Approach     | 99 (goal)     | Approach Goal          |
| Acceptable      |TOC01   | Social Approach   | 99 (75th)     | Approach Top 25 peer Benchmark  |
| Acceptable      |TOC01   | Social Approach   | 99 (90th)     | Approach Top 10 Peer Benchmark  |

### Social Loss CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |PONV05  | Social Loss       | 50 (50th)     | Drop Below Peer Average|
| Acceptable      |PONV05  | Worsening         | n/a           | Getting Worse  |
| Acceptable      |PONV05  | Worsening         | n/a           | Performance Dropped |
| Acceptable      |PONV05  | Social Worse      | 100 (90th)    | Not Top Performer|
| Acceptable      |PONV05  | Unknown           | 100 (50th)    | Opportunity to Improve Peer Average|
| Acceptable      |PONV05  | Unknown           | 100 (goal)    | Opportunity to Improve Goal|

### Social Worse CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |GLU08   | Social Worse      | 50 (90th)     | Not Top Performer|
| Acceptable      |GLU08   | Social Better     | 1 (75th)      | In Top 25%    |

### Worsening CPTest
| Classification  |Measure | Causal Pathway    |Comparator     |  Message Template Name |
|-----------------|--------|-------------------|---------------|------------------------|
| Selected        |TRAN02  | Worsening         | n/a           | Getting Worse  |
| Selected        |TRAN02  | Worsening         | n/a           | Performance Dropped |
| Acceptable      |TRAN02  | Unknown           | 100 (50th)    | Opportunity to Improve Peer Average|



# Historical Information on Input Messages
## Performance JSON data
The following are performance data benchmarks and an editable template that were used to create measure-associated JSON performance metadata for **input_message.json files**.

### JSON data block (12 months)
Variables:
- `staffID` - ID # for personas: replace with number based on which persona you are working with.
- `MSR1` - Measure name (eg SUS04) - note that meausures have hypens removed in JSON data
- `passNumb` - count of successful events for each month. passNumb generally is 50, 85, or 95, based on persona specs, and with `denominator` set to 100 (as below)
- `flagNumb` - remainder of event sum, = 100-`passNumb`
- `p_avg` - peer average, needs to be set based on the vignette data
- `ninety` - 90th percentile benchmark
- `sevenFive` - 75th percentile benchmark
- `pogGoal` - MPOG goal values(measure dependent)

"Performance_data":[
    ["staff_number","measure","month","passed_count","flagged_count","denominator","peer_average_comparator","peer_90th_percentile_benchmark","peer_75th_percentile_benchmark", "MPOG_goal"],
    [staffID,"MSR1","2023-01-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-02-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-03-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-04-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-05-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-06-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-07-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-08-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-09-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-10-01",passNumb,flagNumb,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-11-01",critPass,critFlag,100,p_avg,ninety,sevenFive,pogGoal],
    [staffID,"MSR1","2023-12-01",critPass,critFlag,100,p_avg,ninety,sevenFive,pogGoal],
  ],
  
  
For vignette accurate data, specifications in the [persona data sheet](https://docs.google.com/spreadsheets/d/1ZxtuEPI5EVfnO-YcvzGjbUSy3woixCsaz4slOCozVEU/edit#gid=0) should be followed unless deviations have been documented with a rationale in the PFKB repo.