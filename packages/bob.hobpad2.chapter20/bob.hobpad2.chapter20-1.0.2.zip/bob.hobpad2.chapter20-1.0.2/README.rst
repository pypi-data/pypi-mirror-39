.. vim: set fileencoding=utf-8 :

======================================================================
 Evaluation Methodologies for Biometric Presentation Attack Detection
======================================================================

This package is part of the signal-processing and machine learning toolbox
Bob_. It is a software package to reproduce "Evaluation Methodologies for
Biometric Presentation Attack Detection" chapter of "Handbook of Biometric
Anti- Spoofing: Presentation Attack Detection 2nd Edition"::

    @INCOLLECTION{Chingovska_SPRINGER_2019,
             author = {Chingovska, Ivana and Mohammadi, Amir and Anjos, Andr{\'{e}} and Marcel, S{\'{e}}bastien},
             editor = {Marcel, S{\'{e}}bastien and Nixon, Mark and Fierrez, Julian and Evans, Nicholas},
              title = {Evaluation Methodologies for Biometric Presentation Attack Detection},
          booktitle = {Handbook of Biometric Anti-Spoofing},
            edition = {2nd},
            chapter = {20},
               year = {2019},
          publisher = {Springer International Publishing},
               isbn = {978-3-319-92627-8},
                url = {https://www.springer.com/us/book/9783319926261},
                doi = {10.1007/978-3-319-92627-8},
           crossref = {Chingovska_Idiap-Internal-RR-30-2018},
                pdf = {https://publidiap.idiap.ch/downloads//papers/2018/Chingovska_SPRINGER_2019.pdf}
    }


Reproduction
------------

The installation instructions are based on conda_ and works on **Linux and
MacOS systems only**. `Install conda`_ before continuing.

Once you have installed conda_, create a conda environment with the following
command and activate it::

    $ conda create --name bob.hobpad2.chapter20 --override-channels \
      -c https://www.idiap.ch/software/bob/conda -c defaults \
      bob.hobpad2.chapter20
    $ conda activate bob.hobpad2.chapter20

This will install all the required software to reproduce this book chapter.
Once installed, follow the commands below to generate the plots::

    $ # To generate Figure 4:
    $ bob measure gen generic_scores
    $ bob measure hist generic_scores/scores-dev -o fig4.a.pdf
    $ bob measure det generic_scores/scores-dev -o fig4.b.pdf --lines-at ' ' --no-disp-legend --titles ' '
    $ bob measure epc generic_scores/scores-{dev,eval} -o fig4.c.pdf --titles ' ' --no-disp-legend -xl '$\beta$'
    $ # To generate Figure 5:
    $ bob vulnerability gen vuln_scores
    $ bob vulnerability hist vuln_scores/{licit,spoof}/scores-dev -o fig5.a.pdf --no-iapmr-line
    $ bob vulnerability hist vuln_scores/{licit,spoof}/scores-dev -o fig5.b.pdf --no-real-data
    $ bob vulnerability det vuln_scores/{licit,spoof}/scores-dev -o fig5.c.pdf --fnmr 0.0214 --no-real-data --title ' '
    $ bob vulnerability fmr_iapmr vuln_scores/{licit,spoof}/scores-{dev,eval} -o fig5.d.pdf --no-disp-legend --title ' '
    $ bob vulnerability epc vuln_scores/{licit,spoof}/scores-{dev,eval} -o fig5.e.pdf --title ' '
    $ bob vulnerability epsc vuln_scores/{licit,spoof}/scores-{dev,eval} -o fig5.f.pdf -nI --titles 'EPSC with $\beta = 0.50$' --no-disp-legend


Contact
-------

For questions or reporting issues to this software package, contact our
development `mailing list`_.


.. Place your references here:
.. _bob: https://www.idiap.ch/software/bob
.. _installation: https://www.idiap.ch/software/bob/install
.. _mailing list: https://www.idiap.ch/software/bob/discuss
.. _conda: https://conda.io
.. _install conda: https://conda.io/docs/user-guide/install/index.html
