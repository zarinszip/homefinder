##
## `homefinder` development flake
##

{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";
    };

    outputs = { self, nixpkgs }: let
        inherit (nixpkgs) lib;
        systems = [ "x86_64-linux" ];
    in {
        devShells = lib.genAttrs systems (system: let
            pkgs   = import nixpkgs { inherit system; };
            python = pkgs.python3;
            uv     = python.pkgs.uv;

            packages  = [ uv ];
            shellHook = ''
                leave() {
                	rm -r ./.venv
                	exit "$1"
                }

                uv venv \
                  --python ${ python }/bin/python \
                  --allow-existing -q \
                || leave "$?"

                uv sync --frozen --offline &> /dev/null \
                || uv sync --frozen \
                || leave "$?"

                unset -f leave
                . ./.venv/bin/activate
            '';
        in {
            default = pkgs.mkShell {
                inherit packages shellHook;
            };
        });
};  }

