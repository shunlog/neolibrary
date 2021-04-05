Some useful neo4j queries, all in one place


Advanced search "AND"

``` sql
// Advanced search "AND"
// It is supposed to be used moularly, meaning, if the user
// didn't specify author regex, the second module should
// not be included, etc
// the 'with' lines are supposed to be between blocks
// the 'return b limit 10' should be last 
match (b:Book)
where b.name =~ 'A.*'

with b 

match (b)<-[:WROTE]-(a:Author)
where a.name =~ 'A.*'

with b 

match (t:Tag)-[:TAGS]->(b)
where t.name =~ 'a.*'

return b limit 5
```

Advanced search "OR"

``` sql
// Advanced search "OR"
// Modular too
// 'return b limit .. union' is the gluing line
// 'return b limit ..' in the end 

match (b:Book)
where b.name =~ 'A.*'

return b limit 5
union

match (a:Author)-[:WROTE]->(b:Book)
where a.name =~ 'A.*'

return b limit 5
union

match (t:Tag)-[:TAGS]->(b:Book)
where t.name =~ 'a.*'

return b limit 5
```


Mixed example

``` sql
match (b:Book)
where b.name =~ 'W.*'

return b limit 2 // OR
union

match (b)<-[:WROTE]-(a:Author)
where a.name =~ 'A.*'

with b // AND

match (t:Tag)-[:TAGS]->(b)
where t.name =~ 'a.*'

return b limit 2
```
