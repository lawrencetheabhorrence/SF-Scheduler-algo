cross="o n u"
mut="b f u"
for i in $cross
do
  for j in $mut
  do
    touch "data/model/cross_mut/fitness_$i$j.csv"
  done
done
