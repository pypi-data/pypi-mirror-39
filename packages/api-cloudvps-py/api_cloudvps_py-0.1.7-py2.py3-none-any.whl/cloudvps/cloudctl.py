import cloudvps
import os
import sys
import os.path
import argparse


def get_token():
    """
    Obtain token from different places
    """
    if "CLOUD_TOKEN" in os.environ:
        return os.environ["CLOUD_TOKEN"]
    return get_from_file()


def get_from_file(file=".cloudvps_token"):
    """
    Try get token from default `file`
    """
    try:
        from pathlib import Path

        token_file = Path(os.path.join(Path.home(), file))
        if token_file.exists():
            with token_file.open() as f:
                return f.readline()
    except:
        from os.path import expanduser, exists

        token_file = os.path.join(os.path.expanduser("~"), file)
        if exists(token_file):
            with open(token_file) as f:
                return f.readline()


def serve():
    print("Number of arguments:", len(sys.argv), "arguments.")
    print("Argument List:", str(sys.argv))
    print("forever")
    print(get_token())
    # api = cloudvps.Api('3f7c0a3d*****356b45d59f71a')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--verbose", help="increase output verbosity", action="store_true"
    )

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)

    if args.verbose:
        print("verbosity turned on")

    serve()
