# FNA on Horizon

This fork resolves Horizon content paths against the managed application's base
directory and integrates pinned SDL2 and FNA3D sources. The managed library targets
net8 and can be hosted by [Horizon CoreCLR .NET 10](https://github.com/pixelomer/dotnet-runtime).
Keep the pinned source revisions together rather than substituting moving heads.

## Build

On Linux x86-64, install Python 3.12+, Git and .NET SDK 10.0.1xx. Run:

```sh
python3 build-horizon.py
```

The script fetches exact Git submodule revisions and builds Release outputs into
ignored `artifacts/horizon/`. `--source-mirrors JSON` optionally maps source URLs to Git mirrors for offline
source fetching.
`--fetch-only` prepares source without compiling.

FNA also builds source-pinned [SDL2](https://github.com/pixelomer/SDL) and
[FNA3D](https://github.com/pixelomer/FNA3D), including its paired
[MojoShader](https://github.com/pixelomer/MojoShader). Native builds require
CMake, Ninja, make and devkitPro switch-dev/switch-portlibs. `--managed-only`
builds just `bin/FNA.Core/release_net8.0/FNA.dll`. `--libnx PATH` reuses a built
SDK; by default native dependencies fetch and build pinned libnx themselves.
FNA3D uses SDL2/OpenGL. Native FAudio/Theorafile services are not supplied by this
profile; the managed bindings are retained for API compatibility. Applications
must provide compatible native audio/video services for those APIs.

Upstream FNA/SDL2-CS/FAudio/Theorafile/FNA3D/MojoShader notices and submodule
histories remain intact. FNA's license is in licenses/LICENSE, with separate dependency
licenses in their source trees.

The source-build helpers' recursive source-fetch controls can be run with
`python3 tests/horizon/test_sources.py`; these tests create only temporary,
original Git fixtures and do not require a console or game files.
