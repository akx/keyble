import argparse

from keyble.video_frontend import extract_cards_from_video


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('-i', '--input-video', required=True)
    ap.add_argument('-d', '--dest-dir', required=True)
    args = ap.parse_args()
    extract_cards_from_video(input_video=args.input_video, dest_dir=args.dest_dir)


if __name__ == '__main__':
    main()
