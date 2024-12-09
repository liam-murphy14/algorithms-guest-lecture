{
  description = "Nix flake for the python to run my guest lecture";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
      tex = pkgs: (pkgs.texlive.combine {
        inherit (pkgs.texlive) scheme-basic latexmk
          geometry
          amsfonts
          amsmath
          mathtools
          float
          fontspec
          exam
          etoolbox
          kastrup
          listings
          hyperref
          newpx
          newtx
          pxfonts
          trimspaces
          tex-gyre
          tex-gyre-math
          unicode-math
          lualatex-math
          pagella-otf
          xcolor
          xstring
          xkeyval
          xpatch
          fontaxes
          algorithms
          algorithmicx
          algpseudocodex;
      });
    in
    {
      packages = forEachSupportedSystem ({ pkgs }:
        {
          default = pkgs.python3Packages.callPackage ./default.nix { };
          documents = pkgs.stdenvNoCC.mkDerivation rec {
            name = "documents";
            src = self;
            buildInputs = [ pkgs.coreutils (tex pkgs) ];
            phases = [ "unpackPhase" "buildPhase" "installPhase" ];
            buildPhase = ''
              export PATH="${pkgs.lib.makeBinPath buildInputs}";
              mkdir -p .cache/texmf-var
              env TEXMFHOME=.cache TEXMFVAR=.cache/texmf-var \
                latexmk -interaction=nonstopmode -pdf -pdflatex \
                presentation.tex
            '';
            installPhase = ''
              mkdir -p $out
              cp presentation.pdf $out/
            '';
          };
        });
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [
            (
              python3.withPackages (
                ps: with ps; [
                  tkinter
                  click
                  # dev dependencies
                  black
                ]
              )
            )
            (tex pkgs)
          ];

        };
      });
      formatter = forEachSupportedSystem ({ pkgs }: pkgs.nixpkgs-fmt
      );
    };
}
