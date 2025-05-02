import os
import shutil
import zipfile
import Utils


def gen_template(world, outdir):
    from Options import generate_yaml_templates
    target = Utils.user_path("Players", "Templates")
    generate_yaml_templates(target, False)
    outfile = os.path.join(outdir, world)
    if os.path.exists(outfile):
        os.remove(outfile)
    shutil.copy(os.path.join(target, world), outfile)


def pack_apworld(src_world, dst_world, outdir):
    src_dir = os.path.join('worlds', src_world)
    dst_dir = 'tmp'
    zip_name = os.path.join(outdir, f"{dst_world}.apworld")

    if os.path.exists(dst_dir):
        shutil.rmtree(dst_dir)
    if os.path.exists(zip_name):
        os.remove(zip_name)

    shutil.copytree(src_dir, os.path.join(dst_dir, dst_world))

    # remove pycache
    for root, dirs, files in os.walk(dst_dir, topdown=False):
        for name in files:
            if name.endswith('.pyc'):
                os.remove(os.path.join(root, name))
        for name in dirs:
            if name == '__pycache__':
                shutil.rmtree(os.path.join(root, name))

    # zip cleaned directory
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(dst_dir):
            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, dst_dir)
                zipf.write(full_path, rel_path)

    # remove the temporary directory
    shutil.rmtree(dst_dir)

def main(args):
    pack_apworld('ladx', 'ladx_beta', args.outdir)

    if args.include_artifacts:
        gen_template("Links Awakening DX Beta.yaml", args.outdir)

        connector = 'connector_ladx_bizhawk.lua'
        connector_file = os.path.join(args.outdir, connector)
        if os.path.exists(connector_file):
            os.remove(connector_file)
        shutil.copy(os.path.join('data', 'lua', connector), connector_file)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--apworld-only", dest="include_artifacts", action="store_false")
    parser.add_argument("outdir", default=".", help="Output directory")
    main(parser.parse_args())