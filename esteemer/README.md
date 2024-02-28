## High level Flowchart

```
function esteemer:
    for measure in measures:
        candidates = measure_acceptable_candidates(measure)
        for candidate in candidates:
            score(candidate)
    
    selected_candidate = select_candidate()
    selected_message = render(selected_candidate)
         
```

## measure_acceptable_candidates

1. extracts the list of acceptable candidates for a measure 
2. applies measure business rules.

### apply measure business rules


## score
1. calculate motivating info sub-score
2. calculate history sub-score
3. calculate preferences sub-score
4. calculate final score
4. update candidate score

### calculate motivating info sub-score
### calculate history sub-score
### calculate preferences sub-score
### calculate final score

## select_candidate
1. apply between measure business rules 
2. select candidate

### apply between measure business rules