import ga.data.reader as rea
import ga.data.output as out
import ga.ga_methods.population_initialization as pop
import ga.objective_function.fitness_helper as fh

root = '~/GitHub/SF-Scheduler-algo/src/ga/data/test/'

sf_data = rea.read_sf_data(root + 'test_sf_data.csv')
game_data = rea.read_game_data(root + 'test_game_data.csv')

c = pop.generate_chromosome(5 * 5 * 5)

print(out.bits_to_sched(c, sf_data, game_data))

