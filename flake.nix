{
  description = "Nix flake for the python to run my guest lecture";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      packages = forEachSupportedSystem ({ pkgs }:
        {
          default = pkgs.python3Packages.callPackage ./default.nix { };
        });
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (
              python3.withPackages (
                ps: with ps; [
                  tkinter
                  # dev dependencies
                  black
                ]
              )
            )
          ];

        };
      });
      formatter = forEachSupportedSystem ({ pkgs }: pkgs.nixpkgs-fmt
      );
    };
}
