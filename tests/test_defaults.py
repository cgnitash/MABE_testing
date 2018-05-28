import os, subprocess, pytest
from utils.helpers import this_repo_path, mabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, ABdiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

@pytest.fixture ## indicates this is the constructor fn for all the test fns in this module
def ctx(): ## create a context for all the tests - you could potentially use this to pass an obj to all test fns
    if not ctx.ran: ## prevents reinit before each and every test fn in this module
        ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
        ## and run mabe with defaults
        dirs = [dirname_baseline, dirname_testline]
        for eachdir in dirs: ## loop through each of baseline and testline and generate the files for later diffing
            cd(eachdir)
            runCmdAndSaveOutput( "./{exe} -s".format(exe=mabe), filename='screen-settings' )
            runCmdAndSaveOutput( "./{exe} -h".format(exe=mabe), filename='screen-help' )
            runCmdAndSaveOutput( "./{exe} -l".format(exe=mabe), filename='screen-poploader' )
            runCmdAndSaveOutput( "./{exe} -v".format(exe=mabe), filename='screen-version' )
            runCmdAndSaveOutput( "./{exe}".format(exe=mabe), filename='screen-simulation' )
            cd('..') ## could also have done cd(this_repo_path)
        ## FYI, could have done it the following way if we were up one dir in mabe_testing
        #runCmdAndSaveOutput( "{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_baseline_exe, path=dirname_baseline), filename=dirname_baseline+'screen-simulation' )
        ctx.ran = True

    yield None ## could have actually passed a context object here to all the test fns
    ##
    ## teardown happens after the last test in the module finishes
    ##
    return
ctx.ran = False

## testing consistency of screen output
def test_screen_help(ctx):
    ABdiff('screen-help')
def test_screen_run(ctx):
    ABdiff('screen-settings')
def test_screen_simulation(ctx):
    ABdiff('screen-simulation')
def test_screen_poploader(ctx):
    ABdiff('screen-poploader')

## cfg
def test_settings_cfg(ctx):
    ABdiff('settings.cfg')
def test_settings_organism_cfg(ctx):
    ABdiff('settings_organism.cfg')
def test_settings_world_cfg(ctx):
    ABdiff('settings_world.cfg')

## csv
def test_max_csv(ctx):
    ABdiff('max.csv')
def test_pop_csv(ctx):
    ABdiff('pop.csv')
def test_lod_data_csv(ctx):
    ABdiff('LOD_data.csv')
def test_lod_organisms_csv(ctx):
    ABdiff('LOD_organisms.csv')

## poploader
def test_poploader(ctx):
    ABdiff('population_loader.plf')

## version output
def test_version_baseline(ctx):
    result = getFileContents(dirname_baseline+'screen-version')
    line1=result[0]
    assert len(line1) != 1, "version information not found but should have been included in the build"
def test_version_baseline(ctx):
    result = getFileContents(dirname_testline+'screen-version')
    line1=result[0]
    assert len(line1) != 1, "version information not found but should have been included in the build"
