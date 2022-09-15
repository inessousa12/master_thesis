import statistics
import numpy as np
import functions

class QualityBlock:
    """
    QualityBlock class.
    """

    def __init__(self, cdf_threshold):
        """
        Initializes QualityBlock class.

        Args:
            cdf_threshold ([float]): cdf threshold
        """
        self.cdf_threshold = cdf_threshold

    @staticmethod
    def load_cdf(path):
        """
        Loads cdf file.

        Args:
            path ([str]): cdf file's path
        """
        return functions.load_processed([path + "/cdf.npz"])

    @staticmethod
    def calculate_cdf_probability(x, cdf):   
        """
        Calculates cdf probability.

        Args:
            x ([float]): difference between the measurement and the prediction
            cdf ([dict]): cdf
        """
        x_index = np.searchsorted(cdf['x'], x, side="left")

        if x_index == len(cdf['y']):
            v = 1
        else:
            v = cdf['y'][x_index]

        return v

    @staticmethod
    def calculate_error(actual, predictions):
        """
        Calculates the error between the measurement and the error

        Args:
            actual ([float]): actual value
            predictions ([float]): predicted value
        """
        errors = []
        for p in predictions:
            errors.append(pow(actual - p, 2))
        return errors

    def checks_probability(self, numb_sensors, falses, probabilities):
        """
        Calculates the probability of a measurement to be a fault according to the number of sensors.

        Args:
            numb_sensors ([int]): number of sensors
            falses ([list]): list with values that aren't similar to a prediction, for each sensor
            probabilities ([list]): list of cdf probabilities
        """

        if numb_sensors > 1:
            if len(falses) > 0:
                if len(falses) == 1:
                    """
                    Different from 1 prediction.

                    @Goncalo
                    We start by considering the case where a single prediction is different from m. This can be the
                    prediction that was produced based on past measurements of only the target sensor, the prediction
                    that uses measurements from target and neighbour sensors, or, finally, the prediction based only
                    on measurements from neighbour sensors. In the first case, it is possible to conclude with a high
                    probability that the target sensor is being affected by a real physical event that produces a large
                    difference with respect to past values, hence the measurement is not an outlier. This is supported
                    by the fact that this event was reflected in the measurements of the other sensors and consequently
                    on the predictions that use these measurements, both of which similar to m.

                    @Joao
                    Anything new to the logic of fault detection is added here
                    """
                    return False, probabilities
                elif len(falses) == 2:
                    """
                    Different from 2 predictions.

                    @Goncalo
                    If m is significantly different from two predictions (and hence similar to a singular prediction),
                    then only two cases are relevant and one is unlikely to occur. If m is similar to the prediction
                    based on the target measurements, then the measurement is likely correct and the difference with
                    the other predictions can be explained by an event affecting the neighbour sensors or a severe
                    fault affecting only one of them. If m is similar to the prediction based only on the neighbours
                    measurements, then it is possible to conclude that an event is forcing all measurements to take
                    unexpected values. The prediction based only on neighbour sensors uses as input these unexpected
                    values, which justifies that it is similar to m. On the other hand, the other predictions include the
                    target past measurements that force the model to produce a value that is closer to the one that
                    would be expected without an event. The case in which m is similar only to the prediction using all
                    sensors is unlikely to occur because it does not make sense that a prediction using only neighbour
                    sensors and the prediction using only the target sensor are similar to m but that one is not. 

                    @Joao
                    Anything new to the logic of fault detection is added here
                    """
                    return False, probabilities #estava a False
                else:
                    """
                    Different from all predictions.

                    @Goncalo
                    Finally, the situation that is indicative of a faulty measurement m is the last possible one, when
                    all predictions are different from m.

                    @Joao
                    Anything new to the logic of fault detection is added here
                    """
                    return True, probabilities
            else:
                return False, probabilities
        else:
            """
            @Inês
            This if/else needed to be added in order to treat data when only one sensor is sending data.
            """
            if len(falses) == 1:
                """
                Different from 1 prediction.
                """
                return True, probabilities
            else:
                """
                Not different from predictions.
                """
                return False, probabilities

    def fault_detection(self, predictions, errors):
        """
        Checks the probability of a value to be an error.

        Args:
            predictions ([list]): list of predictions
            errors ([list]): list of calculated errors
        """
        threshold = self.cdf_threshold

        isSimilar = []
        probabilities = []
        for i in range(len(errors)):
            p = predictions[i]
            error = errors[i]
            cdf = self.load_cdf(p[0])
            ann_type = p[1]

            probability = self.calculate_cdf_probability(error, cdf)
            probabilities.append(probability)

            if probability < threshold:
                isSimilar.append((True, error, probability, ann_type))
            else:
                isSimilar.append((False, error, probability, ann_type))

        falses = [i for i in isSimilar if i[0] is False]
        trues = [i for i in isSimilar if i[0] is True]

        numb_sensors = len(predictions)
    
        flag, probabilities = self.checks_probability(numb_sensors, falses, probabilities)

        return flag, probabilities

    def quality_calculation(self, probabilities):
        """
        Calculates the quality based on the predictions

        Args:
            probabilities ([list]): list of predictions
        """
        return 1 - statistics.mean(probabilities)