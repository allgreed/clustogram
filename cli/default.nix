let
  nixpkgs = builtins.fetchGit {
    name = "nixos-unstable-2020-09-26";
    url = "https://github.com/nixos/nixpkgs-channels/";
    ref = "refs/heads/nixos-unstable";
    rev = "daaa0e33505082716beb52efefe3064f0332b521";
    # obtain via `git ls-remote https://github.com/nixos/nixpkgs-channels nixos-unstable`
  };
  pkgs = import nixpkgs { config = {}; };
  pythonEnv = pkgs.python38.withPackages(ps: with ps; [
    pyyaml
    pyhcl
    stringcase
    ]);
in
pkgs.mkShell {
  buildInputs =
  with pkgs;
  [
    git
    gnumake

    pythonEnv
  ];
}
