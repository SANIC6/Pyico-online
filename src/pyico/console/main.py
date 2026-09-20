import argparse


def test_run(args):
    print("Running the Pyico application..."+args.cartfile)
def test_edit(args):
    print("Editing the Pyico application..."+args.cartfile)

parser = argparse.ArgumentParser(description="Pyico-CLI: A command-line interface for Pyico.")

subs = parser.add_subparsers(dest="cmd", help="Available commands", required=True)

p_run = subs.add_parser("run", help="Run the Pyico application.")
p_run.add_argument('cartfile', type=str, help="Path to the cart file to run.")
p_run.set_defaults(func=test_run)

p_edit = subs.add_parser("edit", help="Edit the Pyico application.")
p_edit.add_argument('cartfile', type=str, help="Path to the cart file to edit.")
p_edit.set_defaults(func=test_edit)

args = parser.parse_args()


if hasattr(args, 'func'):
    args.func(args)