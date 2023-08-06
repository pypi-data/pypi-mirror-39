from slime_mind.timer.timer import timed
from argparse import ArgumentParser
from slime_mind.runners.single_match import Runner as SingleMatch
from slime_mind.runners.multi_match import Runner as MultiMatch
from slime_mind.runners.replay import Runner as Replay

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-r", "--runner", default="single_match", help="Name of runner to use, e.g. single_match, replay, multi_match", choices=['single_match', 'multi_match','replay'])
    # multi_match arguments
    parser.add_argument('-m', '--matches', default=4, help='Only valid with -r multi_match. Number of matches to run.', type=int)
    parser.add_argument('-1', '--ai_one_filename', default=None, help='Only valid with -r single_match or -r multi_match. Filename of first AI')
    parser.add_argument('-2', '--ai_two_filename', default=None, help='Only valid with -r single_match or -r multi_match. Filename of second AI.')
    # replay arguments
    parser.add_argument('--recording', default=None, help="Recording file to replay. Only valid with -r replay")
    return parser.parse_args()

def main():
    args = parse_arguments()
    if args.runner == 'single_match':
        runner = SingleMatch('PlayerCode', args.ai_one_filename, args.ai_two_filename)
    elif args.runner == 'multi_match':
        runner = MultiMatch('PlayerCode', args.matches, args.ai_one_filename, args.ai_two_filename)
    elif args.runner == 'replay':
        if args.recording is None:
            print("Must specify --recording with -r replay")
            exit(1)
        runner = Replay('PlayerCode', f'./recordings/{args.recording}')
    else:
        print(f"Unknown runner: {args.runner}")

    timed(runner.run)()

if __name__ == "__main__":
    main()
