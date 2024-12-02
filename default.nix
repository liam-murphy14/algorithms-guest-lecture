{ buildPythonApplication
, setuptools
, tkinter
}:

buildPythonApplication {
  pname = "animations";
  version = "1.0.0";
  pyproject = true;

  src = ./.;

  dependencies = [ tkinter ];

  build-system = [ setuptools ];

  meta = {
    homepage = "https://github.com/liam-murphy14/algorithms-guest-lecture";
    description = "A guest lecture for Prof. Volkovich's algorithms class";
  };
}
