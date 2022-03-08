import ga.data.reader as rea
import ga.data.output as out
import ga.ga_methods.population_initialization as pop
import ga.objective_function.fitness_helper as fh

root = '~/GitHub/SF-Scheduler-algo/src/data/model/'

sf_data = rea.read_sf_data(root + 'big_sf_data.csv')
game_data = rea.read_game_data(root + 'big_game_data.csv', sf_data['teams'])

c = pop.generate_chromosome(15 * 2 * 45)

df = out.bits_to_sched(c, sf_data, game_data)
df.to_csv(root + 'result.csv')
df.to_html(root + 'result.html')

