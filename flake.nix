##
## Development flake for 'home-finder'
##

{
    inputs = {
        nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

        pyproject.url = "github:pyproject-nix/pyproject.nix";
        pyproject.inputs.nixpkgs.follows = "nixpkgs";
    };

    outputs = { self, nixpkgs, pyproject }: let
        inherit (nixpkgs)               lib;
        inherit (pyproject.lib.project) loadPoetryPyproject;

        systems = [ "x86_64-linux" ];
        project = loadPoetryPyproject { projectRoot = ./.; };
    in {
        devShells = lib.genAttrs systems (system: let
            pkgs   = import nixpkgs { inherit system; };
            python = pkgs.python3;

            python-with-deps = python.withPackages (
                project.renderers.withPackages { inherit python; }
            );
            packages = [
                python-with-deps
                pkgs.poetry
            ];
        in {
            default = pkgs.mkShell { inherit packages; };
        });
};  }

