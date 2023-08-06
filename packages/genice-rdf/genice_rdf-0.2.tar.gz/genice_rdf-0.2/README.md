# genice-rdf

A [GenIce](https://github.com/vitroid/GenIce) plugin to calculate the radial distribution functions.

## Requirements

* [GenIce](https://github.com/vitroid/GenIce) >=0.23.

## Installation from PyPI

    % pip install genice-rdf

## Manual Installation

### System-wide installation

    % make install

### Private installation

Copy the files in formats/ into your local formats folder of GenIce.

## Usage

	% genice 1c -r 3 3 3 -f _RDF > 1c.rdf

## Options

You can specify the list of atom types to be calculated.

For example, in the following case, TIP4P water has four different atom types (OW, HW1, HW2, and MW), so all the possible 10 combinations of atom types will be examined.

	% genice 1c -r 3 3 3 -w tip4p -f _RDF > 1c.rdf

If you just want the RDF of OW and H, and HW1 and HW2 should be abbreviated by H, specify the option string like following.

	% genice 1c -r 3 3 3 -w tip4p -f _RDF[OW,H=HW1=HW2] > 1c.rdf

## Test in place

    % make test
