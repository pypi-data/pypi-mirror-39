from DockerBuildSystem import DockerComposeTools
from SwarmManagement import SwarmTools, SwarmManager
from DockerBuildManagement import BuildTools
import sys
import os

SWARM_KEY = 'swarm'
SWARM_MANAGEMENT_PROPERTIES_KEY = 'swarmManagementProperties'
SWARM_MANAGEMENT_FILES_KEY = 'swarmManagementFiles'


def GetInfoMsg():
    infoMsg = "Test selections is configured by adding a 'swarm' property to the .yaml file.\r\n"
    infoMsg += "The 'swarm' property is a dictionary of swarm selections.\r\n"
    return infoMsg


def GetSwarmSelections(arguments):
    return BuildTools.GetProperties(arguments, SWARM_KEY, GetInfoMsg())


def DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, prefix):
    if len(swarmSelectionsToDeploy) == 0:
        for swarmSelection in swarmSelections:
            DeploySwarmSelection(prefix, swarmSelections[swarmSelection])
    else:
        for swarmSelectionToDeploy in swarmSelectionsToDeploy:
            if swarmSelectionToDeploy in swarmSelections:
                DeploySwarmSelection(prefix, swarmSelections[swarmSelectionToDeploy])


def DeploySwarmSelection(swarmSelection, prefix):
    cwd = BuildTools.TryChangeToDirectoryAndGetCwd(swarmSelection)
    SwarmManager.HandleManagement(
        [prefix] + BuildSwarmManagementFilesRow(swarmSelection) + BuildSwarmManagementPropertiesRow(swarmSelection))
    os.chdir(cwd)


def BuildSwarmManagementFilesRow(swarmSelection):
    swarmManagementFiles = []
    for swarmManagementFile in swarmSelection[SWARM_MANAGEMENT_FILES_KEY]:
        swarmManagementFiles += ['-f', swarmManagementFile]
    return swarmManagementFiles


def BuildSwarmManagementPropertiesRow(swarmSelection):
    swarmManagementProperties = []
    for swarmManagementProperty in swarmSelection[SWARM_MANAGEMENT_PROPERTIES_KEY]:
        swarmManagementProperties += [swarmManagementProperty]
    return swarmManagementProperties


def GetPrefix(arguments):
    if '-start' in arguments:
        return '-start'
    if '-stop' in arguments:
        return '-stop'
    if '-restart' in arguments:
        return '-restart'
    return '-start'


def HandleSwarmSelections(arguments):
    if len(arguments) == 0:
        return
    if not('-start' in arguments or '-stop' in arguments or '-restart' in arguments or '-swarm' in arguments):
        return

    if '-help' in arguments:
        print(GetInfoMsg())
        return

    swarmSelectionsToDeploy = SwarmTools.GetArgumentValues(arguments, '-swarm')
    swarmSelectionsToDeploy += SwarmTools.GetArgumentValues(arguments, '-s')

    swarmSelections = GetSwarmSelections(arguments)
    DeploySwarmSelections(swarmSelectionsToDeploy, swarmSelections, GetPrefix(arguments))


if __name__ == "__main__":
    arguments = sys.argv[1:]
    HandleSwarmSelections(arguments)
