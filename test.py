from src.PathEvaluator import PathEvaluator
from src.Datalogger import Datalogger
from src.Visualizer import Visualizer

pathEval = PathEvaluator()
datalogger = Datalogger()
visualizer = Visualizer()

pathEval.updateDataFromLogFile("Experiment_20230814161953810")

pathEval.pathInterpolation("Interpolation1", 200)

visualizer.visualizeExperiments(
    ["Experiment_20230814161953810", "Interpolation1"],
    ["Raw", "Interpolated"],
    viewPts=True,
)
