#!/bin/bash
#setup apptainer
#/cvmfs/oasis.opensciencegrid.org/mis/apptainer/current/bin/apptainer shell --shell=/bin/bash -B /cvmfs,/exp,/nashome,/pnfs/dune,/opt,/run/user,/etc/hostname,/etc/hosts,/etc/krb5.conf --ipc --pid /cvmfs/singularity.opensciencegrid.org/fermilab/fnal-dev-sl7:latest

#!/bin/bash
alias dune_setup="source /cvmfs/dune.opensciencegrid.org/products/dune/setup_dune.sh"
dune_setup

#list to dunwsw version: ups list -aK+ dunesw
export DUNESW_VERSION=v10_04_07d01
setup dunesw $DUNESW_VERSION -q e26:prof

#mrb newDev -v v10_04_05 -q prof:e26

source /exp/dune/app/users/gabrielb/meu_larsoft/localProducts_larsoft_v10_04_07_prof_e26/setup
cd $MRB_BUILDDIR
#mrb g dunesw --> e outros como: duneexamples, duneana, dunereco, dunecalib, dunecore, duneopdet, duneprototypes, dunesim, dunedataprep

setup mrb
mrbsetenv

#mrb b # compila o codigo
#mrb i # instala o codigo?

mrbslp
export FHICL_FILE_PATH=${FHICL_FILE_PATH}:${MRB_BUILDDIR}/dunesw/fcl #para achar as fcls

# Set up proxy
kx509
voms-proxy-init --noregen -rfc -voms dune:/dune/Role=Analysis

# Set up metacat and rucio for finding files
setup metacat
export METACAT_AUTH_SERVER_URL=https://metacat.fnal.gov:8143/auth/dune
export METACAT_SERVER_URL=https://metacat.fnal.gov:9443/dune_meta_prod/app
unsetup python_requests #caso haja problemas
setup rucio
