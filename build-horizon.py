#!/usr/bin/env python3
"""Build paired managed FNA and optional native Horizon graphics dependencies."""
import argparse, json, os, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'eng/horizon'))
from support import digest, git_source, read_mirrors, run, submodules
p = argparse.ArgumentParser(description=__doc__)
p.add_argument('--output', type=Path, default=ROOT / 'artifacts/horizon')
p.add_argument('--dotnet', default='dotnet')
p.add_argument('--managed-only', action='store_true')
p.add_argument('--fetch-only', action='store_true')
p.add_argument('--libnx', type=Path)
p.add_argument('--jobs', type=int, default=min(os.cpu_count() or 2, 8))
p.add_argument('--source-mirrors', type=Path)
a = p.parse_args()
if a.jobs < 1: p.error('--jobs must be positive')
mirrors = read_mirrors(a.source_mirrors)
submodules(ROOT, mirrors)
if a.fetch_only: sys.exit(0)
out = a.output.resolve()
run([a.dotnet, 'build', ROOT / 'FNA.Core.csproj', '-c', 'Release', '-p:TargetFrameworks=net8.0',
     '-p:ArtifactsPath=' + str(out)], cwd=ROOT)
manifest = {'revision': subprocess.check_output(['git', '-C', ROOT, 'rev-parse', 'HEAD'], text=True).strip(),
            'fna_sha256': digest(out / 'bin/FNA.Core/release_net8.0/FNA.dll')}
if not a.managed_only:
    spec = json.loads((ROOT / 'eng/horizon/dependencies.json').read_text())
    sdl = git_source(spec['sdl'], ROOT / 'artifacts/sources/SDL', mirrors)
    for path, name in [(sdl, 'sdl'), (ROOT / 'lib/FNA3D', 'fna3d')]:
        cmd = [sys.executable, path / 'build-horizon.py', '--output', out / name, '--jobs', a.jobs]
        if a.libnx: cmd += ['--libnx', a.libnx.resolve()]
        if a.source_mirrors: cmd += ['--source-mirrors', a.source_mirrors.resolve()]
        run(cmd)
        manifest[name] = json.loads((out / name / 'manifest.json').read_text())
(out / 'manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
print(out)
