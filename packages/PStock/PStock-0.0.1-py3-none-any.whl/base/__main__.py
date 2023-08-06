#author: lladhibhutall 
import pprint
import click

from .classmodule import MyClass
from .funcmodule import my_function, sort_by_time, sorted_XY
from .drawmodule import draw_plot
@click.command()
@click.argument('symbol')
def main(symbol):
    ''' Enter the Symbol'''  
    pp = pprint.PrettyPrinter(indent=4)
    #click.echo(my_function(symbol))
    unsorted_list = my_function(symbol)
    sorted_list = sort_by_time(unsorted_list)
    last_item = sorted_list[-1]
    #pp.pprint(sorted_list)
    X,Y = sorted_XY(sorted_list)
    draw_plot(X,Y)
    print("")
    click.echo("       current open is ${}".format(last_item['open']))
    click.echo("       current close is ${}".format(last_item['close']))
    click.echo("       current low is ${}".format(last_item['low']))
    click.echo("       current high is ${}".format(last_item['high']))
    click.echo("       current volume is {}".format(last_item['volume']))
    print("")

if __name__ == '__main__':
    main()

