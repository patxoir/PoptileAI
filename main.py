import argparse

def main():
    parser = argparse.ArgumentParser()
    interface = parser.add_mutually_exclusive_group()
    interface.add_argument('-c', '--cli', action='store_true',
                            help='run on cli interface')
    interface.add_argument('-g', '--gui', action='store_true',
                            help='run on gui interface')
    
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--train', action='store_true',
                        help='train AI')
    mode.add_argument('--test', action='store_true',
                        help='test AI')
    mode.add_argument('--interactive', action='store_true',
                        help='play the game!')

    parser.add_argument('-n', '--num', type=int, default=5,
                        help='number of train/test iterations')

    args = parser.parse_args()
    

if __name__ == '__main__':
    main()
