-- Write query to get number of assignments for each state

SELECT state, count(state) as StateCount
FROM assignments 
GROUP BY state