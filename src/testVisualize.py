from Visualizer import Visualizer
from PathEvaluator import PathEvaluator
from Datalogger import Datalogger

name = "Experiment_20230512223019066"

visualizer = Visualizer()
pathEval = PathEvaluator()

visualizer.visualizeExperiments([name], ["path"])
pathEval.updateDataFromLog(f"{name}_Raw")

# print(pathEval.pathInterpolation())
pathEval.pathInterpolation(name)

visualizer.visualizeExperiments([name], ["path2"], "Interpolated")

# print(datalogger.readCSV(name))
