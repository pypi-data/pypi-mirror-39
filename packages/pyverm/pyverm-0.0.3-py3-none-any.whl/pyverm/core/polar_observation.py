class PolarObservation:
    """
    Defines a Polar Observation
    """

    def __init__(self, target_point, horizontal_angle,  vertical_angle, distance):
        """

        :param point:
        :param horizontal_angle:
        :param vertical_angle:
        :param distance:
        """
        self.target_point = target_point
        self.horizontal_angle = horizontal_angle
        self.vertical_angle = vertical_angle
        self.distance = distance

